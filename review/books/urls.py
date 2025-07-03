from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all_books, name="all"),
    path("all_rating/", views.all_books_sorted_rating, name="all_rating"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:book_id>/give_review/", views.give_review, name="give_review"),
    path("backfill/", views.backfill_books, name="backfill_books"),
]
