# csp-py

A Python implementation of [Communicating Sequential Processes (CSP)](https://en.wikipedia.org/wiki/Communicating_sequential_processes).

## Installation

You can install from source using Poetry or from PyPI:

```shell
# install from source
git clone git@github.com:shimst3r/csp-py.git
cd csp_py
poetry install

# install from PyPI
pip install csp-py
```

## Idea behind CSP

To put it simply, CSP is a style of concurrency that prefers communication over shared state. Data is passed from process to process using shared input and output channels instead of multiple processes reading and writing using shared memory.

## Workflow

1. Create a `Monitor` that's responsible for coordination for processes.
2. Register functions using the `Monitor`. Channel creation and plumbing is handled by the monitor.
3. Start the `Monitor`.
4. Submit input values to the `Monitor`.
5. Collect results from the `Monitor`.

## Example

This is how you can use `csp-py` (imports ommitted for readability):

```python
fns = [functions.get_url, functions.hash]
urls = [
    "https://docs.pytest.org/",
    "https://www.pypi.org/",
    "https://www.pypy.org/",
    "https://www.python.org/",
]
monitor = Monitor.from_functions(fns, num_procs=mp.cpu_count())
monitor.start()

for url in urls:
    monitor.submit(url)

for url, hash in monitor.collect():
    print(f"{url}: {hash}")
```

## Roadmap

- [ ] Add support for `multiprocessing.Process` and `asyncio`.
- [ ] Add interoperability between `asyncio` coroutines, `multiprocessing.Process` and `threading.Thread`.
- [ ] Add error handling and a cancellation feature to `Monitor`.
