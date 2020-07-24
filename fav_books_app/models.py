import datetime
import re
from django.db import models


class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['reg_email']):
            errors["reg_email"] = "Invalid email address"
        if len(postData["reg_password"]) < 8:
            errors["reg_password"] = "Password must be at least 8 characters in length"
        elif postData["reg_password"] != postData["confirm"]:
            errors["reg_password"] = "Password and confirmation do not match"
        today = datetime.datetime.today()
        if not postData['birthday']:
            errors['birthday'] = "Must include a user birthday"
        elif postData["birthday"] > str(today):
            errors["birthday"] = "Birthday must be in the past"
        elif (today - datetime.datetime.strptime(postData['birthday'], "%Y-%m-%d")).days < 4745:
            errors['birthday'] = "Must be at least 13 years old to make an account"
        return errors

    def login_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_regex.match(postData['email']):
            errors['email'] = "Invalid email address"
        if len(postData["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters in length"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateField()
    pw_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if not postData['title']:
            errors["title"] = "Title is required"
        if len(postData['description']) < 5:
            errors["description"] = "Description must be at least 5 characters in length"
        return errors


class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(default='')
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
