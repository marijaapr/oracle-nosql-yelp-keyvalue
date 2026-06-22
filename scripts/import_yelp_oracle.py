import json
from pathlib import Path
from collections import defaultdict

from tqdm import tqdm
from borneo import (
    NoSQLHandle,
    NoSQLHandleConfig,
    TableRequest,
    PutRequest
)

from borneo.kv import StoreAccessTokenProvider

DATA_DIR = Path("data/processed")

BUSINESS_FILE = DATA_DIR / "business_subset.jsonl"
REVIEW_FILE = DATA_DIR / "review_subset.jsonl"
USER_FILE = DATA_DIR / "user_subset.jsonl"

TABLE_NAME = "kv_store"


def get_handle():
    endpoint = "http://localhost:8080"
    provider = StoreAccessTokenProvider()
    return NoSQLHandle(NoSQLHandleConfig(endpoint, provider))


def create_kv_table(handle):
    statement = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        k STRING,
        v JSON,
        PRIMARY KEY (k)
    )
    """

    request = TableRequest().set_statement(statement)
    result = handle.do_table_request(request, 40000, 3000)
    result.wait_for_completion(handle, 40000, 3000)

    print(f"Table {TABLE_NAME} is ready.")


def put_kv(handle, key, value):
    request = PutRequest().set_table_name(TABLE_NAME).set_value({
        "k": key,
        "v": value
    })
    handle.put(request)


def load_jsonl(path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)


def main():
    handle = get_handle()

    business_reviews = defaultdict(list)
    user_reviews = defaultdict(list)
    business_stats = defaultdict(lambda: {
        "review_count": 0,
        "stars_sum": 0.0
    })
    city_category_index = defaultdict(list)

    try:
        create_kv_table(handle)

        print("Importing businesses...")

        for business in tqdm(load_jsonl(BUSINESS_FILE)):
            business_id = business["business_id"]

            put_kv(handle, f"business:{business_id}", business)

            city = business.get("city", "UNKNOWN")
            categories = business.get("categories") or ""

            if "Restaurants" in categories:
                city_category_index[f"city_category:{city}:Restaurants"].append(business_id)

        print("Importing users...")

        for user in tqdm(load_jsonl(USER_FILE)):
            user_id = user["user_id"]
            put_kv(handle, f"user:{user_id}", user)

        print("Importing reviews...")

        for review in tqdm(load_jsonl(REVIEW_FILE)):
            review_id = review["review_id"]
            business_id = review["business_id"]
            user_id = review["user_id"]
            stars = float(review.get("stars", 0))

            put_kv(handle, f"review:{review_id}", review)

            business_reviews[business_id].append(review_id)
            user_reviews[user_id].append(review_id)

            business_stats[business_id]["review_count"] += 1
            business_stats[business_id]["stars_sum"] += stars

        print("Writing aggregate keys: business_reviews...")

        for business_id, review_ids in tqdm(business_reviews.items()):
            put_kv(handle, f"business_reviews:{business_id}", {
                "business_id": business_id,
                "review_ids": review_ids
            })

        print("Writing aggregate keys: user_reviews...")

        for user_id, review_ids in tqdm(user_reviews.items()):
            put_kv(handle, f"user_reviews:{user_id}", {
                "user_id": user_id,
                "review_ids": review_ids
            })

        print("Writing aggregate keys: business stats...")

        for business_id, stats in tqdm(business_stats.items()):
            count = stats["review_count"]
            avg_stars = stats["stars_sum"] / count if count > 0 else 0

            put_kv(handle, f"stats:business:{business_id}", {
                "business_id": business_id,
                "review_count": count,
                "avg_stars": avg_stars
            })

        print("Writing aggregate keys: city category index...")

        for key, business_ids in tqdm(city_category_index.items()):
            put_kv(handle, key, {
                "business_ids": business_ids
            })

        print("Import finished successfully.")

    finally:
        handle.close()


if __name__ == "__main__":
    main()