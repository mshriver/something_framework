import docker
import pytest


@pytest.fixture(scope='module')
def target_container(request):
    # Let's extend our imagination here for exactly how we're going to deploy a virtual machine
    # Could be on local KVM, could be a container, could be on EC2
    # And you could get it with wrapanapi!

    # Default to a template name, but support indirect parametrization for customization
    image_name = getattr(request, 'param', 'centos')
    docker_client = docker.from_env()
    container = docker_client.run(image_name, 'tail -f /dev/null', detach=True)

    yield container, docker_client  # the test might want to do something with these

    docker_client.stop()

