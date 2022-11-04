import click

from cli.commands import quantexa


@click.group()
def interpreter():
    pass


interpreter.add_command(quantexa)
