import sender_stand_request
import data
from requests import Response, Request

# эта функция меняет значения в параметре firstName
def get_user_body(first_name):
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body["firstName"] = first_name
    # возвращается новый словарь с нужным значением firstName
    return current_body
def removeFirstNameFromBody():
    # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body = data.user_body.copy()
    # изменение значения в поле firstName
    current_body.pop("firstName")
    # возвращается новый словарь с нужным значением firstName
    return current_body

# def test_create_user_2_letter_in_first_name_get_success_response():
#     # В переменную user_body сохраняется обновленное тело запроса с именем “Аа”
#     user_body = get_user_body("Аа")
#     # В переменную user_response сохраняется результат запроса на создание пользователя
#     user_response = sender_stand_request.post_new_user(user_body)
#     # Проверяется, что код ответа равен 201
#     assert user_response.status_code == 201, 'Status code is not 201!'
#     # Проверяется, что в ответе есть поле authToken, и оно не пустое
#     assert user_response.json()["authToken"] != "", 'Token is empty!'
#     users_table_response = sender_stand_request.get_users_table()
#     str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
#                + user_body["address"] + ",,," + user_response.json()["authToken"]
#     print(users_table_response.text)
#     # Проверка, что такой пользователь есть, и он единственный
#     assert users_table_response.text.count(str_user) == 1

def create_user_with_specified_first_name(name: str):
    # В переменную user_body сохраняется обновленное тело запроса с именем “Аа”
    user_body = get_user_body(name)
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)
    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201, 'Status code is not 201!'
    assert user_response.reason == 'Created'
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != "", 'Token is empty!'
    print('@@@', user_response.json())
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]
    print('$%%%', users_table_response.text)
    # print('!!!', user_response.text)
    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

def negative_assert_symbol(name: str):
    user_body = get_user_body(name)
    user_response = sender_stand_request.post_new_user(user_body)
    users_table_response = sender_stand_request.get_users_table()
    print('$%%%', users_table_response.text)
    assert user_response.status_code == 400, 'Status code is ' + user_response.status_code
    assert user_response.json()["code"] == 400
    assert user_response.reason == 'Bad Request'
    assert 'authToken' not in user_response.json(), 'Token is valid!'
    print(user_response.json()['message'])
    assert user_response.json()['message'] == "Имя пользователя введено некорректно. " \
                                             "Имя может содержать только русские или латинские буквы, " \
                                             "длина должна быть не менее 2 и не более 15 символов"

def negative_assert_no_firstname(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    users_table_response = sender_stand_request.get_users_table()
    print('$%%%', users_table_response.text)
    assert user_response.status_code == 400, 'Status code is ' + user_response.status_code
    assert user_response.reason == 'Bad Request'
    assert 'authToken' not in user_response.json(), 'Token is valid!'
    # print(user_response.json()['message'])
    print(user_response.json())
    print(user_response.reason)
    assert user_response.json()['message'] == 'Не все необходимые параметры были переданы'

def test_create_user_2_letter_in_first_name_get_success_response():
    create_user_with_specified_first_name("Аа")

def test_create_user_15_letter_in_first_name_get_success_response():
    create_user_with_specified_first_name("ШурикШурикШурик")

def test_create_user_1_letter_in_first_name_get_failed_result():
    negative_assert_symbol("А")

def test_create_user_16_letter_in_first_name_get_failed_result():
    negative_assert_symbol("ШурикШурикШурикШ")

def test_create_user_english_letters_in_first_name_get_success_response():
    create_user_with_specified_first_name("QWErty")

def test_create_user_spaces_in_first_name_get_failed_result():
    negative_assert_symbol("Человек и Ко")

def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol(" КО")

def test_create_user_spaces_in_first_name_get_failed_result():
    negative_assert_symbol("№%@")

def test_create_user_spaces_in_first_name_get_failed_result():
    negative_assert_symbol("123")

def test_not_all_required_params_provided_no_user_name():
    user_body: dict[str, str] = removeFirstNameFromBody()
    negative_assert_no_firstname(user_body)

def test_not_all_required_params_provided_empty_user_name():
    user_body: dict[str, str] = get_user_body('')
    negative_assert_no_firstname(user_body)

def test_not_all_required_params_provided_wrong_user_name_type():
    user_body: dict[str, str] = get_user_body(2)
    negative_assert_no_firstname(user_body)