from datetime import datetime
from molly import Molly
from molly.constants import VERSION
from molly.utils import format_datetime
import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.option('--basic', is_flag=True, default=False)
@click.option('--full-scan', is_flag=True, default=False)
@click.option('--custom', is_flag=True)
def scan(target, basic, full_scan, custom):

    molly = Molly(target)
    date = datetime.now()
    click.echo(f'Starting Molly (v {VERSION}) at {format_datetime(date)}')

    if basic:
        molly.basic_scan()        
    elif full_scan:
        molly.full_scan()
    elif custom:
        molly.custom_scan()
    else:
        molly.common_scan()


cli.add_command(scan)

if __name__ == "__main__":
    cli()
