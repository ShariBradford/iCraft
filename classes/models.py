from django.db import models
from django import forms
from django.forms import ModelForm
from login_app.models import User
from localflavor.us.models import USStateField
# from django.utils import timezone
from datetime import datetime, date

class Interest(models.Model):
    #id INT
    name = models.CharField(max_length=50)
    description =  models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return f'{self.name} ({self.id})'

class InterestForm(ModelForm):
    class Meta:
        model = Interest
        fields = ['name', 'description']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class Course(models.Model):
    #The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name. 
    #Generally, it’s best to define choices inside a model class, and to define a suitably-named constant for each value
    #For each model field that has choices set, Django will add a method to retrieve the human-readable name for 
    # the field’s current value: get_FOO_display() Where 'FOO' is the name of the field
    #A new migration is created each time the order of choices changes.
    IN_PERSON = 'I'
    VIRTUAL = 'V'
    RECORDED = 'R'     
    COURSE_TYPE_CHOICES = [
        (IN_PERSON, 'In-Person'),
        (VIRTUAL, 'Virtual'),
        (RECORDED, 'Recorded'),
    ]

    # id INT
    title = models.CharField(max_length=255)
    tag_line = models.CharField(max_length=255, help_text="Provide a short description (e.g., <em>Learn to build beautiful photo albums for gifts or to sell</em>).")
    date =  models.DateTimeField(help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
    description =  models.TextField()
    location = models.CharField(max_length=255, help_text="For virtual classes, use the videoconference link; for recorded courses, use the YouTube or video link; for in-person courses, use the address.")
    location_type = models.CharField(max_length=1,choices=COURSE_TYPE_CHOICES,default=VIRTUAL)
    creator = models.ForeignKey(User,related_name="courses_created", on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User,related_name="courses_attended")
    max_size = models.PositiveIntegerField()
    areas_of_interest = models.ManyToManyField(Interest,related_name="related_courses")
    favorited_by = models.ManyToManyField(User,related_name="favorite_courses")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # objects = CourseManager()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/classes/{self.id}'

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'tag_line', 'date', 'location', 'location_type', 'creator', 'max_size', 'areas_of_interest', ]
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}),
            'tag_line' : forms.TextInput(attrs={'class':'form-control'}),
            'location' : forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'location_type': forms.Select(attrs={'class': 'form-control'}),
            'max_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'areas_of_interest': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'creator': forms.HiddenInput(attrs={'class': 'form-control'}),
       }


# class User_Uploads(models.Model):
#     user = models.ForeignKey(User,related_name="uploads", on_delete=models.CASCADE)
#     course = models.ForeignKey(Course,related_name="uploads", on_delete=models.CASCADE)
#     file = models.FileField(upload_to=course_directory_path)

#     # def user_directory_path(self, filename):
#     #     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     #     return f'user_{self.creator.id}/{filename}'

#     def course_directory_path(self, filename):
#         # file will be uploaded to MEDIA_ROOT/course_<id>/<filename>
#         return f'course_{self.course.id}/{filename}'

class Question(models.Model):
    #id INT
    content = models.CharField(max_length=255)
    asker = models.ForeignKey(User,related_name="questions_asked", on_delete=models.CASCADE)
    answer = models.CharField(max_length=255, blank=True)
    answerer = models.ForeignKey(User,related_name="questions_answered", on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name="questions", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.content}'

class UserProfileManager(models.Manager):
    def create_profile(self, user_id, user_data):
        profile = self.create(
            user=User.objects.get(id=user_id), 
            company=user_data["company"], 
            address=user_data["address"], 
            city=user_data["city"], 
            state=user_data["state"], 
            bio=user_data["bio"], 
            birth_date=user_data["birth_date"],
        )

        # assumes that user_data contains a key called 'interests' that is an array of interest_ids
        for interest_id in user_data["interests"]:
            profile.areas_of_interest.add(Interest.objects.get(id=interest_id))

        return profile

class UserProfile(models.Model):
    user = models.OneToOneField(User,models.CASCADE,related_name="profile")
    company = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = USStateField(blank=True)
    bio =  models.TextField(blank=True)
    areas_of_interest = models.ManyToManyField(Interest,related_name="related_profiles")
    birth_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserProfileManager()

    def __str__(self):
        return f'{self.user.full_name()} Profile'

    def __repr__(self):
        return f'{self.user.full_name()} ({self.id})'

    def get_absolute_url(self):
        return f'/users/{self.user.id}' #use the userid for the profile, not profile.id

