from time import sleep

from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_sucessfully(self):
        string_password = 'pass'
        user = User.objects.create_user(username='my_user', password=string_password)

        #user open the login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #user see the login form
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        #user write your username and password
        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        #user send the form
        form.submit()

        #user see the login message sucess and your name
        self.assertIn(
            f'Your are logged in with {user.username}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)
        
    def test_form_login_is_invalid(self):
        #user open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #user see login form
        form = self.browser.find_element(By.CLASS_NAME,'main-form')

        #try send empty fields
        username = self.get_by_placeholder(form, 'Type your username')
        password1 = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password1.send_keys(' ')

        #send the form
        form.submit()

        #see the error message
        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid_credentials(self):
        #user open login page
        self.browser.get(self.live_server_url + reverse('authors:login'))

        #user see login form
        form = self.browser.find_element(By.CLASS_NAME,'main-form')

        #try send data what not corresponding
        username = self.get_by_placeholder(form, 'Type your username')
        password1 = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('invalid_user')
        password1.send_keys('invalid_password')

        #send the form
        form.submit()

        #see the error message
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )