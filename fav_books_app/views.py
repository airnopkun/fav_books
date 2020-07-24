from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book
from django.contrib import messages
import bcrypt


def index(request):
    context = {
        "source": ''
    }
    if "user_id" in request.session:
        del request.session["user_id"]
    if "source" in request.session:
        context["source"] = request.session["source"]
    return render(request, "index.html", context)


def register(request):
    errors = User.objects.registration_validator(request.POST)
    if User.objects.filter(email=request.POST['reg_email']):
        errors["reg_email"] = "User with this email already exists"
    if len(errors) > 0:
        request.session["source"] = "registration"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        reg_email = request.POST['reg_email']
        birthday = request.POST['birthday']
        password = request.POST['reg_password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name, last_name=last_name,
                                   email=reg_email, birthday=birthday,
                                   pw_hash=pw_hash)
        request.session["user_id"] = user.id
        return redirect('/books')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        request.session["source"] = "login"
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.pw_hash.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/books')
    return redirect("/")


def books(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "books": Book.objects.all(),
        "fav_books": User.objects.get(id=request.session["user_id"]).liked_books.all()
    }
    return render(request, "books.html", context)


def add_book(request):
    if "user_id" not in request.session:
        return redirect('/')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/books')
    title = request.POST['title']
    desc = request.POST['description']
    print(desc)
    book = Book.objects.create(title=title, desc=desc, uploaded_by=User.objects.get(id=request.session["user_id"]))
    book.users_who_like.add(User.objects.get(id=request.session["user_id"]))
    return redirect(f'/books/{book.id}')


def add_fav(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    book.users_who_like.add(User.objects.get(id=request.session['user_id']))
    return redirect(f'/books/{book_id}')


def book_profile(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "users_who_like": Book.objects.get(id=book_id).users_who_like.all(),
        "book": Book.objects.get(id=book_id)
    }
    return render(request, "book_profile.html", context)


def update_book(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    errors = Book.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/books/{book_id}')
    title = request.POST['title']
    desc = request.POST['description']
    book = Book.objects.get(id=book_id)
    book.title = title
    book.desc = desc
    book.save()
    return redirect(f'/books/{book.id}')


def delete(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('/books')


def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    if "source" in request.session:
        del request.session["source"]
    return redirect('/')


def unfavorite(request, book_id):
    if "user_id" not in request.session:
        return redirect('/')
    book = Book.objects.get(id=book_id)
    book.users_who_like.remove(User.objects.get(id=request.session['user_id']))
    return redirect(f'/books/{book.id}')
