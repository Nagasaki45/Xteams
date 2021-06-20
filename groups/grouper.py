import random
import statistics

NUM_OF_COMBINATIONS = 125


def create(num_of_groups, elements, key=(lambda x: x)):
    """Partitioning elements into groups with similar total score.

    - Key function should be given to extract scores from each element.
    """
    options = [_random_allocation(num_of_groups, elements)
               for _ in range(NUM_OF_COMBINATIONS)]
    return min(options, key=lambda x: _score_variance(x, key))


def _random_allocation(num_of_groups, elements):
    random.shuffle(elements)
    groups = [[] for _ in range(num_of_groups)]
    for i, e in enumerate(elements):
        groups[i % num_of_groups].append(e)
    return groups


def _score_variance(groups, key):
    scores = [sum([key(p) for p in g]) for g in groups]
    return statistics.variance(scores)
