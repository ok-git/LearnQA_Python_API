# Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_header
# Этот метод возвращает headers с каким-то значением. Необходимо с помощью функции print() понять что за headers и с
# каким значением, и зафиксировать это поведение с помощью assert

import requests


class TestAPI:
    def test_api(self):
        url = 'https://playground.learnqa.ru/api/homework_header'
        response = requests.get(url)
        # print(response.headers)
        expected_header = 'x-secret-homework-header'
        expected_value = 'Some secret value'
        assert expected_header in response.headers, 'There is no secret header in response'
        assert response.headers[expected_header] == expected_value, 'Wrong secret header value'
