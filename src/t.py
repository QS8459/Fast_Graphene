import requests as r
import json
if __name__ == "__main__":
    a = r.post(
        url="http://127.0.0.1:8200/graphql/",
        headers={"Content-Type": "application/json"},
        data=json.dumps(
            {"query": "query{accountList(offset:1, limit: 1){email}}"}
        )

    )

    print(a.text)
