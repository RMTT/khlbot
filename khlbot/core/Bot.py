from khlbot.core.KHLWss import KHLWss
from khlbot.core.Handler import Handler
from khlbot.core.Logger import Logger
from khlbot.core.Commander import Commander
from khlbot.core.BaseHandler import BaseHandler
import asyncio


class Bot:
    """
    Bot class
    """

    def __init__(self, token, handler: Handler = None, queue: asyncio.Queue = None):
        self.__token = token
        self.__wss = KHLWss(token)
        self.__commanders = []

        if queue is None:
            self.__queue = asyncio.Queue()
        else:
            self.__queue = queue

        if handler is None:
            self.__handler = BaseHandler(self.__queue)
        else:
            self.__handler = handler

    def add_commander(self, commander: Commander) -> None:
        self.__commanders.append(commander)

    def set_handler(self, handler: Handler) -> None:
        self.__handler = handler

    def run(self) -> None:
        if self.__handler is None:
            Logger.error(Exception("Please set messages handler."))
            return

        try:
            Logger.init()
            self.__wss.event_queue = self.__queue
            self.__handler.event_queue = self.__queue

            for commander in self.__commanders:
                self.__handler.add_commands(commander.get_commands())

            loop = asyncio.get_event_loop()

            loop.create_task(self.__handler.consume())
            loop.create_task(self.__wss.start())
            loop.run_forever()
        except Exception as e:
            Logger.error(e)
