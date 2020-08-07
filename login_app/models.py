from django.db import models
import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def email_is_unique(self,email):
        users = self.filter(email=email)
        return len(users) == 0

    def email_validator(self, email_to_check):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not email_to_check:
            errors['email'] = "Email is required."
        elif not EMAIL_REGEX.match(email_to_check):
            errors['email'] = "Invalid email address."
        elif self.filter(email=email_to_check):
            errors['email'] = "Email address must be unique."

        return errors

    def name_validator(self, name):
        # checks if name is present, length is greater than 2
        errors = {}

        if not name:
            errors['name'] = "This field is required."
        elif len(name) < 2:
            errors['name'] = "This field should be at least 2 characters."

        return errors
        
    def birthday_validator(self, birth_date):
        errors = {}

        if not birth_date:
            errors['birth_date'] = "Birth date is required."
        else:        
            today = datetime.date.today()
            birthday = datetime.datetime.strptime(birth_date,'%Y-%m-%d')
            years = today.year - birthday.year
            if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
                years -= 1
            #print(f'Today: {today} | Birthday: {birthday} | Years: {years}')

            if years < 13:
                errors['birth_date'] = "You must be over 13 to register."

        return errors

    def password_validator(self, password):
        errors = {}

        if not password:
            errors['password'] = "Password is required."
        elif len(password) < 8:
            errors['password'] = "Password should be at least 8 characters."

        return errors

    def password_confirm_validator(self, password, password_confirm):
        errors = {}

        if not password_confirm:
            errors['password_confirm'] = "Password Confirmation is required."
        elif len(password_confirm) < 8:
            errors['password_confirm'] = "Password should be at least 8 characters."
        
        if password != password_confirm:
            errors['password_confirm'] = "Passwords do not match."

        return errors

    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not postData['first_name']:
            errors['first_name'] = "First Name is required."
        elif len(postData['first_name']) < 2:
            errors['first_name'] = "First name should be at least 2 characters."

        if not postData['last_name']:
            errors['last_name'] = "Last name is required."
        elif len(postData['last_name']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters."

        if not postData['birth_date']:
            errors['birth_date'] = "Birth date is required."
        else:        
            today = datetime.date.today()
            birthday = datetime.datetime.strptime(postData['birth_date'],'%Y-%m-%d')
            years = today.year - birthday.year
            if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
                years -= 1
            #print(f'Today: {today} | Birthday: {birthday} | Years: {years}')

            if years < 13:
                errors['birth_date'] = "You must be over 13 to register."

        if not postData['email']:
            errors['email'] = "Email is required."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        elif self.filter(email=postData['email']):
            errors['email'] = "Email address must be unique."

        if not postData['password']:
            errors['password'] = "Password is required."
        elif len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters."
        elif postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords do not match."

        return errors

    def register(self,postData):
        pw = postData["password"]
        pw_hash = bcrypt.hashpw(
            pw.encode(),
            bcrypt.gensalt()
        ).decode()

        return self.create(
            first_name=postData["first_name"], 
            last_name=postData["last_name"], 
            birth_date=postData["birth_date"],
            email=postData["email"], 
            password=pw_hash, 
        )

    def authenticate(self,email,password):
        user = self.filter(email=email)
        if not user:
            return False

        user_in_database = user.first()
        return bcrypt.checkpw(password.encode(), user_in_database.password.encode())

class User(models.Model):
    # id INT
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateTimeField(default=datetime.date.today)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.id})'