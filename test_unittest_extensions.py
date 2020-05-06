from unittest import TestCase
import asyncio
from extensions import complete_neighbourhood

rules = {}


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def get_neighbours_mocked_factory():
    async def get_neighbours_mocked(node):
        return set(rules.get(node))

    return get_neighbours_mocked


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def add_neighbour_mocked_factory():
    async def add_neighbour_mocked(node, new_neighbour):
        new_neighbour_set = set(rules.get(node))
        new_neighbour_set.add(new_neighbour)
        rules.update({node: new_neighbour_set})

    return add_neighbour_mocked


# setup basic graph of nodes - represented as sets of neighbours
def reset_rules():
    global rules
    rules = {
        0: {1, 2, 3},
        1: {0, 2},
        2: {0, 1},
        3: {0, 4},
        4: {3},
        5: {},
        6: {7},
        7: {6}
    }


class TestCompleteNeighbourhood(TestCase):
    def setUp(self):
        reset_rules()

    def test_complete_neighbourhood(self):
        expected_rules = {
            0: {1, 2, 3},
            1: {0, 2, 3},
            2: {0, 1, 3},
            3: {0, 1, 2, 4},
            4: {3},
            5: {},
            6: {7},
            7: {6}
        }
        loop = asyncio.get_event_loop()
        loop.run_until_complete(complete_neighbourhood(0, get_neighbours_mocked_factory(), add_neighbour_mocked_factory()))

        for x in range(8):
            self.assertTrue(set(rules.get(x)).issubset(set(expected_rules.get(x))))
            self.assertTrue(set(expected_rules.get(x)).issubset(set(rules.get(x))))
