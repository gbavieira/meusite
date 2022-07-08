from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from alurareceita.models import Receita
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']

        if campo_vazio(nome):
            messages.error(request, 'O campo nome não pode ficar em branco')
            return redirect('cadastro')

        if campo_vazio(email):
            messages.error(request, 'O campo email não pode ficar em branco')
            return redirect('cadastro')

        if senhas_nao_sao_iguais(senha, senha2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário com e-mail já cadastrado')
            return redirect('cadastro')

        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('cadastro')

        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso')

        return redirect('login')
    else:
        return render(request,'usuarios/cadastro.html')

def login(request):
    """Realiza o login de uma pessoa no sistema"""
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Os campos email e senha não podem ficar em branco')
            return redirect('login')

        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                auth.login(request,user)
                return redirect ('dashboard')

        else:
            messages.error(request, 'Usuário não cadastrado')
            return redirect('login')

    return render(request,'usuarios/login.html')

def dashboard(request):
    """Página de dashboard(inicial) de cada usuário"""
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)
        dados = {
            'receitas': receitas
        }
        return render(request,'usuarios/dashboard.html', dados)
    else:
        return redirect('index_receita')

def logout(request):
    """Realiza o logout do usuário"""
    auth.logout(request)
    return redirect('index_receita')

def campo_vazio(campo):
    """função para verificação de campos vazios no site"""
    return not campo.strip()

def senhas_nao_sao_iguais(senha,senha2):
    """comparação entre as senhas para verificação de cadastro"""
    return senha != senha2

def busca(request):

    lista_receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        lista_receitas = lista_receitas.filter(nome_receita__icontains=nome_a_buscar)

    dados = {
        'receitas': lista_receitas
    }

    return render(request, 'receitas/buscar.html', dados)

def index_receita(request):

    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    paginator = Paginator(receitas, 9)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page)

    dados = {
        'receitas':receitas_por_pagina
    }

    return render(request,'receitas/index_receita.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    receita_a_exibir = {
        'receita':receita
    }

    return render(request,'receitas/receita.html', receita_a_exibir)

def cria_receita(request):

    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']

        if campo_vazio(nome_receita) or campo_vazio(ingredientes) or campo_vazio(modo_preparo) or campo_vazio(tempo_preparo) or campo_vazio(rendimento) or campo_vazio(categoria):
            messages.error(request, 'Todos os campos são obrigatórios e não podem ficar em branco!')
            return redirect('cria_receita')

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user, nome_receita=nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo, tempo_preparo=tempo_preparo, rendimento=rendimento, categoria=categoria,foto_receita=foto_receita)
        receita.save()
        return redirect ('dashboard')
    else:
        return render(request,'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def edita_receita(request,receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = { 'receita':receita}
    return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')

def campo_vazio(campo):
    return not campo.strip()

def publicar(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    if receita.publicada == False:
        receita.publicada = True
        receita.save()
        print (receita.publicada)
        return redirect('index_receita')
    else:
        receita.publicada = False
        receita.save()
        print (receita.publicada)
        return redirect('index_receita')