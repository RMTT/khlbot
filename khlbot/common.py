from khlbot.config import *
from khlbot.core.Logger import Logger
import requests
import json
import zlib


def create_msg_to_channel(content, channel_id, _type, token):
    """
    发送消息到指定频道
    :param content: 消息内容
    :param channel_id: 频道ID
    :param _type: 消息类型
    :param token: 开黑啦机器人token
    :return: True表示发送成功，False表示发送失败
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


def decompress_to_json(data):
    """
    解压zlib数据
    :param data: zlib压缩过的数据
    :return: None
    """
    return json.loads(zlib.decompress(data))
