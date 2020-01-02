import datetime
from typing import Optional

from starlette.requests import Request

from starlette_context.header_keys import HeaderKeys
from starlette_context.plugins.plugin import Plugin


class DateHeaderPlugin(Plugin):
    key = HeaderKeys.date

    @staticmethod
    def rfc1123_to_dt(s: str) -> datetime.datetime:
        return datetime.datetime.strptime(s, "%a, %d %b %Y %H:%M:%S")

    def process_request(self, request: Request) -> Optional[datetime.datetime]:
        """
        Has to be as stated in rfc2616 which uses rfc1123.
        Has to be in GMT.
        Returns UTC datetime.

        Examples allowed:
            Wed, 01 Jan 2020 04:27:12 GMT
            Wed, 01 Jan 2020 04:27:12
        """
        rfc1123 = self.get_from_header_by_key(request)
        if not rfc1123:
            self.value = None
        else:
            dt_str, dt_data = rfc1123[:25], rfc1123[25:]

            if dt_data.strip() not in ("", "GMT"):  # empty str assumes ok
                raise ValueError(
                    "Date header in wrong format, has to match rfc1123."
                )

            self.value = self.rfc1123_to_dt(dt_str.strip())

        return self.value
