from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from login_app.models import User
from .models import *
from django.contrib import messages
from django.db.models import F

# Create your views here.
def index(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'courses': Course.objects.all().order_by('date'),
        'first_course': Course.objects.get(id=1),
    }
    return render(request, 'classes/dashboard.html', context)

def get_class(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    course = Course(creator=user)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('/classes')
    
    else: #this is a GET request so create a blank form
        form = CourseForm(instance=course)
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',
    }
    return render(request,'classes/class.html', context)

def update_class(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('/classes')
    
    else: #this is a GET request so create a blank form
        form = CourseForm(instance=course)
    
    context = {
        'user': user,
        'form': form,
        'course': course,
        'action': 'update',
    }
    return render(request,'classes/class.html', context)

def class_details(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'course': Course.objects.get(id=course_id),
    }
    return render(request, 'classes/course-details.html', context)

def enroll(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])

    course.attendees.add(user)
    course.save()   #IS THIS NECESSARY?
    # return redirect('/classes')
    return redirect(request.META.get('HTTP_REFERER'))

def unenroll(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])

    course.attendees.remove(user)
    course.save()   #IS THIS NECESSARY?
    # return redirect('/classes')
    return redirect(request.META.get('HTTP_REFERER'))

def interests(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    interests = Interest.objects.all()
    context = {
        'user': user,
        'areas_of_interest' : interests,
    }
    return render(request, 'classes/interests.html', context)

def get_interest(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/classes/interests')
    
    else: #this is a GET request so create a blank form
        form = InterestForm()
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',
    }
    return render(request,'classes/interest.html', context)

def update_interest(request, interest_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    interest = Interest.objects.get(id=interest_id)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect('/classes/interests')
    
    else: #this is a GET request so create a blank form
        form = InterestForm(instance=interest)
    
    context = {
        'user': user,
        'form': form,
        'interest': interest,
        'action': 'update',
    }
    return render(request,'classes/interest.html', context)

def add_interest(request, interest_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    interest = Interest.objects.get(id=interest_id)

    if interest not in user.profile.areas_of_interest.all():
        user.profile.areas_of_interest.add(interest)
        user.profile.save()   #IS THIS NECESSARY?

    return redirect(request.META.get('HTTP_REFERER'))

def remove_interest(request, interest_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    interest = Interest.objects.get(id=interest_id)

    if interest in user.profile.areas_of_interest.all():
        user.profile.areas_of_interest.remove(interest)
        user.profile.save()   #IS THIS NECESSARY?

    return redirect(request.META.get('HTTP_REFERER'))

def interest_classes(request, interest_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    interest = Interest.objects.get(id=interest_id)
    context = {
        'user': user,
        'area_of_interest' : interest,
        'courses': interest.related_courses.all().order_by('date'),
    }
    return render(request, 'classes/interest-classes.html', context)

def favorites(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
        'courses': user.favorite_courses.all().order_by('date'),
    }
    return render(request, 'classes/favorites.html', context)

def favorite(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    print("running favorite view")
    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])
    if user not in course.favorited_by.all():
        course.favorited_by.add(user)
        course.save()   #IS THIS NECESSARY?

    #print("Referrer: ", request.META.get('HTTP_REFERER'))
    #return redirect('/classes')
    # user could be on any numbmer of pages when they push the favorite button
    # return the user to the same page they were on when they favorited the course
    return redirect(request.META.get('HTTP_REFERER'))
    #return HttpResponse("Success")
    #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def unfavorite(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])
    if user in course.favorited_by.all():
        course.favorited_by.remove(user)
        course.save()   #IS THIS NECESSARY?
    #return redirect('/classes')
    return redirect(request.META.get('HTTP_REFERER'))
    #return HttpResponse("Success")
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

