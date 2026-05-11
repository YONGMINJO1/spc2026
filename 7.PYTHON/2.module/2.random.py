import random
import string

def generate_random_password(length =0):
    chars = string.ascil_letter + string.digits
    return "".join(random.choice(chars) for _ in range(length))

print(generate_random_password())
print(generate_random_password(16))
print(generate_random_password(32))