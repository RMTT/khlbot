from khlbot.khl.APIMetaclass import APIMetaclass
import khlbot.config as CONFIG


class GuildAPI(metaclass=APIMetaclass):
    apis = {
        "list": {
            "url": CONFIG.KHL_API_GUILD_LIST,
            "method": "get",
            "params": {}
        },
        "view": {
            "url": CONFIG.KHL_API_GUILD_VIEW,
            "method": "get",
            "params": {
                "guild_id": True
            }
        },
        "user_list": {
            "url": CONFIG.KHL_API_GUILD_USER_LIST,
            "method": "get",
            "params": {
                "guild_id": True
            }
        },
        "nickname": {
            "url": CONFIG.KHL_API_GUILD_NICKNAME,
            "method": "post",
            "params": {
                "guild_id": True
            }
        },
        "leave": {
            "url": CONFIG.KHL_API_GUILD_LEAVE,
            "method": "post",
            "params": {
                "guild_id": True
            }
        },
        "kickout": {
            "url": CONFIG.KHL_API_GUILD_KICKOUT,
            "method": "post",
            "params": {
                "guild_id": True,
                "target_id": True
            }
        },
        "mute_list": {
            "url": CONFIG.KHL_API_GUILD_MUTE_LIST,
            "method": "get",
            "params": {
                "guild_id": True
            }
        },
        "mute_create": {
            "url": CONFIG.KHL_API_GUILD_MUTE_CREATE,
            "method": "post",
            "params": {
                "guild_id": True,
                "user_id": True,
                "type": True
            }
        },
        "mute_delete": {
            "url": CONFIG.KHL_API_GUILD_MUTE_DELETE,
            "method": "post",
            "params": {
                "guild_id": True,
                "user_id": True,
                "type": True
            }
        }
    }

    @staticmethod
    async def list(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def view(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def user_list(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def nickname(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def leave(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def kickout(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def mute_list(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def mute_create(body, token, success=None, failed=None):
        pass

    @staticmethod
    async def mute_delete(body, token, success=None, failed=None):
        pass
