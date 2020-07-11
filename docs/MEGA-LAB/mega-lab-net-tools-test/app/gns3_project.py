import httpx
import asyncio

from app.contants import GNS3_CONTROLLER_API_ROOT, PROJECT_ID


class GNS3Project:
    def __init__(self, id: str) -> None:
        self.id = id
        self.http_client = httpx.AsyncClient()

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.http_client.aclose()

    @classmethod
    async def fetch_from_id(cls, id: str) -> "GNS3Project":
        project_url = GNS3_CONTROLLER_API_ROOT + f'/projects/{PROJECT_ID}'
        async with httpx.AsyncClient() as http_client:
            get_nodes_task = asyncio.create_task(
                http_client.get(f'{project_url}/nodes'))
            get_links_task = asyncio.create_task(
                http_client.get(f'{project_url}/links'))
            await asyncio.gather(get_nodes_task, get_links_task)
            nodes_data = get_nodes_task.result().json()
            links_data = get_links_task.result().json()
