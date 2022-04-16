import random
from copy import copy, deepcopy
from email.message import Message
from typing import List, Union

from numpy import mean

from error_correcting_codes.models.codes.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message, thresholded_random_walk
from util.array import hamming_dist
from util.models.algorithms.algorithm import Algorithm
from util.random import coin_flip, random_int_in_range

"""
    GWW Algorithm

    `step_hook`: step_hook(old_message_parities_sat, old_message_hamming, new_message_tracker)
    `phase_hook`: phase_hook(particles: List[MessageTracker])
"""
class GWW(Algorithm):

    def __init__(self, verbose=False, debug=False, step_hook = None, phase_hook = None):
        super().__init__(MessageTracker, verbose, debug)
        self._step_hook = step_hook
        self._phase_hook = phase_hook


    def _clear(self):
        pass


    def _random_walk(self, msg: MessageTracker, steps: int):
        """ Takes 'msg' on a random walk throughout the solution space of length steps """
        for _ in range(steps):
            msg.swap_index(random_int_in_range(0, msg.msg_len() - 1))
            self.step_hook(msg)
        return msg
    

    def _randomly_generate_solution(self, seed: MessageTracker, bit_flip_prob: float) -> MessageTracker:
        """ Generates random starting particles using 'seed' as seed """
        sol: MessageTracker = deepcopy(seed)
        flip_message(sol, bit_flip_prob)
        return sol


    def _best_particle(self, particles: List[MessageTracker]) -> MessageTracker:
        return max(particles, key = lambda p: p.get_num_parities_satisifed())


    def _mix_particles(self, particles: List[MessageTracker], threshold: int, random_walk_length: int):
        for p in particles:
            thresholded_random_walk(p, threshold, random_walk_length)
    
    def _cut_particles(self, particles: List[MessageTracker], threshold: int) -> List[MessageTracker]:
        return [ x for x in particles if x.get_num_parities_satisifed() >= threshold]
    
    def _replace_particles(self, particles: List[MessageTracker], num_particles: int):
        while len(particles) < num_particles:
            particles.append(deepcopy(random.choice(particles)))
    
    def _calculate_threshold(self, particles: List[MessageTracker]) -> int:
        return round(mean([p.get_num_parities_satisifed() for p in particles]))


    def _run(self, msg: MessageTracker, random_walk_length: int, num_particles: int, init_bit_flip_prob: float):

        # Generate intiail list of particles

        particles: List[MessageTracker] = [self._randomly_generate_solution(msg, init_bit_flip_prob) for p in range(num_particles)]
        # Start off with threshold of half the number of parities being satisfied
        threshold: int = 0
        self.phase_hook(particles, threshold, random_walk_length)

        while threshold < msg.get_num_parities():

            # Calculate new threshold
            new_threshold = self._calculate_threshold(particles)
            if new_threshold <= threshold:
                print("Unable to make progress using GWW average didn't increase")
                self._solution = self._best_particle(particles)
                return
            threshold = new_threshold

            # Replace particles
            new_particles: List[MessageTracker] = self._cut_particles(particles, threshold)
            if len(new_particles) == 0:
                self.verbose_print(f"WARNING: Unable to replicate points because no solutions are better than {threshold}.")
                self._solution = self._best_particle(new_particles)
                return
            particles = new_particles

            self._replace_particles(particles, num_particles)
            self._mix_particles(particles, threshold, random_walk_length)

            # Mark end of a phase, 
            self.phase_hook(particles, threshold, msg.get_num_parities())



        
        self._solution = max(particles, key = lambda p: p.get_num_parities_satisifed())
