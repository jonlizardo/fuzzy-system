from collections import defaultdict
from typing import Dict
from typing import List

from core.models.flight import Flight
from core.models.passenger import Passenger
from core.utils import DateFilter


class PassengerFlight:
    def __init__(self, passenger: Passenger, flights: List[Flight] = None):
        self.passenger = passenger
        self.flights = flights or []
        self.visits_by_country = self._get_country_visits()
        self.total_flights = sum(self._get_country_visits().values())

    def _get_country_visits(self):
        count = defaultdict(int)
        for flight in self.flights:
            count[flight.to_] += 1
        return count

    def monthly_flights(self) -> Dict[str, int]:
        monthly_flights = defaultdict(int)
        for flight in self.flights:
            monthly_flights[flight.date.strftime('%Y-%m')] += 1
        return monthly_flights

    def to_dict(self):
        return {
            **self.passenger.to_dict(),
            'Number of flights': self.total_flights,
        }

    def countries_visited(self, exclude: List[str]) -> int:
        exclude_ = exclude or []
        return len([c for c in self.visits_by_country if c not in exclude_])

    def shared_with(
            self, filter_: DateFilter = None,
    ) -> Dict[str, List[Flight]]:
        if filter_ is not None:
            flights = filter(lambda f: f.within_range(filter_), self.flights)
        else:
            flights = self.flights

        sharing_with = defaultdict(list)
        for flight in flights:
            for pax in flight.passengers:
                if pax == self.passenger.passenger_id:
                    continue
                sharing_with[pax].append(flight)
        return sharing_with

    def __lt__(self, other):
        return self.total_flights < other.total_flights

    def __repr__(self):
        return str(self.to_dict())
