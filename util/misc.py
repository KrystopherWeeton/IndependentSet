import inspect
from typing import Callable, List, Tuple

import numpy as np


def round_all_values(M: List[List[float]], num_points: int) -> List[List[float]]:
    return [
        [
            round(x, num_points) for x in row
        ]
        for row in M
    ]


def guess_timing(recorded: List[float], num_trials: int) -> Tuple[float, float, float, float]:
    """
    Guesses the timing for an iterated experiment. Returns (completed, remaining, upper_remaining, total) as
    four integers, where the last three are guessed (upper_remaining is remaining +2 std. dev of the completed as a rough
    upper bound).
    """
    assert num_trials >= len(recorded), "Can not guess timing with more recorded trials than num_trials"
    trial_avg: float = np.mean(recorded)
    std_dev: float = np.std(recorded)
    remaining_trials: int = num_trials - len(recorded)
    return (sum(recorded), trial_avg * remaining_trials, trial_avg * remaining_trials + 2 * std_dev, trial_avg * num_trials)


def source_code(callable: Callable, skip_header: bool = True, strip_lines: bool = True) -> List[str]:
    lines: List[str] = inspect.getsourcelines(callable)[0]
    if skip_header:
        lines = list(filter(lambda x:x.startswith(' '), lines))
    if strip_lines:
        lines = [l.strip() for l in lines]
    return lines

                           #Random Restart Point: {list(filter(lambda x:x.startswith(' '), inspect.getsourcelines(random_restart_point)[0]))[0]}\n 

def validate(predicate: bool, message: str):
    """ Validates the predicate evaluates to true, printing the message provided if it doesn't """
    if not predicate:
        raise Exception(message)


def pull_values(d: dict, *args) -> List:
    """
    Pulls values from the dictionary provided
        `d` the dictionary to pull values from
        `args` the keys to pull from the dictionary
    NOTE: Validates keys beforehand and throws an error if a key isn't found.
    """
    validate(all([key in d.keys() for key in args]), f"Can't pull {args} from {d} because a key wasn't found.")
    return [d[key] for key in args]
