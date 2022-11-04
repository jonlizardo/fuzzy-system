import datetime as dt

from typing import Dict, List

from core import utils
from core.utils import DateFilter


class Flight:
    def __init__(
            self,
            flight_id: str,
            from_: str,
            to_: str,
            date: dt.date,
            passengers: List[str]
    ):
        self.flight_id = flight_id
        self.from_ = from_
        self.to_ = to_
        self.date = date
        self.passengers = passengers

    def __repr__(self):
        return f'@{self.date}: {self.from_} -> {self.to_}'

    def __lt__(self, other):
        return self.date < other.date

    @classmethod
    def from_csv_records(cls, records: List[Dict[str, str]]):
        reserved = ['to', 'from']
        kwargs = {
            utils.camel_to_snake(k) + ('_' if k in reserved else ''): v
            for k, v
            in records[0].items()
        }
        kwargs['date'] = dt.datetime.strptime(kwargs.pop('date'), '%Y-%m-%d')
        kwargs.pop('passenger_id')
        return cls(
            passengers=[pax.get('passengerId') for pax in records],
            **kwargs,
        )

    def within_range(self, filter_: DateFilter) -> bool:
        return filter_.check(self.date)
