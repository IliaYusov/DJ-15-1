from django.shortcuts import render
from django.conf import settings
import csv


def inflation_view(request):
    template_name = 'inflation.html'

    # чтение csv-файла и заполнение контекста
    with open('inflation_russia.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        header = csv_reader.__next__()
        rows = []
        for row in csv_reader:
            formatted_row = [{'value': row[0], 'color': settings.INFLATION_PALETTE['year']}]
            for item in row[1:-1]:
                if item:
                    if float(item) > 5:
                        color = settings.INFLATION_PALETTE['>5%']
                    elif float(item) > 2:
                        color = settings.INFLATION_PALETTE['2-5%']
                    elif float(item) > 1:
                        color = settings.INFLATION_PALETTE['1-2%']
                    elif float(item) >= 0:
                        color = settings.INFLATION_PALETTE['0-1%']
                    elif float(item) < 0:
                        color = settings.INFLATION_PALETTE['<0%']
                    formatted_row.append({'value': item, 'color': color})
                else:
                    formatted_row.append({'value': '-', 'color': settings.INFLATION_PALETTE['empty']})
            formatted_row.append({'value': row[-1], 'color': settings.INFLATION_PALETTE['sum']})
            rows.append(formatted_row)

    context = {
        'header': header,
        'rows': rows
               }

    return render(request, template_name,
                  context)
