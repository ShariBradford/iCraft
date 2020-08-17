from django.shortcuts import render, redirect, HttpResponse
from .models import User
from classes.models import *
import bcrypt
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
import json
import random

path = os.path.join(settings.BASE_DIR, 'login_app/static/test_users.json') 
with open(path, 'r') as data:
    user_data = json.load(data)

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
        messages.success(request,"Successfully registered!")
        return redirect(f'/users/{user.id}/update')

def login(request):
    if request.method != "POST":
       redirect('/')

    if User.objects.authenticate(request.POST['email'],request.POST['login_password']):
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/classes')
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

    return render(request, 'validation-messages.html', context)


def user_profile(request,profiled_user_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')
    
    profiled_user = User.objects.get(id=profiled_user_id)
    location = profiled_user.profile.state or ''

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'profiled_user': profiled_user,
        'location': location,
    }
    return render(request, 'user-profile.html', context)

def update_user_profile(request, profiled_user_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    profiled_user = User.objects.get(id=profiled_user_id)
    profile = profiled_user.profile

    if request.method == 'POST':

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():

            profile = form.save(commit=False)

            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                profile.profile_pic = UserProfile._meta.get_field('profile_pic').get_default()

            #save the profile and then save the many-to-many data from the form
            profile.save()

            # If your model has a many-to-many relation and you specify commit=False when you save a form, 
            # Django cannot immediately save the form data for the many-to-many relation.
            # Manually save many-to-many data
            form.save_m2m() 

            return redirect(f'/users/{profiled_user_id}')
    
    else: #this is a GET request so create a blank form
        form = UserProfileForm(instance=profile)
    
    context = {
        'user': user,
        'profiled_user': profiled_user,
        'form': form,
    }
    return render(request,'user-profile-form.html', context)

def testdata(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/classes')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'user_data': user_data,
        'test_data': True,
    }
    return render(request, 'classes/test-data.html',context)

def create_users(request):
    i = 0
    for user in user_data["results"]:
        if user["dob"]["age"] <= 13:
            continue

        if User.objects.filter(first_name=user["name"]["first"], last_name=user["name"]["last"]):
            messages.info(request,f'{user["name"]["first"]} {user["name"]["last"]} is already registered. Skipping.') 
            continue

        new_user = {
            'first_name': user["name"]["first"],
            'last_name': user["name"]["last"],
            'email': user["email"],
            'password': '123456789',
            'password_confirm':'123456789',
            'birth_date': user["dob"]["date"][0:10],
        }

        errors = User.objects.basic_validator(new_user)
        if errors: 
            # print(f'Error registering {new_user["first_name"]} {new_user["last_name"]}:')
            for k,v in errors.items():
                messages.add_message(request,messages.ERROR,v)
        
        else:
            created_user = User.objects.register(new_user)
            created_user.profile.address = f'{user["location"]["street"]["number"] } { user["location"]["street"]["name"] }'
            created_user.profile.city = user["location"]["city"]
            created_user.profile.state = user["location"]["state"]
            created_user.profile.bio = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac fringilla ex. Integer in dictum justo, id ornare sapien. Phasellus id tempus odio. Vestibulum vitae ultrices tellus. Quisque id nisi nec tortor hendrerit suscipit. Pellentesque et viverra sapien, interdum iaculis ex. Quisque viverra lacus malesuada, maximus felis eu, mollis nisl. Nunc vel rutrum lorem. Morbi quis lobortis mauris, in lacinia justo. Mauris semper, magna eget mollis gravida, nisi felis mattis tortor, ut volutpat mi dui nec libero."
            created_user.profile.birth_date = created_user.birth_date

            num_interests = random.randint(1,8) #get a random number of interests
            for j in range(num_interests):
                interest_id = random.randint(1,8)
                created_user.profile.areas_of_interest.add(Interest.objects.get(id=interest_id))
            created_user.profile.save()

            message = f"SUCCESS! Registered {created_user.full_name()}."
            messages.success(request,message)
        
        i += 1
        if i > 20:
            break 

    return redirect('/testing')

def reset_users(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/classes')

    user = User.objects.get(id=request.session['user_id'])
    if not user.is_admin:
        return redirect('/classes')

    for one_user in User.objects.all():
        print(f"Updating profile picture for {one_user.full_name()} to {UserProfile._meta.get_field('profile_pic').get_default()}.")

        one_user.profile.profile_pic = UserProfile._meta.get_field('profile_pic').get_default()
        one_user.profile.save()

    return redirect('/testing')
