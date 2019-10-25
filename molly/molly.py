from queue import Queue
from threading import Thread, Event
import click
import os
import time
import sys
import socket
from .utils import is_ip_v4
from .constants import FIRST_1000_PORTS, ALL_PORTS, TOP_20_PORTS, VERSION


class Molly():

    def __init__(self, target, mode, workers):
        self.hostname = target 
        self.mode = mode 
        self.target = self._parse_target(target)
        self.queue = Queue()
        self.open_ports = []
        self.closed_ports = []
        self.max_workers = workers
        self.exit_signal = Event()
        self.start_time = None
        self.end_time = None


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
        while not self.queue.empty() and not self.exit_signal.is_set():

            port = self.queue.get()
            connection_descriptor = self._connect(port)
            if connection_descriptor == 0:
                self.open_ports.append(port)
                click.echo(f'Port {port} is open')
            else:
                self.closed_ports.append(port)

    def run_scan(self):
        click.echo(f'Running scan (Mode: {self.mode}) ...')
        self.start_time = time.time()

        threads = []
        for _ in range(self.max_workers):
            t = Thread(target=self._scan)
            threads.append(t)
            t.start()
        
        try:
            pass
        except KeyboardInterrupt:
            self.exit_signal.set()
            click.echo('\nExiting ...')
            self._send_report()
            sys.exit(1)

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
            try:
                _target = socket.gethostbyname(target)
            except socket.gaierror:
                sys.exit(f'[Error] No Address Associated With Hostname. ({target})')
            else:
                return _target

    
    def _connect(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(.5)
        result = s.connect_ex((self.target, port))
        return result

    def _send_report(self):
        self.end_time = time.time()
        self.open_ports = list(map(str, self.open_ports))

        click.echo(f'\nMolly Scan Report for {self.target} ({self.hostname})')
        click.echo('-' * 40)
        click.echo(f'Found {len(self.closed_ports)} closed ports.\n')
        click.echo(f'Found {len(self.open_ports)} open ports: \n')

        if len(self.open_ports) != 0:
            click.echo(' \n'.join(self.open_ports))

        click.echo(f'\nMolly done: 1 IP scanned (1 Host Up) {self.total_ports_scanned} ports scanned in {self._compute_scan_time()} seconds.')
    
    def _compute_scan_time(self):
        elapsed_time = self.end_time - self.start_time
        return f'{elapsed_time:.2f}'
    
    def _get_custom_port_range(self):
        port_range = click.prompt('Please select a range of ports (separated by a comma)', type=str)
        port_range = port_range.replace(' ', '').split(',')
        port_range = tuple(filter(str, port_range))

        try: 
            port_range = tuple(map(int, port_range))
            if len(port_range) < 2:
                sys.exit(f'[Error]: Port range should be TWO numbers, separated by a comma. You provided {port_range}')
        except ValueError:
            sys.exit(f'[Error]: Illegal value for port range, you provided {port_range}')
        else:
            if port_range[0] > port_range[1]:
                sys.exit(f'[Error]: Start port cannot be bigger than the last port. You provided {port_range}')
            return port_range
        
    @property
    def total_ports_scanned(self):
        return len(self.open_ports + self.closed_ports)