import email
from django import forms
from .validation import *
from .models import LeadBasica
from datetime import datetime

CHOICES = [('on grid', 'On Grid'),('off grid', 'Off Grid')]

class LeadBasicaForms (forms.ModelForm):
    modelo = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    potencia = forms.IntegerField(widget=forms.HiddenInput(), required=False,)
    mchs = forms.IntegerField(widget=forms.HiddenInput(),required=False,)
    class Meta:
        model = LeadBasica
        fields = '__all__'
        labels = {'vazao':'Vazão (L/s)','desnivel':'Desnível (Queda) (m)','cpf_cnpj':'CPF ou CNPJ','concessionaria':'Concessionária','email':'E-mail'}

    def clean(self):
        nome = self.cleaned_data.get('nome')
        desnivel = self.cleaned_data.get('desnivel')
        vazao = self.cleaned_data.get('vazao')
        telefone = self.cleaned_data.get('telefone')
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        concessionaria = self.cleaned_data.get('concessionaria')
        email = self.cleaned_data.get('email')
        lista_de_erros = {}
        campo_tem_algum_numero(nome, 'nome', lista_de_erros)
        campo_tem_algum_numero(nome, 'concessionaria', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data
