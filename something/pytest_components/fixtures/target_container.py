from collections import namedtuple
import docker
import pytest


# Create a simple data type for test parametrization
ContainerParams = namedtuple('ContainerParams', ['image', 'tag'])
CONTAINER_DEFAULTS = ContainerParams('centos', '7')


@pytest.fixture(scope='module')
def target_container(request):
    """Deploy a container on the local env, using parametrized image and tag names
    Use ContainerParams namedtuple to parametrize for this fixture
    """
    # Let's extend our imagination here for exactly how we're going to deploy a test target
    # Could be on local KVM, could be a container, could be on EC2
    # And you could get it with wrapanapi!

    # Default to a template name, but support indirect parametrization for customization
    image_data = getattr(request, 'param', CONTAINER_DEFAULTS)
    docker_client = docker.from_env()
    container = docker_client.run(f'{image_data.image}:{image_data.tag}',
                                  'tail -f /dev/null',
                                  detach=True)

    yield container, docker_client  # the test might want to do something with these

    # Fixture should handle cleanup of the test resource
    docker_client.stop()

