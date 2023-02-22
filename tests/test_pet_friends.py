from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
import os  # библиотека для указания пути к файлу


# инициализируем созданную библиотеку присваиванием переменной
pf = PetFriends()


# создаем тест который проверяет обработку сервером валидных email & password
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # из биюлиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # сверяем результат по статусу и присутствию ключа в ответе
    assert status == 200
    assert "key" in result
    # print(result['key'])


# создаем тест который проверяет отбработку сервером валидных аут.ключ и параметр(filter по умолчанию пустой)
def test_get_all_pets_with_valid_key(filter=''):
    # с помощью метода получаем аут.ключ присваиваем его значение переменной. статус код этого запроса нам не нужен
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # print(auth_key['key'])
    # вызываем метод получения списка питомцев передаем аут.ключ и filter
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


# '''Проверяем возможность добавить питомца с валидными данными (без фото)'''
def test_add_new_pet_dezPHOTO_valid_data(name='Бoкk', animal_type='дворняга', age=6):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца из библиотеки, передаем аут.ключ, имя, породу, возраст
    status, result = pf.post_add_new_pet_No_PHOTO(auth_key, name, animal_type, age)
    # print(result['name'], '****')
    # проверяем полученные ответы статус кода, сверяем имя, отсутствие фото
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''


# '''Проверяем возможность добавить фото питомцу'''
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


# '''Проверяем возможность добавить питомца с валидными данными и фото. БАГ: age принимает только str'''
def test_add_new_pet_and_PHOTO_valid_data(name='Бorissovich', animal_type='дворняга', age='9',
                                          pet_photo='images/image.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца передаем данные
    status, result = pf.post_add_new_pet_and_Photo(auth_key, name, animal_type, age, pet_photo)
    # проверяем полученные ответы статус кода, присутствие фото
    assert status == 200
    assert result['pet_photo'] != ''


# '''проверяем возможность удалить питомца по его id'''
def test_delete_valid_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # print(auth_key,'****')
    # получаем список питомцев
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


# Проверяем возможность обновить данные о существующем питомце
def test_update_valid_pet(name='Vovano', animal_type='volk', age=18):
    # получаем через метод ключ
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # получаем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    id_pet = my_pets['pets'][0]['id']
    # вызываем метод земеняющий информацию о питомце который первый в списке
    status, result = pf.put_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
    # обновляем список питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    new_name = my_pets['pets'][0]['name']
    new_id_pet = my_pets['pets'][0]['id']
    # проверяем что имя питомца поменялось, ид питомца осталось прежним
    assert status == 200
    assert new_name == name
    assert id_pet == new_id_pet


