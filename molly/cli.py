from molly import Molly
from molly.constants import ALLOWED_MODES
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

    molly = Molly(target=target, mode=mode, workers=workers)

    try:
        molly.get_ports_to_scan()
    except ValueError as exc:
        error_msg = exc.args[0]
        sys.exit(f'[Error]: { error_msg }')
    
    molly.run_scan()


cli.add_command(scan)

if __name__ == "__main__":
    cli()
