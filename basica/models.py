from django.db import models
from datetime import datetime

USE_TZ =False

class LeadBasica(models.Model):
    nome = models.CharField(max_length = 50)
    telefone = models.CharField(max_length = 20,)
    concessionaria = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    desnivel = models.IntegerField()
    vazao = models.IntegerField()
    modelo = models.CharField(max_length = 20)
    potencia = models.IntegerField()
    mchs = models.IntegerField()
    data = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.nome

class LeadAvancada(models.Model):
    nome = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 50)
    telefone = models.CharField(max_length = 20,blank=True)
    concessionaria = models.CharField(max_length = 50,blank=True)
    desnivel = models.IntegerField()
    vazao = models.IntegerField()
    potencia = models.IntegerField()
    mchs = models.IntegerField()
    dist_hidr = models.IntegerField()
    dist_eletr = models.IntegerField()
    modelo = models.CharField(max_length = 50)
    tipo_cabo = models.CharField(max_length =50)
    data = models.DateTimeField(default=datetime.now, blank=True,)
    def __str__(self):
        return self.nome

class Conexoe(models.Model):
    nome_conex = models.CharField(max_length = 50)
    k = models.CharField(max_length = 50)
    def __str__(self):
        return self.nome_conex

