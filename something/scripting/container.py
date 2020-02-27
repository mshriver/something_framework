import os
import signal
import sys
from time import sleep

import click

from something.utils.target_container import create_docker_container
from something.utils.target_container import ContainerParams


@click.group(help='Functions for interacting with target container')
def container():
    pass


@container.command('checkout', help="create a detached test target container")
@click.option('--image', default='centos', help="Image name for container source")
@click.option('--tag', default='latest', help="Image tag for container source")
@click.option('--command', default='tail -f /dev/null', help='Command to run on container')
def checkout(image, tag, command):
    click.echo(f'Running a container for [{image}:{tag}], with command [{command}]')

    image_data = ContainerParams(image, tag)
    container, docker_client = create_docker_container(image_data, command=command)

    def exit_with_cleanup(signum, frame):
        container.kill()  # no mercy
        sys.exit(0)

    signal.signal(signal.SIGINT, exit_with_cleanup)
    signal.signal(signal.SIGTERM, exit_with_cleanup)

    try:
        while True:
            sleep(5)
            click.echo(f'Container is running with ID: {container.id}, '
                        'stopping this process stops the container')
    except KeyboardInterrupt:
        container.kill()


if __name__ == "__main__":
    container()