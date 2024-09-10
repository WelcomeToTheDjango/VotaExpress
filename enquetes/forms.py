from django import forms
from enquetes.models import Categoria
from .models import User
from django import forms


class GetDataFromCSVForm(forms.Form):
    csv = forms.FileField()

    def clean_csv(self):
        csv = self.cleaned_data.get("csv")
        extension = csv.name.split(".")[-1].lower()

        if extension != "csv":
            raise forms.ValidationError("Só se permiten arquivos con extensão: csv")
        return csv



class Cadastrar(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Adicionando o campo de confirmação de senha
    password2 = forms.CharField(label='Confirmar senha', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get('senha1')
        senha2 = cleaned_data.get('senha2')

        if senha1 != senha2:
            raise forms.ValidationError("Senhas não coincidem.")

        return cleaned_data


