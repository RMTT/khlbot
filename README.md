# 开黑啦机器人

## 使用样例

```python

from khlbot.core.Bot import Bot
from khlbot.core.Commander import Commander
from khlbot.common import create_msg_to_channel
from khlbot.config import KHL_MSG_TEXT

commander = Commander(prefix="-")


@commander.command("hello")
async def hello(**kwargs):
    create_msg_to_channel("Hello", channel_id=kwargs["target_id"], _type=KHL_MSG_TEXT, token="")


@commander.interval(period=3, times=3)
async def interval_test(**kwargs):
    create_msg_to_channel("interval", channel_id="", _type=KHL_MSG_TEXT,
                          token="")


config = {
    "MAX_CONSUMER_NUMBER": 4,
    "MAX_PROCESSING_NUMBER": 2
}

bot = Bot(token="", _config=config)
bot.add_commander(commander)
bot.run()
```