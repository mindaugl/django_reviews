from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Book


def index(request):
    books_top10 = Book.objects.order_by("-rating")[:10]
    context = {"books_top10": books_top10}
    return render(request, "books/index.html", context)

def detail(request, book_id):
    # return HttpResponse("You're looking at book %s." % book_id)
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "books/detail.html", {"book": book})

def give_review(request, book_id):
    return HttpResponse("You're reviewing book %s." % book_id)