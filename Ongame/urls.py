"""
URL configuration for Ongame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Forum import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adm_manual/', views.adm_manual_view, name='adm_manual'),
    path('cadastrar_usuario/', views.cadastrar_usuario_view, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro_topico/', views.cadastro_topico_view, name='cadastro_topico'),
    path('editar_usuario/', views.editar_usuario_view, name='editar_usuario'),
    path('lista_topico/', views.lista_topico_view, name='lista_topico'),
    path('topico_detalhado/<int:id_topico>/', views.topico_detalhado_view, name='topico_detalhado'),
    path('', views.lista_topico_view, name='home'),
    path('atualizar_tipo_usuario_adm/<int:id_usuario>/', views.atualizar_tipo_usuario_adm_view, name='atualizar_tipo_usuario'),
    path('adm_topico/<int:id_topico>/<str:status_post>/', views.adm_topico_view, name='adm_topico'),
    path('adm_comentario/<int:id_comentario>/<str:status_comentario>/', views.adm_comentario_view, name='adm_comentario'),
]
