from unittest import TestCase
import asyncio
import threading
from extensions import complete_neighbourhood
from extensions import climb_degree
from extensions import distance4

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


class TestExtensions(TestCase):
    def test_complete_neighbourhood(self):
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
        loop.run_until_complete(
            complete_neighbourhood(0, get_neighbours_mocked_factory(), add_neighbour_mocked_factory()))

        for x in range(8):
            self.assertTrue(set(rules.get(x)).issubset(set(expected_rules.get(x))))
            self.assertTrue(set(expected_rules.get(x)).issubset(set(rules.get(x))))

    def test_climb_degree(self):
        global rules
        rules = {
            0: {2},
            1: {4, 5, 6, 7},
            2: {0},
            3: {4},
            4: {1, 3, 5},
            5: {1, 4, 6, 7},
            6: {1, 5},
            7: {1, 5}
        }

        def stop_loop(loop):
            loop.stop()

        def run_forever_safe(loop):
            loop.run_forever()
            loop_tasks_all = asyncio.all_tasks(loop=loop)

            for task in loop_tasks_all: task.cancel()

            for task in loop_tasks_all:
                if not (task.done() or task.cancelled()):
                    try:
                        # wait for task cancellations
                        loop.run_until_complete(task)
                    except asyncio.CancelledError:
                        pass
            loop.close()

        def await_sync(task):
            while not task.done(): pass
            return task.result()

        loop = asyncio.new_event_loop()

        # closures for running and stopping the event-loop
        run_loop_forever = lambda: run_forever_safe(loop)
        close_loop_safe = lambda: loop.call_soon_threadsafe(stop_loop, loop)

        # dedicated thread for running the event loop
        thread = threading.Thread(target=run_loop_forever)

        tested_coroutine = asyncio.run_coroutine_threadsafe(climb_degree(3, get_neighbours_mocked_factory()), loop)

        # begin the thread to run the event-loop
        thread.start()

        # synchronously wait for the result of tested task
        result = await_sync(tested_coroutine)

        # close the loop
        close_loop_safe()
        thread.join()

        # verify test result
        self.assertEqual(result, 1)

    def test_distance4(self):
        global rules
        rules = {
            0: {2},
            1: {4, 5, 6, 7},
            2: {0, 3},
            3: {2, 4},
            4: {1, 3, 5},
            5: {1, 4, 6, 7},
            6: {1, 5},
            7: {1, 5}
        }

        def stop_loop(loop):
            loop.stop()

        def run_forever_safe(loop):
            loop.run_forever()
            loop_tasks_all = asyncio.all_tasks(loop=loop)

            for task in loop_tasks_all: task.cancel()

            for task in loop_tasks_all:
                if not (task.done() or task.cancelled()):
                    try:
                        # wait for task cancellations
                        loop.run_until_complete(task)
                    except asyncio.CancelledError:
                        pass
            loop.close()

        def await_sync(task):
            while not task.done(): pass
            return task.result()

        loop = asyncio.new_event_loop()

        # closures for running and stopping the event-loop
        run_loop_forever = lambda: run_forever_safe(loop)
        close_loop_safe = lambda: loop.call_soon_threadsafe(stop_loop, loop)

        # dedicated thread for running the event loop
        thread = threading.Thread(target=run_loop_forever)

        tested_coroutine = asyncio.run_coroutine_threadsafe(distance4(0, get_neighbours_mocked_factory()), loop)

        # begin the thread to run the event-loop
        thread.start()

        # synchronously wait for the result of tested task
        result = await_sync(tested_coroutine)

        # close the loop
        close_loop_safe()
        thread.join()

        # verify test result
        expected = {1, 5}
        for x in range(8):
            self.assertTrue(result.issubset(expected))
            self.assertTrue(expected.issubset(result))
