# This file is used to test the models of the application

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from ..models import Enquete, Categoria, Pergunta, Opcoes, User, Voto


class ModelTest(TestCase):
    """Test the models of the application"""

    @classmethod
    def setUpTestData(cls):
        """Create data to use in the tests"""

        user = User.objects.create_user(username="Joao", password="1234")

        categoria = Categoria.objects.create(titulo="Categoria Test")

        enquete = Enquete.objects.create(
            titulo="Enquete Test",
            categoria=categoria,
            criador=user,
        )

        pergunta = Pergunta.objects.create(titulo="Pergunta Test", enquete=enquete)

        opcao = Opcoes.objects.create(descricao="Opcao Test", pergunta=pergunta)

        voto = Voto.objects.create(
            usuario=user, enquete=enquete, pergunta=pergunta, resposta=opcao
        )

    def test_create_user(self):
        """Test the creation of a user"""

        user = User.objects.get(id=1)
        self.assertIsInstance(user, User)
        self.assertTrue(user.check_password("1234"))

    def test_create_categoria(self):
        """Test the creation of a Categoria"""

        categoria = Categoria.objects.get(id=1)
        self.assertIsInstance(categoria, Categoria)

    def test_create_enquete(self):
        """Test the creation of a Enquete"""

        enquete = Enquete.objects.get(id=1)
        self.assertIsInstance(enquete, Enquete)

    def test_create_pergunta(self):
        """Test the creation of a Pergunta"""

        pergunta = Pergunta.objects.get(id=1)
        self.assertIsInstance(pergunta, Pergunta)

    def test_create_opcao(self):
        """Test the creation of a Opcao"""

        opcao = Opcoes.objects.get(id=1)
        self.assertIsInstance(opcao, Opcoes)

    def test_create_voto(self):
        """Test the creation of a Voto"""

        voto = Voto.objects.get(id=1)
        self.assertIsInstance(voto, Voto)

    def test_user_str(self):
        """Test the __str__ method of the User model"""

        user = User.objects.get(id=1)
        self.assertEqual(user.__str__(), user.username)

    def test_categoria_str(self):
        """Test the __str__ method of the Categoria model"""

        categoria = Categoria.objects.get(id=1)
        self.assertEqual(categoria.__str__(), categoria.titulo)

    def test_enquete_str(self):
        """Test the __str__ method of the Enquete model"""

        enquete = Enquete.objects.get(id=1)
        self.assertEqual(enquete.__str__(), enquete.titulo)

    def test_pergunta_str(self):
        """Test the __str__ method of the Pergunta model"""

        pergunta = Pergunta.objects.get(id=1)
        self.assertEqual(pergunta.__str__(), pergunta.titulo)

    def test_opcao_str(self):
        """Test the __str__ method of the Opcao model"""

        opcao = Opcoes.objects.get(id=1)
        self.assertEqual(opcao.__str__(), opcao.descricao)

    def test_voto_str(self):
        """Test the __str__ method of the Voto model"""

        voto = Voto.objects.get(id=1)
        self.assertEqual(
            voto.__str__(),
            f"escolha #{voto.resposta.id} em #{voto.enquete.id}/{voto.pergunta.id}",
        )

    def test_voto_count(self):
        """Test the count of votes in an Enquete"""

        voto_by_enquete = Voto.objects.filter(enquete=Enquete.objects.get(id=1)).count()

        self.assertEqual(voto_by_enquete, 1)

    # Error Validations Tests

    def test_resposta_in_pergunta(self):
        """Test if the answer is in the question"""

        with self.assertRaises(Exception):
            Voto.objects.create(
                usuario=User.objects.get(id=1),
                enquete=Enquete.objects.get(id=1),
                pergunta=Pergunta.objects.get(id=1),
                resposta=Opcoes.objects.create(
                    descricao="Opcao Test 2", pergunta=Pergunta.objects.get(id=2)
                ),
            )

    def test_pergunta_in_enquete(self):
        """Test if the question is in the poll"""

        with self.assertRaises(ObjectDoesNotExist):
            Voto.objects.create(
                usuario=User.objects.get(id=1),
                enquete=Enquete.objects.get(id=1),
                pergunta=Pergunta.objects.create(
                    titulo="Pergunta Test 2", enquete=Enquete.objects.get(id=2)
                ),
                resposta=Opcoes.objects.get(id=1),
            )
