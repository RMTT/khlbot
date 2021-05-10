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
        self.__subscribes = {}

    def get_commands(self) -> dict:
        return self.__commands

    def get_intervals(self):
        return self.__intervals

    def get_subscribes(self):
        return self.__subscribes

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
            self.__commands[self.__prefix + command] = {
                CONFIG.COMMANDER_KEY_PARAM_NUMBER: len(params),
                CONFIG.COMMANDER_KEY_HANDLE: func
            }

            if CONFIG.COMMANDER_KEY_PARTIAL in extras:
                self.__commands[self.__prefix + command][CONFIG.COMMANDER_KEY_HANDLE] = \
                    functools.partial(func, *extras["partial"])
                functools.update_wrapper(self.__commands[self.__prefix + command][CONFIG.COMMANDER_KEY_HANDLE], func)
            return func

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
            item = {
                CONFIG.COMMANDER_KEY_PERIOD: period,
                CONFIG.COMMANDER_KEY_TIMES: times
            }

            if CONFIG.COMMANDER_KEY_PARTIAL in extras:
                item[CONFIG.COMMANDER_KEY_HANDLE] = functools.partial(func, *extras["partial"])
                functools.update_wrapper(item[CONFIG.COMMANDER_KEY_HANDLE], func)
            else:
                item[CONFIG.COMMANDER_KEY_HANDLE] = func

            self.__intervals.append(item)

            return func

        return decorator

    def subscribe(self, _type, conditions: dict = None, **extras):
        """
        Decorator for period task
        :param _type: KHL system event tpye
        :param conditions: condition to filter event
        :param extras: Extras data:
         partial: using partial function when invoke this command function
        """

        def decorator(func):
            item = {
                CONFIG.COMMANDER_KEY_CONDITIONS: conditions
            }

            if CONFIG.COMMANDER_KEY_PARTIAL in extras:
                item[CONFIG.COMMANDER_KEY_HANDLE] = functools.partial(func, *extras["partial"])
                functools.update_wrapper(item[CONFIG.COMMANDER_KEY_HANDLE], func)
            else:
                item[CONFIG.COMMANDER_KEY_HANDLE] = func

            if _type not in self.__subscribes:
                self.__subscribes[_type] = []

            self.__subscribes[_type].append(item)

            return func

        return decorator
