# URL: https://playground.learnqa.ru/ajax/api/compare_query_type
# Запрашивать его можно четырьмя разными HTTP-методами: POST, GET, PUT, DELETE
# При этом в запросе должен быть параметр method. Он должен содержать указание метода,
# с помощью которого вы делаете запрос. Например, если вы делаете GET-запрос, параметр method должен равняться
# строке ‘GET’. Если POST-запросом - то параметр method должен равняться ‘POST’.  И так далее.
#
# Надо написать скрипт, который делает следующее:
# 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
# 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
# 3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.
#
# Не забывайте, что для GET-запроса данные надо передавать через params=, а для всех остальных через data=

import requests


def print_result(param, resp_code, resp_text):
    print(f'\tПараметр {param} \tКод ответа - {resp_code}, текст ответа - {resp_text}')


url = 'https://playground.learnqa.ru/ajax/api/compare_query_type'

requests_list = [requests.get, requests.post, requests.put,
                 requests.patch, requests.delete, requests.head, requests.options]
methods_list = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']


# Ответ на вопрос 1 и 2. Перебор всех типов запросов без параметра method
for request in requests_list:
    print(f'Запрос без параметров - {request.__name__} - ', end='')
    response = request(url)
    print_result('', response.status_code, response.text)


# Ответ на вопрос 3 и 4. Перебор всех типов запросов со всеми вариантами значения method
for request in requests_list:
    print(f'\nЗапрос - {request.__name__}:')
    if request.__name__ == 'delete':  # эта функция принимает 1 аргумент - url, параметр передаётся через url
        for method in methods_list:
            payload = f'?method={method}'
            response = request(url + payload)
            print_result(payload, response.status_code, response.text)
    elif request.__name__ not in ['head', 'options']:  # все остальные методы, принимающие параметр
        for method in methods_list:
            payload = f'method={method}'
            response = request(url, payload)
            print_result(payload, response.status_code, response.text)
    else:
        print("Запрос не принимает параметры")
