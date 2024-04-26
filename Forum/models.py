from django.db import models

# Create your models here.
class Cadastro_usuario(models.Model):
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Feminino'), ('N', 'Não Informar')], null=True)
    data_nascimento = models.DateTimeField(null=True, blank=True)
    email = models.EmailField (unique=True)
    senha = models.CharField(max_length=256)
    tipo_usuario = models.CharField(max_length=1, choices=[('C', 'Comum'), ('A', 'Administrador')], default='C')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_alteracao = models.DateTimeField(auto_now=True)
    

class Topico(models.Model): 
    assunto = models.CharField(max_length=200)
    autor = models.ForeignKey(Cadastro_usuario, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50)
    data_postagem = models.DateTimeField(auto_now_add=True)
    #imagem
    mensagens = models.CharField(max_length=2000)
    status_post = models.CharField(max_length=1, choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A')

class Comentario(models.Model):
    topico = models.ForeignKey(Topico, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(Cadastro_usuario, on_delete=models.CASCADE)
    conteudo = models.CharField(max_length=2000)
    data_comentario = models.DateTimeField(auto_now_add=True)
    status_comentario = models.CharField(max_length=1, choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A')
