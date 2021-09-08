import unittest

from util.models.graph_subset_tracker import GraphSubsetTracker
from util.new_graph.models.graph import Graph


class TestCase(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_initialize_graph_subset_tracker(self) -> None:
        self.n = 1
        self.graph_subset_tracker = GraphSubsetTracker()


    def test_add(self) -> None:
        # TODO: Implement
        pass

    
    def test_remove(self) -> None:
        # TODO: Implement
        pass


    def test_num_edges(self) -> None:
        # TODO: Implement
        pass


    def test_density(self) -> None:
        # TODO: Implement
        pass


    def test_num_edges_after_add(self) -> None:
        # TODO: Implement
        pass

if __name__ == "__main__":
    unittest.main()

"""
class GraphSubsetTrackerTests():
    def __init__(self):
        # The number of trials to run for each experiment.
        self.__NUM_TRIALS: int = 10
        # The graph size for the experiments
        self.__GRAPH_SIZE: int = 100
        # The number of modifications to make when adding / removing to test
        # tracking of metadata.
        self.__MODIFICATIONS_TO_MAKE: int = 5
    

    def run_tests(self) -> int:
        return self.__test_add() + \
                self.__test_remove() + \
                self.__test_num_edges() + \
                self.__test_density() + \
                self.__test_num_edges_after_addition()

    
    def num_tests(self) -> int:
        return 5 * self.__NUM_TRIALS

    
    def identifier(self) -> str:
        return "graph subset tracker"

    
    def __test_add(self) -> int:
        G: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            # Test adding vertices to random subset
            subset: set = set(random.sample(G.nodes, t))
            tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
            to_add: int = random.choice(list(set(G.nodes).difference(subset)))
            assert(to_add not in tracker.subset)
            tracker.add_node(to_add)
            assert(to_add in tracker.subset)
            assert(tracker.size() == len(subset) + 1)
        return self.__NUM_TRIALS 


    def __test_remove(self) -> int:
        G: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(G.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
            to_remove: int = random.choice(list(subset))
            assert(to_remove in tracker.subset)
            tracker.remove_node(to_remove)
            assert(to_remove not in tracker.subset)
            assert(tracker.size() == len(subset) - 1)
        return self.__NUM_TRIALS 


    def __test_num_edges(self) -> int:
        G: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(G.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
            num_edges: int = G.subgraph(subset).number_of_edges()
            assert(num_edges == tracker.num_edges())
        return self.__NUM_TRIALS 


    def __test_density(self) -> int:
        G: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(G.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
            density: float = nx.density(G.subgraph(subset))
            assert(density == tracker.density())
        return self.__NUM_TRIALS 

    
    def __test_num_edges_after_addition(self) -> int:
        G: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(G.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(G, subset)
            for i in range(self.__MODIFICATIONS_TO_MAKE):
                added: int = tracker.add_random_node()
                removed: int = tracker.remove_random_node()
                subset.add(added)
                subset.remove(removed)
            num_edges: int = G.subgraph(subset).number_of_edges()
            assert(num_edges == tracker.num_edges())
        return self.__NUM_TRIALS 
"""
