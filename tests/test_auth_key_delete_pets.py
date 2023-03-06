import pytest
from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные


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
    return "☻" * n


@pytest.fixture(autouse=True) #запускается автоматически при обращении к его переменной
def f_get_api_key():
    # Сохраняем ключ в pytest.key *** чтобы он передовался в тест
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key
    yield
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200




'''тест который проверяет обработку сервером валидных email & password'''
'''ПОЗИТИВНЫЙ тест'''
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # из биюлиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # сверяем результат по статусу и присутствию ключа в ответе
    assert status == 200
    assert "key" in result
    # print(result['key'])


'''НЕГАТИВНЫЙ тест'''
@pytest.mark.parametrize("email"
   , ['', generate_string(255), generate_string(1001), russian_chars(),
       russian_chars().upper(), chinese_chars(), special_chars(), '123']
   , ids=['empty', '255 symbols', 'more than 1000 symbols', 'russian', 'RUSSIAN', 'chinese', 'specials', 'digit'])
@pytest.mark.parametrize("password",
                        ['', '-1', '0', '100', '1.5', '2147483647', '2147483648', special_chars(), russian_chars(),
                         russian_chars().upper(), chinese_chars()]
   , ids=['empty', 'negative', 'zero', 'greater than max', 'float', 'int_max', 'int_max + 1', 'specials',
          'russian', 'RUSSIAN', 'chinese'])
def test_get_api_key_for_invalid_user(email, password):
    # из библиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # проверяем результат по статусу и отсутствию ключа в ответе
    assert status == 403
    assert "key" not in result


'''Тест на удаление питомца по id'''
"""ПОЗИТИВНЫЙ тест"""
@pytest.mark.parametrize('i', range(1,2)) #задаем колличество удаляемых питомцев
def test_delete_valid(i):
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # если список пустой, то вызываем метода который добавляет питомца
    # print('***', my_pets.values())
    print('***',len(my_pets['pets']),'***')
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_No_PHOTO(pytest.key, 'Morgan', "kot", '6')
        # формируем список повторно
        _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # первому питомцу в списке присваиваем переменную
    pet_id = my_pets['pets'][i]['id']
    print(pet_id,'***')
    # удаляем питомца вызовом метода
    status = pf.delete_pet(pytest.key, pet_id)
    # сравниваем полученный ответ от сервера
    assert status == 200
    # получаем список питомцев заново
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    print('***', my_pets.values())
    # проверяем что питомец удален
    assert pet_id not in my_pets.values()





'''НЕГАТИВНЫЕ тесты'''
@pytest.mark.parametrize('test_key', ['testik0ff4273e72a94fdc351452fcbe9308af25de0c6e29ac0d2b54a', generate_string(255), generate_string(1001),
                                      russian_chars(), chinese_chars(), special_chars(), smile_chars(5), 1234567890],
                         ids=["another user's key", '255 symbols', 'more than 1001 symbols', 'russian',
                              'chinese', 'specials','smile', 'digit'])
def test_delete_pet_invalid_id(test_key):
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # если список пустой, то вызываем метода который добавляет питомца
    if len(my_pets['pets']) == 0:
        print("НЕТУ ПИТОМЦЕВ ТО...")
        pf.post_add_new_pet_No_PHOTO(pytest.key, 'Morgan', "kot", '6')
        # формируем список повторно
        _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # присваиваем переменной id первого питомца в списке
    pet_id = my_pets['pets'][0]['id']
    test_auth_key = {'key': test_key}
    # удаляем питомца вызовом метода delete передавая ему невалидный key
    status = pf.delete_pet(test_auth_key, pet_id)
    assert status == 403  # Код ошибки означает, что предоставленный auth_key неверен


