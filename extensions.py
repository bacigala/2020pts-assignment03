import asyncio
import requests
import functools


async def complete_neighbourhood(start):
    neighbours = requests.get(f'http://localhost:{start}').text.split(",")
    futures = []
    for neighbour in neighbours:
        async def process(node):
            for other in neighbours:
                if other != node:
                    requests.get(f'http://localhost:{node}/new?port={other}')

        futures.append(asyncio.ensure_future(process(neighbour)))
    await asyncio.gather(*futures)


async def climb_degree(start):
    while True:
        neighbours = requests.get(f'http://localhost:{start}').text.split(",")

        # asynchronous lookup for degrees of neighbour nodes
        futures = []
        neighbour_degree = []
        for neighbour in neighbours:
            async def process(node):
                node_neighbours = requests.get(f'http://localhost:{node}').text.split(",")
                neighbour_degree.append((node, len(node_neighbours)))

            futures.append(asyncio.ensure_future(process(neighbour)))
        await asyncio.gather(*futures)

        # consider start as neighbour of itself
        neighbour_degree.append((start, len(neighbours)))

        # sort neighbour nodes primary acc. to higher degree and secondary acc. to lower port
        def my_comparator(node_degree_1, node_degree_2):
            port1, degree1 = node_degree_1
            port2, degree2 = node_degree_2
            if degree1 < degree2:
                return 1
            elif degree1 > degree2:
                return -1
            else:
                if port1 < port2:
                    return -1
                elif port1 > port2:
                    return 1
                else:
                    return 0
        neighbour_degree = sorted(neighbour_degree, key=functools.cmp_to_key(my_comparator))

        # stop recursion if no higher degree is found in the neighbourhood (or no lower port if degrees equal)
        start_degree = len(neighbours)
        if start_degree > neighbour_degree[0][1] \
                or (start_degree == neighbour_degree[0][1] and start <= neighbour_degree[0][0]):
            return start

        # recursively look for the answer in the neighbour with the highest higher degree
        start = neighbour_degree[0][0]


async def distance4(start):
    current_distance = 0
    current_distance_nodes = set()
    previous_distance_nodes = set()
    visited_nodes = set()

    current_distance_nodes.add(start)

    while current_distance < 4:
        current_distance += 1
        previous_distance_nodes = current_distance_nodes
        current_distance_nodes = set()
        visited_nodes = visited_nodes.union(previous_distance_nodes)

        # find all neighbours of previously visited nodes
        futures = []
        for previous_distance_node in previous_distance_nodes:
            async def process(node):
                nonlocal current_distance_nodes
                node_neighbours = requests.get(f'http://localhost:{node}').text.split(",")
                current_distance_nodes = current_distance_nodes.union(node_neighbours)

            futures.append(asyncio.ensure_future(process(previous_distance_node)))
        await asyncio.gather(*futures)

        current_distance_nodes.difference_update(visited_nodes)

    return current_distance_nodes
