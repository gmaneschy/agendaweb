from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login



# Create your views here.
def login(request):
    login_form = LoginForm()
    register_form = RegistroForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                return redirect('home')  # Redirecione para sua home ou dashboard

        elif 'register_submit' in request.POST:
            register_form = RegistroForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                auth_login(request, user)
                return redirect('home')

    return render(request, 'login.html', {
        'login': login_form,
        'registro': register_form,
    })

@login_required
def home(request):
    return render(request, 'home.html')