import os
from khlbot.core.KHLWss import KHLWss
from khlbot.core.Handler import Handler
from khlbot.core.Logger import Logger
from khlbot.core.Commander import Commander
from khlbot.core.BaseHandler import BaseHandler
import asyncio
import multiprocessing
import khlbot.config as CONFIG


class Bot:
    """
    Bot class, you should use this class to create and launch bot.
    This Bot now supports multiprocessing and coroutine, you can config it to what you want
    """

    def __init__(self, token, handler: Handler = None, queue: multiprocessing.Queue = None, _config: dict = None):
        """
        Create new Bot instance
        :param token: KHL Bot token
        :param handler: The Handler used to consume event message
        :param _config: A dict object which contains configurable items
        """
        if _config is None:
            _config = {}
        self.__token = token
        self.__wss = KHLWss(token)
        self.__commanders = []
        self.__process_manager = multiprocessing.Manager()
        self.__config = _config
        self.__loop = None

        max_queue_size = 10000  # default queue size
        if CONFIG.MAX_EVENT_QUEUE_SIZE in self.__config:
            max_queue_size = 10000
        if queue is None:
            self.__queue = self.__process_manager.Queue(maxsize=max_queue_size)
        else:
            self.__queue = queue

        process_idle_timeout = 60  # default timeout
        if CONFIG.PROCESSING_IDLE_TIMEOUT in self.__config:
            process_idle_timeout = self.__config[CONFIG.PROCESSING_IDLE_TIMEOUT]
        if handler is None:
            self.__handler = BaseHandler(process_idle_timeout, self.__queue)
        else:
            self.__handler = handler

        if CONFIG.MAX_PROCESSING_NUMBER not in self.__config:
            self.__config[CONFIG.MAX_PROCESSING_NUMBER] = os.cpu_count()

        if CONFIG.MAX_CONSUMER_NUMBER not in self.__config:
            self.__config[CONFIG.MAX_CONSUMER_NUMBER] = 4  # default consumers per process

        self.__pool = multiprocessing.Pool(processes=self.__config[CONFIG.MAX_PROCESSING_NUMBER])

    def add_commander(self, commander: Commander) -> None:
        """
        Add commander to Bot
        :param commander: the command will be added
        :return: None
        """
        self.__commanders.append(commander)

    def set_handler(self, handler: Handler) -> None:
        """
        Set Handler
        :param handler: The Handler will be used in bot
        :return: None
        """
        self.__handler = handler

    @staticmethod
    def subprocess_consumer(handler: Handler, consumer_number, is_leader: bool = False) -> None:
        """
        Launch consumers in subprocess, user should not invoke this function directly
        :param handler: The handler to consume event message
        :param consumer_number: The consumer number for per process
        :param is_leader: Mark a subprocess as the first subprocess of consumers if is_leader is True,
         and this process will not be exited even idle. If False, subprocess will be exited when idle
        """
        policy = asyncio.get_event_loop_policy()
        policy.set_event_loop(policy.new_event_loop())
        loop = asyncio.get_event_loop()

        tasks = [loop.create_task(handler.consume(is_leader=is_leader)) for _ in range(consumer_number)]

        loop.run_forever()

    async def __check_queue_size(self) -> None:
        """
        Check event queue size, if the size exceed the configurable limit,
         the bot will create a new subprocess to consume event message
        """
        while True:
            if self.__queue is not None:
                if self.__queue.qsize() > self.__config[CONFIG.MAX_CONSUMER_NUMBER]:
                    self.__launch_subprocess()
            await asyncio.sleep(1)

    def __launch_subprocess(self, is_leader: bool = False) -> None:
        """
        Driver function for starting new subprocess
        :param is_leader: If True, start a leader subprocess for consumers,
         it means the first subprocess for consumers, will not be exited when the process is idle
        :return: None
        """
        self.__pool.apply_async(Bot.subprocess_consumer,
                                (self.__handler, self.__config[CONFIG.MAX_CONSUMER_NUMBER], is_leader),
                                error_callback=lambda err: Logger.error(err))

    def __launch_interval(self) -> None:
        """
        Launch interval tasks
        """
        if self.__loop is None:
            return

        async def __interval(func, period, times, *args, **kwargs):
            unlimited = False

            if times == 0:
                unlimited = True

            while True:
                self.__queue.put({
                    CONFIG.BOT_KEY_MESSAGE_TYPE: CONFIG.BOT_MESSAGE_TYPE_INTERVAL,
                    CONFIG.COMMANDER_KEY_HANDLE: func,
                })

                if not unlimited:
                    times = times - 1
                    if times <= 0:
                        break

                await asyncio.sleep(period)

        for commander in self.__commanders:
            for interval in commander.get_intervals():
                self.__loop.create_task(__interval(func=interval[CONFIG.COMMANDER_KEY_HANDLE],
                                                   period=interval[CONFIG.COMMANDER_KEY_PERIOD],
                                                   times=interval[CONFIG.COMMANDER_KEY_TIMES]))

    def run(self) -> None:
        """
        The entry for launch bot, in this function, bot will connect several components:
        Handler(Consumer), KHLWss(Producer), Commander(Task)
        """
        if self.__handler is None:
            Logger.error(Exception("Please set messages handler."))
            return

        try:
            Logger.init()
            self.__wss.event_queue = self.__queue
            self.__handler.event_queue = self.__queue

            for commander in self.__commanders:
                self.__handler.add_commands(commander.get_commands())
                self.__handler.add_subscribes(commander.get_subscribes())

            self.__launch_subprocess(is_leader=True)

            loop = asyncio.get_event_loop()
            self.__loop = loop

            loop.create_task(self.__wss.start())
            loop.create_task(self.__check_queue_size())

            # launch interval tasks
            self.__launch_interval()

            loop.run_forever()
        except Exception as e:
            Logger.error(e)
