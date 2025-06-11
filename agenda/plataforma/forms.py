from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Service, Especialidades
from django.forms import inlineformset_factory

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    username = forms.CharField(label='Nome do usuário', min_length=4, max_length=150)
    email = forms.EmailField(label='E-mail')
    password1 = forms.CharField(label='Senha', min_length=8, widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar senha', min_length=8, widget=forms.PasswordInput)
    is_provider = forms.BooleanField(label='Sou uma empresa', required=False)
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if User.objects.filter(username=username).exists():
            raise ValidationError("Nome do usuário já existe")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Já existe uma conta com este e-mail")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("As senhas não são iguais")
        return cleaned_data

    def save(self, commit=True):
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            is_provider=self.cleaned_data.get('is_provider', False),
            is_staff=False,
            is_superuser=False
        )
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Usuário ou E-mail')

    def clean(self):
        username = self.cleaned_data.get('username')

        if '@' in username:
            try:
                user = User.objects.get(email=username)
                self.cleaned_data['username'] = user.username
            except User.DoesNotExist:
                pass

        return super().clean()

class ServiceConfigForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['empresa', 'descricao', 'localizacao']

class EspecialidadesForm(forms.ModelForm):
    class Meta:
        model = Especialidades
        fields = ['nome', 'preco']

EspecialidadesFormSet = inlineformset_factory(
    Service, Especialidades, form=EspecialidadesForm,
    fields=['nome', 'preco'], extra=1, can_delete=True
)