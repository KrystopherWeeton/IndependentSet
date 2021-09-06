import networkx as nx


def _generate_random_graph(n: int) -> nx.Graph:	
    return nx.erdos_renyi_graph(n, 0.5)

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
        shc: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            # Test adding vertices to random subset
            subset: set = set(random.sample(shc.nodes, t))
            tracker: GraphSubsetTracker = GraphSubsetTracker(shc, subset)
            to_add: int = random.choice(list(set(shc.nodes).difference(subset)))
            assert(to_add not in tracker.subset)
            tracker.add_node(to_add)
            assert(to_add in tracker.subset)
            assert(tracker.size() == len(subset) + 1)
        return self.__NUM_TRIALS 


    def __test_remove(self) -> int:
        shc: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(shc.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(shc, subset)
            to_remove: int = random.choice(list(subset))
            assert(to_remove in tracker.subset)
            tracker.remove_node(to_remove)
            assert(to_remove not in tracker.subset)
            assert(tracker.size() == len(subset) - 1)
        return self.__NUM_TRIALS 


    def __test_num_edges(self) -> int:
        shc: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(shc.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(shc, subset)
            num_edges: int = shc.subgraph(subset).number_of_edges()
            assert(num_edges == tracker.num_edges())
        return self.__NUM_TRIALS 


    def __test_density(self) -> int:
        shc: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(shc.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(shc, subset)
            density: float = nx.density(shc.subgraph(subset))
            assert(density == tracker.density())
        return self.__NUM_TRIALS 

    
    def __test_num_edges_after_addition(self) -> int:
        shc: nx.Graph = _generate_random_graph(self.__GRAPH_SIZE)
        for t in range(self.__NUM_TRIALS):
            subset: set = set(random.sample(shc.nodes, t + 1))
            tracker: GraphSubsetTracker = GraphSubsetTracker(shc, subset)
            for i in range(self.__MODIFICATIONS_TO_MAKE):
                added: int = tracker.add_random_node()
                removed: int = tracker.remove_random_node()
                subset.add(added)
                subset.remove(removed)
            num_edges: int = shc.subgraph(subset).number_of_edges()
            assert(num_edges == tracker.num_edges())
        return self.__NUM_TRIALS 
"""
# TODO: Implement tests using pytest library