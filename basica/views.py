
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import *
from .forms import LeadBasicaForms, LeadAvancadaForms
import math
from .bitola import *

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
            lead = LeadBasica.objects.create(nome=nome,desnivel=desnivel, vazao=vazao,potencia=potencia,mchs=mchs,telefone=request.POST['telefone'],concessionaria=request.POST['concessionaria'],email=request.POST['email'],modelo=request.POST['modelo'],)
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

def avancada(request):
    #DATA INPUT FROM USER
    form_avancada = LeadAvancadaForms()
    if request.method == 'POST':
        form_avancada = LeadAvancadaForms(request.POST)
        nome = request.POST['nome']
        desnivel = int(float(request.POST['desnivel']))
        vazao = int(float(request.POST['vazao']))
        dist_hidr = int(float(request.POST['dist_hidr']))
        dist_eletr = int(float(request.POST['dist_eletr']))
        modelo = request.POST['modelo']
        tipo_cabo = request.POST['tipo_cabo']

        #CALCULATIONS
        diametro_econ = 0
        potencia = desnivel*vazao*9.81*0.531
        diametro_econ = 123.7*(((float(vazao)/1000)**3)/(1.2*float(desnivel)))**(1/7)*10
        tubos_comerciais = [75,100,125,150,200,250,300,350,400,450,500,550,600,650,700,750,800]
        tubos_comerciais.sort()
        diametro_comercial = math.ceil(diametro_econ)
        
        for i in tubos_comerciais:
            if diametro_comercial < i:
                diametro_comercial = i
                break
                
        vel_escoamento = (4*float(vazao)/1000)/((math.pi)*((diametro_comercial/1000)**2))
        perda_carga_unit = (vel_escoamento/(0.355*140*(diametro_comercial/1000)**0.63))**(1/0.54)
        perda_carga_tub = perda_carga_unit*dist_hidr
        k = 3.6
        perda_carga_conex_total = k*(vel_escoamento**2)/(2*9.81)
    
        if perda_carga_tub + perda_carga_conex_total <= desnivel:
            perda_carga_total = perda_carga_tub + perda_carga_conex_total
            
        else:
            messages.error(request, 'A perda de carga não pode ser maior do que o desnível do terreno.')
            return redirect('avancada')

        desnivel_real = desnivel - perda_carga_total
        porcentagem_perda = (perda_carga_total / desnivel)
        potencia = vazao*desnivel_real*9.81*0.64
        mchs = potencia/1000

        if potencia%1000 >= 500:
            mchs = math.ceil(mchs)
        else:
            mchs = math.floor(mchs)

        if modelo == 'On Grid':
            tensao = 220.0
        else:
            tensao = 130.0

        if modelo == 'On Grid':
            corrente = potencia/tensao
        else:
            corrente = potencia/tensao/math.sqrt(3)


        if tipo_cabo == 'Alumínio':
            ro = 0.0282
        else:
            ro = 0.0172

        for i in bitola:
            f_pot = 1.0
            perda_porc = 1.0
            r = (ro*dist_eletr)/i
            delta_e = 2*r*corrente*f_pot
            perda_porc = delta_e/tensao

            if perda_porc <= 0.05 and corrente<=bitola[i]:
                bitola_real = i
                pot_util = potencia*(1-perda_porc)
                break 
        
        if form_avancada.is_valid():
            print(form_avancada.errors)
            lead = LeadAvancada.objects.create(
                nome=nome,
                desnivel=desnivel,
                vazao=vazao,
                potencia=potencia,
                mchs=mchs,
                dist_hidr=dist_hidr,
                dist_eletr=dist_eletr,
                modelo=modelo,
                tipo_cabo=tipo_cabo,
                email=request.POST['email'],
                telefone=request.POST['telefone'],
                concessionaria=request.POST['concessionaria'],
                )
            lead.save()

            dados = {
                'form_avancada': form_avancada,
                'diametro_econ':diametro_econ,
                'diametro_comercial':diametro_comercial,
                'vel_escoamento':vel_escoamento,
                'perda_carga_unit':perda_carga_unit,
                'perda_carga_tub':perda_carga_tub,
                'perda_carga_conex_total':perda_carga_conex_total,
                'desnivel_real':desnivel_real,
                'porcentagem_perda':"{0:.0%}".format(porcentagem_perda),
                'pot_util':pot_util,
                'mchs':mchs,
                'bitola_real':bitola_real,         
            }

            return render(request,'avancada_resultado.html', dados)
        else:
            print('Form inválido')
            print (form_avancada.errors)
            dados = {'form_avancada':form_avancada,}
            return render(request, 'avancada_forms.html', dados)
    
    else:
        form_avancada = LeadAvancadaForms()
        dados = {'form_avancada':form_avancada,}
        return render(request,'avancada_forms.html', dados)

def avancada_resultado(request):
    if request.method == 'GET':
        nome = LeadAvancada.objects.latest('id')
        desnivel = LeadAvancada.objects.latest('desnivel')
        vazao = LeadAvancada.objects.latest('vazao')
        mchs = LeadAvancada.objects.latest('mchs')
        potencia = LeadAvancada.objects.latest('potencia')
        concessionaria = LeadAvancada.objects.latest('concessionaria')
        email = LeadAvancada.objects.latest('email')
        modelo = LeadAvancada.objects.latest('modelo')
        data = LeadAvancada.objects.latest('data')

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

