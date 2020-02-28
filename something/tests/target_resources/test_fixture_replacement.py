import pytest


@pytest.fixture(scope='module')
def container_command():
    """This replaces the globally defined fixture"""
    return 'tail -f /dev/random'


def test_container_command_local(target_container, container_command):
    container, _ = target_container
    assert container.attrs['Config']['Cmd'] == container_command.split()
    assert container.attrs['Config']['Cmd'] == 'tail -f /dev/random'.split()