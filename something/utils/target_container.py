from collections import namedtuple

import docker

# we'll be reusing these parameters, help keep them consistent
ContainerParams = namedtuple('ContainerParams', ['image', 'tag'])


def create_docker_container(image_data, command=None):
    """assumes ContainerParams instance for image_data
    Returns a tuple of the container instance and docker client
    """
    docker_client = docker.from_env()
    container = docker_client.containers.run(
        f'{image_data.image}:{image_data.tag}',
        command or 'tail -f /dev/null',
        detach=True
    )

    return container, docker_client