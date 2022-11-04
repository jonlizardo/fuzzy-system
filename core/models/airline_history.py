from collections import defaultdict, Counter
from pathlib import Path
from typing import Any, Dict, List

from core.models.flight import Flight
from core.models.flight_shared import FlightShared
from core.models.passenger import Passenger
from core.models.passenger_flight import PassengerFlight
from core.utils import CSVReader, DateFilter


class AirlineHistory:
    def __init__(self, flights: List[Flight], passengers: List[Passenger]):
        self.flights = flights
        self.passengers = passengers
        self._flights_by_id = {f.flight_id: f for f in self.flights}
        self.passenger_flights = self._get_flights_by_passenger()

    @staticmethod
    def _get_flights_from_csv(
            reader: CSVReader, path_to_flights: Path
    ) -> List[Flight]:
        flights_data = reader.read_group_by(path_to_flights, 'flightId')
        return [
            Flight.from_csv_records(data) for _, data in flights_data.items()
        ]

    @staticmethod
    def _get_pax_from_csv(
            reader: CSVReader, path_to_passenger: Path
    ) -> List[Passenger]:
        pax_data = reader.read_group_by(path_to_passenger, 'passengerId')
        return [
            Passenger.from_csv_record(p[0]) for _, p in pax_data.items()
        ]

    @classmethod
    def from_csv(cls, path_to_flights: Path, path_to_passenger: Path):
        csv = CSVReader(separator=',')
        passengers = cls._get_pax_from_csv(csv, path_to_passenger)
        flights = cls._get_flights_from_csv(csv, path_to_flights)
        return cls(flights, passengers)

    def _get_flights_by_passenger(self) -> List[PassengerFlight]:
        """Returns a list of PassengerFlights inlcuding all passengers listed
        in the Passenger dataset. Whether they've travelled yet or not."""
        flights_by_pax = defaultdict(list)
        for flight in self.flights:
            for pax in flight.passengers:
                flights_by_pax[pax].append(
                    self._flights_by_id.get(flight.flight_id)
                )
        return [
            PassengerFlight(pax, flights=flights_by_pax.get(pax.passenger_id))
            for pax
            in self.passengers
        ]

    def monthly_flights(self):
        counter = Counter()
        for pax in self.passenger_flights:
            counter += pax.monthly_flights()
        return [
            {'Month': k, 'Number of flights': v} for k, v in counter.items()
        ]

    def frequent_flyers(self, top: int) -> List[PassengerFlight]:
        flyers = sorted(self.passenger_flights, reverse=True)
        return flyers[:top]

    def longest_run(self, to_exclude: List[str]):
        all_runs = {
            pax.passenger.passenger_id: pax.countries_visited(to_exclude)
            for pax
            in self.passenger_flights
        }
        longest = max(all_runs.values())
        longest_run_pax = {k: v for k, v in all_runs.items() if v == longest}
        return longest_run_pax

    def _sharers(self, filter_: DateFilter = None) -> List[FlightShared]:
        shares = []
        for pax in self.passenger_flights:
            shares += [
                FlightShared(pax.passenger.passenger_id, other, flights)
                for other, flights
                in pax.shared_with(filter_).items()
            ]
        return shares

    def most_flown_together(
            self, min_: int, filter_: DateFilter = None, top: int = 5
    ) -> List:
        results = [
            s.to_dict()
            for s
            in set(self._sharers(filter_))
            if s.total_shared > min_
        ]
        results.sort(key=lambda r: r.get('Total shared'), reverse=True)
        return results[:top]
