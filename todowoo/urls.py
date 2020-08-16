"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
#AUTH
    path('USER_SignUp/', views.USER_SignUp, name ="USER_SignUp"),
    path('USER_Logout/', views.USER_Logout, name ="USER_Logout"),
    path('USER_Login/', views.USER_Login, name ="USER_Login"),
    path('home/', views.home, name ="home"),
#TODO
    path('create/', views.createtodo, name ="createtodo"),
    path('currenttodolist/', views.currenttodolist, name ="currenttodolist"),
    path('completedtodolist/', views.completedtodolist, name ="completedtodolist"),
    path('todo/<int:todo_pk>', views.viewtodo, name ="viewtodo"),
    path('todo/<int:todo_pk>/complete', views.completetodo, name ="completetodo"),
    path('todo/<int:todo_pk>/delete', views.deletetodo, name ="deletetodo"),
]
