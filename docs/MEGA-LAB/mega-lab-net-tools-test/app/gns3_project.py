import httpx
import asyncio

from app.contants import GNS3_CONTROLLER_API_ROOT, PROJECT_ID
from app.gns3_node import GNS3Node
from typing import List, Dict, Any, Iterable, Tuple


class GNS3Project:
    def __init__(self, project_id: str,
                 name_to_node: Dict[str, GNS3Node],
                 id_to_node: Dict[str, GNS3Node]) -> None:
        self.project_id = project_id
        self.http_client = httpx.AsyncClient()
        self.name_to_node = name_to_node
        self.id_to_node = id_to_node

    async def __aenter__(self) -> None:
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.http_client.aclose()

    @property
    def nodes(self) -> Iterable[GNS3Node]:
        return self.name_to_node.values()

    @classmethod
    async def fetch_from_id(cls, project_id: str) -> "GNS3Project":
        project_url = GNS3_CONTROLLER_API_ROOT + f'/projects/{PROJECT_ID}'
        async with httpx.AsyncClient() as http_client:
            get_nodes_task = asyncio.create_task(
                http_client.get(f'{project_url}/nodes'))
            get_links_task = asyncio.create_task(
                http_client.get(f'{project_url}/links'))
            await asyncio.gather(get_nodes_task, get_links_task)
            nodes_data = get_nodes_task.result().json()
            links_data = get_links_task.result().json()
            name_to_node, id_to_node = GNS3Project.parse_nodes_data(nodes_data)
            id_to_link = GNS3Project.parse_links_data(links_data)

        result = cls(project_id=project_id, name_to_node=name_to_node, id_to_node=id_to_node)
        return result

    @staticmethod
    def parse_nodes_data(data: List[Dict[str, Any]]) -> Tuple[Dict[str, GNS3Node], Dict[str, GNS3Node]]:
        name_to_node: Dict[str, GNS3Node] = {}
        id_to_node: Dict[str, GNS3Node] = {}
        for node_data in data:
            node = GNS3Node.load(node_data)
            name_to_node[node.name] = node
            id_to_node[node.id] = node
        return name_to_node, id_to_node

    @staticmethod
    def parse_links_data(data: List[Dict[str, Any]]) -> Dict[str, GNS3Node]:
        id_to_link: Dict[str, GNS3Node] = {}
        return id_to_link
