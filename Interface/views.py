from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
import json
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import base64
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from .models import *
import time
from datetime import date
from django.template.response import TemplateResponse

# Create your views here.
def index(request):
    if request.method == 'POST':
        errors = []
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['username'] = username
            return redirect(home)
        else:
            errors.append('Invalid login credentials')
            return render(request, 'index.html',{'errors':errors})
    else:
        return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        errors = []
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username).exists():
            errors.append('Username already exists! Try logging in')
            return render(request, 'signup.html',{'errors':errors})
        elif cpassword == password:
            u = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username, password=password, date_joined=date.today() , is_superuser=0)
            u.save()
            request.session['username'] = username
            return redirect(home)
        elif cpassword != password:
            errors.append('Passwords does not match')
            return render(request, 'signup.html',{'errors':errors})
        else:
            errors.append('An unknown error occurred. Please try again!')
            return render(request, 'signup.html',{'errors':errors})
    else:
        return render(request, 'signup.html')
    
def home(request):
    username = request.session['username']
    name = User.objects.filter(username=username)[0].first_name
    return render(request, 'home.html', {'name':name})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    depts = []
    all_info = Information.objects.all()
    for i in all_info:
        if i.department in depts:
            continue
        else:
            depts.append(i.department)
    return render(request, 'dashboard.html', {'depts':depts})

def dept(request,dept):
    info = Information.objects.filter(department=dept)
    return render(request, 'dept.html',{'dept':dept, 'info':info})