from pathlib import Path

import click

from core import utils
from core.models.airline_history import AirlineHistory
from core.utils import DateFilter


@click.group()
@click.option('-p', '--path', type=click.Path())
@click.pass_context
def quantexa(ctx, path):
    folder = Path(path)
    path_to_flights = folder / 'flightData.csv'
    path_to_passengers = folder / 'passengers.csv'
    airline = AirlineHistory.from_csv(
        path_to_flights=path_to_flights,
        path_to_passenger=path_to_passengers,
    )
    ctx.obj = airline


@quantexa.command()
@click.pass_obj
def monthly_flights(airline):
    utils.printer(airline.monthly_flights())


@quantexa.command()
@click.option('-t', '--top', type=int, default=10)
@click.pass_obj
def frequent_flyers(airline, top):
    utils.printer(airline.monthly_flights(top))


@quantexa.command()
@click.option('-x', '--exclude', type=str, multiple=True)
@click.pass_obj
def longest_run(airline, exclude):
    utils.printer(airline.longest_run(to_exclude=exclude))


@quantexa.command()
@click.option('-m', '--min-shared', type=int, default=1)
@click.option('-d', '--dates', type=(str, str))
@click.option('-t', '--top', type=int, default=10)
@click.pass_obj
def most_flown_together(airline, min_shared, dates, top):
    filter_ = DateFilter.from_str(*dates) if dates else None
    utils.printer(airline.most_flown_together(min_shared, filter_, top))
