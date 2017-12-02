import base64

class Helper:
    def __init__(self):
        print('Helper init.')

    def base64_encode_for_string(self, content):
        return base64.b64encode(content.encode('utf-8')).decode("utf-8")

    def base64_decode_for_string(self, content):
        return base64.b64decode(content.encode('utf-8')).decode('utf-8')

