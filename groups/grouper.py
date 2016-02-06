# Xteams! Sport teams management utility
# Copyright (C) 2014  Tom Gurion

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
