from khlbot.core.Bot import Bot
from khlbot.core.Commander import Commander
from khlbot.common import create_msg_to_channel

commander = Commander(prefix="-")


@commander.command("hello")
async def hello():
    create_msg_to_channel("Hello", channel_id=12345, _type=0, token="")


bot = Bot(token="")
bot.add_commander(commander)
bot.run()
