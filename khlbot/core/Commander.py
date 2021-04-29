import functools


class Commander:
    KEY_PARAM_NUMBER = "param_number"
    KEY_HANDLE = "handle"
    KEY_PARTIAL = "partial"

    def __init__(self, prefix: str = ''):
        self.__prefix = prefix
        self.__commands = {}

    def get_commands(self):
        return self.__commands

    def command(self, command, *params, **extras):
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
