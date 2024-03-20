from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_django
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.decorators import has_permission_decorator
from core.settings import LOGIN_REDIRECT_URL
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views


@has_permission_decorator('cadastro_user')
def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        tipo = request.POST.get('tipo')
        
        user = User.objects.filter(username=username).first()
        if user:
            # return HttpResponse('Usuário já existe')
            messages.add_message(request, messages.ERROR, 'Usuário já existe.')
            return redirect('cadastro')
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        assign_role(user, tipo)
        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso.')
        return redirect('cadastro')
        # return HttpResponse('Usuário cadastrado com sucesso')


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            login_django(request, user)
            return redirect('sgc_home')
        else:
            messages.add_message(request, messages.ERROR, 'Usuário ou senha incorretos.')
            return redirect('login')


@login_required(login_url="/auth/login/")
def plataforma(request):
    user = request.user
    user_roles = get_user_roles(user)
    
    return render(request, 'home.html', {'user': user, 'user_roles': user_roles})


# @login_required(login_url="/auth/login/")
@login_required(login_url="login")
def reset(request):
    if request.method == "GET":
        users = User.objects.all()
        return render(request, 'reset.html', {'users': users})
    else:
        username = request.POST.get('username')
        password2 = request.POST.get('password2')
        password = request.POST.get('password')
        
        if password == password2:
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso.')
            return redirect('reset')
        else:
            messages.add_message(request, messages.ERROR, 'As senhas fornecidas não correspondem. Por favor, verifique e tente novamente.')
            return redirect('reset')

@login_required
def custom_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged out successfully!')
    return redirect("/")