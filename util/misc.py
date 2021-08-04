from typing import List


def round_all_values(M: [[float]], num_points: int) -> [[float]]:
    return [
        [
            round(x, num_points) for x in row
        ]
        for row in M
    ]


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
