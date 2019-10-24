from molly.molly import Molly
import pytest


@pytest.fixture(scope='function')
def _molly():
    molly = Molly(
        target='scanme.nmap.org',
        mode='common',
        workers=4
    )
    yield molly
