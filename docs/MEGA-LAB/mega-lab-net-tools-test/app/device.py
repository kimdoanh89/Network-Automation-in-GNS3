from ipaddress import IPv4Address, ip_address, IPv4Interface, ip_interface, ip_network
from app.contants import NUM_ROUTERS_PER_GROUP
from app.utils import create_repr

MGMT_INT_TEMPLATE = "10.15.{group}.{number}/24"


# we need:
# hostname R2
# DHCP ip address: 10.15.1.2/24
# default gateway: 10.15.1.254
# 1-100 : group 1, 101-200: group 2


class Device:
    def __init__(
            self,
            num: int,
            group_num: int,
            hostname: str,
            mgmt_int: IPv4Interface) -> None:
        self.num = num
        self.group_num = group_num
        self.hostname = hostname
        self.mgmt_int = mgmt_int

    def __repr__(self) -> str:
        return create_repr(self, ("num", "group_num", "hostname", "mgmt_int"))

    @classmethod
    def from_sequence_num(cls, num: int) -> "Device":
        group = (num - 1) // NUM_ROUTERS_PER_GROUP + 1
        num_in_group = (num - 1) % NUM_ROUTERS_PER_GROUP + 1
        hostname = f"R{num}"
        mgmt_int = ip_interface(MGMT_INT_TEMPLATE.format(group=group, number=num_in_group))
        device = cls(num=num, group_num=group, hostname=hostname, mgmt_int=mgmt_int)
        return device

    @property
    def default_gw(self) -> str:
        result = list(self.mgmt_int.network.hosts())[-1]
        return str(result)

    @property
    def mgmt_int_ip(self) -> str:
        return str(self.mgmt_int.ip)

    @property
    def netmask(self) -> str:
        result = self.mgmt_int.network.netmask
        return str(result)

    @property
    def mgmt_int_network(self) -> str:
        result = self.mgmt_int.network.network_address
        return str(result)
