from extensions import climb_degree, complete_neighbourhood, distance4
from extensions import get_neighbours_from_network
from initialize_nodes import do_stuff
import threading
import asynctest


class TestSystem(asynctest.TestCase):
    async def test_system(self):
        # start servers
        HOST = "localhost"
        graph_base = 8030
        graph = {(0, 2), (2, 3), (3, 4), (4, 1), (4, 5), (5, 1), (5, 7), (5, 6), (6, 1), (7, 1)}
        graph = {(graph_base + x, graph_base + y) for x, y in graph}
        nodes = {x for y in graph for x in y}
        condition_ready = threading.Condition()
        condition_done = threading.Condition()
        server = threading.Thread(target=do_stuff, args=(HOST, nodes, graph, condition_ready, condition_done))
        server.start()
        with condition_ready:
            condition_ready.wait()

        # test: distance4 from 8030
        dist4 = set(await distance4('8030'))
        expected_dist4 = {'8031', '8035'}
        self.assertEqual(dist4, expected_dist4)

        # test: climb from 8030
        climb = await climb_degree('8030')
        self.assertEqual(climb, '8032')

        # test: 'complete_neighbourhood' creates desired connections
        neighbours = set(await get_neighbours_from_network('8032'))
        expected_neighbours = {'8030', '8033'}
        self.assertEqual(neighbours, expected_neighbours)
        await complete_neighbourhood('8033')
        neighbours = set(await get_neighbours_from_network('8032'))
        expected_neighbours.add('8034')
        self.assertEqual(neighbours, expected_neighbours)

        # test: distance4 from 8030 - should have changed
        dist4 = set(await distance4('8030'))
        expected_dist4 = {'8036', '8037'}
        self.assertEqual(dist4, expected_dist4)

        # test: climb from 8030 - should have changed
        climb = await climb_degree('8030')
        self.assertEqual(climb, '8031')

        with condition_done:
            condition_done.notify()
        server.join()
