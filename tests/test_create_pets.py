import pytest

from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
# from generator_sings import * #импортируем генератор символов
# import os  # библиотека для указания пути к файлу

# инициализируем созданную библиотеку присваиванием переменной
pf = PetFriends()

def generate_string(n):
    return "x" * n


def russian_chars():
    return 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'


# Здесь мы взяли 20 популярных китайских иероглифов
def chinese_chars():
    return '的一是不了人我在有他这为之大来以个中上们'


def special_chars():
    return '|\\/!@#$%^&*()-_=+`~?"№;:[]{}'

def smile_chars(n):
    return "☻"*n

@pytest.fixture(autouse=True)
def fix_get_api_key():
    # Сохраняем ключ в pytest.key *** чтобы он передовался в тест
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key
    yield
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200

'''Проверяем возможность добавить питомца с валидными данными и фото. БАГ: age принимает только str '''
# БАГ: age принимает только str
@pytest.mark.parametrize("name, animal_type, age",  [('Bobik', 'Bobikov', '8')])
def test_add_new_pet_and_PHOTO_valid_data(fix_get_api_key, name, animal_type, age,
                                          pet_photo='images/image.jpg'):
    # вызываем метод добавления питомца передаем данные
    status, result = pf.post_add_new_pet_and_Photo(pytest.key, name, animal_type, age, pet_photo)
    # проверяем полученные ответы статус кода, присутствие фото
    assert status == 200
    assert result['pet_photo'] != ''


'''Проверяем возможность добавить питомца с НЕвалидными данными и фото. БАГ: age принимает только str '''
# БАГ питомец добавляется
@pytest.mark.parametrize("name, animal_type, age",   [(chinese_chars(), special_chars(), generate_string(5)),
                                                      (russian_chars().upper(), russian_chars(), smile_chars(1)),
                                                      (smile_chars(2), smile_chars(3),smile_chars(4)),
                                                       (generate_string(255),generate_string(255),generate_string(255))
                ], ids=['chinese_special_chars_string', 'russian_chars', 'smile_chars', 'str_255'])
def test_add_new_pet_and_PHOTO_valid_data(fix_get_api_key, name, animal_type, age, pet_photo='images/image.jpg'):
    status, result = pf.post_add_new_pet_and_Photo(pytest.key, name, animal_type, age, pet_photo)
    assert status == 400
    assert result['pet_photo'] != ''


'''Проверяем возможность добавить питомца с валидными данными (без фото) /api/create_pet_simple'''
""" ПОЗИТИВНЫЕ кейсы"""
@pytest.mark.parametrize("name",
                [generate_string(255), generate_string(1001),
                russian_chars(), russian_chars().upper(),
                chinese_chars(), special_chars(), '123'],
                         ids=[ '255 symbols', 'more than 1000 symbols', 'russian',
                              'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("animal_type"
   , [ generate_string(255), generate_string(1001), russian_chars(),
       russian_chars().upper(), chinese_chars(), special_chars(), '123']
   , ids=[ '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("age", ['1'], ids=['min'])
def test_add_new_pet_simple_positive(name, animal_type, age):
    pytest.status, result = pf.post_add_new_pet_No_PHOTO(pytest.key, name, animal_type, age, )
    # Сверяем полученный ответ с ожидаемым результатом
    assert pytest.status == 200
    assert result['name'] == name
    assert result['age'] == age
    assert result['animal_type'] == animal_type


"""НЕГАТИВНЫЕ тесты"""
#БАГ питомец добавляется
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
          'russian', 'RUSSIAN', 'chinese'])
def test_add_new_pet_dezPHOTO_valid_data(name, animal_type, age):
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца из библиотеки, передаем аут.ключ, имя, породу, возраст
    status, result = pf.post_add_new_pet_No_PHOTO(pytest.key, name, animal_type, age)
    # проверяем полученные ответы статус кода, сверяем имя, отсутствие фото
    assert status == 400
    # assert result['name'] == name
    # assert result['pet_photo'] == ''











