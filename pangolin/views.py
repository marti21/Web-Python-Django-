from email import message
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from .models import Comentario, Post, UserPangolin, FriendRequest, LoggedUser
from .forms import PostForm, SignUpForm, UserChangeForm2
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse

def first(request):
    return render(request, 'first.html')

def user_Registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/login')

    else:
        form = SignUpForm(request.POST, request.FILES)

    return render(request, 'registration.html',{'form':form})

def login_user(request):
    form = AuthenticationForm(data=request.POST)
    
    if form.is_valid():
        user = form.get_user()

        login(request, user)
        return redirect('home')

    return render(request, 'login.html', {'form':form})

def login_out_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def home(request):
    post_objs = Post.objects.all().order_by('-created_at')
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    listaDeAmigos = userLogged.friends.all()
    logged_users=[user.user for user in LoggedUser.objects.all()]

    listaDePosts = []
    for post in post_objs:
        x = get_object_or_404(UserPangolin, username=post.author.username)
        if x in listaDeAmigos or x == userLogged:
            listaDePosts.append(post)
    
    listaDeAmigosConectados = []
    for user in logged_users:
        userPan = get_object_or_404(UserPangolin, username=user.username)
        if userPan in listaDeAmigos and user != userLogged:
            listaDeAmigosConectados.append(userPan)
    
    print("LISTA DE AMIGOS CONECTADOS", listaDeAmigosConectados)

    context = {
        'posts' : listaDePosts,
        'user' : userLogged,
        'friends_conected':listaDeAmigosConectados,
    }
    return render(request, 'home.html', context)

@login_required(login_url='/login')
def add_friends(request):
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    users_objs = UserPangolin.objects.all()
    listaDeAmigos = userLogged.friends.all()

    listaDeNoAmigos = []
    for user in users_objs:
        if user not in listaDeAmigos and user != userLogged:
            listaDeNoAmigos.append(user)

    context = {
        'user2' : userLogged,
        'allusers': listaDeNoAmigos,
    }
    return render(request, 'AddFriends.html', context)

@login_required(login_url='/login')
def see_friends(request):
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    users_objs = UserPangolin.objects.all()

    context = {
        'user2' : userLogged,
        'allusers': users_objs,
    }
    return render(request, 'friends.html', context)

@login_required(login_url='/login')
def user_profile(request, username):
    obj = get_object_or_404(UserPangolin, username=username)

    if username == request.user.username:
        post_objs = Post.objects.filter(author=request.user).order_by('-created_at')
        requestFriends = FriendRequest.objects.filter(to_user = obj)

        print(requestFriends)

        listaDeAmigos = []
        listaDeAmigos = obj.friends.all()

        print(listaDeAmigos)

        context = {
        'userLogged' : obj,
        'posts' : post_objs,
        'listRequestFriends' : requestFriends,
        'listaDeAmigos': listaDeAmigos,
        }
        return render(request, 'own_profile.html', context)
    
    else:
        userLogged = get_object_or_404(UserPangolin, username=request.user.username)
        post_objs = Post.objects.filter(author=obj.id).order_by('-created_at')
       
        context = {
        'userSign' : userLogged,
        'posts' : post_objs,
        'pubUser' : obj,
        }
        
        return render(request, 'profile.html', context)
  
@login_required(login_url='/login')
def add_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    if form.is_valid():
        

        post = form.save(commit=False)
        post.author = request.user

        form.save()
        return redirect('home')

    context = {
        'form' : form,
        'user':userLogged,
    }
    return render(request, 'add_post.html', context)

    
