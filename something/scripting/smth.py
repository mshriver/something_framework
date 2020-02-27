import click

# Import other click commands to register with the main group, don't define all of them here

# click documentation is great, but briefly:
# Click group defines the top level `smth` command we're defining here
# We can then decorate methods as commands within that group
# We can add main methods imported from other modules as well that are decorated for click

from something.scripting.smth_shell import main as smth_shell_main
from something.scripting.container import container as container_main  # this one has its own group


@click.group()
def smth():
    pass


smth.add_command(smth_shell_main, name='shell')
smth.add_command(container_main, name='container')


# `smth` is available via entrypoints, so this is legacy for direct use
if __name__ == "__main__":
    smth()