import click
import sys
import socket
from .utils import is_ip_v4
from .constants import FIRST_1000_PORTS, ALL_PORTS, COMMON_PORTS


class Molly():

    def __init__(self, target):
        self.target = self._parse_target(target)
        self.open_ports = []

    def basic_scan(self):
        click.echo('Scanning ports 1 to 1023')
        self._scan(FIRST_1000_PORTS)
        self._send_report()

    def full_scan(self):
        click.echo('perfoming a full port scan ...')

    def custom_scan(self):
        value = click.prompt('Please select a range of ports (separated by a comma)', type=str)
        print(value)

    def common_scan(self):
        click.echo('scanning most common ports ...')

    def _parse_target(self, target):

        if is_ip_v4(target):
            return target
        else:
            return socket.gethostbyname(target)
    
    def _connect(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(.5)
        try: 
            result = s.connect_ex((self.target, port))
        except KeyboardInterrupt:
            click.echo('\nExiting ...')
            self._send_report()
            sys.exit(1)
        else:
            return result

    def _scan(self, start, end=None):

        if end == None:
            end = start
            start = 1

        for port in range(start, end):
            if self._connect(port) != 0:
                click.echo(f'port {port} is closed')
            else:
                click.echo(f'port {port} is open')
                self.open_ports.append(str(port))

    def _send_report(self):
        click.echo('\nReport')
        click.echo('-' * 50)
        if len(self.open_ports) == 0:
            click.echo('This scan did not find any open ports')
        else:
            click.echo('Open ports: ')
            click.echo(' '.join(self.open_ports))