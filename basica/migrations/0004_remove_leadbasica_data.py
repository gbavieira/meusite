# Generated by Django 4.0.5 on 2022-07-07 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basica', '0003_leadbasica_concessionaria_leadbasica_cpf_cnpj_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadbasica',
            name='data',
        ),
    ]
