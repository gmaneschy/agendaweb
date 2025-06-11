from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ServiceConfigForm, EspecialidadesFormSet

# Create your views here.
User = get_user_model()

def login(request):
    active_tab = 'login'  # Aba padrão

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            login_form = CustomAuthenticationForm(request, data=request.POST)
            register_form = CustomUserCreationForm()  # Formulário vazio

            if login_form.is_valid():
                user = login_form.get_user()
                auth_login(request, user)
                if user.is_provider:
                    return redirect('serviceconfig')
                else:
                    return redirect('home')
            active_tab = 'login'

        elif action == 'registro':
            login_form = CustomAuthenticationForm()  # Formulário vazio
            register_form = CustomUserCreationForm(request.POST)

            if register_form.is_valid():
                register_form.save()
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('login')
            else:
                active_tab = 'registro'  # Fica na aba de registro se houver erros

    else:  # GET
        login_form = CustomAuthenticationForm()
        register_form = CustomUserCreationForm()

    return render(request, 'login.html', {
        'login': login_form,
        'form': register_form,
        'active_tab': active_tab,
    })


@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def serviceconfig(request):
    if request.method == 'POST':
        service_form = ServiceConfigForm(request.POST, request.FILES)
        formset = EspecialidadesFormSet(request.POST)

        if service_form.is_valid() and formset.is_valid():
            service = service_form.save(commit=False)
            service.usuario = request.user
            service.save()

            formset.instance = service
            formset.save()

            messages.success(request, 'Serviço e especialidades salvos com sucesso!')
            return redirect('home')  # ou outra tela de confirmação

    else:
        service_form = ServiceConfigForm()
        formset = EspecialidadesFormSet()

    return render(request, 'serviceconfig.html', {
        'service_form': service_form,
        'formset': formset,
    })