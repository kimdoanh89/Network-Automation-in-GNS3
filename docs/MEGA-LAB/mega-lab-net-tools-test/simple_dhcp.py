from jinja2 import Environment, FileSystemLoader


def main():
    env = Environment(loader=FileSystemLoader("app/templates"))
    template = env.get_template('dhcp2.j2')
    msg = template.render()
    with open("output/dhcpd.conf", "w") as f:
        f.write(msg)


if __name__ == "__main__":
    main()
