import re

def filter_input(input_string):
    filtered_string = re.sub(r'[^a-zA-Z\s]', '', input_string)
    if filtered_string != input_string:
        return "ERROR"
    return filtered_string

