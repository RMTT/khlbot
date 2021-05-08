import multiprocessing
import khlbot.config as CONFIG

from khlbot.config import *
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

    async def handle_command(self, text: str, **kwargs) -> None:
        """
        Parse commands and its parameters
        :param text: The text contains commands and its parameters
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

                        await func(*params, **kwargs)
                        break

    async def handle(self, item) -> None:
        """
        Same as Handler.handle
        """
        if item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_COMMAND:
            item = item[CONFIG.BOT_KEY_MESSAGE_DATA]
            await self.handle_command(item["content"], target_id=item["target_id"], extra=item["extra"])
        elif item[CONFIG.BOT_KEY_MESSAGE_TYPE] == CONFIG.BOT_MESSAGE_TYPE_INTERVAL:
            await item[CONFIG.COMMANDER_KEY_HANDLE]()
