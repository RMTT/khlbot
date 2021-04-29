import logging

KHL_API_BASEURL = "https://www.kaiheila.cn/api"

KHL_API_GATEWAY = "/v3/gateway/index"
KHL_API_CREATE_MSG = "/v3/message/create"

LOGGING_FILE_LEVEL = logging.WARNING
LOGGING_CONSOLE_LEVEL = logging.INFO

# 以下是开黑啦消息类型常量
KHL_MSG_TEXT = 1
KHL_MSG_CARD = 10
KHL_MSG_MARKDOWN = 9
