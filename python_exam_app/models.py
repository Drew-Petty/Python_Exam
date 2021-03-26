from django.db import models
import re
import bcrypt
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name'])<2 or postData['first_name'].isalpha() == False:
            errors['first_name'] = 'Please enter a valid first name'
        if len(postData['last_name'])<2 or postData['last_name'].isalpha() == False:
            errors['last_name'] = 'Please enter a valid last name'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'please enter a valid email address'
        for user in User.objects.all():
            if user.email == postData['email']:
                errors['email_used'] = 'a user with that email is already in existance'
        if len(postData['password']) < 8:
            errors['password'] = 'please enter a password with at least 8 charactors'
        if postData['password'] != postData['pw_confirm']:
            errors['confirm_pw'] = 'conformation password does not match'
        return errors
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email = postData['email'])
        if len(user)<1:
            errors['logged_email'] = 'that email is not regstered'
        else:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(),logged_user.password.encode()):
                errors['incorrect_password'] = 'password incorrect'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 15)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class JobManagaer(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors['title'] = 'please provide a longer title'
        if len(postData['title']) < 1:
            errors['title'] = 'please provide a title'
        if len(postData['desc']) < 3:
            errors['desc'] = 'please provide a longer description'
        if len(postData['desc']) < 1:
            errors['desc'] = 'please provide a description'
        if len(postData['location'])<3:
            errors['location'] = 'please provide a more descriptive location'
        if len(postData['location'])<1:
            errors['location'] = 'please provide a location'
        return errors

class Job(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField()
    location = models.TextField()
    created_by = models.ForeignKey(User, related_name = 'jobs_poseted', on_delete = models.CASCADE)
    performed_by = models.ManyToManyField(User, related_name = 'my_jobs')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManagaer()

class Category(models.Model):
    cat_name = models.CharField(max_length = 255)
    jobs = models.ManyToManyField(Job, related_name = 'categories')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)