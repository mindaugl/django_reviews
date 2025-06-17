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

def backfill_books(request):
    # file_name = request.POST["file_name"]
    file_name = "../../../Downloads/books_dataset/books.txt"
    file = open(file_name, 'r')
    columns = file.readline().rstrip().split(',')
    ind = {"title": 9, "author": 7, "date": 8, "rating": 12, "reviews": 14}

    lens = {}
    for line in file.readlines():
        data = line.rstrip().split(',')
        book = Book()
        book.title = data[ind["title"]]
        book.author = data[ind["author"]]
        book.publication_date = data[ind["date"]]
        # book.rating = (float(data[ind["rating"]]) - 1) * 10 / 4
        book.reviews = data[ind["reviews"]]
        if len(data) in lens:
            lens[len(data)] += 1
        else:
            lens[len(data)] = 1

    return HttpResponseRedirect(reverse("books:index"))