import functools


class Commander:
    """
    Class for configure and save concrete task, for example, the "-hello" command,
     when bot find a message which contains "-hello", it will using the functions saved in
     commander to handle this event
    """
    KEY_PARAM_NUMBER = "param_number"
    KEY_HANDLE = "handle"
    KEY_PARTIAL = "partial"

    def __init__(self, prefix: str = ''):
        """
        :param prefix: The prefix of commands
        """
        self.__prefix = prefix
        self.__commands = {}

    def get_commands(self) -> dict:
        return self.__commands

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
                Commander.KEY_PARAM_NUMBER: len(params),
                Commander.KEY_HANDLE: wrapper
            }

            if Commander.KEY_PARTIAL in extras:
                self.__commands[self.__prefix + command][Commander.KEY_HANDLE] = functools.partial(wrapper,
                                                                                                   *extras["partial"])
            return wrapper

        return decorator
