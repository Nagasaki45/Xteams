import random
import statistics

MIN_CHANCE = 0.1
DEFAULT_CHANCE = 0.2


class GrouperError(Exception):
    pass


def create(num_of_groups, elements, key=(lambda x: x),
           chance=DEFAULT_CHANCE):
    '''Partitioning elements into groups with similar total score.

    - Comparator should be given in order to extract the score
    from the elements.
    - Low chance values will evaluate to the most closed scores
    between the groups, and the opposite.
    '''

    _validate(num_of_groups, elements, chance)
    chances = int((1 / chance) ** 3)
    options = [_random_allocation(num_of_groups, elements)
               for _ in range(chances)]
    return min(options, key=lambda x: _score_variance(x, key))


def _validate(num_of_groups, elements, chance):
    if num_of_groups < 2:
        raise GrouperError('Minimum 2 groups.')
    if len(elements) < num_of_groups:
        raise GrouperError('Not enough elements to create groups.')
    if not MIN_CHANCE <= chance <= 1:
        raise GrouperError(
            'Chance should be between {} and 1.'.format(MIN_CHANCE))


def _random_allocation(num_of_groups, elements):
    random.shuffle(elements)
    groups = [[] for _ in range(num_of_groups)]
    for i, e in enumerate(elements):
        groups[i % num_of_groups].append(e)
    return groups


def _score_variance(groups, key):
    scores = [sum([key(p) for p in g]) for g in groups]
    return statistics.variance(scores)
