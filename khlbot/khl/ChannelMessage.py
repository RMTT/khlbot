import khlbot.config as CONFIG
import aiohttp


class ChannelMessage:

    @staticmethod
    async def create(body: dict, token: str, success=None, failed=None) -> {None, dict}:
        """
        Create a message to channel
        :param body: Request body
        :param token: KHL bot token
        :param success: callback when success create message
        :param failed: callback when failed to create message
        :return: None if failed, json response if  success
        """
        _type = 1
        if "type" in body:
            _type = body["type"]

        if "target_id" not in body:
            raise ValueError("must set target_id!")

        if "content" not in body:
            raise ValueError("must set content!")

        payload = {
            "type": _type,
            "target_id": body["target_id"],
            "content": body["content"]
        }

        if "quote" in body:
            payload["quote"] = body["quote"]

        if "nonce" in body:
            payload["nonce"] = body["nonce"]

        if "temp_target_id" in body:
            payload["temp_target_id"] = body["temp_target_id"]

        headers = {
            "Authorization": f"Bot {token}"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(CONFIG.KHL_API_CHANNEL_MESSAGE_CREATE, json=payload,
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

    @staticmethod
    async def update(body: dict, token, success=None, failed=None) -> {None, dict}:
        """
         Update a message of channel
         :param body: Request body
         :param token: KHL bot token
         :param success: callback when success update message
         :param failed: callback when failed to update message
         :return: None if failed, json response if  success
        """
        if "msg_id" not in body:
            raise ValueError("must set msg_id!")

        if "content" not in body:
            raise ValueError("must set content!")

        payload = {
            "content": body["content"],
            "msg_id": body["msg_id"],
        }

        if "quote" in body:
            payload["quote"] = body["quote"]

        if "temp_target_id" in body:
            payload["temp_target_id"] = body["temp_target_id"]

        headers = {
            "Authorization": f"Bot {token}"
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(CONFIG.KHL_API_CHANNEL_MESSAGE_UPDATE, json=payload,
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
