import json
import khlbot.config as CONFIG
from khlbot.khl.Extra import Extra


class Event:
    """
    KHL Event message object
    """

    def __init__(self, body: dict):
        self.__data = body
        self.__extra = None

    @property
    def data(self):
        return self.__data

    def __getitem__(self, item):
        if item in self.__data:
            return self.__data[item]

        return None

    def __getattr__(self, item):
        if item in self.__data:
            return self.__data[item]
        return None

    @property
    def channel_type(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_CHANNEL_TYPE]

    @property
    def type(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_TYPE]

    @property
    def target_id(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_TARGET_ID]

    @property
    def author_id(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_AUTHOR_ID]

    @property
    def content(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_CONTENT]

    @property
    def msg_id(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_MSG_ID]

    @property
    def msg_timestamp(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_MSG_TIMESTAMP]

    @property
    def nonce(self):
        return self.__data[CONFIG.KHL_EVENT_KEY_NONCE]

    @property
    def extra(self):
        if self.__extra is None:
            self.__extra = Extra(body=self.__data[CONFIG.KHL_EVENT_KEY_EXTRA])

        return self.__extra

    def is_system_msg(self):
        return self.type == CONFIG.KHL_MSG_SYSTEM
