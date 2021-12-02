from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


class TestUserDelete(BaseCase):
    BUG_TRACKER_LINK = 'https://bugtracker_link'

    @allure.link(BUG_TRACKER_LINK, name='Bug report')
    @allure.title("Delete user with user id 2")
    @allure.description('This test checks that it impossible to delete user with id 2')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_user_id_2(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, 'user_id')

        response2 = MyRequests.delete(f'/user/{user_id}',
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response2, 400)
        assert response2.content.decode('utf-8') == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", \
            f'Unexpected response content {response2.content}'

    @allure.title("Delete just created user")
    @allure.description('This test successfully deletes just created user')
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_just_created_user(self):
        # REGISTER
        with allure.step(f"REGISTER new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user', data=register_data)

            Assertions.assert_status_code(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        # LOGIN
        with allure.step(f"LOGIN new user id {user_id}"):
            login_data = {
                'email': email,
                'password': password
            }
            response2 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # DELETE
        with allure.step(f"DELETE new user id {user_id}"):
            response3 = MyRequests.delete(f'/user/{user_id}',
                                          headers={"x-csrf-token": token},
                                          cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response3, 200)

        # GET
        with allure.step(f"GET new user {user_id}"):
            response4 = MyRequests.get(f'/user/{user_id}',
                                       headers={"x-csrf-token": token},
                                       cookies={"auth_sid": auth_sid})

        Assertions.assert_status_code(response4, 404)
        assert response4.content.decode('utf-8') == "User not found", \
            f'Unexpected response content {response4.content}'

    @allure.title("Delete user after auth as another user")
    @allure.description('This test checks that it impossible to delete user from another auth user')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_auth_as_another_user(self):
        # REGISTER user_1
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        user_1_email = register_data['email']
        user_1_password = register_data['password']
        user_1_id = self.get_json_value(response1, 'id')

        # REGISTER user_2
        register_data = self.prepare_registration_data()
        response2 = MyRequests.post('/user', data=register_data)

        Assertions.assert_status_code(response2, 200)
        Assertions.assert_json_has_key(response2, 'id')

        user_2_id = self.get_json_value(response2, 'id')

        # LOGIN user_1
        login_data = {
            'email': user_1_email,
            'password': user_1_password
        }
        response3 = MyRequests.post('/user/login', data=login_data)

        user_1_auth_sid = self.get_cookie(response3, "auth_sid")
        user_1_token = self.get_header(response3, "x-csrf-token")

        # DELETE user_2 by user_1
        response4 = MyRequests.delete(f'/user/{user_2_id}',
                                      headers={"x-csrf-token": user_1_token},
                                      cookies={"auth_sid": user_1_auth_sid})

        Assertions.assert_status_code(response4, 200)

        # GET user_2
        response5 = MyRequests.get(f'/user/{user_2_id}')

        Assertions.assert_status_code(response5, 200)
        Assertions.assert_json_has_key(response5, 'username')
