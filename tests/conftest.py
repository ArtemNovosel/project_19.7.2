import pytest
from settings import *
from api import PetFriends
from datetime import datetime
import sys
pf = PetFriends()


#фикстура должна находится в файле с тестами или conftest
@pytest.fixture(scope="class") #запускается автоматически
def fix_get_api_key():
    # Сохраняем ключ в pytest.key *** чтобы он передовался в тест
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    assert status == 200
    assert 'key' in pytest.key
    yield
    assert status == 200


@pytest.fixture(autouse=True)  #фикстура логирует запущенный тест если в ее названии есть Pets
def request_fixtur(request):
    with open("log.txt", "a") as f:
        f.write(f"{request.function.__name__} \n")
    print('*',request.fixturename)
    print('**',request.scope)
    print(request.function.__name__)
    print(request.cls)
    print(request.module.__name__)
    print(request.fspath,'***')
    if request.cls:
        return f"\n У теста {request.function.__name__} класс есть\n"
    else:
        return f"\n У теста {request.function.__name__} класса нет\n"


@pytest.fixture(autouse=True) #autouse запускает автоматически при выполнении любого теста
def time_delta():
    start_time = datetime.now()
    yield #ключ заставляющий исполняться основной тест
    end_time = datetime.now() #teardown (после теста/действия)
    print (f"\nТЕСТ ШЕЛ: {end_time - start_time}")
    with open("log.txt", "a") as f:
        f.write(f"{end_time - start_time} \n")


