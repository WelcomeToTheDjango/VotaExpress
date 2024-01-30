import csv
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.db import transaction
from django.contrib import admin
from enquetes.models import User, Enquete, Pergunta, Opcoes, Voto, Categoria

from enquetes.forms import GetDataFromCSVForm


class CustomAdmin(admin.ModelAdmin):
    """
    Classe personalizada para adicionar a funcionalidade de subir dados via .csv
    """

    change_list_template = "admin/customs/change_list.html"

    def get_urls(self):
        """
        Adiciona o registro de uma nova url no admin
        """

        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv)]

        return new_urls + urls

    def upload_csv(self, request):
        """
        Faz o envio de dados via um arquivo .csv

        GET: Mostra um form com um unico campo pra carregar .csv

        POST: Faz o processamento do form e salva os dados no banco de dados
        """

        if request.method == "GET":
            form = GetDataFromCSVForm()

        if request.method == "POST":
            form = GetDataFromCSVForm(request.POST, request.FILES)

            if form.is_valid():
                # tratando os dados com livaria csv de python
                csv_file = form.cleaned_data["csv"]
                data_array_by_rows = csv_file.read().decode("utf-8").splitlines()
                csv_reader = csv.DictReader(data_array_by_rows)

                # encapsulando o salvado em uma só transaction
                try:
                    with transaction.atomic():
                        for dict_obj in csv_reader:
                            # usando metodo especial para hashear password cuando o modelo é user
                            if self.model == User:
                                User.objects.create_user(**dict_obj)
                            else:
                                self.model.objects.create(**dict_obj)

                # dando mensagem de erro e redireccionado para url anterior
                except Exception as e:
                    messages.warning(
                        request,
                        "Não foi possivel processar sua solicitação, por favor verifique o formato de seu arquivo",
                    )
                    messages.error(request, f"{e}")  # informacões do erro
                    return HttpResponseRedirect(request.path_info)
                else:
                    # dando mensagem de sucesso e redirecionado para change list do respetivo modelo
                    messages.success(
                        request, "Seus dados foram carregados com sucesso!"
                    )
                    changelist_url = reverse(
                        "admin:%s_%s_changelist"
                        % (self.model._meta.app_label, self.model._meta.model_name)
                    )
                    return redirect(changelist_url)

        context = {"nome_do_modelo": self.model.__name__, "form": form}

        return render(request, "admin/csv_upload.html", context)


class OpcoesInline(admin.TabularInline):
    """para registrar as Opções como parte da admin view de Perguntas"""

    model = Opcoes
    extra = 1


@admin.register(Pergunta)
class PerguntaAdmin(CustomAdmin):
    """registra o modelo Pergunta e coloca um formset de Opções dentro dele"""

    inlines = [OpcoesInline]


class PerguntaInline(admin.TabularInline):
    """para registrar as Perguntas como parte da admin view de Enquete"""

    model = Pergunta
    extra = 1
    show_change_link = True


@admin.register(Enquete)
class EnqueteAdmin(CustomAdmin):
    """registra o modelo Enquete y coloca um form de Pergunta dentro dele"""

    list_display = ["titulo", "criador"]
    search_fields = ["titulo", "criador"]
    inlines = [PerguntaInline]


@admin.register(Voto)
class VotoAdmin(CustomAdmin):
    """registra o modelo Voto em Uso"""

    pass


@admin.register(Categoria)
class CategoriaAdmin(CustomAdmin):
    pass


@admin.register(User)
class UserAdmin(CustomAdmin):
    pass


@admin.register(Opcoes)
class OpcoesAdmin(CustomAdmin):
    pass
