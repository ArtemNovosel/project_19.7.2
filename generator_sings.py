import requests
import pytest
import json

base_url = "https://petfriends.skillfactory.ru"

valid_email = 'tes111t@mail.ru'
valid_password = '12345'
@pytest.fixture(autouse=True) #запускается автоматически при обращении к его переменной
def get_api_key():
    headers = {
        "email": valid_email,
        "password": valid_password
    }
    # формируем запрос на получение ключа апи
    response = requests.get(base_url+'/api/key', headers=headers)
    # достаем ключ из ответа
    valid_key = response.json()["key"]
    print('******',valid_key)
    # говорим что у нас есть сессия она позволяет 'хранить историю'
    session = requests.Session()
    # в рамках сесии ...
    session.headers.update({"auth_key": valid_key})
    # дальше пишем terdown
    yield session
    # уничтожаем (тушим) сессию если требуется
    session.post(base_url+"/api/auth/logout")

def log_request(func): #пишем декоратор для логирования тестов
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        with open("log.txt", 'a') as f:
            f.write(f"{response.request.method} {response.url}\n") #записываем метод запроса
            f.write(f"Request headers: {response.request.headers}\n") #записываем заголовки запроса
            f.write(f"Request body: {response.request.body}\n") #записываем тело запроса
            f.write(f"Response status code: {response.status_code}\n") #забираем статус код ответа
            f.write(f"Response headers: {response.headers}\n") #записываем заголовки ответа
            f.write(f"Response body: {response.body}\n") #записываем тело ответа
        return response
    return wrapper


# @log_request
def test_get_pets(get_api_key): #вызывается фикстура
    response = get_api_key.get(base_url+"/api/pets") #результат виполнения yield
    assert response.status_code == 200
    assert len(response.json()['pets']) > 0


# @pytest.fixture
def test_c_create_pet(get_api_key):
    data = {
        "name": 'Bobik',
        "age": 5,
        "anymal_type": 'Dog'
    }
    heders = {'auth_key': get_api_key['key']}
    response = get_api_key.post(base_url+'/api/create_pet_simple', json=data)
    pet_id = response.json()['id']
    print(pet_id,'***')
    # yield pet_id
    # get_api_key.delete(base_url+"/api/pets/"+pet_id)

def test_create_pet(create_pet):
    assert create_pet is not None