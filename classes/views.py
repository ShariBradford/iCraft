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
    return redirect('/classes')

def unenroll(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    course = Course.objects.get(id=course_id)
    user = User.objects.get(id=request.session['user_id'])
    course.attendees.remove(user)
    course.save()   #IS THIS NECESSARY?
    return redirect('/classes')

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
    return render(request, 'classes/interests.html', context)

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

