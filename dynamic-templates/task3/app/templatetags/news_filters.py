from django import template
from datetime import datetime, timedelta


register = template.Library()


def hour_ending(hours):
    if 4 >= hours % 20 >= 2:
        return 'a'
    elif hours % 20 == 1:
        return ''
    return 'ов'


@register.filter
def format_date(value):
    post_age = datetime.now() - datetime.fromtimestamp(value)
    if post_age < timedelta(seconds=600):
        return "только что"
    elif post_age < timedelta(hours=24):
        return f"{str(post_age.seconds//3600)} " \
                f"час{hour_ending(post_age.seconds//3600)} назад"
    else:
        return datetime.fromtimestamp(value).strftime('%Y-%b-%d')


@register.filter
def format_score(value):
    if value < -5:
        return 'все плохо'
    elif value > 5:
        return 'хорошо'
    else:
        return 'нейтрально'


@register.filter
def format_num_comments(value):
    if value > 50:
        return '50+'
    elif value > 0:
        return value
    else:
        return 'Оставьте комментарий'


@register.filter
def format_selftext(value, count):
    if value:
        return ' '.join(value.split()[:count]) + ' ... ' + ' '.join(value.split()[-count:])
    return ''
