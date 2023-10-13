from requests import Response, Request

import configuration
import requests
import data


def get_docs():
    return requests.get(configuration.URL_SERVICE + configuration.DOC_PATH)


# response: Response = get_docs()
# # print(response._content)
# print(response.text)

def get_logs():
    return requests.get(configuration.URL_SERVICE + configuration.LOG_MAIN_PATH + '?count=20')


# response: Response = get_logs()
# # print(response._content)
# print(response.text)
# print(response.headers)
# print(response.status_code)


def get_users_table():
    return requests.get(configuration.URL_SERVICE + configuration.USERS_TABLE_PATH)


# response: Response = get_users_table()
# print(response.text)
# print(response.status_code)


def post_new_user(body: Request):
    return requests.post(
        configuration.URL_SERVICE + configuration.CREATE_USER_PATH,  # подставляем полный url
        json=body,  # тут тело
        headers=data.headers)  # а здесь заголовки


# response = post_new_user(data.user_body);
# print(response.status_code)
# # print(response.text)
# print(response.json())

def post_products_kits(products_ids: list[int]):
    return requests.post(
        configuration.URL_SERVICE + configuration.PRODUCTS_KITS_PATH,
        json=products_ids,
        headers=data.headers
    )

# response = post_products_kits(data.product_ids);
# print(response.status_code)
# print(response.json())