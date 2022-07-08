
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import LeadBasicaForms
import math

def calculadora(request):
    return render(request,'calculadora.html')


def basica(request):
    if request.method == 'POST':
        print('2')
        form = LeadBasicaForms(request.POST)
        nome = request.POST['nome']
        desnivel = math.floor(int(float(request.POST['desnivel'])))
        vazao = math.floor(int(float(request.POST['vazao'])))
        potencia = math.ceil(desnivel*vazao*9.81*0.531)
        if potencia <= 75000:
            mchs = potencia/1000
            if potencia%1000 >= 500:
                mchs = math.ceil(mchs)
            else:
                mchs = math.floor(mchs)
        else:
            messages.error(request, 'Todos os campos são obrigatórios e não podem ficar em branco!')
            return redirect('basica_forms')

        if form.is_valid():
            lead = LeadBasica.objects.create(nome=nome,desnivel=desnivel, vazao=vazao,potencia=potencia,mchs=mchs,telefone=request.POST['telefone'],cpf_cnpj=request.POST['cpf_cnpj'],concessionaria=request.POST['concessionaria'],email=request.POST['email'],modelo=request.POST['modelo'],)
            lead.save()
            print('3')
            dados = {
                'form':form,
                'potencia':potencia,
                'mchs':mchs,
            }
            return render(request,'basica_resultado.html', dados)
        else:
            print('Form inválido')
            print (form.errors)
            dados = {'form':form,}
            return render(request, 'basica_forms.html', dados)
    else:
        form = LeadBasicaForms()
        dados = {'form':form, }
        return render(request,'basica_forms.html', dados)


    
def basica_resultado (request):
    if request.method == 'POST':
        print('4')
        nome = LeadBasica.objects.latest('id')
        desnivel = LeadBasica.objects.latest('desnivel')
        vazao = LeadBasica.objects.latest('vazao')
        mchs = LeadBasica.objects.latest('mchs')
        potencia = LeadBasica.objects.latest('potencia')
        concessionaria = LeadBasica.objects.latest('concessionaria')
        email = LeadBasica.objects.latest('email')
        modelo = LeadBasica.objects.latest('modelo')

        dados = {
            'nome':nome,
            'desnivel':desnivel,
            'vazao':vazao,
            'mchs':mchs,
            'potencia':potencia,
            'concessionaria':concessionaria,
            'email':email,
            'modelo':modelo,
        }

        return render(request,'basica_resultado.html', dados)

