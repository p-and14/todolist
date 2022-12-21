import random
import string


def generate_verification_code(length):
    """
    generate random verification code
    """
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, length))
    return rand_string
