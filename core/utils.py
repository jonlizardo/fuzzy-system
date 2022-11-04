import datetime as dt
import re
from collections import defaultdict
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List
from typing import Union

from core.exceptions import PrinterDataTypeError


def camel_to_snake(s: str) -> str:
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    return pattern.sub('_', s).lower()


class CSVReader:
    def __init__(self, separator: str = ','):
        self.separator = separator

    def _read(self, path: Path) -> Iterator[List[Any]]:
        with open(path) as csv:
            for row in csv:
                row = row.replace('\n', '')
                yield row.split(self.separator)

    @staticmethod
    def _read_as_record(reader: Iterator[List[Any]]):
        headers = next(reader)
        for row in reader:
            yield dict(zip(headers, row))

    def read(self, path: Path, as_records: bool = True):
        reader = self._read(path)
        if as_records:
            yield from self._read_as_record(reader)
        else:
            yield from reader

    def read_group_by(
        self,
        path: Path,
        key: str,
    ) -> Dict[Any, List[Dict[str, Any]]]:
        """Reads CSV and returns all records grouped by a given key"""
        grouped_by = defaultdict(list)
        for record in self.read(path, as_records=True):
            grouped_by[record[key]].append(record)
        return grouped_by


class DateFilter:
    def __init__(self, start: dt.date, end: dt.date):
        self.start = min(start, end)
        self.end = max(start, end)

    def check(self, d: dt.date) -> bool:
        return self.start <= d <= self.end

    def __repr__(self):
        return f'{self.start} - {self.end}'

    @classmethod
    def from_str(cls, start_str: str, end_str: str, format_: str = '%Y-%m-%d'):
        return cls(
            dt.datetime.strptime(start_str, format_).date(),
            dt.datetime.strptime(end_str, format_).date(),
        )

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end


def printer(data: Union[List, Dict]):
    if isinstance(data, list):
        for i in data:
            print(i)
    elif isinstance(data, dict):
        print(data)
    else:
        raise PrinterDataTypeError(data)
