from datetime import datetime
from molly import Molly
from molly.constants import ALLOWED_MODES, VERSION
from molly.utils import format_datetime
import click
import sys

@click.group()
def cli():
    r"""

    Molly is a network reconaissance tool. 
    Use it to scan an IP/Host for open ports.
    
    /!\ REMINDER /!\

    Scanning ports against targets for which you don't have EXPLICIT WRITTEN PERMISSION
    from their owners is a may be considered a CRIME depending on your local law. 
    You should only use this tool on your own hosts/IPs 
    or those you have been given permission to scan.
    """
    pass

@cli.command()
@click.argument('target')
@click.option(
                '--mode', 
                default='basic', 
                type=click.Choice(
                    ALLOWED_MODES,
                    case_sensitive=False
                ),
                help="Scan mode"
            )
@click.option('--workers', default=100, type=int, help='How many worker threads to run')
def scan(target, mode, workers):
    """
    Perform a TCP port scan against the specified target.

    Allowed modes are: basic, full, custom and common
    
    basic: the first 1023 reserved ports.

    full: will perform a full scan on all TCP ports.

    common: scan the top 20 most commonly used ports. This includes ssh, ftp, http, https ...

    custom: will prompt you to enter your desired port range (separated by a comma)
    """

    date = datetime.now()
    click.echo(f'Starting Molly (v {VERSION}) at {format_datetime(date)}')

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
