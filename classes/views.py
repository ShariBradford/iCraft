from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from login_app.models import User
from .models import *
from django.contrib import messages
from django.db.models import Avg, F, Q
from django.core.paginator import Paginator
import math

COURSES_PER_PAGE = 6

# Create your views here.
def index(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')
    
    courses = Course.objects.all().order_by('date')

    paginator = Paginator(courses, COURSES_PER_PAGE) # NUMBER OF courses per page TO DISPLAY
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'page_obj': page_obj,
        'current_page': page_number,
    }
    return render(request, 'classes/dashboard.html', context)

def get_class(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    course = Course(creator=user)

    #POST request ==> save new course
    if request.method == 'POST':
        
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
        
            course = form.save(commit=False)
        
            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                course.profile_pic = Course._meta.get_field('profile_pic').get_default()

            #save the course and then save the many-to-many data from the form
            course.save()
            
            # If your model has a many-to-many relation and you specify commit=False when you save a form, 
            # Django cannot immediately save the form data for the many-to-many relation.
            # Manually save many-to-many data
            form.save_m2m() 

            return redirect(f'/classes/{course.id}')
    
    else: #this is a GET request so create a blank form
        form = CourseForm(instance=course)
    
    context = {
        'user': user,
        'form': form,
        'action': 'new',
    }
    return render(request,'classes/class.html', context)

def rate_class(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    course = Course.objects.get(id=course_id)

    print(f'Processing rating of course {course.title} by {user.full_name()}')
    if request.method == 'POST':

        rating = Rating(user=user, course=course)
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            rating = form.save()
            # rating = form.save(commit=False)
            # rating.user = user
            # rating.course = course
            # rating.save()
            
            # return redirect(f'/classes/{course_id}')
            # return HttpResponse('Thanks!')
    
    else: #this is a GET request so create a blank form
        return redirect(f'/classes/{course.id}')
    
    if hasattr(course,'ratings'):
        if course.ratings.filter(user=user).count() > 0:
            user_has_rated_course = True
            user_rating_this_course = course.ratings.filter(user=user).first()
            form = None

        else:
            user_has_rated_course = False
            user_rating_this_course = None

        average_rating = Rating.objects.filter(course=course).aggregate(Avg('number_of_stars'))['number_of_stars__avg'] or 0
        temp_avg = math.floor(average_rating)
        temp_rating = Rating(user=user, course=course, number_of_stars = temp_avg)
        average_rating_text = temp_rating.get_number_of_stars_display()
        all_ratings = course.ratings.all()

    else:
        average_rating = 0
        average_rating_text = ''
        all_ratings = None

    context = {
        'user': user,
        'course': course,
        'average_rating': average_rating,
        'average_rating_text' : average_rating_text,
        'all_ratings': all_ratings,
        'user_has_rated_course': user_has_rated_course,
        'user_rating_this_course': user_rating_this_course,
        'ratings_form': form,
    }
   
    return render(request, 'classes/ratings-form.html', context)

def update_class(request, course_id):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':

        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():

            course = form.save(commit=False)

            # if the user deleted the previous photo, add the default photo
            if form.cleaned_data['profile_pic'] == None or form.cleaned_data['profile_pic'] == False:
                course.profile_pic = Course._meta.get_field('profile_pic').get_default()
            
            course.save()
            
            # If your model has a many-to-many relation and you specify commit=False when you save a form, 
            # Django cannot immediately save the form data for the many-to-many relation.
            # Manually save many-to-many data
            form.save_m2m() 

            return redirect(f'/classes/{course_id}')
    
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

    user = User.objects.get(id=request.session['user_id'])
    course = Course.objects.get(id=course_id)

    if hasattr(course,'ratings'):

        if course.ratings.filter(user=user).count() > 0:
            print(f"Ratings for {course.title}: {course.ratings.filter(user=user).count()}")
            user_has_rated_course = True
            user_rating_this_course = course.ratings.filter(user=user).first()
            form = None

        else:
            user_has_rated_course = False
            user_rating_this_course = None
            form = RatingForm()

        average_rating = Rating.objects.filter(course=course).aggregate(Avg('number_of_stars'))['number_of_stars__avg'] or 0
        temp_avg = math.floor(average_rating)
        temp_rating = Rating(user=user, course=course, number_of_stars = temp_avg)
        average_rating_text = temp_rating.get_number_of_stars_display()
        all_ratings = course.ratings.all()

    else:
        print(f"No ratings yet for {course.title}.")
        form = RatingForm()
        average_rating = 0
        average_rating_text = ''
        all_ratings = None

    context = {
        'user': user,
        'course': course,
        'average_rating': average_rating,
        'average_rating_text': average_rating_text,
        'all_ratings': all_ratings,
        'user_has_rated_course': user_has_rated_course,
        'user_rating_this_course': user_rating_this_course,
        'ratings_form': form,
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

def search_classes(request):
    if (not 'user_id' in request.session.keys()) or (request.session['user_id'] == ''):
        return redirect('/')

    query = request.GET.get('q', '')
    print("SEARCHING FOR: ", query)
    if query:
        queryset = (Q(title__icontains = query)) | (Q(tag_line__icontains=query)) | (Q(description__icontains=query))
        courses = Course.objects.filter(queryset).distinct().order_by('date')
        print("COURSES: ", courses)
    else:
        courses = Course.objects.all().order_by('date')

    paginator = Paginator(courses, COURSES_PER_PAGE) #show 9 courses per page
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'page_obj': page_obj,
        'courses': page_obj.object_list,
        'current_page': page_number,
        'search_query': query,
    }
    return render(request, 'classes/card-course.html', context)
    # return render(request, 'classes/dashboard.html', context)