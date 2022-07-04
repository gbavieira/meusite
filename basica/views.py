
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import LeadBasicaForms
import math

def calculadora(request):
    return render(request,'calculadora.html')

def basica (request):
    form = LeadBasicaForms()
    if request.method == 'POST':
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

        lead = LeadBasica.objects.create(nome=nome,desnivel=desnivel, vazao=vazao,potencia=potencia,mchs=mchs,telefone=request.POST['telefone'],cpf_cnpj=request.POST['cpf_cnpj'],concessionaria=request.POST['concessionaria'],email=request.POST['email'],modelo=request.POST['modelo'],data=request.POST['data'],)
        lead.save()

        dados = {'form':form,'potencia':potencia,'mchs':mchs,}
        return redirect('basica/resultado', dados)

    else:
        form = LeadBasicaForms()
        dados = {'form':form,}
        return render(request,'basica_forms.html', dados)
    
def basica_resultado (request):
    if request.method == 'GET':
        nome = LeadBasica.objects.latest('id')
        desnivel = LeadBasica.objects.latest('desnivel')
        vazao = LeadBasica.objects.latest('vazao')
        mchs = LeadBasica.objects.latest('mchs')
        potencia = LeadBasica.objects.latest('potencia')
        concessionaria = LeadBasica.objects.latest('concessionaria')
        email = LeadBasica.objects.latest('email')
        modelo = LeadBasica.objects.latest('modelo')
        data = LeadBasica.objects.latest('data')

        dados = {
            'nome':nome,
            'desnivel':desnivel,
            'vazao':vazao,
            'mchs':mchs,
            'potencia':potencia,
            'concessionaria':concessionaria,
            'email':email,
            'modelo':modelo,
            'data':data,
        }

        return render(request,'basica_resultado.html', dados)
