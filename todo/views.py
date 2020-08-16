from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'todo/home.html')

#User related functions
def USER_SignUp(request):
    if request.method == "GET":
        return render(request,'todo/USER_SignUp.html',{'form':UserCreationForm()})
    else:
        #create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodolist')
            except IntegrityError:
                return render(request,'todo/USER_SignUp.html',{'form':UserCreationForm(),'error':"Username already been taken. Please choose a different username."})
        else:
            return render(request,'todo/USER_SignUp.html',{'form':UserCreationForm(),'error':"Passwords do not match."})

@login_required
def USER_Logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def USER_Login(request):
    if request.method == "GET":
        return render(request,'todo/USER_Login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/USER_Login.html',{'form':AuthenticationForm(),'error':"Username and Password authentication failed"})
        else:
            login(request,user)
            return redirect('currenttodolist')

# Todo related functions

@login_required
def currenttodolist(request):
    todos = Todo.objects.filter(user = request.user, dateCompleted__isnull = True)
    return render(request,'todo/currenttodolist.html',{'todos': todos})

@login_required
def completedtodolist(request):
    todos = Todo.objects.filter(user = request.user, dateCompleted__isnull = False).order_by('-dateCompleted')
    return render(request,'todo/completedtodolist.html',{'todos': todos})

@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request,'todo/createtodo.html',{'form':TodoForm()})
    else :
        try:
            form            = TodoForm(request.POST)
            newtodo         = form.save(commit=False)
            newtodo.user    = request.user
            newtodo.save()
            return redirect('currenttodolist')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':"Bad Data Entered"})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk,  user = request.user)
    if request.method == "GET":
        form = TodoForm(instance = todo)
        return render(request,'todo/viewtodo.html',{'todo': todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance = todo)
            form.save()
            return redirect('currenttodolist')
        except ValueError:
            return render(request,'todo/viewtodo.html',{'todo': todo, 'form':form,'error':"Bad Data Entered"})

@login_required
def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk,  user = request.user)
    if request.method == "POST":
        todo.dateCompleted  = timezone.now()
        todo.save()
        return redirect('currenttodolist')

@login_required
def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo,pk = todo_pk,  user = request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodolist')
