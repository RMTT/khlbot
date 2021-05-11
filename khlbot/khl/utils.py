import aiohttp
from khlbot.core.Logger import Logger


async def post_json_to_khl_api(url, body, token, success=None, failed=None):
    headers = {
        "Authorization": f"Bot {token}"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, json=body,
                                    headers=headers) as response:
                json_rep = await response.json()

                if response.status == 200 and json_rep["code"] == 0:
                    if success is not None:
                        success(json_rep)
                else:
                    if failed is not None:
                        failed(json_rep)

                return json_rep
        except Exception as e:
            failed({
                "code": -1,
                "message": str(e)
            })


async def get_from_khl_api(url, body, token, success=None, failed=None):
    headers = {
        "Authorization": f"Bot {token}"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url, params=body,
                                   headers=headers) as response:
                json_rep = await response.json()

                if response.status == 200 and json_rep["code"] == 0:
                    if success is not None:
                        success(json_rep)
                else:
                    if failed is not None:
                        failed(json_rep)

                return json_rep
        except Exception as e:
            Logger.error(e)
            if failed is not None:
                failed({
                    "code": -1,
                    "message": str(e)
                })
