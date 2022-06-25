"""
url_hashing is an example for how to use csp_py:

    1. the first Runner downloads the content for the given URL
    2. the second Runner hashes the content using hashlib.sha512
"""
import multiprocessing as mp
import sys
from csp_py import Monitor, functions


def main():
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


if __name__ == "__main__":
    sys.exit(main())
