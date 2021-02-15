from django.shortcuts import render
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    print(context['books'][0].pub_date)
    return render(request, template, context)


def book_detail_view(request, date):
    template = 'books/books_detail_view.html'
    context = {}
    books_ordered = Book.objects.order_by('pub_date')
    for index, book in enumerate(books_ordered):
        if book.pub_date == date.date():
            context['book'] = book
            if index > 0:
                context['previous_book'] = books_ordered[index - 1]
            else:
                context['previous_book'] = None
            if index < len(books_ordered) - 1:
                context['next_book'] = books_ordered[index + 1]
            else:
                context['next_book'] = None
            break
    print(context)
    return render(request, template, context)
