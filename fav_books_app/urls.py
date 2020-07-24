from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('books', views.books),
    path('add_book', views.add_book),
    path('books/<int:book_id>', views.book_profile),
    path('add_fav/<int:book_id>', views.add_fav),
    path('unfavorite/<int:book_id>', views.unfavorite),
    path('update_book/<int:book_id>', views.update_book),
    path('delete/<int:book_id>', views.delete),
    path('logout', views.logout)
]
