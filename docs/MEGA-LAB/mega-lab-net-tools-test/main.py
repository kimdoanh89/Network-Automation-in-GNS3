import asyncio
import aiofiles
from jinja2 import Environment, FileSystemLoader
from app.contants import PROJECT_ID
from app.gns3_project import GNS3Project


async def generate_dhcp_config():
    env = Environment(loader=FileSystemLoader("app/templates"))
    template = env.get_template('dhcp2.j2')
    msg = template.render()
    async with aiofiles.open("output/dhcpd2.conf", "w") as f:
        f.write(msg)


async def main():
    await generate_dhcp_config()
    gns3_project = await GNS3Project.fetch_from_id(PROJECT_ID)
    breakpoint()


if __name__ == "__main__":
    asyncio.run(main())
