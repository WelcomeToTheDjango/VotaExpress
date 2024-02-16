# This file is used to test the views of the application

from django.urls import reverse_lazy
from django.test import TestCase

from ..models import User


class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """

        cls.LOGIN_URL = f"{reverse_lazy('account_login')}?next={reverse_lazy('home')}"
        cls.HOME_URL = reverse_lazy("home")
        cls.username = "admin"
        cls.password = "admin"

        User.objects.create_user(username=cls.username, password=cls.password)

    def test_should_return_200_when_logged_in(self):
        """
        Check if the login works properly
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.HOME_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "enquetes/home.html")

    def test_should_redirect_if_not_logged_in(self):
        """
        Check if the non-logged user is redirect to the right login page
        """

        response = self.client.get(self.HOME_URL)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.LOGIN_URL)

    def test_should_use_home_template_when_logged_in(self):
        """
        Check if the home template is being used
        """

        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.HOME_URL)
        self.assertTemplateUsed(response, "enquetes/home.html")
