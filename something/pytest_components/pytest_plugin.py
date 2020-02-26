# base file for loading pytest plugins

# pytest looks for this defintion, via entrypoints specifying this module
# the included modules will be loaded by pytest
pytest_plugins = [
    'something.pytest_components.markers.manual',
    'something.pytest_components.fixtures.target_container',
    #'something.pytest_components.fixtures.something',
]