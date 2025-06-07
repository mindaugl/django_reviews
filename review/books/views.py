from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Book


def index(request):
    books_top10 = Book.objects.order_by("-rating")[:10]
    context = {"books_top10": books_top10}
    return render(request, "books/index.html", context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "books/detail.html", {"book": book})

def give_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    print(F("rating"))
    rating = request.POST["rating"]
    book.rating = (F("rating") * F("reviews") + rating) / (F("reviews") + 1)
    book.reviews = F("reviews") + 1
    print(book.rating)
    book.save()
    return HttpResponseRedirect(reverse("books:index"))

def all_books(request):
    books_all = Book.objects.order_by("title")
    context = {"books_all": books_all}
    return render(request, "books/all.html", context)