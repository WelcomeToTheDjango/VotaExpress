from django import forms
from enquetes.models import Categoria

class GetDataFromCSVForm(forms.Form):
    csv =  forms.FileField()

    def clean_csv(self):
        csv = self.cleaned_data.get('csv')
        extension = csv.name.split('.')[-1].lower()
        
        if extension != 'csv':
            raise forms.ValidationError("Só se permiten arquivos con extensão: csv")
        return csv
    