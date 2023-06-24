from datetime import datetime
from django import template

register = template.Library()

@register.filter
def convert_time(time_stamp):
    try:
        dt = datetime.fromtimestamp(int(time_stamp))
        time = dt.strftime('%m %b, %Y | %I:%M %p')
        return time
    except:
        return