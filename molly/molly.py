from queue import Queue
from threading import Thread
import click
import os
import time
import sys
import socket
from .utils import is_ip_v4
from .constants import FIRST_1000_PORTS, ALL_PORTS, TOP_20_PORTS


class Molly():

    def __init__(self, target, mode, workers):
        self.hostname = target 
        self.mode = mode 
        self.target = self._parse_target(target)
        self.queue = Queue()
        self.open_ports = []
        self.closed_ports = []
        self.start_time = time.time()
        self.max_workers = workers


    def get_ports_to_scan(self):
        if self.mode == 'basic':
            self._add_ports_to_queue(FIRST_1000_PORTS)
        elif self.mode == 'full':
            self._add_ports_to_queue(ALL_PORTS)
        elif self.mode == 'common':
            self._add_ports_to_queue(TOP_20_PORTS)
        elif self.mode == 'custom':
            ports = self._get_custom_port_range()
            self._add_ports_to_queue(ports)
        else:
            raise ValueError(f'Unexpected value for --mode option: {self.mode}')
    
    def _scan(self):
        while not self.queue.empty():
            port = self.queue.get()
            connection_descriptor = self._connect(port)
            if connection_descriptor == 0:
                self.open_ports.append(port)
                click.echo(f'Port {port} is open')
            else:
                self.closed_ports.append(port)

    def run_scan(self):
        print(f'Running scan (Mode: {self.mode}) ...')
        threads = []
        for _ in range(self.max_workers):
            t = Thread(target=self._scan)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        
        self._send_report()
        
    
    def _add_ports_to_queue(self, ports):
        if isinstance(ports, int):
            for port in range(1, ports):
                self.queue.put(port)
        elif isinstance(ports, list):
            for port in ports:
                self.queue.put(port)
        elif isinstance(ports, tuple):
            start = ports[0]
            end = ports[1]
            for port in range(start, end):
                self.queue.put(port)

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

    def _send_report(self):
        click.echo(f'\nMolly Scan Report for {self.target} ({self.hostname})')
        click.echo('-' * 40)
        self.open_ports = list(map(str, self.open_ports))
        if len(self.open_ports) == 0:
            click.echo('This scan did not find any open ports')
        else:
            click.echo(f'Found {len(self.closed_ports)} closed ports.\n')
            click.echo(f'Found {len(self.open_ports)} open ports: \n')
            click.echo(' \n'.join(self.open_ports))

        click.echo(f'\nMolly done: 1 IP scanned (1 Host Up) {self.total_ports_scanned} ports scanned in {self._compute_scan_time()} seconds.')
    
    def _compute_scan_time(self):
        elapsed_time = time.time() - self.start_time
        return f'{elapsed_time:.2f}'
    
    def _get_custom_port_range(self):
        port_range = click.prompt('Please select a range of ports (separated by a comma)', type=str)
        port_range = port_range.replace(' ', '').split(',')
        port_range = tuple(filter(str, port_range))

        try: 
            port_range = tuple(map(int, port_range))
            if len(port_range) < 2:
                click.echo(f'[Error]: Port range should be TWO numbers, separated by a comma. You provided {port_range}')
                sys.exit(1)
        except ValueError:
            click.echo(f'[Error]: Illegal value for port range, you provided {port_range}')
            sys.exit(1)
        else:
            if port_range[0] > port_range[1]:
                click.echo(f'[Error]: Start port cannot be bigger than the last port. You provided {port_range}')
                sys.exit(1)
            return port_range
        
    @property
    def total_ports_scanned(self):
        return len(self.open_ports + self.closed_ports)