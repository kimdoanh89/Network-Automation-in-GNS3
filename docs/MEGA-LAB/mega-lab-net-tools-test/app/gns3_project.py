import httpx
import asyncio

from app.contants import GNS3_CONTROLLER_API_ROOT, PROJECT_ID
from app.gns3_node import GNS3Node
from typing import List, Dict, Any, Iterable


class GNS3Project:
    def __init__(self, id: str, name_to_node: Dict[str, GNS3Node]) -> None:
        self.id = id
        self.http_client = httpx.AsyncClient()
        self.name_to_node = name_to_node

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.http_client.aclose()

    @property
    def nodes(self) -> Iterable[GNS3Node]:
        return self.name_to_node.values()

    @classmethod
    async def fetch_from_id(cls, id: str) -> "GNS3Project":
        project_url = GNS3_CONTROLLER_API_ROOT + f'/projects/{PROJECT_ID}'
        async with httpx.AsyncClient() as http_client:
            get_nodes_task = asyncio.create_task(
                http_client.get(f'{project_url}/nodes'))
            get_links_task = asyncio.create_task(
                http_client.get(f'{project_url}/links'))
            await asyncio.gather(get_nodes_task, get_links_task)
            name_to_node = GNS3Project.parse_nodes_data(get_nodes_task.result().json())
            links_data = get_links_task.result().json()
        result = cls(id=id, name_to_node=name_to_node)
        return result

    @staticmethod
    def parse_nodes_data(data: List[Dict[str, Any]]) -> Dict[str, GNS3Node]:
        result: Dict[str, GNS3Node] = {}
        for node_data in data:
            node = GNS3Node.load(node_data)
            result[node.name] = node
        return result
