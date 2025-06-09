from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('cliente', 'Cliente'),
        ('prestador', 'Prestador de Serviço'),
    )
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO)

    def is_cliente(self):
        return self.tipo == 'cliente'

    def is_prestador(self):
        return self.tipo == 'prestador'

class PerfilCliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'Cliente: {self.usuario.username}'

class PerfilPrestador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nome_empresa = models.CharField(max_length=100)
    servico_oferecido = models.CharField(max_length=100)
    endereco = models.TextField()

    def __str__(self):
        return f'{self.nome_empresa} - {self.usuario.username}'


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Usuario)
def criar_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        if instance.tipo == 'cliente':
            PerfilCliente.objects.create(usuario=instance)
        elif instance.tipo == 'prestador':
            PerfilPrestador.objects.create(usuario=instance)