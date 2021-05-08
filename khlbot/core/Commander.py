import functools
import khlbot.config as CONFIG


class Commander:
    """
    Class for configure and save concrete task, for example, the "-hello" command,
     when bot find a message which contains "-hello", it will using the functions saved in
     commander to handle this event
    """

    def __init__(self, prefix: str = ''):
        """
        :param prefix: The prefix of commands
        """
        self.__prefix = prefix
        self.__commands = {}
        self.__intervals = []

    def get_commands(self) -> dict:
        return self.__commands

    def get_intervals(self):
        return self.__intervals

    def command(self, command, *params, **extras):
        """
        Decorator for command handle function, recommend use this decorator to
         create command handle function
        :param command: The command
        :param params: The parameters for command handle function
        :param extras: Extra configurable items:
        partial: using partial function when invoke this command function
        """

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            self.__commands[self.__prefix + command] = {
                CONFIG.COMMANDER_KEY_PARAM_NUMBER: len(params),
                CONFIG.COMMANDER_KEY_HANDLE: wrapper
            }

            if CONFIG.COMMANDER_KEY_PARTIAL in extras:
                self.__commands[self.__prefix + command][CONFIG.COMMANDER_KEY_HANDLE] = functools.partial(wrapper,
                                                                                                          *extras[
                                                                                                              "partial"])
            return wrapper

        return decorator

    def interval(self, period, times=0, **extras):
        """
        Decorator for period task
        :param period: The period
        :param times: Executed times, 0 represents unlimited
        :param extras: Extras data:
         partial: using partial function when invoke this command function
        """

        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                await func(*args, **kwargs)

            item = {
                CONFIG.COMMANDER_KEY_PERIOD: period,
                CONFIG.COMMANDER_KEY_TIMES: times
            }

            if CONFIG.COMMANDER_KEY_PARTIAL in extras:
                item[CONFIG.COMMANDER_KEY_HANDLE] = functools.partial(wrapper, *extras["partial"])
            else:
                item[CONFIG.COMMANDER_KEY_HANDLE] = wrapper

            self.__intervals.append(item)

            return wrapper

        return decorator
