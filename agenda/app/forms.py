from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class RegistroForm(UserCreationForm):
    tipo = forms.ChoiceField(choices=Usuario.TIPO_USUARIO, widget=forms.RadioSelect)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
