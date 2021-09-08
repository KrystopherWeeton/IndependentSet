import random
import unittest
from typing import Set, Tuple

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import Graph, generate_erdos_renyi_graph


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.n: int = 100
        self.subset_size: int = 20

    def _generate_test_graph_and_subset(self) -> Tuple[Graph, Set[int], GraphSubsetTracker]:
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        return (G, subset, GraphSubsetTracker(G, subset))


    def test_add(self) -> None:
        """Test `in` / `not in` behavior after adding element"""
        G, subset, tracker = self._generate_test_graph_and_subset()
        to_add: int = random.choice(list(G.vertex_set().difference(subset)))
        assert(to_add not in tracker.subset)
        tracker.add_node(to_add)
        assert(to_add in tracker.subset)
        assert(tracker.size() == len(subset) + 1)


    def test_edge_boundary(self) -> None:
        G, subset, tracker = self._generate_test_graph_and_subset()
        for v in G.vertex_list():
            assert(G.edge_boundary(v, subset) == tracker.internal_degree(v))


    def test_edge_boundary_after_modifications(self) -> None:
        G, subset, tracker = self._generate_test_graph_and_subset()
        for _ in range(10):
            if random.randint(0, 1) == 0:
                node: int = tracker.add_random_node()
                assert(node in tracker.subset)
                assert(node not in subset)
                subset.add(node)
            else:
                node: int = tracker.remove_random_node()
                assert(node not in tracker.subset)
                assert(node in subset)
                subset.remove(node)
        for v in G.vertex_list():
            assert(G.edge_boundary(v, subset) == tracker.internal_degree(v))

    
    def test_remove(self) -> None:
        """Test `in` / `not in` behavior after removing element"""
        G, subset, tracker = self._generate_test_graph_and_subset()
        to_remove: int = random.choice(list(subset))
        assert(to_remove in tracker.subset)
        tracker.remove_node(to_remove)
        assert(to_remove not in tracker.subset)
        assert(tracker.size() == len(subset) - 1)


    def test_num_edges(self) -> None:
        G, subset, tracker = self._generate_test_graph_and_subset()
        num_edges: int = G.edges(subset)
        assert(num_edges == tracker.num_edges())


    def test_density(self) -> None:
        G, subset, tracker = self._generate_test_graph_and_subset()
        assert(G.density(subset) == tracker.density())


    def test_num_edges_after_add(self) -> None:
        G, subset, tracker = self._generate_test_graph_and_subset()
        added: int = tracker.add_random_node()
        removed: int = tracker.remove_random_node()
        subset.add(added)
        subset.remove(removed)
        assert(G.edges(subset) == tracker.num_edges())
