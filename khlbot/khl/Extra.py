import khlbot.config as CONFIG
from khlbot.khl.User import User


class Extra:
    def __init__(self, _type: int, body: dict):
        self.__data = body
        self.__type = _type

    @property
    def type(self):
        return self.__type

    @property
    def body(self):
        if self.__type == CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_BODY]
        return None

    @property
    def guild_id(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_GUILD_ID]
        return None

    @property
    def channel_name(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_CHANNEL_NAME]
        return None

    @property
    def mention(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_MENTION]
        return None

    @property
    def mention_all(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_MENTION_ALL]
        return None

    @property
    def mention_roles(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_MENTION_ROLES]
        return None

    @property
    def mention_here(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return self.__data[CONFIG.KHL_EVENT_KEY_MENTION_HERE]
        return None

    @property
    def author(self):
        if self.__type != CONFIG.KHL_MSG_SYSTEM:
            return User(self.__data[CONFIG.KHL_EVENT_KEY_AUTHOR])
        return None
