from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Cadastrar
from django.contrib.auth.forms import AuthenticationForm

def registro(request):
    if request.method == 'POST':
        form = Cadastrar(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return render(request, 'registro/login.html', {'form': form})
        else:
            messages.error(request, 'Erro ao cadastrar usuário.')
    else:
        form = Cadastrar()
    return render(request, 'registro/registro.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect('home.html')
        else:
            messages.error(request, 'Credenciais inválidas.')
    else:
        form = AuthenticationForm()
    return render(request, 'registro/login.html', {'form': form})