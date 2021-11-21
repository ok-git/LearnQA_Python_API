import pytest
import requests


class TestUserAuth:
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]

    def setup(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)

        assert "auth_sid" in response1.cookies,  "There is no auth cookie in response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token in response"
        assert "user_id" in response1.json(), "There is no user_id in response"

        self.auth_sid = response1.cookies.get("auth_sid")
        self.token = response1.headers.get("x-csrf-token")
        self.user_id_from_auth_method = response1.json()["user_id"]

    def test_auth_user(self):

        response2 = requests.get(
            'https://playground.learnqa.ru/api/user/auth',
            headers={"x-csrf-token": self.token},
            cookies={"auth_sid": self.auth_sid}
        )
        