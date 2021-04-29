import asyncio
from khlbot.config import *
from khlbot.core.Handler import Handler
from khlbot.core.Commander import Commander


class BaseHandler(Handler):
    """
    处理各类消息的class
    """

    def __init__(self, queue: asyncio.Queue):
        """
        :param queue: 获取消息的队列
        """
        super().__init__(queue)

    async def handle_command(self, text: str, **kwargs) -> None:
        """
        解析各种命令和其参数
        :param text: 包含命令和参数的文本
        :param kwargs: 包含一些在处理各种命令时可能用到的信息，一般都需要包含target_id
        :return: None
        """
        if len(self.get_commands()) == 0:
            return

        for commands in self.get_commands():
            for command in commands:
                pos = text.find(command)

                if pos != -1:
                    params = []
                    for _ in range(commands[command][Commander.KEY_PARAM_NUMBER]):
                        next_space = text.find(' ', pos + len(command) + 1)
                        if next_space != -1:
                            params.append(text[pos + len(command) + 1:next_space])
                        else:
                            params.append(text[pos + len(command) + 1:])

                        if len(params[-1]) == 0:
                            params = []
                            break

                        pos = next_space + 1

                    if len(params) == commands[command][Commander.KEY_PARAM_NUMBER]:
                        func = commands[command][Commander.KEY_HANDLE]

                        await func(*params, **kwargs)
                        break

    async def handle(self, item):
        if item["type"] == KHL_MSG_TEXT and item["channel_type"] == "GROUP":
            await self.handle_command(item["content"], target_id=item["target_id"], extra=item["extra"])
