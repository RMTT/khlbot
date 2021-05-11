import logging

KHL_API_BASEURL = "https://www.kaiheila.cn/api"

KHL_API_GATEWAY = "/v3/gateway/index"

KHL_API_CHANNEL_MESSAGE_CREATE = KHL_API_BASEURL + "/v3/message/create"
KHL_API_CHANNEL_MESSAGE_UPDATE = KHL_API_BASEURL + "/v3/message/update"
KHL_API_CHANNEL_MESSAGE_LIST = KHL_API_BASEURL + "/v3/message/list"
KHL_API_CHANNEL_MESSAGE_DELETE = KHL_API_BASEURL + "/v3/message/delete"
KHL_API_CHANNEL_MESSAGE_REACTION_LIST = KHL_API_BASEURL + "/v3/message/reaction-list"
KHL_API_CHANNEL_MESSAGE_ADD_REACTION = KHL_API_BASEURL + "/v3/message/add-reaction"
KHL_API_CHANNEL_MESSAGE_DELETE_REACTION = KHL_API_BASEURL + "/v3/message/delete-reaction"
KHL_API_GUILD_LIST = KHL_API_BASEURL + "/v3/guild/list"
KHL_API_GUILD_VIEW = KHL_API_BASEURL + "/v3/guild/view"
KHL_API_GUILD_USER_LIST = KHL_API_BASEURL + "/v3/guild/user-list"
KHL_API_GUILD_NICKNAME = KHL_API_BASEURL + "/v3/guild/nickname"
KHL_API_GUILD_LEAVE = KHL_API_BASEURL + "/v3/guild/leave"
KHL_API_GUILD_KICKOUT = KHL_API_BASEURL + "/v3/guild/kickout"
KHL_API_GUILD_MUTE_LIST = KHL_API_BASEURL + "/v3/guild-mute/list"
KHL_API_GUILD_MUTE_CREATE = KHL_API_BASEURL + "/v3/guild-mute/create"
KHL_API_GUILD_MUTE_DELETE = KHL_API_BASEURL + "/v3/guild-mute/delete"

LOGGING_FILE_LEVEL = logging.INFO
LOGGING_CONSOLE_LEVEL = logging.INFO
LOGGING_FILE_DIR = "./log/"

# configurable items for bot
MAX_PROCESSING_NUMBER = "MAX_PROCESSING_NUMBER"
MAX_CONSUMER_NUMBER = "MAX_CONSUMER_NUMBER"
MAX_EVENT_QUEUE_SIZE = "MAX_EVENT_QUEUE_SIZE"
PROCESSING_IDLE_TIMEOUT = "PROCESSING_IDLE_TIMEOUT"

# keys for bot
BOT_MESSAGE_TYPE_INTERVAL = 0
BOT_MESSAGE_TYPE_EVENT = 1

BOT_KEY_MESSAGE_TYPE = "type"
BOT_KEY_MESSAGE_DATA = "data"
BOT_KEY_EVENT = "event"
BOT_KEY_EVENT_FILTER = "event_filter"

# keys for commander
COMMANDER_KEY_PARAM_NUMBER = "param_number"
COMMANDER_KEY_HANDLE = "handle"
COMMANDER_KEY_PARTIAL = "partial"
COMMANDER_KEY_PERIOD = "period"
COMMANDER_KEY_TIMES = "times"
COMMANDER_KEY_CONDITIONS = "conditions"
COMMANDER_KEY_EVENT_TYPE = "event_type"
COMMANDER_KEY_EVENT = "event"

# khl message type
KHL_MSG_TEXT = 1
KHL_MSG_CARD = 10
KHL_MSG_MARKDOWN = 9
KHL_MSG_SYSTEM = 255

# khl channel type
KHL_CHANNEL_TYPE_GROUP = 0
KHL_CHANNEL_TYPE_PERSON = 1

# khl event key
KHL_EVENT_KEY_CHANNEL_TYPE = "channel_type"
KHL_EVENT_KEY_TARGET_ID = "target_id"
KHL_EVENT_KEY_AUTHOR_ID = "author_id"
KHL_EVENT_KEY_CONTENT = "content"
KHL_EVENT_KEY_MSG_ID = "msg_id"
KHL_EVENT_KEY_MSG_TIMESTAMP = "msg_timestamp"
KHL_EVENT_KEY_NONCE = "nonce"
KHL_EVENT_KEY_EXTRA = "extra"
KHL_EVENT_KEY_TYPE = "type"
KHL_EVENT_KEY_BODY = "body"
KHL_EVENT_KEY_GUILD_ID = "guild_id"
KHL_EVENT_KEY_CHANNEL_NAME = "channel_name"
KHL_EVENT_KEY_MENTION = "mention"
KHL_EVENT_KEY_MENTION_ALL = "mention_all"
KHL_EVENT_KEY_MENTION_ROLES = "mention_roles"
KHL_EVENT_KEY_MENTION_HERE = "mention_here"
KHL_EVENT_KEY_AUTHOR = "author"

# khl event type
KHL_EVENT_TYPE_JOINED_GUILD = "joined_guild"
KHL_EVENT_TYPE_EXITED_GUILD = "exited_guild"
KHL_EVENT_TYPE_UPDATED_GUILD_MEMBER = "updated_guild_member"
KHL_EVENT_TYPE_GUILD_MEMBER_ONLINE = "guild_member_online"
KHL_EVENT_TYPE_GUILD_MEMBER_OFFLINE = "guild_member_offline"
