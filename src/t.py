import requests as r
import json
from src.core.service.authentication import generate_token

if __name__ == "__main__":
    request = r.post(
        url="http://127.0.0.1:8200/api/token/"
    )
    print(request.headers)
    # print(generate_token(
    #     {
    #         "guid": "1",
    #         "username": "string17@example.com"
    #     },
    #     exp_time=1800
    # ))
    # a = r.post(
    #     url="http://127.0.0.1:8200/graphql/",
    #     headers={
    #         "Content-Type": "application/json",
    #         "Authentication": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoiMSIsInVzZXJuYW1lIjoic3RyaW5nMTdAZXhhbXBsZS5jb20iLCJleHAiOjE3NDQ2NzcxMDl9.SezW-YZl-eT5mHDx8sODkAIZaQIxPaDZj4tam-_gtlM"
    #     },
    #     data=json.dumps(
    #         {"query": """
    #         mutation{
    #             signUp(
    #                 accountData: {
    #                     email: "string17@example.com",
    #                     password: "String_1!"
    #                 }
    #             ){
    #                 account{
    #                     guid,
    #                     email
    #                 }
    #             }
    #         }
    #         """
    #          }
    #     )
    #
    # )
    #
    # print(a.json())
    # print(a.status_code)
