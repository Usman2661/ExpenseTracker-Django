from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render_to_response

# Create your views here.

def index(request):

    if request.user.is_authenticated:
        return redirect('home')
    elif request.method=='POST':
    
        email=request.POST['email']
        password=request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home') 
        else:
            messages.error(request,'email or password not correct')
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    elif request.method=='POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']

        try:

            user = User.objects.create_user(password=password, username=email, first_name=first_name,last_name=last_name)
            # status=user.save()
        except IntegrityError:
            messages.error(request,'Error: Regiseration unsucessfull email may already be in use!!')
            return redirect('register')
        else:
            messages.success(request,'Registered Succesfully')
            return redirect('login')
    else:
        return render(request,'accounts/register.html')


def logout(request):
    if request.method =='POST':
        auth.logout(request)
        messages.success(request,'You are now logged out')
        return redirect ('login')
    else:
        return


