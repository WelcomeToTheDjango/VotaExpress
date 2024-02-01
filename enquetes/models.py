from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import Truncator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """
    This is a custom user model that extends the base Django model
    """

    pass

    def __str__(self):
        return self.username


class Categoria(models.Model):
    """
    This is a model to represent the categories of the polls

    titulo: The title of the category
    """

    titulo = models.CharField(max_length=120)

    def __str__(self):
        return self.titulo


class Enquete(models.Model):
    """
    This is a model to represent the polls

    titulo: The title of the poll
    categoria: The category of the poll, related 1 to 1 with Categoria model
    criador: The user that created the poll, related 1 to 1 with User model
    aberto: A boolean field to indicate if the poll is open or closed
    """

    titulo = models.CharField(max_length=120)
    categoria = models.ForeignKey(
        Categoria,
        blank=True,
        null=True,
        related_name="enquetes",
        on_delete=models.SET_NULL,
    )
    criador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="enquetes_criados"
    )
    aberto = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class Pergunta(models.Model):
    """
    This is a model to represent the questions of the polls

    titulo: The title of the question
    enquete: The poll that the question belongs to, related 1 to 1 with Enquete model
    """

    titulo = models.CharField(max_length=120)
    enquete = models.ForeignKey(
        Enquete, on_delete=models.CASCADE, related_name="perguntas"
    )

    def __str__(self):
        return self.titulo


class Opcoes(models.Model):
    """
    This is a model to represent the options of the questions

    descricao: The description of the option
    pergunta: The question that the option belongs to, related 1 to 1 with Pergunta model
    """

    descricao = models.TextField()
    pergunta = models.ForeignKey(
        Pergunta, on_delete=models.CASCADE, related_name="opcoes"
    )

    def __str__(self) -> str:
        """
        The truncator method is used to leave only the first 5 words of the description        
        """

        return Truncator(self.descricao).words(5)


class Voto(models.Model):
    """
    This is a model to represent the votes of the users

    usuario: The user that voted, related 1 to 1 with User model
    enquete: The poll that the vote belongs to, related 1 to 1 with Enquete model
    pergunta: The question that the vote belongs to, related 1 to 1 with Pergunta model
    resposta: The option that the user voted, related 1 to 1 with Opcoes model
    """

    usuario = models.ForeignKey(
        User, blank=True, null=True, related_name="votos", on_delete=models.SET_NULL
    )
    enquete = models.ForeignKey(Enquete, related_name="votos", on_delete=models.CASCADE)
    pergunta = models.ForeignKey(
        Pergunta, related_name="votos", on_delete=models.CASCADE
    )
    resposta = models.ForeignKey(
        Opcoes, blank=True, null=True, related_name="votos", on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"escolha #{self.resposta.id} em #{self.enquete.id}/{self.pergunta.id}"

    def save(self, *args, **kwargs):
        """
        This methos is used to validate the vote before saving it

        Raises:
            ValidationError: If the option chosen does not belong to the question
            ValidationError: If the question chosen does not belong to the poll
        """

        if self.resposta not in self.pergunta.opcoes.all():
            raise ValidationError(
                "resposta invalida, por favor escolha uma opcao que corresponda á pergunta"
            )

        if self.pergunta not in self.enquete.perguntas.all():
            raise ValidationError(
                "pergunta invalida, por favor escolha uma opcao que corresponda ao enquete"
            )

        super(Voto, self).save(*args, **kwargs) # Call the "real" save() method.
