from click.testing import CliRunner
from molly.cli import cli


def test_scan_no_target():
    runner = CliRunner()
    result = runner.invoke(cli, ['scan'])
    assert result.exit_code == 2
    assert isinstance(result.exception, SystemExit)


def test_scan_unknown_mode():
    mode = 'kwjelkweowh'
    runner = CliRunner()
    result = runner.invoke(cli, ['scan', 'scanme.nmap.org', '--mode', mode])
    assert result.exception
    assert result.exit_code == 2
    assert isinstance(result.exception, SystemExit)


def test_scan_invalid_port_range_type():
    mode = 'custom'
    port_range = '23,wewkwe'
    runner = CliRunner()
    result = runner.invoke(cli, ['scan', 'scanme.nmap.org', '--mode', mode], input=port_range)
    assert result.exception
    assert result.exit_code == 1 
    assert isinstance(result.exception, SystemExit)
    assert str(tuple(port_range.split(','))) in result.output


def test_scan_missing_second_port():
    mode = 'custom'
    port_range = '23'
    runner = CliRunner()
    result = runner.invoke(cli, ['scan', 'scanme.nmap.org', '--mode', mode], input=port_range)
    assert result.exception
    assert result.exit_code == 1 
    assert isinstance(result.exception, SystemExit)
    assert "Port range should be TWO numbers, separated by a comma." in result.output


def test_scan_wrong_order():
    mode = 'custom'
    port_range = '98, 23'
    runner = CliRunner()
    result = runner.invoke(cli, ['scan', 'scanme.nmap.org', '--mode', mode], input=port_range)
    assert result.exception
    assert result.exit_code == 1
    assert isinstance(result.exception, SystemExit)
    assert 'Start port cannot be bigger than the last port' in result.output