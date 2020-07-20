In this post, we will set up an Ansible playbook to collect some information
from hosts and save the outputs to different files depending on the hostname.

The following steps show how to setup and run an Ansible playbook:
- Creating the inventory file
- Modifying the `ansible.cfg`
- Writing the playbook

## 1. The ansible folder structure

We will need to create the ansible folder according to the following structure:

```bash
.
├── ansible.cfg
├── gather_commands.yml
├── inventory
│   └── hosts.yml
└── output
    ├── R1.txt
    └── R2.txt
```

The `ansible.cfg` is as follows:
```buildoutcfg
[defaults]
inventory = hosts.yml
host_key_checking = False
ANSIBLE_SSH_ARGS = -oKexAlgorithms=+diffie-hellman-group1-sha1 -oHostKeyAl
gathering = explicit
#interpreter_python = .venv/bin/python

[paramiko_connection]
#host_key_auto_add = True
look_for_keys = False
host_key_checking = False

[persistent_connection]

connect_timeout = 30
#connect_retry_timeout = 15
command_timeout = 30
```

## 2. Create the hosts inventory file

```yaml
all:
  children:
    CORE1:
      children:
        Switch1:
          hosts:
            R1:
              ansible_host: 10.15.1.1
            R2:
              ansible_host: 10.15.1.2

  vars:
    ansible_user: cisco
    ansible_password: cisco
    ansible_connection: network_cli
    ansible_network_os: ios
```

We can check the connection to a groups of router defined in the inventory
file.
```bash
ansible all -i inventory -m ping
```
Output:
```bash
R1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/home/doanh/.pyenv/shims/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
R2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/home/doanh/.pyenv/shims/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
```

We can use the Ansible ad-hoc CLI tool to run a command on a remote host.
```bash
ansible -i inventory -m setup -u cisco R1
```
Here `cisco` is the user on the router `R1`.

The setup module, which is part of Ansible core, enables users to view facts 
gathered on remote hosts. By default, Ansible collects these facts when we 
use the Ansible tool to manage hosts. 

Suppose that we want to run a command on dozens of routers. Instead of 
opening a terminal session to each router and scraping the output, we can 
use the Ansible ad-hoc CLI with group definition in an inventory file.
```bash
ansible  -i inventory -m command -a "df -k" -u cisco Switch1
```

## 3. Create the Ansible playbook

```yaml
---
- name: Gather commands
  hosts: Switch1
  vars:
    commands:
      - show version
      - show ip int br
      - show memory statistics
      - show arp
      - show ip route
  tasks:
    - name: Gather commands
      ios_command:
        commands: "{{ commands }}"
      register: output

    - name: save output to a file
      copy:
        content: "{{output.stdout | zip(commands) |
        reverse | flatten | join('\n') }}"
        dest: "output/{{ inventory_hostname }}.txt"

```

## 4. Running the Ansible playbook

We run the Ansible playbook to gather information:
- show version
- show ip int br
- show memory statistics
- show arp
- show ip route
The command to run is as follow:
```bash
ansible-playbook -i inventory gather_commands.yml
```
Output:
```bash
PLAY [Gather commands] ************************************************************************************************************

TASK [Gather commands] ************************************************************************************************************
ok: [R1]
ok: [R2]

TASK [save output to a file] ******************************************************************************************************
changed: [R2]
changed: [R1]

PLAY RECAP ************************************************************************************************************************
R1                         : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
R2                         : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

The outputs file will be saved in the `output` folder: `R1.txt` and `R2.txt`.