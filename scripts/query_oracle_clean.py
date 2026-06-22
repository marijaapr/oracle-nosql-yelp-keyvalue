from borneo import (
    NoSQLHandle,
    NoSQLHandleConfig,
    GetRequest
)

from borneo.kv import StoreAccessTokenProvider

TABLE_NAME = "kv_store"


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


def main():
    handle = get_handle()

    try:
        city_key = "city_category:Philadelphia:Restaurants"

        print("=== QUERY 1: Restaurants in Philadelphia ===")

        city_result = get_key(handle, city_key)

        if not city_result:
            print("No result for city category key.")
            return

        business_ids = city_result["v"]["business_ids"]

        print(f"Key: {city_key}")
        print(f"Total restaurants found: {len(business_ids)}")
        print(f"First 3 business ids: {business_ids[:3]}")

        first_business_id = business_ids[0]

        print("\n=== QUERY 2: Business by ID ===")
        business_result = get_key(handle, f"business:{first_business_id}")

        if business_result:
            business = business_result["v"]

            print(f"Business ID: {first_business_id}")
            print(f"Name: {business.get('name')}")
            print(f"City: {business.get('city')}")
            print(f"Stars: {business.get('stars')}")
            print(f"Review count: {business.get('review_count')}")
            print(f"Categories: {business.get('categories')}")

        print("\n=== QUERY 3: Reviews for business ===")
        reviews_result = get_key(handle, f"business_reviews:{first_business_id}")

        first_review_id = None

        if reviews_result:
            review_ids = reviews_result["v"]["review_ids"]

            print(f"Business ID: {first_business_id}")
            print(f"Total reviews stored for this business: {len(review_ids)}")
            print(f"First 3 review ids: {review_ids[:3]}")

            if review_ids:
                first_review_id = review_ids[0]

        print("\n=== QUERY 4: Business statistics ===")
        stats_result = get_key(handle, f"stats:business:{first_business_id}")

        if stats_result:
            stats = stats_result["v"]

            print(f"Business ID: {stats.get('business_id')}")
            print(f"Review count: {stats.get('review_count')}")
            print(f"Average stars: {stats.get('avg_stars')}")

        if first_review_id:
            print("\n=== QUERY 5: Review by ID ===")
            review_result = get_key(handle, f"review:{first_review_id}")

            if review_result:
                review = review_result["v"]

                print(f"Review ID: {first_review_id}")
                print(f"Business ID: {review.get('business_id')}")
                print(f"User ID: {review.get('user_id')}")
                print(f"Stars: {review.get('stars')}")
                print(f"Text preview: {review.get('text', '')[:200]}...")

                user_id = review.get("user_id")

                print("\n=== QUERY 6: User by ID ===")
                user_result = get_key(handle, f"user:{user_id}")

                if user_result:
                    user = user_result["v"]

                    print(f"User ID: {user_id}")
                    print(f"Name: {user.get('name')}")
                    print(f"Review count: {user.get('review_count')}")
                    print(f"Average stars: {user.get('average_stars')}")

    finally:
        handle.close()


if __name__ == "__main__":
    main()