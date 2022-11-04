from typing import List

from core.models.flight import Flight


class FlightShared:
    def __init__(self, pax_1: str, pax_2: str, flights: List[Flight]):
        self.main_pax = min(pax_1, pax_2)
        self.other_pax = max(pax_1, pax_2)
        self.flights = flights
        self.total_shared = len(self.flights)

    def to_dict(self):
        return {
            'Pax 1': self.main_pax,
            'Pax 2': self.other_pax,
            'Total shared': self.total_shared,
            'First flight': min(self.flights),
            'Last flight': max(self.flights)
        }

    def __repr__(self):
        return str(self.to_dict())

    def __eq__(self, other):
        return self.main_pax == other.main_pax \
               and self.other_pax == other.other_pax

    def __hash__(self):
        return hash((self.main_pax, self.other_pax))
