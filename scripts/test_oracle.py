from borneo import (
    NoSQLHandle,
    NoSQLHandleConfig,
    TableRequest,
    PutRequest,
    GetRequest
)

from borneo.kv import StoreAccessTokenProvider


def get_handle():
    endpoint = "http://localhost:8080"
    provider = StoreAccessTokenProvider()

    config = NoSQLHandleConfig(endpoint).set_authorization_provider(provider)
    return NoSQLHandle(config)


def main():
    handle = get_handle()

    try:
        statement = """
        CREATE TABLE IF NOT EXISTS kv_store (
            k STRING,
            v JSON,
            PRIMARY KEY (k)
        )
        """

        request = TableRequest().set_statement(statement)
        result = handle.do_table_request(request, 40000, 3000)
        result.wait_for_completion(handle, 40000, 3000)

        print("Tabela kv_store e kreirana.")

        put_request = PutRequest().set_table_name("kv_store").set_value({
            "k": "test:1",
            "v": {
                "message": "Oracle NoSQL raboti",
                "project": "Key-value bazi"
            }
        })

        handle.put(put_request)

        get_request = GetRequest().set_table_name("kv_store").set_key({
            "k": "test:1"
        })

        get_result = handle.get(get_request)

        print("Procitan zapis:")
        print(get_result.get_value())

    finally:
        handle.close()


if __name__ == "__main__":
    main()
