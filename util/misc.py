
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