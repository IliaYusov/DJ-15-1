from datetime import datetime
from os import listdir, stat, path
from django.shortcuts import render
from django.conf import settings


def file_list(request, date=None):
    template_name = 'index.html'
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    files = []
    for name in listdir(settings.FILES_PATH):
        file_path = path.join(settings.FILES_PATH, name)
        ctime = datetime.fromtimestamp(stat(file_path).st_ctime)
        mtime = datetime.fromtimestamp(stat(file_path).st_mtime)
        if not date or date.date() == ctime.date() or date.date() == mtime.date():
            files.append({
                'name': name,
                'ctime': ctime,
                'mtime': mtime
            })
    context = {
        'files': files,
        'date': date
    }
    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:
    file_path = path.join(settings.FILES_PATH, name)
    with open(file_path) as f:
        content = f.read()
    return render(
        request,
        'file_content.html',
        context={'file_name': name, 'file_content': content}
    )
