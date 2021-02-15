from django.shortcuts import render
from phones.models import PhoneApple, PhoneSamsung, PhoneXiaomi


def show_catalog(request):
    template = 'catalog.html'
    phones_list = [PhoneApple.objects.first(), PhoneSamsung.objects.first(), PhoneXiaomi.objects.first()]
    context = []
    all_fields = []
    for phone in phones_list:
        for field in phone._meta.get_fields():
            if [field.name, field.verbose_name] not in all_fields:
                all_fields.append([field.name, field.verbose_name])
    for field in all_fields:
        field_list = []
        for phone in phones_list:
            value = getattr(phone, field[0], '-')
            if value is True:
                field_list.append('Есть')
            elif value is False or value is None:
                field_list.append('-')
            else:
                field_list.append(value)
        context.append([field[1]] + field_list)
    return render(
        request,
        template,
        {'table_header': context[1], 'table_lines': context[2:]}
    )
