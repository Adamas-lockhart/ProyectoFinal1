from django.urls import path
from django.contrib.auth.views import LogoutView
from App1.views import *

#modificar abajo 

urlpatterns = [
    path('', loginWeb),
    path('inicio/', inicio),
    path('usuarios/', Usuarios, name="Usuarios"),
    path('setUsuarios/', setUsuarios, name="setUsuarios"),
    path('getUsuarios/', getUsuarios, name="getUsuarios"),
    path('buscarUsuarios/', buscarUsuarios, name="buscarUsuarios"),
    path('eliminarUsuarios/<nombre_Usuarios>', eliminarUsuarios, name="eliminarUsuarios"),
    path('editarUsuarios/<nombre_Usuarios>', editarUsuarios, name="editarUsuarios"),
    path('login/', loginWeb, name="login"),
    path('registro/', registro, name="registro"),
    path('Logout/',LogoutView.as_view(template_name = 'App1/login.html'), name="Logout"),
    path('perfil/', perfilview, name="perfil"),
    path('Perfil/editarPerfil/', editarPerfil, name="editarPerfil"),
    path('Perfil/changePassword/', changePassword, name="changePassword"),
    path('Perfil/changeAvatar/', editAvatar, name="editAvatar"),
]