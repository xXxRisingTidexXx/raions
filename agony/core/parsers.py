from json import loads
from rest_framework.parsers import BaseParser


class JSONParser(BaseParser):
    media_type = 'application/json'

    def parse(self, stream, media_type=None, parser_context=None):
        return loads(stream.read())
