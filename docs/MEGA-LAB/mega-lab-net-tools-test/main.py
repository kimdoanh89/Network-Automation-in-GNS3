from app.device import Device

from jinja2 import Environment, FileSystemLoader

MAX_NUMBER_ROUTERS = 1000
def main():
    devices = [Device.from_sequence_num(i) for i in range(1, MAX_NUMBER_ROUTERS+1)]
    
    env = Environment(loader=FileSystemLoader("app/templates"))
    
    template = env.get_template('dhcp2.j2')
    msg = template.render(devices=devices)
    with open("output/dhcpd.conf", "w") as f:
        f.write(msg)


if __name__ == "__main__":
    main()