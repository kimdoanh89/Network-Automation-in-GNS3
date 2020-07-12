import asyncio
import aiofiles
from jinja2 import Environment, FileSystemLoader
from app.contants import PROJECT_ID
from app.gns3_project import GNS3Project
from app.device import Device

MAX_NUMBER_ROUTER = 1000


async def generate_dhcp_config():
    env = Environment(loader=FileSystemLoader("app/templates"))
    template = env.get_template('dhcp2.j2')
    msg = template.render()
    async with aiofiles.open("output/dhcpd2.conf", "w") as f:
        f.write(msg)


async def main():
    devices = [Device.from_sequence_num(i) for i in range(1, MAX_NUMBER_ROUTER + 1)]
    await generate_dhcp_config()
    gns3_project = await GNS3Project.fetch_from_id(PROJECT_ID)
    breakpoint()
    # TODO: Add asyncio context manager


if __name__ == "__main__":
    asyncio.run(main())
