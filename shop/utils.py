import re
import random
from base64 import b64encode

def phone_validator(phone_number):
    """
    Returns true if phone number is correct else false
    """
    regix = r'^\+?1?\d{10}$'
    com = re.compile(regix)
    find = len(com.findall(phone_number))
    if find == 1:
        return True
    else:
        return False


def password_generator(length):
    """
    Generate fake password of passed length.
    """
    string = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    password = "".join(random.sample(string, length))
    return password


def otp_generator():
    otp = random.randint(999, 9999)
    return otp
