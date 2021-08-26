import random
from typing import List

from graph_coloring.heuristics.graph_coloring_heuristic import GraphColoringHeuristic
from util.graph import generate_random_color_partition
from util.models.graph_coloring_tracker import GraphColoringTracker


class K_GWW(GraphColoringHeuristic):

    def __init__(self, verbose: bool = False, debug: bool = False):
        super(K_GWW, self).__init__([
            'num_particles',
            'random_walk_steps',
            'initial_conflict_threshold',
            'conflict_threshold_iteration_change',
            'goal_conflict_threshold'
            'k'
        ])

    def __select_initial_coloring(self) -> GraphColoringTracker:
        return GraphColoringTracker(self.G, generate_random_color_partition(self.k))

    def __random_walk(self, tracker: GraphColoringTracker, steps: int):
        for step in range(steps):
            # Get a random node
            node = tracker.get_random_node()

            # and color it a random AVAILABLE color (but only if we can
            if len(tracker.available_colors_at[node]) == 0:
                continue
                # print(f'Couldn\'t recolor a node at iteration {self.solution.calls_to_color_node}')
            else:
                tracker.color_node(node, tracker.get_random_color())

    def __get_best_coloring(self, trackers: List[GraphColoringTracker]) -> GraphColoringTracker:
        return min(trackers, key=lambda t: t.num_conflicting_edges)

    def _run_heuristic(
            self,
            num_particles,
            random_walk_steps,
            initial_conflict_threshold,
            conflict_threshold_iteration_change,
            goal_conflict_threshold,
            k
    ):
        self.verbose_print(f"Received metadata: {self.metadata}. Running with {num_particles} particles.")
        # ? Metadata validation
        if num_particles < 1:
            raise Exception("Cannot run GWW with non-positive number of points")

        trackers: List[GraphColoringTracker] = [
            self.__select_initial_coloring() for p in range(num_particles)
        ]
        threshold = initial_conflict_threshold

        while threshold > goal_conflict_threshold:
            for tracker in trackers:
                self.__random_walk(tracker, random_walk_steps)

                temp_trackers = [
                    tracker for tracker in trackers if tracker.num_conflicting_edges <= threshold
                ]

                self.verbose_print(f'Number of trackers after removal is {len(temp_trackers)}')

                if len(temp_trackers) == 0:
                    self.solution = self.__get_best_coloring(trackers)
                    self.verbose_print(f"WARNING: Unable to continue replicating points because no colorings survived.")
                    return

                while len(temp_trackers) < num_particles:
                    temp_trackers.append(random.choice(list(temp_trackers)).replicate())

                trackers = temp_trackers
