# First Hop Redundancy Protocols

The topology is as in figure below.

![Alt_text](/docs/ROUTING/images/0_HSRP.png)
## 1. Host Standby Router Protocol (HSRP)
The GNS3 project file is [0_HSRP.gns3project](/docs/ROUTING/GNS3%20files/0_HSRP.gns3project).

Tasks:
- Configure HSRP for servicing the virtual IP address 10.1.1.1
- R1 = active router, R2 = standby router
- Configure routers to reclaim roles in case of a failure
- Test failover configuration

### 1.1. Initial configuration
#### Internet
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
#### R1
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
#### R2
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
#### PC
```bash
!
hostname PC
int g0/1
 ip address 10.1.1.100 255.255.255.0
 no sh
ip default-gateway 10.1.1.1
ip route 0.0.0.0 0.0.0.0 10.1.1.1
!
```

### 1.2. HSRP configuration
Tasks:
- Configure HSRP for servicing the virtual IP address 10.1.1.1
- R1 = active router, R2 = standby router
- Configure routers to reclaim roles in case of a failure
- Test failover configuration

#### R1
```bash
!
int g0/2
 standby 10 ip 10.1.1.1
 standby 10 priority 110 # default priority 100, 110 > 100, this will be active
 standby 10 preempt
!
```
Check with `show standby brief` or `show standby`.
#### R2
```bash
!
int g0/2
 standby 10 ip 10.1.1.1
 standby 10 preempt
!
```
Check with `show standby brief` or `show standby`.
#### Test failover
- From PC, `traceroute 1.1.1.1`, then `ping 1.1.1.1 repeat 100`.
- On R1, shutdown g0/2.
- On PC
  - see ping packets, `!!` means ok, `...` means no response.
  - `traceroute 1.1.1.1`
- On R1, no shutdown g0/2.
- On PC, `traceroute 1.1.1.1`.

### Other settings
We can set HSRP version, the hello time and hold time on R1, and R2.
```bash
conf t
int g0/2
standby version 2
standby 10 timers 100 msec 300 msec # group number: 10, hello time: 100msec, hold time: 300ms 
```

#### Debugging
- On R2, enable debug with `debug standby terse`.
- On R1, shutdown int g0/2.
- See debugging message on R2, and stop with `u all`.

#### Enhanced object tracking
**Tracking int g0/1 go down**
- Configure track int g0/1 goes down,
- On int g0/2: reduce the priority on int g0/2 by 20 when g0/1 goes down, 
the priority becomes `110 - 20 = 90 < 100`.
- Then R2 will take over as active router.

```bash
conf t
track 1 int g0/1 line-protocol
int g0/2
 standby 10 track 1 decrement 20
```

**Track a route disappears from routing table**
- Configure track 2 that tracks the route `ip route 2.2.2.0 255.255.255.0 null 0`
- On int g0/2: reduce the priority by 20 if this route is deleted.
- Test with `sh standby` when delete the route and add it back again.

```bash
conf t 
ip route 2.2.2.0 255.255.255.0 null 0
track 2 ip route 2.2.2.0/24 reachability
int g0/2
 standby 10 track 2 decrement 20
```

**Authentication setting on both R1, R2**
- Using MD5 key-string for authentication.
```bash
conf t
int g0/2
 standby 10 authentication md5 key-string $3cr3T
```

## 2. Virtual Router Redundancy Protocol (VRRP)
We used the same topology and initial configuration of routers as in HSRP. 
We import the same GNS3 portable project above for initial setup, and rename
the project to VRRP.
### 2.1. VRRP configuration
On R1
```bash
conf t
int g0/2
 vrrp 10 ip 10.1.1.1
 vrrp 10 priority 110
```
On R2
```bash
conf t
int g0/2
 vrrp 10 ip 10.1.1.1
```
### 2.2. VRRP object tracking
On R1, setting tracks:
- Track 1: interface g0/1 goes down, reduce priority by 20.
- Track 2: no route in routing table, reduce priority by 20.
```bash
conf t
track 1 int g0/1 line-protocol
ip route 2.2.2.0 255.255.255.0 null 0
track 2 ip route 2.2.2.0/24 reachability
```
On R1, setting VRRP object tracking:
```bash
conf t
int g0/2
 vrrp 10 track 1 decrement 20
 vrrp 10 track 2 decrement 20
```


