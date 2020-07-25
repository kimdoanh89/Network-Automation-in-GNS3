## HSRP configuration
The GNS3 project file is [0_HSRP.gns3project](/docs/ROUTING/GNS3%20files/0_HSRP.gns3project).

The topology is as in figure below.

![Alt_text](/docs/ROUTING/images/0_HSRP.png)

## Initial configuration
### Internet
```bash
!
hostname INTERNET
int g0/1
 ip address 172.16.0.6 255.255.255.252
 no sh
int g0/2
 ip address 172.16.0.2 255.255.255.252
 no sh
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0
!
```
### R1
```bash
!
hostname R1
int g0/1
 ip address 172.16.0.1 255.255.255.252
 no sh
int g0/2
 ip address 10.1.1.2 255.255.255.0
 no sh
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0
!
```
### R2
```bash
!
hostname R2
int g0/1
 ip address 172.16.0.5 255.255.255.252
 no sh
int g0/2
 ip address 10.1.1.3 255.255.255.0
 no sh
router ospf 1
 network 0.0.0.0 255.255.255.255 area 0
!
```
### PC
```bash
!
hostname PC
int g0/1
 ip address 10.1.1.100 255.255.255.0
 no sh
ip default-gateway 10.1.1.1
!
```

## HSRP configuration
Tasks:
- Configure HSRP for servicing the virtual IP address 10.1.1.1
- R1 = active router, R2 = standby router
- Configure routers to reclaim roles in case of a failure
- Test failover configuration

### R1
```bash
!
int g0/2
 standby 10 ip 10.1.1.1
 standby 10 priority 110 # default priority 100, 110 > 100, this will be active
 standby 10 preempt
!
```
### R2
```bash
!
int g0/2
 standby 10 ip 10.1.1.1
 standby 10 preempt
!
```

### Test failover
- From PC, `traceroute 1.1.1.1`, then `ping 1.1.1.1 repeat 100`.
- On R1, shutdown g0/2.
- On PC
  - see ping packets, `!!` means ok, `...` means no response.
  - `traceroute 1.1.1.1`
- On R1, no shutdown g0/2.
- On PC, `traceroute 1.1.1.1`.