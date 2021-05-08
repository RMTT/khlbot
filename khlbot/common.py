from khlbot.config import *
from khlbot.core.Logger import Logger
import requests
import json
import zlib


def create_msg_to_channel(content, channel_id, _type, token):
    """
    Send message to specific channel
    :param content: message content
    :param channel_id: channel id
    :param _type: message type
    :param token: KHL bot token
    :return: True if success, else False
    """
    url = KHL_API_BASEURL + KHL_API_CREATE_MSG

    data = {
        "type": _type,
        "target_id": channel_id,
        "content": content
    }

    headers = {
        "Authorization": f"Bot {token}"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.json()["code"] == 0:
            return True
    except Exception as e:
        Logger.error(e)

    return False


def decompress_to_json(data) -> json:
    """
    Decompress zlib data
    :param data: Data be compressed via zlib
    :return: json
    """
    return json.loads(zlib.decompress(data))
