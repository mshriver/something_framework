import click
from IPython.terminal.interactiveshell import TerminalInteractiveShell

DEFAULT_IMPORTS = [
    'from something.utils.target_container import create_docker_container',
    'from pprint import pformat',
    # Add other useful default imports for your project
]


@click.command(help="Open a pre-configured ipython shell")
def main():
    ipython = TerminalInteractiveShell.instance()
    for import_statement in DEFAULT_IMPORTS:
        click.echo(f'> {import_statement}')
        ipython.run_cell(import_statement)
        # This can be improved to read a default conf file location
        # So that users can write their own default imports for their local clone

    ipython.interact()


if __name__ == '__main__':
    main()