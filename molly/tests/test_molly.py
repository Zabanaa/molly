import pytest
from unittest import mock
from molly.constants import TOP_20_PORTS, ALL_PORTS, FIRST_1000_PORTS

def test_basic_molly(_molly):
    assert _molly.max_workers == 4
    assert _molly.hostname == 'scanme.nmap.org'
    assert _molly.mode == 'common'

    _molly.max_workers = 20
    _molly.target = 'localhost'
    _molly.mode = 'custom'

    assert _molly.max_workers == 20
    assert _molly.target == 'localhost'
    assert _molly.mode == 'custom'


def test_add_ports_to_queue_ints(_molly):
    assert _molly.queue.qsize() == 0
    _molly._add_ports_to_queue(FIRST_1000_PORTS)
    assert _molly.queue.qsize() == 1023


def test_add_ports_to_queue_list(_molly):
    assert _molly.queue.qsize() == 0
    _molly._add_ports_to_queue(TOP_20_PORTS)
    assert _molly.queue.qsize() == 20 


def test_add_ports_to_queue_tuple(_molly):
    port_range = (23, 99)
    assert _molly.queue.qsize() == 0
    _molly._add_ports_to_queue(port_range)
    assert _molly.queue.qsize() == (port_range[1] - port_range[0])


def test_get_ports_to_scan_basic(_molly):
    _molly.mode = 'basic'
    with mock.patch.object(_molly, '_add_ports_to_queue') as add_ports_mock:
        _molly.get_ports_to_scan()

    add_ports_mock.assert_called_once_with(FIRST_1000_PORTS)


def test_get_ports_to_scan_common(_molly):
    _molly.mode = 'common'
    with mock.patch.object(_molly, '_add_ports_to_queue') as add_ports_mock:
        _molly.get_ports_to_scan()
    add_ports_mock.assert_called_once_with(TOP_20_PORTS)


def test_get_ports_to_scan_error(_molly):
    _molly.mode = 'wjlwqoehwewe'
    with pytest.raises(ValueError) as exc_info:
        _molly.get_ports_to_scan()
    err_msg = f"Unexpected value for --mode option: {_molly.mode}"
    assert str(exc_info.value) == err_msg


def test_get_ports_to_scan_full(_molly):
    _molly.mode = 'full'
    with mock.patch.object(_molly, '_add_ports_to_queue') as add_ports_mock:
        _molly.get_ports_to_scan()
    add_ports_mock.assert_called_once_with(ALL_PORTS)


def test_get_ports_to_scan_custom(_molly):
    _molly.mode = 'custom'
    custom_port_range = (23, 34)
    with mock.patch.object(_molly, '_add_ports_to_queue') as add_ports_mock:
        with mock.patch.object(
            _molly, '_get_custom_port_range', 
            return_value=custom_port_range) as mock_port_range:
            _molly.get_ports_to_scan()
        mock_port_range.assert_called_once()
    add_ports_mock.assert_called_once_with(custom_port_range)


def test_get_custom_port_range_one_port_error(_molly):
    invalid_port_range = '23, '
    with mock.patch('click.prompt', return_value=invalid_port_range) as clk:
        with pytest.raises(SystemExit) as exc_info:
            _molly._get_custom_port_range()
        err_msg = "[Error]: Port range should be TWO numbers, separated by a comma. You provided (23,)"
        assert err_msg == str(exc_info.value)
    clk.assert_called_once()


def test_get_custom_port_range_number_string_error(_molly):
    invalid_port_range = '23, somestring'
    with mock.patch('click.prompt', return_value=invalid_port_range) as clk:
        with pytest.raises(SystemExit) as exc_info:
            _molly._get_custom_port_range()
        err_msg = "[Error]: Illegal value for port range, you provided ('23', 'somestring')"
        assert err_msg == str(exc_info.value)
    clk.assert_called_once()


def test_get_custom_port_range_number_wrong_order_error(_molly):
    invalid_port_range = '233, 98'
    with mock.patch('click.prompt', return_value=invalid_port_range) as clk:
        with pytest.raises(SystemExit) as exc_info:
            _molly._get_custom_port_range()
        err_msg = "[Error]: Start port cannot be bigger than the last port. You provided (233, 98)"
        assert err_msg == str(exc_info.value)
    clk.assert_called_once()


def test_molly_connect(_molly):
    port = 90
    with mock.patch('molly.molly.socket') as sock:
        _molly._connect(port)
    sock.socket.assert_called_once_with(sock.AF_INET, sock.SOCK_STREAM)


def test_molly_parse_target_ip_v4(_molly):
    ip = '34.165.22.11'
    target = _molly._parse_target(ip)
    assert target == ip


def test_molly_parse_target_ip_domain_name(_molly):
    ip = '45.33.32.156'
    domain = 'scanme.nmap.org'
    target = _molly._parse_target(domain)
    assert target == ip

    with mock.patch('socket.gethostbyname', return_value=None) as sock:
        _molly._parse_target(domain)
    sock.assert_called_once_with(domain)

def test_molly_parse_target_ip_error_domain(_molly):
    domain = 'pkepowe.eqpwewqe.l'

    with pytest.raises(SystemExit) as exc_info:
        _molly._parse_target(domain)
    
    assert domain in str(exc_info.value)
