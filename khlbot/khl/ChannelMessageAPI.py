import khlbot.config as CONFIG
from khlbot.khl.APIMetaclass import APIMetaclass


class ChannelMessageAPI(metaclass=APIMetaclass):
    apis = {
        "create": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_CREATE,
            "method": "post",
            "params": {
                "target_id": True,
                "content": True
            }
        },
        "update": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_UPDATE,
            "method": "post",
            "params": {
                "msg_id": True,
                "content": True
            }
        },
        "list": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_LIST,
            "method": "get",
            "params": {
                "target_id": True
            }
        },
        "delete": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_DELETE,
            "method": "post",
            "params": {
                "msg_id": True
            }
        },
        "reaction_list": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_REACTION_LIST,
            "method": "get",
            "params": {
                "msg_id": True,
                "emoji": True
            }
        },
        "add_reaction": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_ADD_REACTION,
            "method": "post",
            "params": {
                "msg_id": True,
                "emoji": True
            }
        },
        "delete_reaction": {
            "url": CONFIG.KHL_API_CHANNEL_MESSAGE_DELETE_REACTION,
            "method": "post",
            "params": {
                "msg_id": True,
                "emoji": True
            }
        }
    }

    @staticmethod
    async def create(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def update(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def list(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def delete(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def reaction_list(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def add_reaction(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def delete_reaction(body, token, success=None, failed=None):
        pass
