import abc
import datetime
from typing import Optional, Union, Type

from starlette.requests import Request, HTTPConnection
from starlette.responses import Response
from starlette.types import Message

from starlette_context.request_strategies import *
from starlette_context.response_strategies import *
from starlette_context.header_keys import HeaderKeys


class Plugin(metaclass=abc.ABCMeta):
    """
    Base class for building those plugins to extract things from request.
    One plugins should be responsible for extracting one thing.

    key: the key that allows to access value in headers
    """

    key: str = None
    enrich_resp_strategy_cls: Type[
        EnrichResponseStrategy
    ] = NoEnrichResponseStrategy
    process_request_strategy_cls: Type[
        ProcessRequestStrategy
    ] = BasicProcessRequestStrategy

    async def process_request(
        self, request: Union[Request, HTTPConnection]
    ) -> Union[str, int, dict]:
        process_request_strategy = self.process_request_strategy_cls(self.key)
        return await process_request_strategy.process_request(request)

    async def enrich_response(self, arg: Union[Response, Message]) -> None:
        enrich_response_strategy = self.enrich_resp_strategy_cls(self.key)
        await enrich_response_strategy.enrich_response(arg)


class CorrelationIdPlugin(Plugin):
    key = HeaderKeys.correlation_id
    process_request_strategy_cls = UUIDProcessRequestStrategy
    enrich_resp_strategy_cls = EnrichResponseStrategy


class DateHeaderPlugin(Plugin):
    key = HeaderKeys.date

    @staticmethod
    def rfc1123_to_dt(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S")

    async def extract_value_from_header_by_key(
        self, request: Union[Request, HTTPConnection]
    ) -> Optional[datetime.datetime]:
        """
        Has to be as stated in rfc2616 which uses rfc1123.
        Has to be in GMT.
        Returns UTC datetime.

        Examples allowed:
            Wed, 01 Jan 2020 04:27:12 GMT
            Wed, 01 Jan 2020 04:27:12
        """
        rfc1123 = request.headers.get(self.key)
        if not rfc1123:
            value = None
        else:
            dt_str, dt_data = rfc1123[:25], rfc1123[25:]

            if dt_data.strip() not in ("", "GMT"):  # empty str assumes ok
                raise ValueError(
                    "Date header in wrong format, has to match rfc1123."
                )

            value = self.rfc1123_to_dt(dt_str.strip())

        return value


class ForwardedForPlugin(Plugin):
    key = HeaderKeys.forwarded_for


class RequestIdPlugin(Plugin):
    key = HeaderKeys.request_id
    process_request_strategy_cls = UUIDProcessRequestStrategy
    enrich_resp_strategy_cls = EnrichResponseStrategy


class UserAgentPlugin(Plugin):
    key = HeaderKeys.user_agent
