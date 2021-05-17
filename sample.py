from khlbot.core.Bot import Bot
from khlbot.core.Commander import Commander
import khlbot.config as CONFIG
from khlbot.khl.ChannelMessageAPI import ChannelMessageAPI as ChannelMessage

commander = Commander(prefix="-")


# 处理"-hello" 和 "-hello2"
@commander.command("hello", partial=(2,))
@commander.command("hello2", partial=(1,))
async def hello(i, **kwargs):
    event = kwargs["event"]
    payload = {
        "content": "**Hello**",
        "target_id": event.target_id,
        "quote": event.msg_id,
        "type": CONFIG.KHL_MSG_MARKDOWN
    }
    json_rep = await ChannelMessage.create(body=payload, token="")


# 周期任务，间隔3秒，运行3次
@commander.interval(period=3, times=3)
async def interval_test():
    payload = {
        "content": "**Hello**",
        "target_id": "",
        "quote": "",
        "type": CONFIG.KHL_MSG_MARKDOWN
    }
    json_rep = await ChannelMessage.create(body=payload, token="")


# 订阅系统消息，服务器有用户更新信息时将被调用
@commander.subscribe(_type=CONFIG.KHL_EVENT_TYPE_UPDATED_GUILD_MEMBER)
async def online(**kwargs):
    event = kwargs["event"]
    payload = {
        "content": "**Hello**",
        "target_id": "",
        "type": CONFIG.KHL_MSG_MARKDOWN
    }
    json_rep = await ChannelMessage.create(body=payload, token="")


config = {
    "MAX_CONSUMER_NUMBER": 4,
    "MAX_PROCESSING_NUMBER": 2
}

bot = Bot(token="", _config=config)
bot.add_commander(commander)
bot.run()
