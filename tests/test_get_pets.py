import pytest
import requests
import sys
# from conftest import version_36

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


 # '''Проверяем что запрос всех питомцев возвращает не пустой список. Доступное значение параметра filter - 'my_pets' либо ''  '''
class TestClassPets: #'''Позитивные тесты'''
        @pytest.mark.parametrize("filter",
                 ['', 'my_pets'],ids=['empty string', 'only my pets'])
        def test_get_all_pets_with_valid_key(self, fix_get_api_key, filter):
           # вызываем метод получения списка питомцев передаем аут.ключ и filter
            status, result = pf.get_list_of_pets(pytest.key, filter) # проверяем     что     список     не пустой.
            assert len(result['pets']) > 0


#Негативные тесты на корректную обработку сервером не валидного filter'''
# БАГ 500 ошибка сервера
#фикстура выполняет тест только на python версии 3,6 и выше
@pytest.mark.skipif(sys.version_info < (3, 6), reason="Тест требует python версии 3.6 или выше")
@pytest.mark.parametrize("filter", [generate_string(255), generate_string(1001),
                                    russian_chars(), russian_chars().upper(), chinese_chars(),
                                    special_chars(), 123],
                             ids=['255 symbols', '1001 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_all_pets_with_INvalid_filter(fix_get_api_key, filter):
    status, result = pf.get_list_of_pets(pytest.key, filter)
    assert status == 400 #Bad Request

'''Проверяем обработку НЕ валидного auth_key в методе получения питомцев /api/pets '''
def test_get_all_pets_with_invalid_key(filter='my_pets'):
    # присваиваем аут.ключу невалидное значение
    auth_key = {'key': 'b00000ff4273e72a94fdc351452fcbe9308af25de0c6e29ac0d2b54a'}
    # вызываем метод получения списка питомцев передаем аут.ключ и filter
    status, _ = pf.get_list_of_pets(auth_key, filter)
    # проверяем     что  сервер возвращает код 403
    assert status == 403




