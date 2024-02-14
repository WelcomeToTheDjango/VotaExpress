from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from django.test import TestCase

from ..forms import GetDataFromCSVForm
from ..models import User

# TODO: Make the code more generic to be used in other models
# TODO: Better error validation

class CSVUploadTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """
        
        cls.username = "admin"
        cls.password = "admin"
        cls.url = reverse_lazy("admin:enquetes_user_upload_csv") 
        cls.base_url = reverse_lazy("admin:enquetes_user_changelist")

        User.objects.create_superuser(cls.username, 'admin@example.com', cls.password)

    def setUp(self):
        """
        Set up objects used by all test methods
        """

        self.client.login(username=self.username, password=self.password)

    def test_get_request(self):
        """
        Check if the form is being rendered properly     
        """

        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], GetDataFromCSVForm)

    def test_post_request_valid_csv(self):
        """
        Check if the upload of a valid csv is working
        """

        csv_content = b'username,password\nuser1,password1\nuser2,password2'
        csv_file = SimpleUploadedFile('test.csv', csv_content)
        response = self.client.post(self.url, {'csv': csv_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.base_url)
        self.assertEqual(User.objects.count(), 3)

    def test_post_request_invalid_csv(self):
        """
        Verify if the upload of an invalid csv is being handled properly
        """

        csv_content = b'invalid content of csv files'
        csv_file = SimpleUploadedFile('test.csv', csv_content)
        response = self.client.post(self.url, {'csv': csv_file})
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.base_url)
        self.assertEqual(User.objects.count(), 1)
