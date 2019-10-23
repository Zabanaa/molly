from datetime import datetime
from molly import Molly
from molly.constants import VERSION, ALLOWED_MODES
from molly.utils import format_datetime
import click
import sys

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.option(
                '--mode', 
                default='basic', 
                type=click.Choice(
                    ALLOWED_MODES,
                    case_sensitive=False
                )
            )
@click.option('--workers', default=100, type=int)
def scan(target, mode, workers):

    date = datetime.now()
    click.echo(f'Starting Molly (v {VERSION}) at {format_datetime(date)}')

    molly = Molly(target=target, mode=mode, workers=workers)

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
