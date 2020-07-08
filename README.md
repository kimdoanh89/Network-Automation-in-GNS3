# Network Automation in GNS3
This repo is for testing Network Automation tools such as python, ansible, nornir,
NETCONF/YANG, RESTCONF, ncclient in GNS3 platform. This repo provides hand-on labs 
from basic to advanced including:
- Setup GNS3 lab.
- Setup small network automation lab with 1 network automation container, one router, one switch.
- Setup mega-lab with 200 routers, Zero Touch Provision.
 
 ## Table of Contents
The following listing links to the notebooks in this repository. Topics Covered:
### 1. Basic settings for GNS3
We start with some basic knowledge about how to set up GNS3, download
Cisco images and create new template in GNS3. There are a lot of 
tutorial videos from David Bombal YouTube channel.
- <a href="https://www.youtube.com/watch?v=Ibe3hgP8gCA" target="_blank">GNS3 installation</a> 
- <a href="https://www.youtube.com/watch?v=A0DEnMi09LY" target="_blank">GNS3 Install: VMware Workstation Pro</a>
- <a href="https://www.youtube.com/watch?v=jhh2_PP9JLU&t=639s" target="_blank">Download Cisco IOS images and use in GNS3</a>

### 2. Network automation with Python
This section introduces network automation with python programming
in GNS3. It starts with download the network automation container
from GNS3 marketplace, set up a basic lab in GNS3 for network 
automation.
- Download Network Automation docker container: [part 1](https://www.youtube.com/watch?v=qsXDZTPnlro), 
[part 2](https://www.youtube.com/watch?v=_iuz6x2vBSw&t=24s)
- [Setup small lab for Network Automation in GNS3](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/INE-Python-Network-Automation/01_Lab_setup.ipynb?flush_cache=true)
- [Advantages of network automation with Multiple Switches](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/INE-Python-Network-Automation/02_advantages_of_network_automation.ipynb?flush_cache=true)
- [SSH with netmiko library in Python](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/INE-Python-Network-Automation/03_SSH_with_netmiko.ipynb?flush_cache=true)

### 3. Network management with NETCONF/YANG
- Configuration of CSR1000v in GNS3 video tutorials: [part 1](https://www.youtube.com/watch?v=5yypbiX1vlI),
[part 2](https://www.youtube.com/watch?v=xdIHNe2XXvM)
- [Configuration of CSR1000v notebook](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/Network-Management-Netconf/00_csr1000v_in_gns3.ipynb?flush_cache=true)
- [Configure ssh, netconf, restconf for cisco_ios_xe_16.6](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/COMET/00_configure_ssh_netconf_restconf_cisco_ios_16.6.ipynb?flush_cache=true)
- [Using ncclient to connect to router](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/Network-Management-Netconf/00_build_topology.ipynb?flush_cache=true)
 
 
### 4. Mega-Lab with 200 routers + Nornir, Ansible
- [Set up first initial mega-lab](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/MEGA-LAB/00_lab_setup_initial.ipynb?flush_cache=true)
- [Refine the initial mega-lab](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/MEGA-LAB/01_lab_setup_refined.ipynb?flush_cache=true)
- [DHCP config with Python/Jinja](https://nbviewer.jupyter.org/github/kimdoanh89/Network-Automation-in-GNS3/blob/master/docs/MEGA-LAB/02_DHCP_config_with_python_jinja.ipynb?flush_cache=true)
