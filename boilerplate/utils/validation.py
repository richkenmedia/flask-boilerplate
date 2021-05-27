import re


def check_empty_field(value):
    if len(value) != 0:
        return value
    raise ValueError('This Field is Required')


def check_email_field(value):
    if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", value) != None and len(value) != 0:
        return value
    raise ValueError('Please Enter Valid email address')


def check_password(value):
    if re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#^?&])[A-Za-z\d@$!%*#^?&}]+$', value) != None and len(value) > 6:
        return value
    raise ValueError(
        'Minimum six characters, at least one letter, one number and one special character')
