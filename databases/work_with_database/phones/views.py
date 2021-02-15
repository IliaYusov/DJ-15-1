from django.shortcuts import render
from phones.models import Phone


def show_catalog(request):
    sort = request.GET.get('sort')
    phones_list = []
    template = 'catalog.html'
    if sort == 'name':
        phones = Phone.objects.order_by('name').all()
    elif sort == 'min-price':
        phones = Phone.objects.order_by('price').all()
    elif sort == 'max-price':
        phones = Phone.objects.order_by('-price').all()
    else:
        phones = Phone.objects.all()
    for phone in phones:
        phones_list.append(phone)
    return render(request, template, {'phones': phones_list})


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.get(slug=slug)
    context = {'phone': phone}
    return render(request, template, context)
