from django.urls import path

from . import views

app_name = "books"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:book_id>/", views.detail, name="detail"),
    path("<int:book_id>/give_review/", views.give_review, name="give_review"),
]
