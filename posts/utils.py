import datetime
import re

from django.utils.html import strip_tags


def count_word(html_string):
    word_string = strip_tags(html_string)
    count = len(re.findall(r'\w+', word_string))
    return count


def get_read_time(html_string):
    count = count_word(html_string)
    read_time_min = (count / 200.0)  # Average read Time Per Minutes
    read_time_sec = read_time_min * 60
    read_time = str(datetime.timedelta(seconds=read_time_sec))
    return read_time
