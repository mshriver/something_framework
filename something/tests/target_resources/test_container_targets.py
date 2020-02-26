import pytest

# Import the namedtuple for parametrization - do not import the fixture method!
from something.pytest_components.fixtures.target_container import ContainerParams
from something.pytest_components.fixtures.target_container import CONTAINER_DEFAULTS

target_params = [
    ContainerParams('centos', '8'),
    ContainerParams('centos', 'latest')
]

module_scope_container_id = None


# first a simple test case using the defaults
def test_default_target_container(target_container):
    global module_scope_container_id  # don't do this.
    container, docker_client = target_container  # it yields a tuple!
    container.reload()  # refresh status
    module_scope_container_id = container.id
    assert container.attrs['State']['Status'] == 'running'
    assert container.attrs['State']['Running']
    assert container.image.tags[0] == f'{CONTAINER_DEFAULTS.image}:{CONTAINER_DEFAULTS.tag}'


def test_default_target_container_again(target_container):
    # This test function should be using the same container instance as the first
    # target_container is module scoped by default
    container, docker_client = target_container
    global module_scope_container_id
    assert module_scope_container_id == container.id


# indirect parametrization allows for customizing a "generic" fixture for this test
@pytest.mark.parametrize('target_container',
                         target_params,
                         indirect=True,
                         ids=[f'container-{p.image}-{p.tag}' for p in target_params])
def test_custom_target_containers(target_container):
    global module_scope_container_id
    container, docker_client = target_container
    container.reload()
    assert module_scope_container_id != container.id  # its not the same container from the default test
    assert container.attrs['State']['Status'] == 'running'
    assert container.attrs['State']['Running']
    assert 'centos' in container.image.tags[0]
    assert '8' in container.image.tags[0] or 'latest' in container.image.tags[0]