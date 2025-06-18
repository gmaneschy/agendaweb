from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
import requests
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    is_provider = models.BooleanField("É provedor de serviço?", default=False)

class Service(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    empresa = models.CharField('Empresa', max_length=100)
    descricao = models.CharField('Descrição', max_length=100, default='Descreva sua empresa')

    cep = models.CharField('CEP', max_length=9, blank=True)
    rua = models.CharField('Rua', max_length=100, blank=True)
    numero = models.CharField('Número', max_length=10, blank=True)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = models.CharField('Estado', max_length=2, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    portifolio = models.FileField('Portfólio (PDF, imagens, etc)', upload_to='portfolios/', blank=True, null=True)

    def clean(self):
        cep_limpo = self.cep.replace("-", "").strip()
        if len(cep_limpo) != 8 or not cep_limpo.isdigit():
            raise ValidationError({'cep': 'CEP deve conter 8 dígitos numéricos.'})

        response = requests.get(f"https://brasilapi.com.br/api/cep/v1/{cep_limpo}")
        if response.status_code != 200:
            raise ValidationError({'cep': 'CEP inválido ou não encontrado.'})

    def save(self, *args, **kwargs):
        self.localizacao = f"{self.rua}, {self.numero} - {self.bairro}, {self.cidade} - {self.estado}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empresa} - {self.descricao} - {self.cidade}/{self.estado}"

class Especialidades(models.Model):
    servicos = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Serviços', blank=True)
    nome = models.CharField('Nome do Serviço', max_length=100, blank=True)
    preco = models.DecimalField('Preço', max_digits=7, decimal_places=2, blank=True)
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"