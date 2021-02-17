from django.shortcuts import render
from books.models import Book


def books_view(request):
    template = 'books/books_list.html'
    context = {'books': Book.objects.all()}
    print(context['books'][0].pub_date)
    return render(request, template, context)


def book_detail_view(request, date):
    template = 'books/books_detail_view.html'
    context = {'books': Book.objects.filter(pub_date=date).order_by('pub_date'),
               'next_book': Book.objects.filter(pub_date__gt=date).order_by('pub_date').first(),
               'previous_book': Book.objects.filter(pub_date__lt=date).order_by('-pub_date').first()}
    print(context)
    return render(request, template, context)
