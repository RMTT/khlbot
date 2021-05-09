import multiprocessing
import khlbot.config as CONFIG
from khlbot.khl.Event import Event
from khlbot.core.Handler import Handler


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
                        await func(*params, **kwargs)
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

            await handle(**kwargs)

    async def handle(self, item) -> None:
        """
        Same as Handler.handle
        """
        if item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_EVENT:
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

        elif item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_INTERVAL:
            await item[CONFIG.COMMANDER_KEY_HANDLE]()
