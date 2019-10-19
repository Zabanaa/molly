import click
import time
import sys
import socket
from .utils import is_ip_v4
from .constants import FIRST_1000_PORTS, ALL_PORTS, COMMON_PORTS


class Molly():

    def __init__(self, target):
        self.hostname = target 
        self.target = self._parse_target(target)
        self.open_ports = []
        self.closed_ports = []
        self.start_time = time.time()

    def basic_scan(self):
        click.echo('Scanning ports 1 to 1023 ...')
        self._scan(FIRST_1000_PORTS)

    def full_scan(self):
        click.echo('Perfoming a full port scan ...')
        self._scan(ALL_PORTS)

    def custom_scan(self):
        ports = click.prompt('Please select a range of ports (separated by a comma)', type=str)
        try:
            start, end = self._get_custom_port_range(ports)
        except ValueError as e:
            click.echo(str(e))
            sys.exit(1)
        else:
            self._scan(start, end)

    def common_scan(self):
        click.echo('Scanning top 20 ports ...')
        for port in COMMON_PORTS:
            self._connect(port)
        self._send_report()

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
            if result == 0:
                self.open_ports.append(str(port))
            else:
                self.closed_ports.append(str(port))

    def _scan(self, start, end=None):

        if end == None:
            end = start
            start = 1
        for port in range(start, end):
            self._connect(port)
        
        self._send_report()

    def _send_report(self):
        click.echo(f'\nMolly Scan Report for {self.target} ({self.hostname})')
        click.echo('-' * 40)
        if len(self.open_ports) == 0:
            click.echo('This scan did not find any open ports')
        else:
            click.echo(f'Found {len(self.closed_ports)} closed ports.\n')
            click.echo(f'Found {len(self.open_ports)} open ports: \n')
            click.echo(' \n'.join(self.open_ports))

        click.echo(f'\nMolly done: 1 IP scanned (1 Host Up) scanned in {self._compute_scan_time()} seconds.')
    
    def _compute_scan_time(self):
        elapsed_time = time.time() - self.start_time
        return f'{elapsed_time:.2f}'
    
    def _get_custom_port_range(self, input_value):

        try:
            ports = [int(port) for port in input_value.replace(' ', '').split(',')[0:2]]
        except ValueError:
            click.echo(f'Error: invalid port range ({input_value})')
            sys.exit()

        if len(ports) < 2:
            raise ValueError('Error: ports should be separated by commas')
        else:
            if ports[1] < ports[0]:
                raise ValueError(f'Error: Start range is bigger than end range: {ports}')
            return ports