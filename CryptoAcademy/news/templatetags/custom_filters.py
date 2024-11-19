from django import template
import datetime

register = template.Library()

@register.filter
def format_date(value):
    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]
    return f"{value.day} {months[value.month - 1]} {value.year}"

@register.filter
def time_ago(value):
    now = datetime.datetime.now(datetime.timezone.utc)
    diff = now - value

    if diff.days >= 1:
        if diff.days == 1:
            return "1 день назад"
        return f"{diff.days} дней назад"

    seconds = diff.seconds
    if seconds < 60:
        return "только что"
    elif seconds < 3600:
        minutes = seconds // 60
        if minutes == 1:
            return "1 минуту назад"
        return f"{minutes} минут назад"
    else:
        hours = seconds // 3600
        if hours == 1:
            return "1 час назад"
        return f"{hours} часов назад"

    return value.strftime("%H:%M")
