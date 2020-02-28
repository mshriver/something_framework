
def test_container_command_local(target_container, container_command):
    container, _ = target_container
    assert container.attrs['Config']['Cmd'] == container_command.split()
    assert container.attrs['Config']['Cmd'] == 'tail -f /dev/null'.split()