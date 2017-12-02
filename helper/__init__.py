import functools
import base64
from .path import setup as setup_path

class Helper:
    def __init__(self):
        print('Helper init.')

    def base64_encode_for_string(self, content):
        return base64.b64encode(content.encode('utf-8')).decode("utf-8")

    def base64_decode_for_string(self, content):
        return base64.b64decode(content.encode('utf-8')).decode('utf-8')

    @classmethod
    def set_instance_method(cls, func):
        @functools.wraps(func)
        def dummy(self, *args, **kwargs):
            return func(*args, **kwargs)
        setattr(cls, func.__name__, dummy)

setup_path(Helper)