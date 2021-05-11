import functools

from khlbot.khl.utils import post_json_to_khl_api, get_from_khl_api


class APIMetaclass(type):
    KEY_API = "apis"
    KEY_URL = "url"
    KEY_PARAMS = "params"
    KEY_METHOD = "method"
    KEY_METHOD_POST = "post"
    KEY_METHOD_GET = "get"
    KEY_PARAMS_name = "name"
    KEY_PARAMS_REQUIRE = "require"

    def __new__(cls, name, bases, attrs):
        if APIMetaclass.KEY_API not in attrs:
            raise ValueError(f"API class must have '{APIMetaclass.KEY_API}' attribute")

        if not isinstance(attrs[APIMetaclass.KEY_API], dict):
            raise ValueError(f"{APIMetaclass.KEY_API} attribute must be a dict")

        return type.__new__(cls, name, bases, attrs)

    @staticmethod
    def request(url: str, params: dict, method: str):
        async def wrapper(body, token, success=None, failed=None):
            for param in params:
                if params[param] and param not in body:
                    raise ValueError(f"request body must contains {param}")

            if method == APIMetaclass.KEY_METHOD_POST:
                return await post_json_to_khl_api(url, body, token, success, failed)
            elif method == APIMetaclass.KEY_METHOD_GET:
                return await get_from_khl_api(url, body, token, success, failed)

        return wrapper

    def __getattribute__(cls, item):
        apis = object.__getattribute__(cls, APIMetaclass.KEY_API)
        print(item)
        if item in apis:
            desc = apis[item]
            url = desc[APIMetaclass.KEY_URL]
            params = desc[APIMetaclass.KEY_PARAMS]
            method = desc[APIMetaclass.KEY_METHOD]

            func = APIMetaclass.request(url, params, method)
            return func
        else:
            return object.__getattribute__(cls, item)
