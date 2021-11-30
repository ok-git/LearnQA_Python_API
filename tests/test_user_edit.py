from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = 'Changed Name'
        response3 = MyRequests.put(f'/user/{user_id}',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name})

        Assertions.assert_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(f'/user/{user_id}',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response4,
            'firstName',
            new_name,
            'Wrong name of the user after edit'
        )

    def test_edit_no_auth_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_id = self.get_json_value(response1, 'id')

        # EDIT
        new_name = 'Changed Name'
        response2 = MyRequests.put(f'/user/{user_id}',
                                   data={'firstName': new_name})

        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode('utf-8') == "Auth token not supplied", \
            f'Unexpected response content {response2.content}'

    def test_edit_auth_as_another_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT another user_id 2
        new_name = 'Changed Name'
        response3 = MyRequests.put('/user/2',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_name})

        Assertions.assert_status_code(response3, 200)

        # LOGIN as user_id 2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response4 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response4, "auth_sid")
        token = self.get_header(response4, "x-csrf-token")

        # GET user_id 2
        response5 = MyRequests.get('/user/2',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(
            response5,
            'firstName',
            'Vitalii',
            'Wrong username of the user after edit from another auth user'
        )

    def test_edit_just_created_user_invalid_email(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_email = 'new.email.com'
        response3 = MyRequests.put(f'/user/{user_id}',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'email': new_email})

        Assertions.assert_status_code(response3, 400)
        assert response3.content.decode('utf-8') == f"Invalid email format", \
            f'Unexpected response content {response3.content}'

    def test_edit_just_created_user_invalid_firstname(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post('/user/login', data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_firstname = '1'
        response3 = MyRequests.put(f'/user/{user_id}',
                                   headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid},
                                   data={'firstName': new_firstname})

        Assertions.assert_status_code(response3, 400)
        Assertions.assert_json_value_by_name(
            response3,
            "error",
            "Too short value for field firstName",
            f"Unexpected response content {response3.content}'"
        )
