import pytest
import sys
from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
# from generator_sings import * #импортируем генератор символов
import os  # библиотека для указания пути к файлу

# инициализируем созданную библиотеку присваиванием переменной
pf = PetFriends()
# иницавлизируем библиотеку генератора символов
# gen = Generator_sings

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



"""Проверяем возможность обновить данные о существующем питомце /api/pets/{pet_id}"""
'''ПОЗИТИВНЫЕ тесты'''
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
def test_update_valid_pet(name, animal_type, age):
    # получаем через метод ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Ессли список не пустой, то пробуем обновить имя, тип и возраст первого питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")


"""Проверяем возможность обновить данные о существующем питомце /api/pets/{pet_id}"""
'''НЕГАТИВНЫЕ тесты'''
# БАГ данные питомца меняются
@pytest.mark.xfail(sys.platform == "win32", reason="Эта фикстура помечает тест как часто падающий на win 32")
@pytest.mark.parametrize("name", [''], ids=['empty'])
@pytest.mark.parametrize("animal_type", [''], ids=['empty'])
@pytest.mark.parametrize("age",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
          'russian', 'RUSSIAN', 'chinese'])
def test_update_invalid_pet(name, animal_type, age):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 400 и имя питомца не соответствует заданному
        print(my_pets['pets'][0]['animal_type'])
        print(my_pets['pets'][0]['name'])
        assert status == 400  # Код ошибки означает, что предоставленные данные неверны
        assert result['name'] != name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")


'''Проверяем возможность добавить фото питомцу /api/pets/set_photo/{pet_id}'''
"""ПОЗИТИВНЫЙ тест"""
@pytest.mark.parametrize('pet_photo', ['images/image.jpg','images/testtest.jpg'],
                         ids=['img', 'img_51_Mb'])
def test_add_photo_pet_correct(fix_get_api_key, pet_photo):
    # в переменную сохраняем полный путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # cписок питомцев, сохраняем их в переменные
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # если список не пустой, то отправляем запрос на добавление фото первому в списке питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_photo_pet(pytest.key, my_pets['pets'][0]['id'], pet_photo)
        # Сверяем ответы с ожидаемым результатом
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception('там нет моих домашних животных')


'''Проверяем корректную обработку сервером НЕ валидных файлов фото (0 байт, png, текст) питомцу /api/pets/set_photo/{pet_id}'''
'''НЕГАТИВНЫЕ тесты'''
# БАГ 500 ошибка сервера
@pytest.mark.parametrize('pet_photo', ['images/test.jpg','images/test.png', 'images/test.txt'], ids=['jpg_0_Mb','png_photo','txt_file'])
def test_add_invalid_photo_pet(fix_get_api_key, pet_photo):
    # в переменную сохраняем полный путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # запрашиваем ключ и список питомцев, сохраняем их в переменные
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # если список не пустой, то отправляем запрос на добавление фото первому в списке питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_photo_pet(pytest.key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 400  # Код ошибки означает, что предоставленные данные неверны
        assert result['pet_photo'] is not None
    else:
        raise Exception('там нет моих домашних животных')
