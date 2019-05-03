import os
from binascii import hexlify


def random_id():
    return str(hexlify(os.urandom(16)), 'ascii')
