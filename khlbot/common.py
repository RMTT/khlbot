from khlbot.config import *
from khlbot.core.Logger import Logger
import requests
import json
import zlib


def decompress_to_json(data) -> json:
    """
    Decompress zlib data
    :param data: Data be compressed via zlib
    :return: json
    """
    return json.loads(zlib.decompress(data))


def decompress_to_str(data) -> str:
    """
     Decompress zlib data
    :param data: Data be compressed via zlib
    :return: str
    """
    return str(zlib.decompress(data))
