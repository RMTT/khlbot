import abc
import asyncio


class Handler(metaclass=abc.ABCMeta):
    def __init__(self, queue: asyncio.Queue = None):
        self.__queue = queue
        self.__commands = []

    @property
    def event_queue(self):
        return self.__queue

    @event_queue.setter
    def event_queue(self, value):
        self.__queue = value

    def add_commands(self, commands: dict) -> None:
        self.__commands.append(commands)

    def get_commands(self) -> list:
        return self.__commands

    async def consume(self) -> None:
        if self.__queue is None:
            raise RuntimeError("missing event queue for Handler")

        while True:
            if self.__queue.empty():
                await asyncio.sleep(1)
                continue

            item = await self.__queue.get()
            await self.handle(item=item)
            self.__queue.task_done()

    @abc.abstractmethod
    def handle(self, item):
        pass
