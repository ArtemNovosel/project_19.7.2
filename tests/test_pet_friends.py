from api import PetFriends  # импортируем созданную библиотеку
from settings import *  # добавляем регистрационные данные
import os  # библиотека для указания пути к файлу

# инициализируем созданную библиотеку присваиванием переменной
pf = PetFriends()

'''тест который проверяет обработку сервером валидных email & password'''


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    # из биюлиотеки вызываем метод, результаты прискваиваем переменным
    status, result = pf.get_api_key(email, password)
    # сверяем результат по статусу и присутствию ключа в ответе
    assert status == 200
    assert "key" in result
    # print(result['key'])


'''Проверяем что запрос всех питомцев возвращает не пустой список. Доступное значение параметра filter - 'my_pets' либо ''  '''


def test_get_all_pets_with_valid_key(filter='my_pets'):
    # с помощью метода получаем аут.ключ присваиваем его значение переменной. статус код этого запроса нам не нужен
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # print(auth_key['key'])
    # вызываем метод получения списка питомцев передаем аут.ключ и filter
    status, result = pf.get_list_of_pets(auth_key, filter)
    # проверяем     что     список     не пустой.
    assert status == 200
    assert len(result['pets']) > 0


'''Проверяем возможность добавить питомца с валидными данными и фото. БАГ: age принимает только str '''


def test_add_new_pet_and_PHOTO_valid_data(name='Бorissovich', animal_type='дворняга', age='9',
                                          pet_photo='images/image.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # вызываем метод добавления питомца передаем данные
    status, result = pf.post_add_new_pet_and_Photo(auth_key, name, animal_type, age, pet_photo)
    # проверяем полученные ответы статус кода, присутствие фото
    assert status == 200
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