@login_required(login_url='/login')
def get_post(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    postAuthor = get_object_or_404(UserPangolin, username=obj.author.username)
    comentarios = Comentario.objects.filter(post=obj)
    listaAmigos = postAuthor.friends.all()

    print(listaAmigos)

    context = {
        'post' : obj,
        'comments': comentarios,
        'listFriends': listaAmigos,
        'userLogged': userLogged,
        'postAuthor': postAuthor,
    }
    return render(request, 'post.html', context)


@login_required(login_url='/login')
def edit_post(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=obj)

    context = {
        'form' : form,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('post_details',kwargs={'post_id':obj.id}))
            
    else:
        form = PostForm(request.POST or None, request.FILES or None, instance=obj)

    return render(request, 'edit_post.html', context)



@login_required(login_url='/login')
def change_password(request):
    form = PasswordChangeForm(data = request.POST, user=request.user)

    if form.is_valid():
        form.save()
        return redirect('/')

    context = {
        'form' : form,
    }
    return render(request, 'change_password.html', context)


@login_required(login_url='/login')
def change_user_profile(request):
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    form = UserChangeForm2(request.POST or None, request.FILES or None, instance=userLogged)

    context = {
        'form' : form,
        'user' : userLogged,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect(reverse('profile_user', kwargs={'username':userLogged.username}))
            
    else:
        form = UserChangeForm2(request.POST or None, request.FILES or None, instance=userLogged)

       
    return render(request, 'change_profile.html', context)


@login_required(login_url='/login')
def send_friend_request(request, username):
    delUsuario = get_object_or_404(UserPangolin, username=request.user.username)
    paraUsuario = get_object_or_404(UserPangolin, username=username)
    friend_request, created = FriendRequest.objects.get_or_create(from_user=delUsuario, to_user=paraUsuario)

    if created:
        return HttpResponse('Friend request Sent')
    else:
        return HttpResponse('Friend request was already Sent')


@login_required(login_url='/login')
def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    userLogeado = get_object_or_404(UserPangolin, username=request.user.username)
    
    if friend_request.to_user == userLogeado:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
    
        return HttpResponse('Friend request accepted')


@login_required(login_url='/login')
def reject_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    
    if friend_request.to_user == userLogged:
        friend_request.delete()
    
        return HttpResponse('Friend request rejected')


@login_required(login_url='/login')
def delete_friend(request, username):
    friend = get_object_or_404(UserPangolin, username=username)
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
  
    userLogged.friends.remove(friend)
    friend.friends.remove(userLogged)
      
    return HttpResponse('Deleted Friend')


@login_required(login_url='/login')
def add_friends_search(request):
    userLogged = get_object_or_404(UserPangolin, username=request.user.username)

    buscadorUsuario = request.GET["buscarUsuario"]

    users_objs = UserPangolin.objects.filter(username__icontains=buscadorUsuario)
    users_objs2 = UserPangolin.objects.filter(first_name__icontains=buscadorUsuario)
    listaDeAmigos = userLogged.friends.all()

    listaUsuarios = []

    for user in users_objs:
        listaUsuarios.append(user)

    for user in users_objs2:
        if user not in listaUsuarios:
            listaUsuarios.append(user)

    print(listaUsuarios)

    listaDeNoAmigosFiltrados = []
    for user in listaUsuarios:
        if user not in listaDeAmigos and user != userLogged:
            listaDeNoAmigosFiltrados.append(user)
        
    print(listaDeNoAmigosFiltrados)

    context = {
        'user2' : userLogged,
        'allusers': listaDeNoAmigosFiltrados,
    }
    return render(request, 'AddFriends.html', context)


@login_required(login_url='/login')
def comment(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    comentarios = Comentario.objects.filter(post=obj)

    userLogged = get_object_or_404(UserPangolin, username=request.user.username)
    postAuthor = get_object_or_404(UserPangolin, username=obj.author.username)
    listaAmigos = postAuthor.friends.all()

    text2 = request.GET["comentario"]

    if text2:
        Comentario.objects.get_or_create(author = request.user,post = obj, text = text2)
    
    context = {
        'post' : obj,
        'comments': comentarios,
        'listFriends': listaAmigos,
        'userLogged': userLogged,
        'postAuthor': postAuthor,
    }
    return render(request, 'post.html', context)


@login_required(login_url='/login')
def delete_post(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    
    obj.delete()

    return redirect('home')
    