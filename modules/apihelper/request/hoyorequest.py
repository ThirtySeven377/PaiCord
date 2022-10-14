from typing import Union

import httpx

from modules.apihelper.error import NetworkException, ResponseException, TimedOut
from modules.apihelper.request.httpxrequest import HTTPXRequest
from modules.apihelper.typedefs import POST_DATA, JSON_DATA


class HOYORequest(HTTPXRequest):
    async def get(
        self, url: str, *args, de_json: bool = True, re_json_data: bool = False, **kwargs
    ) -> Union[POST_DATA, JSON_DATA, bytes]:
        try:
            response = await self._client.get(url=url, *args, **kwargs)
        except httpx.TimeoutException as err:
            raise TimedOut from err
        except httpx.HTTPError as exc:
            raise NetworkException(f"Unknown error in HTTP implementation: {repr(exc)}") from exc
        if response.is_error:
            raise ResponseException(message=f"response error in status code: {response.status_code}")
        if not de_json:
            return response.content
        json_data = response.json()
        return_code = json_data.get("retcode", None)
        data = json_data.get("data", None)
        message = json_data.get("message", None)
        if return_code is None:
            return json_data
        if return_code != 0:
            if message is None:
                raise ResponseException(message=f"response error in return code: {return_code}")
            else:
                raise ResponseException(response=json_data)
        if not re_json_data and data is not None:
            return data
        return json_data