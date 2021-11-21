# URL: https://playground.learnqa.ru/ajax/api/longtime_job
# Если мы вызываем его БЕЗ GET-параметра token, метод заводит новую задачу, а в ответ выдает нам JSON со следующими
# полями:
# * seconds - количество секунд, через сколько задача будет выполнена
# * token - тот самый токен, по которому можно получить результат выполнения нашей задачи
# Если же вызвать метод, УКАЗАВ GET-параметром token, то мы получим следующий JSON:
# * error - будет только в случае, если передать token, для которого не создавалась задача.
# В этом случае в ответе будет следующая надпись - No job linked to this token
# * status - если задача еще не готова, будет надпись Job is NOT ready, если же готова - будет надпись Job is ready
# * result - будет только в случае, если задача готова, это поле будет содержать результат
# Наша задача - написать скрипт, который делал бы следующее:
# 1) создавал задачу
# 2) делал один запрос с token ДО того, как задача готова, убеждался в правильности поля status
# 3) ждал нужное количество секунд с помощью функции time.sleep() - для этого надо сделать import time
# 4) делал бы один запрос c token ПОСЛЕ того, как задача готова, убеждался в правильности поля status и
# наличии поля result

import requests
from json.decoder import JSONDecodeError
import time


class Job:
    def __init__(self, token, seconds=0):
        self.token = token
        self.seconds = seconds
        self.status = None
        self.result = None

    def __repr__(self):
        return f'token: {self.token}, sec:{self.seconds}, status:{self.status}, result:{self.result}'


class JobsManager:
    def __init__(self, url):
        self.url = url
        self.token_key = 'token'
        self.seconds_key = 'seconds'
        self.status_key = 'status'
        self.result_key = 'result'
        self.error_key = 'error'

    def create_job(self):  # Создание задачи на сервере
        response = requests.get(self.url)
        try:
            json_response = response.json()
        except JSONDecodeError:
            print('Error: Response is not a JSON format')
            return False
        if self.token_key in json_response and self.seconds_key in json_response:  # если ключи есть, создаём объект
            new_job = Job(json_response[self.token_key], json_response[self.seconds_key])
            return new_job
        else:
            print('Error: No key in JSON')
            return False

    def update_job(self, job):  # Обновление статуса задачи
        payload = f'token={job.token}'
        response = requests.get(self.url, params=payload)
        try:
            json_response = response.json()
        except JSONDecodeError:
            print('Error: Response is not a JSON format')
            return False
        if self.status_key in json_response:
            job.status = json_response[self.status_key]
        if self.result_key in json_response:
            job.result = json_response[self.result_key]
        if self.error_key in json_response:  # печать ошибки, если неверный токен
            print(f'Error: {json_response[self.error_key]}, token={job.token}')
        return job


jm = JobsManager('https://playground.learnqa.ru/ajax/api/longtime_job')  # создаём менеджер задач
my_job = None

while not my_job:  # пытаемся создать задачу, пока не создадим успешно
    my_job = jm.create_job()
    print(f'Создана новая задача - {my_job}')

print(f'Первая проверка задачи - {jm.update_job(my_job)}')
timeout = my_job.seconds + 1
print(f'Ждем выполнения задачи  - {timeout} сек.')
time.sleep(timeout)
print(f'Вторая проверка задачи - {jm.update_job(my_job)}')

print(f'\nПроверка статуса несуществующей задачи:')
fake_job = Job('fake_token')
print(f'Задача - {jm.update_job(fake_job)}')
