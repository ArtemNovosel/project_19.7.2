import pytest
from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
import os  # библиотека для указания пути к файлу

# инициализируем созданную библиотеку присваиванием переменной
pf = PetFriends()

def smile_chars(n):
    return "☻♥" * n

@pytest.fixture(autouse=True)
def f_get_api_key():
    # Сохраняем ключ в pytest.key *** чтобы он передовался в тест
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key
    yield
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200

'''проверяет обработку сервером НЕвалидных email & password /api/key'''
def test_get_api_key_for_invalid_user(email='xxx@xx.xxx', password='00000'):
    # из библиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # проверяем результат по статусу и отсутствию ключа в ответе
    assert status == 403
    assert "key" not in result


'''Проверяем обработку НЕ валидного auth_key в методе получения питомцев /api/pets '''
def test_get_all_pets_with_invalid_key(filter='my_pets'):
    # присваиваем аут.ключу невалидное значение
    auth_key = {'key': 'b00000ff4273e72a94fdc351452fcbe9308af25de0c6e29ac0d2b54a'}
    # вызываем метод получения списка питомцев передаем аут.ключ и filter
    status, _ = pf.get_list_of_pets(auth_key, filter)
    # проверяем     что  сервер возвращает код 403
    assert status == 403


'''Проверяем возможность добавить питомца с валидными данными (без фото) /api/create_pet_simple'''
def test_add_new_pet_dezPHOTO_valid_data(name='Бoкks', animal_type='дворняга', age=6):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца из библиотеки, передаем аут.ключ, имя, породу, возраст
    status, result = pf.post_add_new_pet_No_PHOTO(auth_key, name, animal_type, age)
    # проверяем полученные ответы статус кода, сверяем имя, отсутствие фото
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


'''Проверяем НЕ возможность добавить питомца с Пустыми данными (без фото) /api/create_pet_simple'''
# БАГ пиомец добавляется
def test_add_new_pet_dezPHOTO_invalid_data(name="", animal_type='', age=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца из библиотеки, передаем аут.ключ, имя, породу, возраст
    status, result = pf.post_add_new_pet_No_PHOTO(auth_key, name, animal_type, age)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # сверяем  что ответ от сервера имеет статус код 400,  список питомцев не содержит питомца с пустыми данными
    assert status == 400  # 400  Код ошибки означает, что предоставленные данные неверны
    assert result['id'] != my_pets['pets'][0]['id']


'''Проверяем НЕ возможность добавить питомца с данными в виде смайлов (без фото). /api/create_pet_simple '''
# БАГ пиомец добавляется
@pytest.mark.parametrize("name, animal_type, age", [(smile_chars(1),smile_chars(2), smile_chars(3))])
def test_add_new_pet_dezPHOTO_invalid_data_smile(f_get_api_key, name, animal_type, age):
    # _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца из библиотеки, передаем аут.ключ, имя, породу, возраст
    status, result = pf.post_add_new_pet_No_PHOTO(pytest.key, name, animal_type, age)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')
    # сверяем  что ответ от сервера имеет статус код 400,  список питомцев не содержит питомца с невалидными данными
    assert status == 400  # 400  Код ошибки означает, что предоставленные данные неверны
    assert result['id'] != my_pets['pets'][0]['id']


'''Проверяем возможность добавить фото питомцу /api/pets/set_photo/{pet_id}'''
def test_add_photo_pet_correct(pet_photo='images/image.jpg'):
    # в переменную сохраняем полный путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # запрашиваем ключ и список питомцев, сохраняем их в переменные
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # print('***', my_pets['pets'][0]['id'], '***')
    # если список не пустой, то отправляем запрос на добавление фото первому в списке питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Сверяем ответы с ожидаемым результатом
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception('там нет моих домашних животных')


'''Проверяем НЕ возможность добавить фото 0 байт питомцу /api/pets/set_photo/{pet_id}'''
# БАГ 500 ошибка сервера
def test_add_invalid_photo_pet(pet_photo='images/test.jpg'):
    # в переменную сохраняем полный путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # запрашиваем ключ и список питомцев, сохраняем их в переменные
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # если список не пустой, то отправляем запрос на добавление фото первому в списке питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 400  # Код ошибки означает, что предоставленные данные неверны
        assert result['pet_photo'] is not None
    else:
        raise Exception('там нет моих домашних животных')


'''Проверяем возможность добавить фото 51 Mбайт питомцу /api/pets/set_photo/{pet_id}'''
def test_add_valid_photo_pet(pet_photo='images/testtest.jpg'):
    # в переменную сохраняем полный путь до фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # запрашиваем ключ и список питомцев, сохраняем их в переменные
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # если список не пустой, то отправляем запрос на добавление фото первому в списке питомцу
    if len(my_pets['pets']) > 0:
        status, result = pf.post_set_photo_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] is not None
    else:
        raise Exception('там нет моих домашних животных')


'''проверяем ответ сервера на НЕвалидный auth_key в методе delete'''
def test_delete_pet_invalid_id():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # если список пустой, то вызываем метода который добавляет питомца
    if len(my_pets['pets']) == 0:
        pf.post_add_new_pet_No_PHOTO(auth_key, 'Morgan', "kot", 6)
        # формируем список повторно
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # присваиваем переменной id первого питомца в списке
    pet_id = my_pets['pets'][0]['id']
    test_auth_key = {'key': 'testik0ff4273e72a94fdc351452fcbe9308af25de0c6e29ac0d2b54a'}
    # удаляем питомца вызовом метода delete передавая ему невалидный key
    status = pf.delete_pet(test_auth_key, pet_id)
    assert status == 403  # Код ошибки означает, что предоставленный auth_key неверен



"""Проверяем НЕвозможность обновить данные о существующем питомце если использовать 500 символов в имени, иероглифы и отрицательный возраст """
# БАГ данные питомца меняются
def test_update_invalid_pet(animal_type='原千五百秋瑞', age=-999):
    file = open('text500.txt', 'r')
    name = file.read()
    file.close()
    # print(name)
    # получаем через метод ключ
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
