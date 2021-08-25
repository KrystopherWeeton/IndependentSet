import copy
import random
import time

from graph_coloring.experiments.common import CENTER_SET_SIZE
from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from graph_coloring.result_models.basic_heuristic_results import BasicHeuristicResults
from util.graph import get_big_independent_set
from util.models.graph_coloring_tracker import \
    GraphColoringTracker, \
    AVAILABLE_COLORS_AT, \
    UNCOLORED_NODES, \
    NUM_CONFLICTING_EDGES, \
    COLORED_NODES, \
    NUM_NEIGHBORING_COLORS, \
    SATURATION_MAX, CENTER_SET

greedy_strategies = {
    'random',
    'DSatur',
    'no-choice'
}


class GreedyColor(GraphColoringHeuristic):

    def __init__(self, verbose: bool = False):
        # Frieze Random Greedy doesn't really need anything
        super(GreedyColor, self).__init__(expected_metadata_keys=[
            'greedy_strategy',
            'cheat',
            'results',
            'trial'
        ])

    def _random_greedy(self):
        k: int = 0
        # Make independent sets
        while len(self.solution.get_uncolored_nodes()) != 0:
            # print(f'[V]: Making {k}th color class')
            if self.verbose:
                num_un = len(self.solution.uncolored_nodes)
                cc_size = len(self.solution.uncolored_nodes.intersection(self.solution.center_set))
                print(f'On iteration {k}...Num Uncolored={num_un}, '
                      f'CC_size={cc_size}, '
                      f'Ratio={cc_size / num_un}')

            ind_set: set = copy.copy(self.solution.get_uncolored_nodes())

            num_added: int = 0
            while len(ind_set) != 0:
                num_added += 1

                v: int = random.choice(list(ind_set))
                ind_set.remove(v)

                # Now color the node according to the right greedy strategy
                color: int = k

                self.solution.color_node(node=v, color=color)

                ind_set = ind_set.difference(set(self.G[v]))
            # print(f'[V] Was able to make a color class of size {num_added}.')
            k += 1

            # self.results.add_result(
            #     len(self.solution.G),
            #     self.trial,
            #     num_un=len(self.solution.uncolored_nodes),
            #     cc_siz=len(self.solution.uncolored_nodes.intersection(self.solution.center_set))
            # )

    def _DSatur(self):
        while len(self.solution.get_uncolored_nodes()) != 0:
            v: int = self.solution.pop_most_saturated_node()
            color: int = self.solution.get_random_available_color(v, True)
            self.solution.color_node(node=v, color=color)

    def __useless_coloring(self):
        for i, v in enumerate(self.solution.G):
            self.solution.color_node(v, i)

    def _no_choice(self, cheat: int):
        # Find a cheat-clique
        maximal_clique: list = get_big_independent_set(self.solution.G_comp, cheat)

        if len(maximal_clique) < cheat:
            if self.verbose:
                print('[V] no-choice failed to find a large clique')
            self.__useless_coloring()
            return

        # Color the maximal clique uniquely.
        for k, v in enumerate(maximal_clique):
            self.solution.color_node(v, k)

        # Now color the rest of the graph
        while len(self.solution.uncolored_nodes) != 0:
            colored_node: bool = False
            for node in self.solution.uncolored_nodes:
                # Essentially just color a node with the one color we can put on it
                if self.solution.available_colors_at[node] == 1 or self.solution.available_colors_at[node] == 2:
                    colored_node = True
                    self.solution.color_node(node, self.solution.available_colors_at[node].pop())
                    break
            if not colored_node:
                break

        if len(self.solution.uncolored_nodes) != 0:
            if self.verbose:
                print('[V] no-choice failed to color the graph with only no-choice steps')
            self.solution.clear_coloring()
            self.__useless_coloring()
            return

    # TODO: It's not necessary that the heuristic should know the trial or the n, but fuck it i guess
    def _run_heuristic(self, greedy_strategy: str, cheat: int, results: BasicHeuristicResults, trial: int):

        requested_data = {'uncolored_nodes', 'colored_nodes'}
        if greedy_strategy == 'DSatur' or greedy_strategy == 'no-choice':
            requested_data = requested_data.union({
                UNCOLORED_NODES,
                NUM_CONFLICTING_EDGES,
                AVAILABLE_COLORS_AT,
                COLORED_NODES,
                NUM_NEIGHBORING_COLORS,
                SATURATION_MAX
            })
        if CENTER_SET_SIZE in results.experiments:
            requested_data.add(CENTER_SET)

        self.solution: GraphColoringTracker = GraphColoringTracker(
            self.G,
            requested_data=requested_data
        )
        self.results = results
        self.trial = trial

        if greedy_strategy not in greedy_strategies:
            raise AttributeError(f'{greedy_strategy} is not implemented')

        # greedy_node_selection, greedy_coloring_selection = {
        #     'DSatur': (self.solution.get_most_saturated_node, self.solution.get_random_available_color),
        #     'random': (self.solution.get_random_node, self.solution.get_random_available_color)
        # }[greedy_strategy]
        start_time = time.time()
        if greedy_strategy == 'random':
            self._random_greedy()
        elif greedy_strategy == 'DSatur':
            self._DSatur()
        elif greedy_strategy == 'no-choice':
            self._no_choice(cheat)

        if self.verbose:
            print(f'[V] Heuristic took {time.time() - start_time} seconds')
