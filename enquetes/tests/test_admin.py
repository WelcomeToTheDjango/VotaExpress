import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse_lazy
from django.test import TestCase

from ..forms import GetDataFromCSVForm
from ..models import User, Enquete, Categoria, Pergunta, Opcoes, Voto

# TODO: Better error validation


class BaseCSVUploadTest(TestCase):
    url = None
    base_url = None
    csv_content_valid = None

    @classmethod
    def setUpTestData(cls):
        """
        Set up non-modified objects used by all test methods
        """

        if cls is BaseCSVUploadTest:
            raise unittest.SkipTest("Skip BaseCSVUploadTest tests, it's a base class")

        cls.username = "admin"
        cls.password = "admin"

        User.objects.create_superuser(cls.username, "admin@example.com", cls.password)

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
        self.assertIsInstance(response.context["form"], GetDataFromCSVForm)

    def test_post_request_valid_csv(self):
        """
        Check if the upload of a valid csv is working
        """

        csv_file = SimpleUploadedFile("test.csv", self.csv_content_valid)
        response = self.client.post(self.url, {"csv": csv_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.base_url)
        self.assertEqual(self.get_model().objects.count(), 2)

    def test_post_request_invalid_csv(self):
        """
        Verify if the upload of an invalid csv is being handled properly
        """

        csv_content = b"invalid content of csv files"
        csv_file = SimpleUploadedFile("test.csv", csv_content)
        response = self.client.post(self.url, {"csv": csv_file})

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_url=self.base_url)

    def get_model(self):
        """
        Get the model to be used in the tests, used to count objects

        Only the subclasses should implement this method
        """

        pass


class UserCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the User model
    """

    url = reverse_lazy("admin:enquetes_user_upload_csv")
    base_url = reverse_lazy("admin:enquetes_user_changelist")
    csv_content_valid = b"username,password\nuser1,password1"

    def get_model(self):
        return User


class EnqueteCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the Enquete model
    """

    url = reverse_lazy("admin:enquetes_enquete_upload_csv")
    base_url = reverse_lazy("admin:enquetes_enquete_changelist")
    csv_content_valid = b"categoria_id,criador_id,titulo\n1,1,Habitos Alimentares\n1,1,Entretenimento e cultura"

    @classmethod
    def setUpTestData(cls):
        """
        Create a Categoria object to be used in the tests
        """

        super().setUpTestData()
        Categoria.objects.create(titulo="Categoria 1")

    def get_model(self):
        return Enquete


class CategoriaCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the Categoria model
    """

    url = reverse_lazy("admin:enquetes_categoria_upload_csv")
    base_url = reverse_lazy("admin:enquetes_categoria_changelist")
    csv_content_valid = b"titulo\nCategoria 1\nCategoria 2"

    def get_model(self):
        return Categoria


class PerguntaCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the Pergunta model
    """

    url = reverse_lazy("admin:enquetes_pergunta_upload_csv")
    base_url = reverse_lazy("admin:enquetes_pergunta_changelist")
    csv_content_valid = (
        b"enquete_id,titulo\n1,Qual o seu prato favorito?\n1,Qual o seu filme favorito?"
    )

    @classmethod
    def setUpTestData(cls):
        """
        Create a Categoria and Enquete object to be used in the tests
        """

        super().setUpTestData()
        Categoria.objects.create(titulo="Categoria 1")
        Enquete.objects.create(categoria_id=1, criador_id=1, titulo="Enquete 1")

    def get_model(self):
        return Pergunta


class OpcoesCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the Opcoes model
    """

    url = reverse_lazy("admin:enquetes_opcoes_upload_csv")
    base_url = reverse_lazy("admin:enquetes_opcoes_changelist")
    csv_content_valid = b"pergunta_id,descricao\n1,Arroz\n1,Feijao"

    @classmethod
    def setUpTestData(cls):
        """
        Create a Categoria, Enquete and Pergunta object to be used in the tests
        """

        super().setUpTestData()
        Categoria.objects.create(titulo="Categoria 1")
        Enquete.objects.create(categoria_id=1, criador_id=1, titulo="Enquete 1")
        Pergunta.objects.create(enquete_id=1, titulo="Pergunta 1")

    def get_model(self):
        return Opcoes


class VotosCSVUploadTest(BaseCSVUploadTest):
    """
    Test the upload of a csv file for the Voto model
    """

    url = reverse_lazy("admin:enquetes_voto_upload_csv")
    base_url = reverse_lazy("admin:enquetes_voto_changelist")
    csv_content_valid = (
        b"usuario_id,enquete_id,pergunta_id,resposta_id\n1,1,1,1\n1,1,1,1"
    )

    @classmethod
    def setUpTestData(cls):
        """
        Create a Categoria, Enquete, Pergunta and Opcoes object to be used in the tests
        """

        super().setUpTestData()
        Categoria.objects.create(titulo="Categoria 1")
        Enquete.objects.create(categoria_id=1, criador_id=1, titulo="Enquete 1")
        Pergunta.objects.create(enquete_id=1, titulo="Pergunta 1")
        Opcoes.objects.create(pergunta_id=1, descricao="Opcao 1")

    def get_model(self):
        return Voto
