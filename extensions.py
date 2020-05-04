import asyncio
import requests


async def complete_neighbourhood(start):
    neighbours = (requests.get(f'http://localhost:{start}').text.split(","))
    futures = []
    for node in neighbours:
        async def process(node_):
            for other in neighbours:
                if other != node_:
                    requests.get(f'http://localhost:{node_}/new?port={other}')

        futures.append(asyncio.ensure_future(process(node)))
    await asyncio.gather(*futures)


async def climb_degree(start):
    pass


async def distance4(start):
    pass