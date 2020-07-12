import attr
from typing import Dict, Any


@attr.s(auto_attribs=True, repr=False, kw_only=True)
class GNS3Node:
    id: str
    type: str
    name: str
    x: int
    y: int
    z: int

    @classmethod
    def load(cls, data: Dict[str, Any]) -> "GNS3Node":
        node_data = {
            "id": data["node_id"],
            "type": data["node_type"],
            "name": data["name"],
            "x": data["x"],
            "y": data["y"],
            "z": data["z"]
        }
        result = cls(**node_data)
        return result
