import unittest
from extensions import complete_neighbourhood


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def get_neighbours_mocked_factory(rules):
    def get_neighbours_mocked(node):
        return rules.get(node)

    return get_neighbours_mocked


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def add_neighbour_mocked_factory(rules):
    def add_neighbour_mocked(node, new_neighbour):
        rules.get(node).add(new_neighbour)

    return add_neighbour_mocked


class TestExtensions(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "0": {"1", "2", "3"},
            "1": {"0", "2"},
            "2": {"0", "1"},
            "3": {"0", "4"},
            "4": {"4"},
            "5": {}
        }


if __name__ == '__main__':
    unittest.main()
