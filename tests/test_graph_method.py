import unittest
from typing import List, Dict

import networkx as nx
import sympy

from util.graph import PerfectGraphGenerator, generate_random_color_partition


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.generator: PerfectGraphGenerator = PerfectGraphGenerator(n=10, p=.5, co_split=False)
        self.G, _ = self.generator.generate_random_split_graph()

    def test_bell_number(self):
        # self.assertRaises(Exception, self.PerfectGraphGenerator.bell_number(-1))
        # self.assertRaises(Exception, self.PerfectGraphGenerator.bell_number(11))
        self.assertEqual(self.generator.bell_number(5), sympy.bell(5))
        self.assertEqual(self.generator.bell_number(0), sympy.bell(0))
        self.assertEqual(self.generator.bell_number(10), sympy.bell(10))

    def test_binomial_coefficient(self):
        self.assertEqual(self.generator.binomial_coefficient(7, 2), sympy.binomial(7, 2))

    def test_graph_generation(self):
        # NOTE: At the very least we can make sure that clique and chromatic number are the same
        self.assertEqual(nx.graph_clique_number(self.G), len(set(nx.greedy_color(self.G).values())),
                         "Make sure that the graph is perfect")

    def test_random_color_partitioning(self):
        k: int = 5
        partition: Dict[int, List[int]] = generate_random_color_partition(self.G, k)
        self.assertEqual(k, len(partition.keys()), "Make sure we didn't add any colors")
        nodes_in_partition: set = set()
        for col_class in partition.values():
            nodes_in_partition = nodes_in_partition.union(set(col_class))
        for n in self.G:
            self.assertIn(n, nodes_in_partition)


class TestPlantColoring(unittest.TestCase):
    def setUp(self):

        # NOTE: Seems like this takes a lot of time for n = 100, so we made it 50. BUT, it still works at 100, so
        self.generator: PerfectGraphGenerator = PerfectGraphGenerator(n=50, p=.5, co_split=False)
        self.G, _ = self.generator.generate_random_split_graph(15)

    def test_graph_generation(self):
        # NOTE: At the very least we can make sure that clique and chromatic number are the same
        # Question: Can we make a better test?
        self.assertEqual(nx.graph_clique_number(self.G), len(set(nx.greedy_color(self.G).values())),
                         "Make sure that the graph is perfect")
        self.assertEqual(15, nx.graph_clique_number(self.G))

    def test_random_color_partitioning(self):
        k: int = 5
        partition: Dict[int, List[int]] = generate_random_color_partition(self.G, k)
        self.assertEqual(k, len(partition.keys()), "Make sure we didn't add any colors")
        nodes_in_partition: set = set()
        for col_class in partition.values():
            nodes_in_partition = nodes_in_partition.union(set(col_class))
        for n in self.G:
            self.assertIn(n, nodes_in_partition)


if __name__ == '__main__':
    unittest.main()