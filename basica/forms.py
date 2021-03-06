import email
from django import forms
from .validation import *
from .models import *
from datetime import datetime

CHOICES = [('on grid', 'On Grid'),('off grid', 'Off Grid')]

class LeadBasicaForms (forms.ModelForm):
    modelo = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    potencia = forms.IntegerField(widget=forms.HiddenInput(), required=False,)
    mchs = forms.IntegerField(widget=forms.HiddenInput(),required=False,)
    class Meta:
        model = LeadBasica
        fields = '__all__'
        labels = {'vazao':'Vazão (L/s)','desnivel':'Desnível (Queda) (m)','concessionaria':'Concessionária','email':'E-mail'}

    def clean(self):
        nome = self.cleaned_data.get('nome')
        desnivel = self.cleaned_data.get('desnivel')
        vazao = self.cleaned_data.get('vazao')
        telefone = self.cleaned_data.get('telefone')
        concessionaria = self.cleaned_data.get('concessionaria')
        email = self.cleaned_data.get('email')
        lista_de_erros = {}
        campo_tem_algum_numero(nome, 'nome', lista_de_erros)
        campo_tem_algum_numero(nome, 'concessionaria', lista_de_erros)
        campo_tem_alguma_letra(telefone,'telefone',lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data


class LeadAvancadaForms (forms.ModelForm):
    choices_cabo = [('Alumínio', 'Alumínio'),('Cobre', 'Cobre'),]
    modelo = forms.ChoiceField(choices=CHOICES, widget = forms.RadioSelect)
    tipo_cabo = forms.ChoiceField(choices=choices_cabo, widget = forms.RadioSelect)
    potencia = forms.IntegerField(widget=forms.HiddenInput(), required=False,)
    mchs = forms.IntegerField(widget=forms.HiddenInput(),required=False,)

    class Meta:
        model = LeadAvancada
        fields = '__all__'
        labels = {'desnivel':'Desnível (Queda) (m)','vazao':'Vazão (L/s)','dist_hidr':'Distância Hidráulica (Tubulação) (m)','dist_eletr':'Distância Elétrica (m)','concessionaria':'Concessionária','email':'E-mail','telefone':'Telefone com DDD'}
        widget = {
            'telefone': forms.CharField(required=False,max_length = 20),
            'concessionaria': forms.CharField(max_length = 50,required=False,)
        }

    def clean(self):
        nome = self.cleaned_data.get('nome')
        desnivel = self.cleaned_data.get('desnivel')
        vazao = self.cleaned_data.get('vazao')
        telefone = self.cleaned_data.get('telefone')
        concessionaria = self.cleaned_data.get('concessionaria')
        email = self.cleaned_data.get('email')
        dist_hidr = self.cleaned_data.get('dist_hidr')
        dist_eletr = self.cleaned_data.get('dist_eletr')
        modelo = self.cleaned_data.get('modelo')
        tipo_cabo = self.cleaned_data.get('tipo_cabo')
        lista_de_erros = {}
        campo_tem_algum_numero(nome, 'nome', lista_de_erros)
        campo_tem_algum_numero(concessionaria, 'concessionaria', lista_de_erros)
        campo_tem_alguma_letra(telefone,'telefone',lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data