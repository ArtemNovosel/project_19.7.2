import pytest

from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
import os  # библиотека для указания пути к файлу

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


'''тест который проверяет обработку сервером валидных email & password'''


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # из биюлиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # сверяем результат по статусу и присутствию ключа в ответе
    assert status == 200
    assert "key" in result
    # print(result['key'])


'''Проверяем что запрос всех питомцев возвращает не пустой список. Доступное значение параметра filter - 'my_pets' либо ''  '''
@pytest.mark.parametrize("filter",
                         ['', 'my_pets'],ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(fix_get_api_key, filter):
    # print(pytest.key,'***')
    # вызываем метод получения списка питомцев передаем аут.ключ и filter
    status, result = pf.get_list_of_pets(pytest.key, filter)
    # проверяем     что     список     не пустой.
    assert len(result['pets']) > 0


'''Проверяем корректную обработку сервером не валидного filter '''
# БАГ 500 ошибка сервера
@pytest.mark.parametrize("filter", [generate_string(255), generate_string(1001),
                                    russian_chars(), russian_chars().upper(), chinese_chars(),
                                    special_chars(), 123],
                         ids=['255 symbols', '1001 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
def test_get_all_pets_with_INvalid_filter(fix_get_api_key, filter):
    status, result = pf.get_list_of_pets(pytest.key, filter)
    print(status,'**')
    assert status == 400 #Bad Request


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



'''проверяем удаление питомца по id'''
def test_delete_valid_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # если список пустой, то вызываем метода который добавляет питомца
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_No_PHOTO(auth_key, 'Morgan', "kot", 6)
        # формируем список повторно
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # первому питомцу в списке присваиваем переменную
    pet_id = my_pets['pets'][0]['id']

    # удаляем питомца вызовом метода
    status = pf.delete_pet(auth_key, pet_id)
    # сравниваем полученный ответ от сервера
    assert status == 200
    # получаем список питомцев заново
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # проверяем что питомец удален
    assert pet_id not in my_pets.values()


"""Проверяем возможность обновить данные о существующем питомце"""


def test_update_valid_pet(name='Vovano', animal_type='volk', age=18):
    # получаем через метод ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("Питомцы отсутствуют")
