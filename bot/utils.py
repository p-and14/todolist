import random
import string


def generate_verification_code():
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(random.sample(letters_and_digits, 10))
    return rand_string
