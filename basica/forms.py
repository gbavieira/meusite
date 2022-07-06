from django import forms
from .validation import *
from .models import LeadBasica
from datetime import datetime

CHOICES = [('on grid', 'On Grid'),('off grid', 'Off Grid')]

class LeadBasicaForms (forms.ModelForm):
    modelo = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    data = forms.DateField(label='Data da Pesquisa', disabled=True, initial=datetime.today)
    class Meta:
        model = LeadBasica
        fields = '__all__'
        labels = {'vazao':'Vazão','desnivel':'Desnível','cpf_cnpj':'CPF ou CNPJ','concessionaria':'Concessionária','email':'E-mail'}
        widgets = {
            'potencia': forms.HiddenInput(),
            'mchs': forms.HiddenInput(),
            'data':forms.HiddenInput(),
        }

    def clean(self):
        nome = self.cleaned_data.get('nome')
        lista_de_erros = {}
        campo_tem_algum_numero(nome, 'nome', lista_de_erros)
        if lista_de_erros is not None:
            for erro in lista_de_erros:
                mensagem_erro = lista_de_erros[erro]
                self.add_error(erro, mensagem_erro)
        return self.cleaned_data
