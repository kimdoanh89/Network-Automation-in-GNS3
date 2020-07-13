import attr
from typing import Dict, Any, List, TYPE_CHECKING, NamedTuple
if TYPE_CHECKING:
    from app.gns3_node import GNS3Node


@attr.s(auto_attribs=True, kw_only=True)
class GSN3Port(NamedTuple):
    adapter_num: int  # start with 0
    port_num: int  # start with 0
    node: "GNS3Node"


@attr.s(auto_attribs=True, kw_only=True)
class GNS3Link:
    id: str
    type: str
    ports: List[GSN3Port]

    @classmethod
    def load(cls, data: Dict[str, Any], id_to_node: Dict[str, "GNS3Node"]) -> "GNS3Link":
        ports = [
            GSN3Port(adapter_num=port_data["adapter_number"],
                     port_num=port_data["port_number"],
                     node=id_to_node(port_data["node_id"]))
            for port_data in data["nodes"]
        ]
        link_data = {
            "id": data["link_id"],
            "type": data["link_type"],
            "ports": ports
        }
        result = cls(**link_data)
        return result
