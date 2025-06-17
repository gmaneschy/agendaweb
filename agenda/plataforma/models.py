
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    is_provider = models.BooleanField("É provedor de serviço?", default=False)

class Service(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    empresa = models.CharField('Empresa', max_length=100)
    descricao = models.CharField('Descrição', max_length=100, default='Descreva sua empresa')
    localizacao = models.CharField('Endereço', max_length=150)
    portifolio = models.FileField('Portfólio (PDF, imagens, etc)', upload_to='portfolios/', blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empresa} - {self.descricao} - {self.localizacao}"

class Especialidades(models.Model):
    servicos = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='Serviços', blank=True)
    nome = models.CharField('Nome do Serviço', max_length=100, blank=True)
    preco = models.DecimalField('Preço', max_digits=7, decimal_places=2, blank=True)
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"