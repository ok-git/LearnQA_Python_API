from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import random
import string
import pytest


class TestUserRegister(BaseCase):
    exclude_fields = [
        'password',
        'username',
        'firstName',
        'lastName',
        'email'
    ]

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"Users with email '{email}' already exists",\
            f'Unexpected response content {response.content}'

    def test_create_user_with_incorrect_email(self):
        email = 'vinkotov.example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"Invalid email format",\
            f'Unexpected response content {response.content}'

    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] = '0'

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too short",\
            f'Unexpected response content {response.content}'

    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()

        symbols = string.ascii_letters + string.digits
        data['username'] = "".join([random.choice(symbols) for i in range(251)])

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The value of 'username' field is too long", \
            f'Unexpected response content {response.content}'

    @pytest.mark.parametrize('exclude_field', exclude_fields)
    def test_create_user_without_field(self, exclude_field):
        data = self.prepare_registration_data()
        data.pop(exclude_field)

        response = MyRequests.post('/user', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f"The following required params are missed: {exclude_field}", \
            f'Unexpected response content {response.content}'
