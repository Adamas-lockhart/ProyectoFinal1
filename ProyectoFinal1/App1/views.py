from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from App1.models import Usuarios, Avatar #mod
from App1.forms import formSetUsuario, UserEditForm, ChangePasswordForm, AvatarForm #mod
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#abajo, tratar de ver como importarlo
from App1.templates.App1 import *

# Create your views here.

@login_required
def inicio(request):
    avatar = getavatar(request)
    return render(request, "App1/inicio.html", {"avatar": avatar})

def Usuario(request):
    Usuario = Usuario.objects.all()
    return render(request, "App1/Usuarios.html",{"Usuarios": Usuario})

@login_required
def setUsuarios(request):
    Usuario = Usuario.objects.all()
    if request.method == 'POST':
        Usuario = Usuario(nombre=request.POST["nombre"],apellido=request.POST["apellido"], email=request.POST["email"])
        Usuario.save()  
        miFormulario = formSetUsuario()  
        return render(request, "App1/setUsuarios.html", {"miFormulario":miFormulario, "Usuarios":Usuario})
    else:
        miFormulario = formSetUsuario()
    return render(request, "App1/setUsuarios.html", {"miFormulario":miFormulario, "Usuarios":Usuario})

def getUsuarios(request):
    return render(request, "App1/getUsuarios.html")

def buscarUsuarios(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        Usuario = Usuario.objects.filter(nombre = nombre)
        return render(request, "App1/getUsuarios.html", {"Usuarios":Usuarios, "key": "value"})
    else:
        respuesta = "No se enviaron datos"
    
    return HttpResponse(respuesta)

def eliminarUsuarios(request, nombre_Usuarios):
    Usuario = Usuario.objects.get(nombre= nombre_Usuarios)
    Usuario.delete()
    miFormulario = setUsuarios()
    Usuario = Usuario.objects.all()
    return render(request, "App1/setUsuarios.html", {"miFormulario":miFormulario, "Usuarios":Usuario})

def editarUsuarios(request, nombre_Usuarios):
    Usuario = Usuario.objects.get(nombre= nombre_Usuarios)
    if request.method == 'POST':
        miFormulario = setUsuarios(request.POST)
        if miFormulario.is_valid:
            print(miFormulario)
            data = miFormulario.cleaned_data

            Usuario.nombre = data['nombre']
            Usuario.apellido = data['apellido']
            Usuario.email = data['email']
            Usuario.save()
            miFormulario = formSetUsuario()
            Usuario = Usuario.objects.all()
            return render(request, "App1/setUsuarios.html", {"miFormulario":miFormulario, "Usuarios":Usuario})
    else:
        miFormulario = formSetUsuario(initial={'nombre': Usuario.nombre, 'apellido': Usuario.apellido, 'email': Usuario.email})
    return render(request, "App1/editarUsuarios.html", {"miFormulario":miFormulario})

def loginWeb(request):
    if request.method == "POST":
        user = authenticate(username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect("../inicio")
        else:
            return render(request, 'App1/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'App1/login.html')

def registro(request):
    if request.method == "POST":
        userCreate = UserCreationForm(request.POST)
        if userCreate is not None:
            userCreate.save()
            return render(request, 'App1/login.html')
    else:
        return render(request, 'App1/registro.html')
        #return render(request, 'ProyectoFinal1/App1/templates/App1/registro.html')
        #return render(request, 'App1/registro.html')

@login_required  
def perfilview(request):
    return render(request, 'App1/Perfil/Perfil.html')

@login_required  
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'App1/Perfil/Perfil.html')
    else:
        form = UserEditForm(initial= {'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name })
        return render(request, 'App1/Perfil/editarPerfil.html', {"form": form})

@login_required
def changePassword(request):
    usuario = request.user    
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            if request.POST['new_password1'] == request.POST['new_password2']:
                user = form.save()
                update_session_auth_hash(request, user)
            return HttpResponse("Las constraseñas no coinciden")
        return render(request, "App1/inicio.html")
    else:
        form = ChangePasswordForm(user = usuario)
        return render(request, 'App1/Perfil/changePassword.html', {"form": form})

def editAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None           
            return render(request, "App1/inicio.html", {'avatar': avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, "App1/Perfil/avatar.html", {'form': form})

def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        avatar = None
    return avatar