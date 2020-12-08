
def round_all_values(M: [[float]], num_points: int) -> [[float]]:
    return [
        [
            round(x, num_points) for x in row
        ]
        for row in M
    ]