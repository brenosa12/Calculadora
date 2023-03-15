import re

NUM_OR_DOT_REGEX = re.compile(r'^[0-9.]$')


# function to checked if number is a number or Dot
def IsNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


# function to checked if slot is a number valid
def IsValidNumber(string: str):
    valid = False
    try:
        float(string)
        valid = True
    except ValueError:
        valid = False
    return valid


# function to checked if slot is empty
def isEmpty(string: str):
    return string == ''
