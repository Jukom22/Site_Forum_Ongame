from django import forms
from .models import Cadastro_usuario, Topico, Comentario
import hashlib

class Formulario_cadastro_usuario(forms.ModelForm):
    class Meta:
        model = Cadastro_usuario
        fields = ['nome', 'sobrenome', 'sexo', 'data_nascimento', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

    # def save(self, commit=True):
    #     usuario = super().save(commit=False)
    #     # Hash SHA-256 da senha
    #     hashed_password = hashlib.sha256(self.cleaned_data['senha'].encode('utf-8')).hexdigest()
    #     usuario.senha = hashed_password
    #     if commit:
    #         usuario.save()
    #     return usuario


class Formulario_para_login(forms.ModelForm):
    class Meta:
        model = Cadastro_usuario
        fields = ['email', 'senha']
        widgets = {'senha': forms.PasswordInput(),}


class Novo_topico(forms.ModelForm):
    CATEGORIAS = [
        ('Tutorial', 'Tutorial'),
        ('Dúvidas', 'Dúvidas'),
        ('Problema/Reclamação', 'Problema/Reclamação'),
    ]
    categoria = forms.ChoiceField(choices=CATEGORIAS)
    class Meta:
        model = Topico
        fields = ['assunto', 'categoria', 'mensagens']
        widgets = {
            'mensagens': forms.Textarea(attrs={'cols': 60, 'rows': 5}),
        }


class Novo_comentario(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'cols': 60, 'rows': 5}),
        }        


