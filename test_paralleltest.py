import asyncio
import asynctest
from extensions import complete_neighbourhood, climb_degree, distance4
import time

SLEEP_TIME = 5
TOLERANCE = 0.2

rules = {}


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def get_neighbours_mocked_factory():
    async def get_neighbours_mocked(node):
        await  asyncio.sleep(SLEEP_TIME)
        return set(rules.get(node))

    return get_neighbours_mocked


# factory of mocked get_neighbours_from_network (to omit networking)
# @rules parameter is a dictionary where key is server port and value set of neighbours
def add_neighbour_mocked_factory():
    async def add_neighbour_mocked(node, new_neighbour):
        new_neighbour_set = set(rules.get(node))
        new_neighbour_set.add(new_neighbour)
        rules.update({node: new_neighbour_set})
        await asyncio.sleep(SLEEP_TIME)

    return add_neighbour_mocked


class TestParallelity(asynctest.TestCase):
    def setUp(self):
        global rules
        rules = {
            1: {4, 5, 6, 7},
            2: {3},
            3: {2, 4},
            4: {1, 3, 5},
            5: {1, 4, 6, 7},
            6: {1, 5},
            7: {1, 5}
        }

    async def test_complete_neighbourhood(self):
        start = time.time()
        await complete_neighbourhood(3, get_neighbours_mocked_factory(), add_neighbour_mocked_factory())
        finish = time.time()
        expected_runtime = 2 * SLEEP_TIME
        real_runtime = finish - start
        self.assertTrue(expected_runtime <= real_runtime)
        self.assertTrue(real_runtime < expected_runtime + 2*TOLERANCE)

    async def test_climb_degree(self):
        start = time.time()
        await climb_degree(3, get_neighbours_mocked_factory())
        finish = time.time()
        expected_runtime = 6 * SLEEP_TIME
        real_runtime = finish - start
        self.assertTrue(expected_runtime <= real_runtime)
        self.assertTrue(real_runtime < expected_runtime + 6*TOLERANCE)

    async def test_distance4(self):
        start = time.time()
        await distance4(2, get_neighbours_mocked_factory())
        finish = time.time()
        expected_runtime = 4 * SLEEP_TIME
        real_runtime = finish - start
        self.assertTrue(expected_runtime <= real_runtime)
        self.assertTrue(real_runtime < expected_runtime + 4*TOLERANCE)


if __name__ == '__main__':
    asynctest.main()
