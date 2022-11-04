from typing import Any, Dict

from core import utils


class Passenger:
    def __init__(
            self,
            passenger_id: str,
            first_name: str,
            last_name: str,
    ):
        self.passenger_id = passenger_id
        self.first_name = first_name
        self.last_name = last_name

    @classmethod
    def from_csv_record(cls, record: Dict[str, Any]):
        pax = {utils.camel_to_snake(k): v for k, v in record.items()}
        return cls(**pax)

    def __repr__(self):
        return f'({self.passenger_id}): {self.first_name} {self.last_name}'

    def to_dict(self) -> Dict[str, Any]:
        return {
            'Passenger ID': self.passenger_id,
            'First name': self.first_name,
            'Last name': self.last_name
        }
