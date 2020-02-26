# Wrap core ssh library for framework customizations and optimizations

from paramiko import SSHClient


# Sometimes sessions get lost, maybe a context manager wasn't used, maybe a neutrino hit it
# Be wary of lingering unclosed connections hanging shutdown


class SSHSession(SSHClient):
    # Let's customize how the ssh connection created by paramiko is used
    # by default, its context manager will close the connection on __exit__

    # By instead closing the connection on __del__
    # The connection stays open through separate context manager uses of the same client instance

    # This also means that the connection arguments supplied at the instance creation
    # are re-used for the duration of this session

    # This can be handled in a few ways
    # Delete the cached instance when connection kwargs need to change
    # Modify __call__ to update connection and reconnect if context manager is called with kwargs
    # Explicitly call close, then update instance attributes and start new context manager

    def __init__(self, **connect_kwargs):
        # You can customize how connect_kwargs are handled, defaulted, etc here
        self._connect_kwargs = connect_kwargs  # store the connection kwargs for use in context mgr
        super().__init__()

    def __enter__(self):
        self.connect(self._connect_kwargs)
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __del__(self):
        self.close()