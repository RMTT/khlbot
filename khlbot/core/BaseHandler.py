import functools
import multiprocessing
import khlbot.config as CONFIG
from khlbot.khl.Event import Event
from khlbot.core.Handler import Handler
from khlbot.core.Logger import Logger


class BaseHandler(Handler):
    """
    A simple but good enough implementation for Handler.
    For detail, see khlbot.core.Handler
    """

    def __init__(self, timeout, queue: multiprocessing.Queue):
        """
        :param queue: Event Queue
        """
        super().__init__(timeout, queue)

    async def handle_command(self, text: str, event, **kwargs) -> None:
        """
        Parse commands and its parameters
        :param text: The text contains commands and its parameters
        :param event: KHL Event object
        :param kwargs: extra data
        :return: None
        """
        if len(self.get_commands()) == 0:
            return

        for commands in self.get_commands():
            for command in commands:
                pos = text.find(command)

                if pos != -1:
                    params = []
                    for _ in range(commands[command][CONFIG.COMMANDER_KEY_PARAM_NUMBER]):
                        next_space = text.find(' ', pos + len(command) + 1)
                        if next_space != -1:
                            params.append(text[pos + len(command) + 1:next_space])
                        else:
                            params.append(text[pos + len(command) + 1:])

                        if len(params[-1]) == 0:
                            params = []
                            break

                        pos = next_space + 1

                    if len(params) == commands[command][CONFIG.COMMANDER_KEY_PARAM_NUMBER]:
                        func = commands[command][CONFIG.COMMANDER_KEY_HANDLE]
                        kwargs[CONFIG.BOT_KEY_EVENT] = event
                        try:
                            await func(*params, **kwargs)
                        except Exception as err:
                            if isinstance(func, functools.partial):
                                func_name = func.func.__name__
                            else:
                                func_name = func.__name__

                            Logger.warning(
                                f"command [{command}] and it's handle function [{func_name}] raise some error")
                            Logger.error(err)
                        break

    async def handle_subscribe(self, _type, condition: dict, handle, event: Event) -> None:
        """
        Handle subscribe events
        :param _type: KHL Event type
        :param condition: Conditions to filter event
        :param handle: Handle function
        :param event: Event Object
        :return: None
        """
        can_run = True

        if condition is not None:
            for item in condition:
                keys = str(item).strip().split('.')
                step = None
                for key in keys:
                    if step is None:
                        step = condition[key]
                    else:
                        step = step[key]
                if step != condition[item]:
                    can_run = False
                    break

        if can_run:
            kwargs = {
                CONFIG.COMMANDER_KEY_EVENT: event
            }
            try:
                await handle(**kwargs)
            except Exception as err:
                if isinstance(handle, functools.partial):
                    func_name = handle.func.__name__
                else:
                    func_name = handle.__name__

                Logger.warning(f"subscribe event function [{func_name}] raises an error")
                Logger.error(err)

    async def handle(self, item) -> None:
        """
        Same as Handler.handle
        """
        if item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_EVENT:
            try:
                item = item[CONFIG.BOT_KEY_MESSAGE_DATA]
                event = Event(item)

                if event.type == CONFIG.KHL_MSG_TEXT:
                    await self.handle_command(item["content"], event=event)
                elif event.type == CONFIG.KHL_MSG_SYSTEM:
                    system_event_type = event.extra.type
                    _subscribes = self.get_subscribes()
                    if system_event_type is not None and system_event_type in _subscribes:
                        for item in _subscribes[system_event_type]:
                            await self.handle_subscribe(_type=system_event_type,
                                                        condition=item[CONFIG.COMMANDER_KEY_CONDITIONS],
                                                        handle=item[CONFIG.COMMANDER_KEY_HANDLE],
                                                        event=event)
            except ValueError as err:
                Logger.warning("Please check commands configuration")
                Logger.error(err)

        elif item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_INTERVAL:
            try:
                await item[CONFIG.COMMANDER_KEY_HANDLE]()
            except Exception as err:
                func = item[CONFIG.COMMANDER_KEY_HANDLE]
                if isinstance(func, functools.partial):
                    func_name = func.func.__name__
                else:
                    func_name = func.__name__

                Logger.warning(f"interval function [{func_name}] raises an error")
                Logger.error(err)
