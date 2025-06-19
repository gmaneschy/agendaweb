from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ServiceConfigForm, EspecialidadesForm
from .models import Service, Especialidades

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
    especialidades = Especialidades.objects.select_related('servicos').all()
    return render(request, 'home.html', {'especialidades': especialidades})


@login_required
def serviceconfig(request):
    service, created = Service.objects.get_or_create(usuario=request.user)
    service_form = ServiceConfigForm(request.POST or None, request.FILES or None, instance=service)
    especialidade_form = EspecialidadesForm(request.POST or None, service=service)
    especialidades = Especialidades.objects.filter(servicos=service)

    if request.method == 'POST':
        # Verifica se é uma requisição AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if 'add_especialidade' in request.POST:
                especialidade_form = EspecialidadesForm(request.POST, service=service)
                if especialidade_form.is_valid():
                    especialidade = especialidade_form.save()
                    return JsonResponse({
                        'success': True,
                        'id': especialidade.id,
                        'nome': especialidade.nome,
                        'preco': str(especialidade.preco)
                    })
                return JsonResponse({
                    'success': False,
                    'error': 'Dados inválidos',
                    'errors': especialidade_form.errors.as_json()
                })

            elif 'save_service' in request.POST:
                if service_form.is_valid():
                    service = service_form.save(commit=False)
                    service.usuario = request.user
                    service.save()
                    return JsonResponse({'success': True})
                return JsonResponse({
                    'success': False,
                    'error': 'Dados inválidos',
                    'errors': service_form.errors.as_json()
                })

            return JsonResponse({'success': False, 'error': 'Ação não reconhecida'})

        # Processamento normal do formulário
        if 'finalizar' in request.POST:
            messages.success(request, 'Configuração concluída com sucesso!')
            return redirect('home')

        elif service_form.is_valid():
            service = service_form.save(commit=False)
            service.usuario = request.user
            service.save()
            messages.success(request, 'Dados da empresa atualizados com sucesso!')
            return redirect('serviceconfig')

    return render(request, 'serviceconfig.html', {
        'service_form': service_form,
        'especialidade_form': especialidade_form,
        'especialidades': especialidades,
    })


@login_required
def remover_especialidade(request, especialidade_id):
    especialidade = get_object_or_404(Especialidades, id=especialidade_id)

    if especialidade.servicos.usuario == request.user:
        especialidade.delete()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, 'Serviço removido com sucesso!')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Permissão negada'})
        messages.error(request, 'Você não tem permissão para remover este serviço.')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('serviceconfig')

@login_required
def usuario(request):
    pass