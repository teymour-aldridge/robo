"""
general methods to be used anywhere
"""

from datetime import datetime

def parse_timestamp(timestamp):
    # if timestamp is in ms, convert to seconds
    if len(str(timestamp)) > 10:
        timestamp = timestamp // 1000

    unformatted_datetime = str(datetime.fromtimestamp(timestamp))
    
    time = unformatted_datetime[11:15]
    date = unformatted_datetime[:10]

    day, month, year = date.split("-")

    # if the minutes value is less than 10, add a 0 in front (e.g. 10:5 -> 10:05)
    if int(time[3:]) < 10:
        time = f"{time[:2]}:0{time[3]}"

    return f"{time} {day}/{month}/{year}"

def wrap(text, max_chars_per_line):
    text = text.strip(" ")
    text_split = text.split(" ")
    chars_on_this_line = 0

    wrapped_text = ""

    for word in text_split:
        wrapped_text += word + " "
        chars_on_this_line += len(word)
        if chars_on_this_line >= max_chars_per_line:
            if len(wrapped_text) < len(text):
                wrapped_text += "\n"
                chars_on_this_line = 0

    wrapped_text = wrapped_text.strip(" ")

    return wrapped_text