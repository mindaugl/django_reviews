from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from .models import Book

def split_backfill_str(s):
    """
    Splits string s based on comma (,), while ignoring commas inside parenthesis ("").
    Removes all parenthesis.
    """
    i_appos = 0
    j = 0
    el = []
    words = []
    s_len = len(s)
    while j < s_len:
        c = s[j]
        j += 1
        if c == '"':
            i_appos += 1
        elif c == ',' and i_appos % 2 == 0:
            words += [''.join(el)]
            el = []
        else:
            el += [c]
    words += [''.join(el)]
    return words


def index(request):
    books_top10 = Book.objects.order_by("-rating")[:10]
    context = {"books_top10": books_top10}
    return render(request, "books/index.html", context)

def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, "books/detail.html", {"book": book})

def give_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    rating = request.POST["rating"]
    book.rating = (F("rating") * F("reviews") + rating) / (F("reviews") + 1)
    book.reviews = F("reviews") + 1
    book.save()
    return HttpResponseRedirect(reverse("books:index"))

def all_books(request):
    books_all = Book.objects.order_by("title")
    context = {"books_all": books_all}
    return render(request, "books/all.html", context)

def backfill_books(request):
    file = request.FILES['file']
    file_name = file.temporary_file_path()
    with open(file_name, 'r') as file:
        columns = file.readline().rstrip().split(',')
        index_map = {"title": 10, "author": 7, "date": 8, "rating": 12, "reviews": 14}

        books = []
        for line in file.readlines():
            data = split_backfill_str(line.rstrip())
            if len(data) != len(columns):
                raise ValueError(f"Too many elements parsed, {len(data) = }.")

            book = Book()
            book.title = data[index_map["title"]]
            book.author = data[index_map["author"]]
            date_str = data[index_map["date"]]
            if date_str == '':
                date_str = '-9999'
            book.publication_year = int(float(date_str))
            book.rating = (float(data[index_map["rating"]]) - 1) * 10 / 4
            book.reviews = data[index_map["reviews"]]
            book.save()
            books.append(book)

    return HttpResponseRedirect(reverse("books:index"))