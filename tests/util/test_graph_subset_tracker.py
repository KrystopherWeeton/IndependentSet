import random
import unittest

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import Graph, generate_erdos_renyi_graph


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.n: int = 100
        self.subset_size: int = 10


    def test_add(self) -> None:
        """Test `in` / `not in` behavior after adding element"""
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
        to_add: int = random.choice(list(G.vertex_set().difference(subset)))
        assert(to_add not in tracker.subset)
        tracker.add_node(to_add)
        assert(to_add in tracker.subset)
        assert(tracker.size() == len(subset) + 1)

    
    def test_remove(self) -> None:
        """Test `in` / `not in` behavior after removing element"""
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
        to_remove: int = random.choice(list(subset))
        assert(to_remove in tracker.subset)
        tracker.remove_node(to_remove)
        assert(to_remove not in tracker.subset)
        assert(tracker.size() == len(subset) - 1)


    def test_num_edges(self) -> None:
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
        num_edges: int = G.edges(subset)
        assert(num_edges == tracker.num_edges())


    def test_density(self) -> None:
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
        assert(G.density(subset) == tracker.density())


    def test_num_edges_after_add(self) -> None:
        G: Graph = generate_erdos_renyi_graph(self.n, 0.5)
        subset: set = set(random.sample(G.vertex_list(), self.subset_size))
        tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
        added: int = tracker.add_random_node()
        removed: int = tracker.remove_random_node()
        subset.add(added)
        subset.remove(removed)
        assert(G.edges(subset) == tracker.num_edges())
