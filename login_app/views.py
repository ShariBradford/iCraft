from django.shortcuts import render, redirect, HttpResponse
from .models import User
from trips.models import Trip
import bcrypt
from django.contrib import messages
from trips.templates import *

def index(request): 
    return render(request,'index.html')

def register(request):
    #print(request.POST)

    errors = User.objects.basic_validator(request.POST)
    if errors: 
        for k,v in errors.items():
            messages.add_message(request,messages.ERROR,v, extra_tags='register')
        return redirect("/")
        
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        messages.success(request,"Successfully logged in!")
        return redirect('/trips')

def login(request):
    if request.method != "POST":
       redirect('/')

    if User.objects.authenticate(request.POST['email'],request.POST['login_password']):
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/trips')
    else:
        request.session.clear()
        messages.error(request,"Invalid email or password.",extra_tags="login")
        return redirect("/")

def logout(request):
    request.session.clear()
    return redirect('/')

def validate_fields(request):
    #expect request.POST to contain keys: 'fieldname', 'value', csrfmiddlewaretoken
    messages = {}
    errors = {}
    # print(request.POST)

    if request.POST['fieldname'] == 'first_name' or request.POST['fieldname'] == 'last_name':
        errors = User.objects.name_validator(request.POST['value'])
    elif request.POST['fieldname'] == 'email':
        errors = User.objects.email_validator(request.POST['value'])
    elif request.POST['fieldname'] == 'birth_date':
        errors = User.objects.birthday_validator(request.POST['value'])
    elif request.POST['fieldname'] == 'password':
        errors = User.objects.password_validator(request.POST['value'])
    elif request.POST['fieldname'] == 'password_confirm':
        errors = User.objects.password_confirm_validator(request.POST['value'],request.POST['password'])

    if errors:
        for key, error in errors.items():
            messages[key] = {
                'tag': 'danger',
                'message': error
            }
    else:
        messages[request.POST['fieldname']] = {
            'tag': 'success',
            'message': "Valid"
        }
    # messages['extra']='extra'
    context = {
        'messages': messages,
    }
    # print(context)

    return render(request, 'validation-messages.html',context)