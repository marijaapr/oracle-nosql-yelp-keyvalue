import csv
import time
from pathlib import Path

from borneo import (
    NoSQLHandle,
    NoSQLHandleConfig,
    GetRequest
)

from borneo.kv import StoreAccessTokenProvider

TABLE_NAME = "kv_store"
RESULTS_FILE = Path("results/oracle_performance.csv")


def get_handle():
    endpoint = "http://localhost:8080"
    provider = StoreAccessTokenProvider()
    config = NoSQLHandleConfig(endpoint).set_authorization_provider(provider)
    config.set_timeout(10000)
    return NoSQLHandle(config)


def get_key(handle, key):
    request = GetRequest().set_table_name(TABLE_NAME).set_key({
        "k": key
    })

    result = handle.get(request)
    return result.get_value()


def measure_query(handle, label, key, runs=100):
    times = []

    for _ in range(runs):
        start = time.perf_counter()
        get_key(handle, key)
        end = time.perf_counter()

        times.append((end - start) * 1000)

    avg_ms = sum(times) / len(times)
    min_ms = min(times)
    max_ms = max(times)

    return {
        "query": label,
        "key": key,
        "runs": runs,
        "avg_ms": round(avg_ms, 4),
        "min_ms": round(min_ms, 4),
        "max_ms": round(max_ms, 4)
    }


def main():
    handle = get_handle()

    try:
        city_key = "city_category:Philadelphia:Restaurants"
        city_result = get_key(handle, city_key)

        if not city_result:
            print("City category key not found.")
            return

        business_ids = city_result["v"]["business_ids"]
        first_business_id = business_ids[0]

        business_reviews_key = f"business_reviews:{first_business_id}"
        reviews_result = get_key(handle, business_reviews_key)

        first_review_id = None
        first_user_id = None

        if reviews_result and reviews_result["v"]["review_ids"]:
            first_review_id = reviews_result["v"]["review_ids"][0]
            review_result = get_key(handle, f"review:{first_review_id}")

            if review_result:
                first_user_id = review_result["v"]["user_id"]

        queries = [
            {
                "label": "Get restaurants in city/category",
                "key": city_key
            },
            {
                "label": "Get business by id",
                "key": f"business:{first_business_id}"
            },
            {
                "label": "Get reviews for business",
                "key": business_reviews_key
            },
            {
                "label": "Get business statistics",
                "key": f"stats:business:{first_business_id}"
            }
        ]

        if first_review_id:
            queries.append({
                "label": "Get review by id",
                "key": f"review:{first_review_id}"
            })

        if first_user_id:
            queries.append({
                "label": "Get user by id",
                "key": f"user:{first_user_id}"
            })

        results = []

        print("Measuring Oracle NoSQL performance...")

        for query in queries:
            print(f"Measuring: {query['label']}")
            result = measure_query(
                handle,
                query["label"],
                query["key"],
                runs=100
            )
            results.append(result)

        RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)

        with RESULTS_FILE.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["query", "key", "runs", "avg_ms", "min_ms", "max_ms"]
            )
            writer.writeheader()
            writer.writerows(results)

        print(f"\nPerformance results saved to: {RESULTS_FILE}")

        print("\nResults:")
        for r in results:
            print(r)

    finally:
        handle.close()


if __name__ == "__main__":
    main()