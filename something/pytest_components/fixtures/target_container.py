import pytest

from something.utils.target_container import ContainerParams
from something.utils.target_container import create_docker_container


# Create a simple data type for test parametrization
CONTAINER_DEFAULTS = ContainerParams('centos', '7')


@pytest.fixture(scope='module')
def container_command(request):
    command = getattr(request, 'param', 'tail -f /dev/null')
    return command


@pytest.fixture(scope='module')
def target_container(request, container_command):
    """Deploy a container on the local env, using parametrized image and tag names
    Use ContainerParams namedtuple to parametrize for this fixture
    """
    # Let's extend our imagination here for exactly how we're going to deploy a test target
    # Could be on local KVM, could be a container, could be on EC2
    # And you could get it with wrapanapi!

    # Default to a template name, but support indirect parametrization for customization
    image_data = getattr(request, 'param', CONTAINER_DEFAULTS)
    container, docker_client = create_docker_container(image_data, container_command)
    yield container, docker_client

    # Fixture should handle cleanup of the test resource
    container.stop()

