# Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie
# Этот метод возвращает какую-то cookie с каким-то значением. Необходимо с помощью функции print() понять что за cookie
# и с каким значением, и зафиксировать это поведение с помощью assert

import requests


class TestAPI:
    def test_api(self):
        url = 'https://playground.learnqa.ru/api/homework_cookie'
        response = requests.get(url)
        # print(response.cookies)
        expected_cookie = 'HomeWork'
        expected_value = 'hw_value'
        assert expected_cookie in response.cookies, 'There is no cookie in response'
        assert response.cookies[expected_cookie] == expected_value, 'Wrong cookie value'
