import unittest

import networkx as nx

from util.models.graph_coloring_tracker import \
    GraphColoringTracker, \
    NUM_CONFLICTING_EDGES, \
    COLORED_NODES, \
    UNCOLORED_NODES, \
    AVAILABLE_COLORS_AT, NUM_NEIGHBORING_COLORS


def initialize_basic_graph(test_case: unittest.TestCase) -> None:
    test_case.n = 5
    test_case.G: nx.Graph = nx.path_graph(test_case.n)
    nx.relabel_nodes(test_case.G, dict(zip(range(1, test_case.n + 1), range(test_case.n))))
    test_case.solution: GraphColoringTracker = GraphColoringTracker(test_case.G, {
        NUM_CONFLICTING_EDGES,
        COLORED_NODES,
        UNCOLORED_NODES,
        AVAILABLE_COLORS_AT,
        NUM_NEIGHBORING_COLORS
    })


# @unittest.skip("Skipping simple tests")
class SimpleTestCases(unittest.TestCase):
    def setUp(self):
        initialize_basic_graph(self)

    def test_initial_state(self):
        self.assertCountEqual(self.solution.uncolored_nodes, list(self.G.nodes))
        self.assertEqual(self.solution.num_conflicting_edges, 0)

    def test_color_one_node(self):
        node = 1
        color = 0
        self.solution.color_node(node, color)
        self.assertEqual(color, self.solution.node_to_color[node])
        self.assertTrue(len(self.solution.color_to_nodes) != 0)
        self.assertIn(node, self.solution.color_to_nodes[0])
        self.assertCountEqual(self.solution.uncolored_nodes, set(range(self.n)).difference({node}))


class BadCompleteColoringTests(unittest.TestCase):
    def setUp(self) -> None:
        initialize_basic_graph(self)

        self.solution.set_coloring_with_node_labels({
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 1
        })

    def test_init_state(self):
        self.assertEqual(self.solution.num_conflicting_edges, 1 + 1 + 1 + 0)

        self.assertCountEqual([1], self.solution.available_colors_at[0])
        self.assertCountEqual([1], self.solution.available_colors_at[1])
        self.assertCountEqual([1], self.solution.available_colors_at[2])

        self.assertCountEqual([], self.solution.available_colors_at[3])
        self.assertCountEqual([1], self.solution.available_colors_at[4])

        true_neighbor_colors = [
            [1, 0],
            [2, 0],
            [2, 0],
            [1, 1],
            [1, 0],
        ]

        self.assertListEqual(true_neighbor_colors[0], self.solution.num_neighboring_colors[0])
        self.assertListEqual(true_neighbor_colors[1], self.solution.num_neighboring_colors[1])
        self.assertListEqual(true_neighbor_colors[2], self.solution.num_neighboring_colors[2])
        self.assertListEqual(true_neighbor_colors[3], self.solution.num_neighboring_colors[3])
        self.assertListEqual(true_neighbor_colors[4], self.solution.num_neighboring_colors[4])

    def test_favorable_recoloring(self):
        self.solution.color_node(0, 1)
        self.assertEqual(self.solution.num_conflicting_edges, 0 + 1 + 1 + 0)

        self.assertCountEqual([1], self.solution.available_colors_at[0])
        self.assertCountEqual([], self.solution.available_colors_at[1])
        self.assertCountEqual([1], self.solution.available_colors_at[2])

        self.assertCountEqual([], self.solution.available_colors_at[3])
        self.assertCountEqual([1], self.solution.available_colors_at[4])

        true_neighbor_colors = [
            [1, 0],
            [1, 1],
            [2, 0],
            [1, 1],
            [1, 0],
        ]

        self.assertListEqual(true_neighbor_colors[0], self.solution.num_neighboring_colors[0])
        self.assertListEqual(true_neighbor_colors[1], self.solution.num_neighboring_colors[1])
        self.assertListEqual(true_neighbor_colors[2], self.solution.num_neighboring_colors[2])
        self.assertListEqual(true_neighbor_colors[3], self.solution.num_neighboring_colors[3])
        self.assertListEqual(true_neighbor_colors[4], self.solution.num_neighboring_colors[4])


class CompleteColoringTests(unittest.TestCase):
    def setUp(self):
        initialize_basic_graph(self)
        self.solution.set_coloring_with_node_labels({
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4
        })

    def test_nn_colors(self):
        # self.assertCountEqual(self.solution.num_neighboring_colors[0], {0: 0, 1: 1, 2: 0, 3: 0, 4: 0})
        # self.assertCountEqual(self.solution.num_neighboring_colors[2], {0: 0, 1: 1, 2: 0, 3: 1, 4: 0})
        self.assertEqual(self.solution.num_neighboring_colors[0][0], 0)
        self.assertEqual(self.solution.num_neighboring_colors[0][1], 1)

    # @unittest.skip("Skipping simple tests as it is not yet implemented")
    def test_available_colors(self):
        self.assertEqual(len(self.solution.available_colors_at[1]), 3)

        # Ok, now try coloring a node
        self.solution.color_node(2, 0)
        self.assertEqual(len(self.solution.available_colors_at[1]), 4)

        # Should have no conflicts
        self.assertEqual(self.solution.num_conflicting_edges, 0)


class PartialColoringTests(unittest.TestCase):

    def setUp(self) -> None:
        initialize_basic_graph(self)
        self.solution.set_coloring_with_color_classes({
            0: [0, 2],
            1: [1],
        })

    def test_partial_partitioning(self):
        self.assertCountEqual(range(3, self.n), self.solution.uncolored_nodes)

        # Should be no conflicts
        self.assertEqual(0, self.solution.num_conflicting_edges)


if __name__ == '__main__':
    unittest.main()
