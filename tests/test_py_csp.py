import pytest
from csp_py import Monitor, __version__, functions


@pytest.fixture
def raw_strings():
    return ("Hello", "wOrld", "arE", "You", "oKay?")


@pytest.fixture
def urls():
    return (
        "https://docs.pytest.org/",
        "https://www.pypi.org",
        "https://www.pypy.org",
        "https://www.python.org",
    )


def test_version():
    assert __version__ == "0.1.0"


def test_monitor_from_functions():
    fns = [str.upper, functions.replace]
    monitor = Monitor.from_functions(fns, num_procs=4)

    for fn in fns:
        assert fn in [runner.fn for runner in monitor.runners]

    assert len(monitor.channels) == len(fns) + 1


def test_monitor_from_graph_simple():
    graph = {
        functions.identity: [
            {str.upper: [functions.replace]},
            {str.lower: [functions.replace]},
        ]
    }

    # TODO: The graph should look like this
    #                 input
    #                   |
    #                   v
    #               identity
    #              /        \
    #             v         v
    #         str.upper    str.lower
    #             |         |
    #             v         v
    #         replace      replace
    #             |         |
    #             v         v
    #          output      output
    assert False


def test_basic_monitor(raw_strings):
    expected_strings = ("HOLLE", "WERLD", "URO", "YEA", "EKUY?")

    monitor = Monitor(num_procs=4)
    monitor.register_function(str.upper)
    monitor.register_function(functions.replace)
    monitor.start()

    for s in raw_strings:
        monitor.submit(s)

    assert set(monitor.collect()) == set(expected_strings)


@pytest.mark.integration
def test_url_hashing(urls):
    monitor = Monitor(num_procs=4)
    monitor.register_function(functions.get_url)
    monitor.register_function(functions.hash)
    monitor.start()

    for url in urls:
        monitor.submit(url)

    actual_urls = {url for url, _ in monitor.collect()}

    assert actual_urls == set(urls)
