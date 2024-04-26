from django.shortcuts import render, redirect, get_object_or_404
from .forms import Formulario_cadastro_usuario, Formulario_para_login, Novo_topico, Novo_comentario
from .models import Cadastro_usuario, Topico, Comentario
import hashlib
from django.db import IntegrityError

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout

# Create your views here.

def adm_manual_view(request):
    tipo_usuario = request.session.get('tipo_usuario', 'C')
    if tipo_usuario == 'A':
        pass
        # # Update por seleção em Model
        # topicos_a_atualizar = Topico.objects.filter(id=4)
        # topicos_a_atualizar.update(assunto='novo_assuntoo')
        # # Delete por seleção em Model
        # usuarios_a_deletar = Cadastro_usuario.objects.filter(id__gte=9) #Maior ou igual que
        # usuarios_a_deletar.delete()
    return render(request, 'confirma_operacao.html', {'mensagem':'Operação no banco de dados efetuada'})

def cadastrar_usuario_view(request):
    if request.method == 'POST':
        form = Formulario_cadastro_usuario(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.nome = form.cleaned_data['nome']
            usuario.sobrenome = form.cleaned_data['sobrenome']
            usuario.sexo = form.cleaned_data['sexo']
            usuario.data_nascimento = form.cleaned_data['data_nascimento']
            usuario.email = form.cleaned_data['email']
            usuario.senha = form.cleaned_data['senha']
            usuario.save()
            return redirect('login')
        return render(request, 'cadastro_usuario.html', {'form':form})
    else:
        formulario_cadastro_usuario = Formulario_cadastro_usuario()
        return render(request, 'cadastro_usuario.html', {'form': formulario_cadastro_usuario})


def editar_usuario_view(request):
    if request.method == 'POST':
        form = Formulario_cadastro_usuario(request.POST, instance=buscar_usuario(request.session.get('id_usuario', 0)))
        if form.is_valid():
            form.save()
            return redirect('lista_topico')
    else:
        form = Formulario_cadastro_usuario(instance=buscar_usuario(request.session.get('id_usuario', 0)))
    return render(request, 'editar_usuario.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
       form = Formulario_para_login(request.POST)
       email_digitado = request.POST['email']
       senha_digitada = request.POST['senha']
       if validar_login(email_digitado, senha_digitada):
            usuario = Cadastro_usuario.objects.get(email=email_digitado)
            request.session['id_usuario'] = usuario.id
            request.session['nome_usuario'] = usuario.nome
            request.session['tipo_usuario'] = usuario.tipo_usuario
            return redirect('lista_topico')
       else:
            formulario_para_login = Formulario_para_login()
            erro = "Login/Senha Invalido"
            return render(request, 'login.html', {'form': formulario_para_login, 'mensagem': erro})
    else:
        formulario_para_login = Formulario_para_login()
        return render(request, 'login.html', {'form': formulario_para_login})


def logout_view(request):
    request.session['id_usuario'] = 0
    request.session['nome_usuario'] = ''
    request.session['tipo_usuario'] = ''
    return redirect('lista_topico')


def lista_topico_view(request):
    tipo_usuario = request.session.get('tipo_usuario', 'C')
    if tipo_usuario == 'A':
        topicos = Topico.objects.all()
    else:
        topicos = Topico.objects.filter(status_post='A')
    return render(request, 'lista_topico.html', {'topicos': topicos})


def validar_login(email, senha):
    return Cadastro_usuario.objects.filter(email=email, senha=senha).exists()


# def validar_login(email, senha):
#     return Cadastro_usuario.objects.filter(email=email, senha=criptografar_senha).exists()


# def criptografar_senha(senha_pura):
#     return hashlib.sha256(senha_pura.encode('utf-8')).hexdigest()


def cadastro_topico_view(request):
    if request.method == 'POST':
        form = Novo_topico(request.POST)
        if form.is_valid():
                topico = form.save(commit=False)
                topico.autor = buscar_usuario(request.session.get('id_usuario', 0)) 
                topico.assunto = form.cleaned_data['assunto']
                topico.categoria = form.cleaned_data['categoria']
                topico.mensagens = form.cleaned_data['mensagens']
                topico.save()
        return redirect('topico_detalhado', id_topico=topico.id)
    else:
        formulario_novo_topico = Novo_topico()
        return render(request, 'cadastro_topico.html', {'form': Novo_topico})


def topico_detalhado_view(request, id_topico):
    tipo_usuario = request.session.get('tipo_usuario', 'C')
    if tipo_usuario == 'A':
        topico = get_object_or_404(Topico, id=id_topico)
        comentarios = topico.comentarios.all()
    else:
        topico = get_object_or_404(Topico, id=id_topico, status_post='A')
        comentarios = topico.comentarios.filter(status_comentario='A')
    if request.method == 'POST':
        form = Novo_comentario(request.POST)
        if form.is_valid():
            novo_comentario = form.save(commit=False)
            novo_comentario.topico = topico
            novo_comentario.autor = buscar_usuario(request.session.get('id_usuario', 0))
            novo_comentario.save()
            return redirect('topico_detalhado', id_topico = id_topico)
    else:
        form = Novo_comentario()
    return render(request, 'topico_detalhado.html', {'topico': topico, 'comentarios': comentarios, 'form':form, 'tipo_usuario': tipo_usuario})


def buscar_usuario(id_usuario):
    objeto_usuario = Cadastro_usuario.objects.get(id = id_usuario)
    return objeto_usuario


def atualizar_tipo_usuario_adm_view(request, id_usuario):
    #Logado com usuário ADM, acessar http://localhost:8000/atualizar_tipo_usuario_adm/ID_USUARIO_QUE_VAI_VIRAR_ADM
    tipo_usuario_logado = request.session.get('tipo_usuario', 'C')
    if tipo_usuario_logado == 'A':
        usuario = get_object_or_404(Cadastro_usuario, id = id_usuario)
        usuario.tipo_usuario = 'A'
        usuario.save()
        return render(request, 'confirma_operacao.html', {'mensagem':'Usuário ' + usuario.nome + ' atualizado para Administrador'})
    else:
        return redirect('lista_topico')

def adm_topico_view(request, id_topico, status_post):
    tipo_usuario_logado = request.session.get('tipo_usuario', 'C')
    if tipo_usuario_logado == 'A':
        topico = get_object_or_404(Topico, id = id_topico)
        topico.status_post = status_post
        topico.save()
        return redirect('topico_detalhado', id_topico=id_topico)
    else:
        return redirect('lista_topico')


def adm_comentario_view(request, id_comentario, status_comentario):
    tipo_usuario_logado = request.session.get('tipo_usuario', 'C')
    if tipo_usuario_logado == 'A':
        comentario = get_object_or_404(Comentario, id = id_comentario)
        comentario.status_comentario = status_comentario
        comentario.save()
        id_topico = comentario.topico.id
        return redirect('topico_detalhado', id_topico=id_topico)
    else:
        return redirect('lista_topico')

