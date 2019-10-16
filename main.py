import click
import socket

def parse_target(target):

    if is_ip_v4(target):
        return target
    else:
        return socket.gethostbyname(target)

def is_ip_v4(target):
    try:
        ip = ip_address(target)
    except:
        return False
    else:
        return True

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target')
@click.option('--basic', is_flag=True, default=False)
@click.option('--full-scan', is_flag=True, default=False)
@click.option('--range', is_flag=True)
def scan(target, basic, full_scan, range):
    ip = parse_target(target)
    click.echo(f'requesting info for { ip }')
    if basic:
        click.echo('scanning ports 1 to 1024 ...')
    if full_scan:
        click.echo('perfoming a full port scan ...')
    if range:
        value = click.prompt('Please select a range of ports (separated by a comma)', type=str)
        print(value)

cli.add_command(scan)

if __name__ == "__main__":
    cli()














# # this is the test file for now
# from ipaddress import ip_address
# import socket 
# import sys


# if __name__ == "__main__":
#     # Step 1: translate the domain or if it's an ip use that instead

#     if is_ip_v4(sys.argv[1]):
#         target = sys.argv[1]
#     else:
#         target = socket.gethostbyname(sys.argv[1])

#     try:
#         port = int(sys.argv[2])
#     except ValueError:
#         print("Error: The port should be an integer")
#         sys.exit(1)

#     print(target, port)


