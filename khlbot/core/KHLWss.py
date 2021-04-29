import asyncio
import requests
import json
from khlbot.core.Logger import Logger
import websockets
import websockets.client
from khlbot.config import *
from khlbot.common import decompress_to_json


class KHLWss:
    """
    于连接开黑啦WS网关的类用
    """

    def __init__(self, token, queue: asyncio.Queue = None):
        self.__token = token
        self.latest_sn = 0
        self.__event_queue = queue

    @property
    def event_queue(self):
        return self.__event_queue

    @event_queue.setter
    def event_queue(self, value):
        self.__event_queue = value

    @classmethod
    def get_gateway(cls, token, url):
        """
        获取开黑啦的WS网关地址
        :param url: 获取网关地址的api
        :param token: 开黑啦token
        :return: KHL WS地址
        """
        headers = {
            "Authorization": f"Bot {token}"
        }

        try:
            response = requests.get(url, headers=headers)
            json_data = response.json()

            if json_data["code"] != 0:
                return None

            return json_data["data"]["url"]
        except Exception as e:
            Logger.error(e)

    async def heartbeat(self, ws_connection):
        """
        维持websocket心跳
        :param ws_connection: ws连接
        :return: None
        """
        while True:
            await asyncio.sleep(25)

            send_data = {
                "s": 2,
                "sn": self.latest_sn
            }

            if ws_connection.open:
                await ws_connection.send(json.dumps(send_data))

    async def start(self) -> None:
        """
        完成ws通信的主要操作
        :return: None
        """
        Logger.info("开始获取开黑啦网关地址")
        uri = KHLWss.get_gateway(token=self.__token, url=KHL_API_BASEURL + KHL_API_GATEWAY)
        if uri is None:
            Logger.error(Exception("网关地址获取失败"))
            return

        Logger.info(f"网关地址获取成功")
        async with websockets.client.connect(uri) as ws_connection:
            Logger.info("Websocket连接成功，机器人启动")

            asyncio.create_task(self.heartbeat(ws_connection))

            while True:
                try:
                    if not ws_connection.open:
                        Logger.warning("正在重新连接Websocket")
                        uri = KHLWss.get_gateway(token=self.__token, url=KHL_API_BASEURL + KHL_API_GATEWAY)  # uri可能已经更新
                        ws_connection = await websockets.client.connect(uri)
                        Logger.warning("重新连接Websocket成功")

                    msg = await ws_connection.recv()
                    json_rep = decompress_to_json(msg)

                    if json_rep['s'] == 0:
                        self.latest_sn = json_rep["sn"]
                        if self.__event_queue is not None:
                            await self.event_queue.put(json_rep['d'])
                except (websockets.ConnectionClosedError, websockets.ConnectionClosed) as e:
                    Logger.warning("Websocket已经关闭")
                    ws_connection = None

                    Logger.error(e)
                    await asyncio.sleep(5)
                except Exception as e:
                    Logger.error(e)
                    await asyncio.sleep(5)
