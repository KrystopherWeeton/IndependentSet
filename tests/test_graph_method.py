import unittest
from typing import Dict, Set, List

import networkx as nx
import sympy

from util.graph import PerfectGraphGenerator, generate_random_color_partition
from util.models.graph_coloring_tracker import GraphColoringTracker, NUM_CONFLICTING_EDGES, COLORED_NODES, \
    UNCOLORED_NODES


@unittest.skip("Don't need to time generation anymore")
class TimeGenerateGraph(unittest.TestCase):
    def setUp(self):
        self.G, _ = PerfectGraphGenerator(n=500).generate_random_split_graph(.5, co_split=False)

    def test_time_generation(self):
        # self.assertEqual(False, True)
        self.assertEqual(len(self.G), 500)
        self.assertEqual(-1, nx.density(self.G))


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.generator: PerfectGraphGenerator = PerfectGraphGenerator(n=50)
        self.G, _ = self.generator.generate_random_split_graph(.5, co_split=False)

    def test_bell_number(self):
        # self.assertRaises(Exception, self.PerfectGraphGenerator.bell_number(-1))
        # self.assertRaises(Exception, self.PerfectGraphGenerator.bell_number(11))
        self.assertEqual(self.generator.bell_number(5), sympy.bell(5))
        self.assertEqual(self.generator.bell_number(0), sympy.bell(0))
        self.assertEqual(self.generator.bell_number(10), sympy.bell(10))


    def test_graph_generation(self):
        # NOTE: At the very least we can make sure that clique and chromatic number are the same
        self.assertEqual(nx.graph_clique_number(self.G), len(set(nx.greedy_color(self.G).values())),
                         "Make sure that the graph is perfect")
        self.assertEqual(-1, nx.graph_clique_number(self.G))

    def test_random_color_partitioning(self):
        k: int = 5
        partition: Dict[int, Set[int]] = generate_random_color_partition(self.G, k)
        self.assertEqual(k, len(partition.keys()), "Make sure we didn't add any colors")
        nodes_in_partition: set = set()
        for col_class in partition.values():
            nodes_in_partition = nodes_in_partition.union(set(col_class))
        for n in self.G:
            self.assertIn(n, nodes_in_partition)


class TestPlantColoring(unittest.TestCase):
    def setUp(self):

        # NOTE: Seems like this takes a lot of time for n = 100, so we made it 50. BUT, it still works at 100, so
        self.generator: PerfectGraphGenerator = PerfectGraphGenerator(n=50)
        self.G, _ = self.generator.generate_random_split_graph(.5, False, 15)

    def test_graph_generation(self):
        # NOTE: At the very least we can make sure that clique and chromatic number are the same
        # Question: Can we make a better test?
        self.assertEqual(nx.graph_clique_number(self.G), len(set(nx.greedy_color(self.G).values())),
                         "Make sure that the graph is perfect")
        self.assertEqual(15, nx.graph_clique_number(self.G))

    def test_random_color_partitioning(self):
        k: int = 5
        partition: Dict[int, Set[int]] = generate_random_color_partition(self.G, k)
        self.assertEqual(k, len(partition.keys()), "Make sure we didn't add any colors")
        nodes_in_partition: set = set()
        for col_class in partition.values():
            nodes_in_partition = nodes_in_partition.union(set(col_class))
        for n in self.G:
            self.assertIn(n, nodes_in_partition)


class TestSplitGraphGeneration(unittest.TestCase):
    def setUp(self):
        self.graphs: List[nx.Graph] = [
            PerfectGraphGenerator(n=n).generate_random_split_graph(.5, co_split=False) for n in [500] * 10
        ]

    def test_density(self):
        for g, cheat in self.graphs:
            print(f'Graph density is {nx.density(g)}')

    def test_random_color_partition(self):
        for g, cheat in self.graphs:
            sol: GraphColoringTracker = GraphColoringTracker(
                g, nx.complement(g), requested_data={NUM_CONFLICTING_EDGES, COLORED_NODES, UNCOLORED_NODES}
            )
            sol.set_coloring_with_color_classes(generate_random_color_partition(g, cheat))
            print(
                f'Randomly colored graph optimally with {cheat} colors resulting in {sol.num_conflicting_edges} conflicts')


class TestCo_SplitGraphGeneration(unittest.TestCase):
    def setUp(self):
        self.graphs: List[nx.Graph] = [
            PerfectGraphGenerator(n=n).generate_random_split_graph(.5, co_split=False) for n in [500] * 10
        ]

    def test_density(self):
        for g, cheat in self.graphs:
            print(f'Graph density is {nx.density(g)}')

    def test_random_color_partition(self):
        for g, cheat in self.graphs:
            sol: GraphColoringTracker = GraphColoringTracker(
                g, nx.complement(g), requested_data={NUM_CONFLICTING_EDGES, COLORED_NODES, UNCOLORED_NODES}
            )
            sol.set_coloring_with_color_classes(generate_random_color_partition(g, cheat))
            print(
                f'Randomly colored graph optimally with {cheat} colors resulting in {sol.num_conflicting_edges} conflicts')
