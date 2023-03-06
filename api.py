import requests  # помогает осуществлять вызовы
from requests_toolbelt.multipart.encoder import MultipartEncoder
import json
import pytest


# Пишем api  библиотеку к веб приложению Pet Friends
class PetFriends:
    # сохраняем базовый url при инициализации
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'


    def get_api_key(self, email: str, password: str):
        '''Метод делает запрос к API сервера и возвращает стстус запроса и результата в формате JSON
        с уникальным ключом пользователя, найденного по указанным email и паролю'''
        # составляем заголовок (в виде словаря)
        headers = {
            'email': email,
            'password': password}
        # формируем запрос с соответствующим методом на сервер, присваиваем переменную
        res = requests.get(self.base_url + '/api/key', headers=headers)
        # присваиваем переменной статус код ответа
        status = res.status_code
        result = ''
        # в случае ошибки извлечения json извлекаем text
        try:
            result = res.json()
        except:
            result = res.text
        # возвращаем статускод и ответ
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        '''метод принимает аут.ключ и фильтр(my_pets) и делает запрос к API сервера и возвращает результат в формате JSON
        со списком питомцев принадлежащих пользователю'''
        headers = {'auth_key': auth_key['key']}  # в заголовке передаем ключ
        filter = {'filter': filter}  # формируем фильтр
        # формируем запрос с url заголовком и в качестве параметров- фильтр
        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def post_add_new_pet_No_PHOTO(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет (постит) на сервер информацию о новом питомце name,animal_type, age(в виде number), (без фото) и возвращает статус
                ответа сервера и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        # отправляем запрос url+urn, заголовком(аут.ключом) и телом(параметрами нового питомца)
        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result

    def post_set_photo_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер фото питомца и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def post_add_new_pet_and_Photo(self, auth_key: json, name: str, animal_type: str, age, pet_photo: str) -> json:
        """Метод отправляет (постит) на сервер информацию о новом питомце name,animal_type, age, фото и возвращает статус
                ответа сервера и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={'name': name,
                    'animal_type': animal_type,
                    'age': age,
                    'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
                    })
        # в заголовке отправляем аут.ключ
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}
        # формируем запрос метода post
        res = requests.post(self.base_url + '/api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        # print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод удаляет питомца по конкретному id и возвращает статус код ответа сервера """
        heders = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + '/api/pets/' + pet_id, headers=heders)
        status = res.status_code
        return status

    def put_update_pet(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: str) -> json:
        """Метод обновляет информацию о питомце по конкретному id питомца ии возвращает статус
                ответа сервера и результат в формате JSON с данными добавленного питомца"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.put(self.base_url + '/api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result






