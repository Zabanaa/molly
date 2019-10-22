from datetime import datetime
from molly import Molly
from molly.constants import VERSION
from molly.utils import format_datetime
import click
import sys

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.option('--mode', default='basic', type=str)
def scan(target, mode):

    date = datetime.now()
    click.echo(f'Starting Molly (v {VERSION}) at {format_datetime(date)}')

    molly = Molly(target=target, mode=mode)
    try:
        molly.get_ports_to_scan()
    except ValueError as exc:
        error_msg = exc.args[0]
        click.echo(f'[Error]: { error_msg }')
        sys.exit(1)
    
    molly.run_scan()



cli.add_command(scan)

if __name__ == "__main__":
    cli()
