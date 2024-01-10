from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import re
import json
import os
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import base64
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.conf import settings
from .models import *
import time
from datetime import date
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe

# Information Database
users = [
    {'first_name': 'Soumyajit', 'last_name': 'Mitra', 'username': 'SMitra', 'email': 'soumyajit120503@gmail.com', 'password': 'sm@1253'},
    {'first_name': 'Subhajit', 'last_name': 'Mitra', 'username': 'SubhajitM', 'email': 'subhajitm@britindia.com', 'password': '1234'}
]
data = [
    {
        'id': '1',
        'department':'Sales',
        'tag':'Cosistent Retailers',
        'link':'https://reports.britindia.com/#/workbooks/2650/views'
    },
    {
        'id': '2',
        'department':'Sales',
        'tag':'KATS Dashboard',
        'link':'https://reports.britindia.com/#/workbooks/2649/views'
    },
    {
        'id': '3',
        'department':'Marketing',
        'tag':'Marketing Intelligence Control Tower (MICT)',
        'link':'https://reports.britindia.com/#/views/Britannia_Nov_23/SummaryView?:iid=1'
    },
    {
        'id': '4',
        'department':'Procurement',
        'tag':'Procurement Dashboard (ProDas)',
        'link':'https://prodas.britindia.com/'
    }
]

# Create your views here.
def index(request):
    global current_user
    if request.method == 'POST':
        errors = []
        username = request.POST['username']
        password = request.POST['password']

        # user = authenticate(username=username, password=password)
        user = False
        for i in users:
            if i['username'] == username and i['password'] == password:
                user = True
                break
            else:
                continue

        if user:
            current_user = username
            return redirect(home)
        else:
            errors.append('Invalid login credentials')
            return render(request, 'index.html',{'errors':errors})
    else:
        return render(request, 'index.html')

def signup(request):
    global current_user
    if request.method == 'POST':
        errors = []
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user_exits = False
        for i in users:
            if i['username'] == username:
                user_exits = True
                break
            else:
                continue

        if user_exits:
            errors.append('Username already exists! Try logging in')
            return render(request, 'signup.html',{'errors':errors})
        elif cpassword == password:
            # u = User.objects.create_user(first_name=firstname,last_name=lastname,email=email,username=username, password=password, date_joined=date.today() , is_superuser=0)
            # u.save()
            user_dict = {
                'first_name':firstname,
                'last_name':lastname,
                'username':username,
                'email':email,
                'password':password
            }
            users.append(user_dict.copy())
            current_user = username
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
    username = current_user
    for i in users:
        if i['username'] == username:
                name = i['first_name']
                break
        else:
            continue
    return render(request, 'home.html', {'name':name})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def dashboard(request):
    depts = []
    for i in data:
        if i['department'] in depts:
            continue
        else:
            depts.append(i['department'])
    return render(request, 'dashboard.html', {'depts':depts})

def dept(request,dept):
    tags = []
    links = []
    ids = []
    for i in data:
        if i['department'] == dept:
            tags.append(i['tag'])
            links.append(i['link'])
            ids.append(i['id'])
        else:
            continue
    content = zip(tags,links,ids)
    return render(request, 'dept.html',{'dept':dept, 'content':content})