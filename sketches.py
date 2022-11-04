from pathlib import Path

from core.models.airline_history import AirlineHistory

pax = Path('/Users/miguel/Downloads/Flight Data Assignment/passengers.csv')
flights = Path('/Users/miguel/Downloads/Flight Data Assignment/flightData.csv')

airline = AirlineHistory.from_csv(flights, pax)

print(airline.monthly_flights())
print(airline.frequent_flyers(3))
print(airline.longest_run('uk'))
print(airline.most_flown_together(min_=3))


