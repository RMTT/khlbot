import abc
import asyncio
import multiprocessing
import time


class Handler(metaclass=abc.ABCMeta):
    """
    The Handler class is the consumer of bot, you should check the queue content
     and get message from queue and then handle it on Handler class.
    This class is a very basic Handler and cannot use it directly, however, there is a
     simple Handler implementation which BaseHandler can easily use
    """

    def __init__(self, timeout, queue: multiprocessing.Queue = None):
        """
        :param timeout: Max idle time, it the process take long time to idle,
        it will be exited automatically
        :param queue: Event queue for consumer
        """
        self.__queue = queue
        self.__commands = []
        self.__active_time = time.time()
        self.__timeout = timeout
        self.__subscribes = {}

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
        while True:
            if time.time() - self.__active_time >= self.__timeout:
                exit(0)

            await asyncio.sleep(1)

    async def consume(self, is_leader: bool = False) -> None:
        """
        This function is a real consumer, get event message from event queue
         and handle it
        :param is_leader: if True, the process will not be exited even it is idle
        """
        if not is_leader:
            asyncio.create_task(self.check_timeout())

        if self.__queue is None:
            raise RuntimeError("missing event queue for Handler")

        while True:
            if self.__queue.empty():
                await asyncio.sleep(1)
                continue

            item = self.__queue.get()
            await self.handle(item=item)
            self.__queue.task_done()

            self.__active_time = time.time()

    @abc.abstractmethod
    async def handle(self, item):
        """
        When consume function get a message, it will handle it using this function.
        This function is a abstract function, must be implemented on subclass
        :param item: The content will be handled
        """
        pass
