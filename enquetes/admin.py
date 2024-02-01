from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from django.contrib import messages
from django.db import transaction
from django.contrib import admin

import csv

from enquetes.models import User, Enquete, Pergunta, Opcoes, Voto, Categoria
from enquetes.forms import GetDataFromCSVForm


class CustomAdmin(admin.ModelAdmin):
    """
    Improve the functionality of uploading data via .csv
    """

    change_list_template = "admin/customs/change_list.html"

    def get_urls(self):
        """
        Add the url of the upload_csv view to the admin urls
        """

        urls = super().get_urls()
        new_urls = [path("upload-csv/", self.upload_csv)]

        return new_urls + urls

    def upload_csv(self, request):
        """
        Handle the upload of .csv files

        GET: Shows the form to upload the .csv file

        POST: Reads the .csv file and saves the data to the database
        """

        if request.method == "GET":
            form = GetDataFromCSVForm()

        elif request.method == "POST":
            form = GetDataFromCSVForm(request.POST, request.FILES)

            if form.is_valid():
                # Read the .csv file
                csv_file = form.cleaned_data["csv"]
                data_array_by_rows = csv_file.read().decode("utf-8").splitlines()
                csv_reader = csv.DictReader(data_array_by_rows)

                # Using a transaction to save all data as a single transaction, so if an error occurs, all previous processes are rolled back
                try:
                    with transaction.atomic():
                        for dict_obj in csv_reader:
                            # If the model is User, we create a user using the create_user method for password hashing
                            if self.model == User:
                                User.objects.create_user(**dict_obj)
                            else:
                                self.model.objects.create(**dict_obj)

                # Show error message when the .csv file is not in the correct format
                except Exception as e:
                    messages.warning(
                        request,
                        "Não foi possivel processar sua solicitação, por favor verifique o formato de seu arquivo",
                    )
                    messages.error(request, f"{e}")
                    return HttpResponseRedirect(request.path_info)
                else:
                    # Show success message when the data is saved successfully
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
    """
    Register the Opcoes model as part of the Pergunta admin view
    """

    model = Opcoes
    extra = 1


@admin.register(Pergunta)
class PerguntaAdmin(CustomAdmin):
    """
    Register the Pergunta model and put an Opcoes formset inside it
    """

    inlines = [OpcoesInline]


class PerguntaInline(admin.TabularInline):
    """
    Register the Pergunta model as part of the Enquete admin view
    """

    model = Pergunta
    extra = 1
    show_change_link = True


@admin.register(Enquete)
class EnqueteAdmin(CustomAdmin):
    """
    Register the Enquete model and put a Pergunta formset inside it
    """

    list_display = ["titulo", "criador"]
    search_fields = ["titulo", "criador"]
    inlines = [PerguntaInline]


@admin.register(Voto)
class VotoAdmin(CustomAdmin):
    """
    Register the Voto model in the admin panel
    """

    pass


@admin.register(Categoria)
class CategoriaAdmin(CustomAdmin):
    """
    Register the Categoria model in the admin panel
    """

    pass


@admin.register(User)
class UserAdmin(CustomAdmin):
    """
    Register the User model in the admin panel
    """

    pass


@admin.register(Opcoes)
class OpcoesAdmin(CustomAdmin):
    """
    Register the Opcoes model in the admin panel
    """

    pass
