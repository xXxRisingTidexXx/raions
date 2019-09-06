from json import loads
from typing import Any, Union, List, Dict
from rest_framework.parsers import BaseParser


class JSONParser(BaseParser):
    media_type = 'application/json'

    def parse(
        self, stream: Any, media_type: str = None, parser_context: str = None
    ) -> Union[List[Any], Dict[str, Any]]:
        return loads(stream.read())
