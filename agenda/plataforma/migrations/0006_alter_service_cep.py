# Generated by Django 5.2.2 on 2025-06-18 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0005_alter_service_cep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='cep',
            field=models.CharField(blank=True, max_length=9, verbose_name='CEP'),
        ),
    ]
