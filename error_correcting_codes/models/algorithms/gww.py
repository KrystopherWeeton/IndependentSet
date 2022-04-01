import random
from copy import copy, deepcopy
from email.message import Message
from typing import List, Union

from error_correcting_codes.models.codes.ldpc import LDPC
from error_correcting_codes.models.message_tracker import MessageTracker
from error_correcting_codes.util import flip_message
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
    

    def _run(self, msg: MessageTracker, random_walk_length: int, num_particles: int, init_bit_flip_prob: float):

        # Generate intiail list of particles

        particles: List[MessageTracker] = [self._randomly_generate_solution(msg, init_bit_flip_prob) for p in range(num_particles)]
        # Start off with threshold of half the number of parities being satisfied
        threshold: int = msg.get_num_parities() // 2

        while threshold < msg.get_num_parities():
            print(threshold)
            # Mark end of a phase, 
            self.phase_hook(particles, threshold, msg.get_num_parities())

            # While we are not at locally optimal solution
            new_particles: List[MessageTracker] = []
            for p in particles:
                old_parities: int = p.get_num_parities_satisifed()
                old_hamming: int = p.get_hamming_dist_to_original_message()
                self._random_walk(p, random_walk_length)
                if p.get_num_parities_satisifed() >= threshold:
                    new_particles.append(p)
            
            if len(new_particles) == 0:
                # No solutions above new threshold
                best_msg: MessageTracker = max(particles, key=lambda p: p.get_num_parities_satisifed())
                self._solution = best_msg
                self.verbose_print(f"WARNING: Unable to replicate points because no solutions are better than {threshold}.")
                return
        
            while len(new_particles) < num_particles:
                new_particles.append(deepcopy(random.choice(new_particles)))
            particles = new_particles

            threshold = threshold + 5

        
        self._solution = max(particles, key = lambda p: p.get_num_parities_satisifed())
