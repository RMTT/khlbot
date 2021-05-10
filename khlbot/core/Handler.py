import abc
import asyncio
import multiprocessing
import os
import queue
import time
from khlbot.core.Logger import Logger


class Handler(metaclass=abc.ABCMeta):
    """
    The Handler class is the consumer of bot, you should check the queue content
     and get message from queue and then handle it on Handler class.
    This class is a very basic Handler and cannot use it directly, however, there is a
     simple Handler implementation which BaseHandler can easily use
    """

    def __init__(self, timeout, _queue: multiprocessing.Queue = None):
        """
        :param timeout: Max idle time, it the process take long time to idle,
        it will be exited automatically
        :param _queue: Event queue for consumer
        """
        self.__queue = _queue
        self.__commands = []
        self.__active_time = time.time()
        self.__timeout = timeout
        self.__subscribes = {}
        self.__task_count = 0
        self.__pending_exit = False

    @property
    def event_queue(self):
        return self.__queue

    @event_queue.setter
    def event_queue(self, value: multiprocessing.Queue):
        self.__queue = value

    def add_commands(self, commands: dict) -> None:
        """
        Add command to handler, if find a match command, the handler will handle it
         by handle function
        :param commands: A dict contains commands
        :return: None
        """
        self.__commands.append(commands)

    def add_subscribes(self, items: dict) -> None:
        """
        Add subscribes to handler
        :param items: A list contains subscribes
        :return: None
        """
        for item in items:
            if item not in self.__subscribes:
                self.__subscribes[item] = []

            self.__subscribes[item] = self.__subscribes[item] + items[item]

    def get_commands(self) -> list:
        """
        Get command of this commander
        """
        return self.__commands

    def get_subscribes(self) -> dict:
        """
        Get subscribes
        """
        return self.__subscribes

    async def check_timeout(self):
        """
        Check the idle time of consumer
        """
        while True:
            if time.time() - self.__active_time >= self.__timeout and self.__task_count == 0:
                Logger.warning(
                    f"consumers on [Process-{os.getpid()} {multiprocessing.current_process().name}] "
                    f"is pending to exit, because it's idle too long")
                self.__pending_exit = True

            await asyncio.sleep(self.__timeout)

    async def consume(self) -> None:
        """
        This function is a real consumer, get event message from event queue
         and handle it
        """
        if self.__queue is None:
            raise RuntimeError("missing event queue for Handler")

        while True:
            if self.__queue.empty():
                # If this consumer is idle too long, will be exited
                if self.__pending_exit:
                    break

                await asyncio.sleep(1)
                continue

            try:
                item = self.__queue.get_nowait()
                self.__active_time = time.time()

                self.__task_count = self.__task_count + 1
                await self.handle(item=item)
                self.__task_count = self.__task_count - 1
            except ValueError as err:
                Logger.error(RuntimeError("Event has closed unexpectedly, consumer cannot get anything"))
            except queue.Empty as err:
                await asyncio.sleep(0.5)

    @abc.abstractmethod
    async def handle(self, item):
        """
        When consume function get a message, it will handle it using this function.
        This function is a abstract function, must be implemented on subclass
        :param item: The content will be handled
        """
        pass
