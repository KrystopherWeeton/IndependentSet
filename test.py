#!env/bin/python3
import click

from tests.graph_subset_tracker_tests import GraphSubsetTrackerTests
from tests.test_model import TestModel


ACTIVE_TESTS: [TestModel] = [
    GraphSubsetTrackerTests()
]

@click.command()
@click.option("--verbose", is_flag=True, default=False)
def run(verbose):
    total_tests: int = sum([t.num_tests() for t in ACTIVE_TESTS])
    completed: int = 0
    for t in ACTIVE_TESTS:
        if verbose:
            print(f"[V] Running tests for {t.identifier()}...")
        done: int = t.run_tests()
        if verbose:
            print(f"[V] {done} / {t.num_tests()} tests passed.")
        completed += done
        print(f"{completed}/{total_tests} Complete")


if __name__ == "__main__":
    run()
