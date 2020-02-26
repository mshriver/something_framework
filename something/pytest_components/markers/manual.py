import pytest


# manual test marking, this adds it to pytest so you don't get warnings about registering them
def pytest_configure(config):
    # its this simple to add your own pytest marker!
    config.addinivalue_line('markers', 'manual: Marker to indicate manual test cases')


# add a CLI option to control collection of manual tests
def pytest_addoption(parser):
    parser.addoption(
        '--manual',
        action='store_true',
        default=False,
        help='Collect manual tests ONLY'
    )
    parser.addoption(
        '--include-manual',
        action='store_true',
        default=False,
        help='Include manual tests in collection'
    )


@pytest.mark.tryfirst
def pytest_collection_modifyitems(config, items):
    if config.getvalue('include_manual'):
        return  # they're already included!

    only_manual = config.getvalue('manual')

    keep, discard = [], []
    for item in items:
        # We know to discard manual tests, since include_manual is false
        # this discards if --manual is false and the test case is marked manual
        # By default, only_manual is false, and cases that are automated are kept
        if bool(item.get_closest_marker('manual')) == only_manual:
            keep.append(item)
        else:
            discard.append(item)

    items[:] = keep  # rewrite items with the keep list
    config.hook.pytest_deselected(items=discard)  # reporting hook for cases that were deselected
