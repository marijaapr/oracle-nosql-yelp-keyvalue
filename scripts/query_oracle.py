from borneo import (
    NoSQLHandle,
    NoSQLHandleConfig,
    GetRequest
)

from borneo.kv import StoreAccessTokenProvider

TABLE_NAME = "kv_store"


def get_handle():
    print("Connecting to Oracle NoSQL...")

    endpoint = "http://localhost:8080"
    provider = StoreAccessTokenProvider()

    config = NoSQLHandleConfig(endpoint).set_authorization_provider(provider)
    config.set_timeout(10000)

    handle = NoSQLHandle(config)

    print("Connected.")
    return handle


def get_key(handle, key):
    print(f"\nTrying key: {key}")

    request = GetRequest().set_table_name(TABLE_NAME).set_key({
        "k": key
    })

    result = handle.get(request)
    value = result.get_value()

    if value is None:
        print("No result found.")
    else:
        print("Result found:")
        print(value)

    return value


def main():
    print("Script started.")

    handle = get_handle()

    try:
        print("\n=== Test 1: test key ===")
        get_key(handle, "test:1")

        print("\n=== Test 2: city category index ===")
        result = get_key(handle, "city_category:Philadelphia:Restaurants")

        if not result:
            print("\nNema city_category key. Mozno e Yelp importot da ne e napraven ili gradot ne e Philadelphia.")
            return

        business_ids = result.get("v", {}).get("business_ids", [])

        if not business_ids:
            print("\nKey postoi, ama nema business_ids vnatre.")
            return

        first_business_id = business_ids[0]

        print("\n=== Test 3: business by id ===")
        get_key(handle, f"business:{first_business_id}")

        print("\n=== Test 4: business reviews ===")
        get_key(handle, f"business_reviews:{first_business_id}")

        print("\n=== Test 5: business stats ===")
        get_key(handle, f"stats:business:{first_business_id}")

    finally:
        handle.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    main()