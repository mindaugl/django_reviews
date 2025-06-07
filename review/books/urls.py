from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("all/", views.all_books, name="all"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:book_id>/give_review/", views.give_review, name="give_review"),
    # path("<int:book_id>/<int:rating>/give_review/", views.give_review, name="give_review"),
]
