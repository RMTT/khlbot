import asyncio
import multiprocessing
import queue

import khlbot.config as CONFIG
import requests
import json
from khlbot.core.Logger import Logger
import websockets
import websockets.client
from khlbot.config import *
from khlbot.common import decompress_to_json


class KHLWss:
    """
    Class for KHL Websocket operations, also as a producer in Bot
    """

    def __init__(self, token, queue: multiprocessing.Queue = None):
        """
        :param token: KHL Bot token
        :param queue: Event queue, producer will produce message to this queue
        """
        self.__token = token
        self.latest_sn = 0
        self.__event_queue = queue

    @property
    def event_queue(self):
        return self.__event_queue

    @event_queue.setter
    def event_queue(self, value: multiprocessing.Queue):
        self.__event_queue = value

    @classmethod
    def get_gateway(cls, token, url) -> {str, None}:
        """
        Get gateway address of khl websocket
        :param url: url of khl gateway api
        :param token: khl bot token
        :return: khl websocket address
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

    async def heartbeat(self, ws_connection) -> None:
        """
        Maintain heartbeat for websocket
        :param ws_connection: websocket connection
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
        Launch websocket, and do some important operations
        :return: None
        """
        Logger.info("Getting KHL Websocket address")
        uri = KHLWss.get_gateway(token=self.__token, url=KHL_API_BASEURL + KHL_API_GATEWAY)
        if uri is None:
            Logger.error(Exception("Failed to get websocket address"))
            return

        Logger.info(f"Success to get websocket address")
        async with websockets.client.connect(uri) as ws_connection:
            Logger.info("Connect to websocket success, launch bot")

            asyncio.create_task(self.heartbeat(ws_connection))

            while True:
                try:
                    if ws_connection is None or not ws_connection.open:
                        Logger.warning("Reconnecting to khl websocket")
                        uri = KHLWss.get_gateway(token=self.__token, url=KHL_API_BASEURL + KHL_API_GATEWAY)  # uri可能已经更新
                        ws_connection = await websockets.client.connect(uri)
                        Logger.warning("Reconnect to khl websocket success")

                    msg = await ws_connection.recv()
                    json_rep = decompress_to_json(msg)

                    if json_rep['s'] == 0:
                        self.latest_sn = json_rep["sn"]
                        if self.__event_queue is not None:
                            try:
                                self.__event_queue.put_nowait({
                                    CONFIG.BOT_KEY_MESSAGE_TYPE: CONFIG.BOT_MESSAGE_TYPE_EVENT,
                                    CONFIG.BOT_KEY_MESSAGE_DATA: json_rep['d']
                                })
                            except ValueError as err:
                                Logger.error(RuntimeError("Event queue has closed unexpectedly"))
                                Logger.error(err)
                            except queue.Full:
                                Logger.warning("Event queue is full")


                except (websockets.ConnectionClosedError, websockets.ConnectionClosed) as e:
                    Logger.warning("The websockets have closed unexpectedly")

                    Logger.error(e)

                    # Try reconnection after 3 seconds, avoid too many times to reconnection on a short time
                    await asyncio.sleep(3)
                except Exception as e:
                    Logger.warning("The websockets have closed unexpectedly")

                    Logger.error(e)

                    await asyncio.sleep(3)
