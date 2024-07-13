# T3-full-cfg

This topology creates the full lab configuration: virtual devices, addressing, OSPF and BGP configuration.

You can use this as a reference deployment to check the full configuration.

You can export all the configuration, after `netlab up`, with `netlab collect`.

You can validate lab configuration logging into any device to check the routes, or use `netlab validate`.

If you log into any customer host (`c1host`, `c2host` or `c3host`) you can also check the reachability of *WINstagram* or *Newspaper-X* webservers using *traceroute* and/or *curl*.

## netlab validate

example:

```
T3-full-cfg$ netlab validate
[ospf_c1_c2]       Check the CORE-1 to CORE-2 OSPF session [ node(s): core1 ]
[PASS]             core1: Neighbor 100.100.0.2 is in state Full
[PASS]             Test succeeded

[pfx_c1_ospf]      Check for OSPF prefix for CORE-1 loopback [ node(s): igw1,igw2,ixp,corp1,corp2,bras ]
[PASS]             igw1: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             igw2: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             ixp: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             corp1: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             corp2: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             bras: The prefix 100.100.0.1/32 is in the OSPF topology
[PASS]             The CORE-1 loopback is redistributed back into OSPF

[pfx_c2_ospf]      Check for OSPF prefix for CORE-2 loopback [ node(s): igw1,igw2,ixp,corp1,corp2,bras ]
[PASS]             igw1: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             igw2: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             ixp: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             corp1: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             corp2: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             bras: The prefix 100.100.0.2/32 is in the OSPF topology
[PASS]             The CORE-2 loopback is redistributed back into OSPF

[ibgp_c1]          Check IBGP session towards CORE-1 [ node(s): core2,igw1,igw2,ixp,corp1,corp2,bras ]
[PASS]             core2: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             igw1: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             igw2: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             ixp: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             corp1: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             corp2: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             bras: Neighbor 100.100.0.1 (core1) is in state Established
[PASS]             Test succeeded

[ibgp_c2]          Check IBGP session towards CORE-2 [ node(s): core1,igw1,igw2,ixp,corp1,corp2,bras ]
[PASS]             core1: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             igw1: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             igw2: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             ixp: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             corp1: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             corp2: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             bras: Neighbor 100.100.0.2 (core2) is in state Established
[PASS]             Test succeeded

[bgp_igw1_transit] Check the IGW-1 - TRANSIT-1 EBGP session [ node(s): igw1 ]
[PASS]             igw1: Neighbor 100.71.0.2 (transit1) is in state Established
[PASS]             Test succeeded

[bgp_igw2_transit] Check the IGW-2 - TRANSIT-2 EBGP session [ node(s): igw2 ]
[PASS]             igw2: Neighbor 100.72.0.2 (transit2) is in state Established
[PASS]             Test succeeded

[pfx_tr1_bgp]      Check for BGP prefix for transit-1 loopback on BGP core routers [ node(s): core1,core2 ]
[PASS]             core1: The prefix 100.71.1.1/32 is in the BGP table
[PASS]             core2: The prefix 100.71.1.1/32 is in the BGP table
[PASS]             The transit-1 loopback is present as a BGP prefix

[pfx_tr2_bgp]      Check for BGP prefix for transit-2 loopback on BGP core routers [ node(s): core1,core2 ]
[PASS]             core1: The prefix 100.72.2.2/32 is in the BGP table
[PASS]             core2: The prefix 100.72.2.2/32 is in the BGP table
[PASS]             The transit-2 loopback is present as a BGP prefix

[c1_prefix]        Check the propagation of Customer 1 prefixes [ node(s): core1,core2 ]
[PASS]             core1: The prefix 100.100.15.0/24 is in the BGP table with AS path=65535
[PASS]             core2: The prefix 100.100.15.0/24 is in the BGP table with AS path=65535
[PASS]             Core router is receiving prefixes from Customer 1

[aspath_t1]        Check correct AS-Path on Transit-1 [ node(s): transit1 ]
[PASS]             transit1: The prefix 100.100.0.0/20 is in the BGP table with AS path=64666 64666
[PASS]             Test succeeded

[aspath_t2]        Check correct AS-Path on Transit-2 [ node(s): transit2 ]
[PASS]             transit2: The prefix 100.100.0.0/20 is in the BGP table with AS path=64666 64666 64666
[PASS]             Test succeeded

[c1_bestpath]      Check correct Best Path on Customer-1 Router [ node(s): c1rt ]
[PASS]             c1rt: The prefix 100.100.0.0/20 is in the BGP table with BGP router ID=100.100.0.14,best path=True
[PASS]             Test succeeded

[best_to_wins]     Check correct Best Path TO WINstagram [ node(s): core1 ]
[PASS]             core1: The prefix 100.80.44.0/24 is in the BGP table with BGP router ID=100.100.0.13,best path=True,AS path=65040
[PASS]             Test succeeded

[best_from_wins]   Check correct Best Path FROM WINstagram [ node(s): winsrt ]
[PASS]             winsrt: The prefix 100.100.0.0/20 is in the BGP table with BGP next hop=100.70.70.13/24,best path=True
[PASS]             Test succeeded

[best_to_nx]       Check correct Best Path TO Newspaper-X [ node(s): core1 ]
[PASS]             core1: The prefix 100.90.55.0/24 is in the BGP table with BGP router ID=100.100.0.11,best path=True
[PASS]             Test succeeded

[best_from_nx]     Check correct Best Path FROM Newspaper-X [ node(s): nxrt ]
[PASS]             nxrt: The prefix 100.100.0.0/20 is in the BGP table with BGP router ID=100.71.1.1,best path=True,AS path=65001 64666 64666
[PASS]             Test succeeded

[ping_wins]        Pinging WINstagram Web Server [ node(s): c1host,c2host,c3host ]
[PASS]             Validation succeeded on c1host
[PASS]             Validation succeeded on c2host
[PASS]             Validation succeeded on c3host
[PASS]             Test succeeded

[ping_nx]          Pinging Newspaper-X Web Server [ node(s): c1host,c2host,c3host ]
[PASS]             Validation succeeded on c1host
[PASS]             Validation succeeded on c2host
[PASS]             Validation succeeded on c3host
[PASS]             Test succeeded

[SUCCESS]          Tests passed: 48
```

## traceroute test

example:

```
c1host:/# traceroute winsweb
traceroute to winsweb (100.80.44.44), 30 hops max, 46 byte packets
 1  100.100.15.20 (100.100.15.20)  0.010 ms  0.008 ms  0.008 ms
 2  100.100.2.2 (100.100.2.2)  0.007 ms  0.008 ms  0.008 ms
 3  100.100.1.33 (100.100.1.33)  0.008 ms  0.007 ms  0.008 ms
 4  100.100.1.26 (100.100.1.26)  0.007 ms  0.008 ms  0.008 ms
 5  100.70.70.40 (100.70.70.40)  0.008 ms  0.008 ms  0.008 ms
 6  winsweb (100.80.44.44)  0.008 ms  0.008 ms  0.008 ms
```

## curl test

example:

```
c1host:/# curl winsweb
Hey, this is WINstagram!
Your IP Address is: 100.100.15.21

c1host:/# curl -v winsweb
* Host winsweb:80 was resolved.
* IPv6: (none)
* IPv4: 100.80.44.44
*   Trying 100.80.44.44:80...
* Connected to winsweb (100.80.44.44) port 80
> GET / HTTP/1.1
> Host: winsweb
> User-Agent: curl/8.8.0
> Accept: */*
>
* Request completely sent off
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: BaseHTTP/0.6 Python/3.10.14
< Date: Sat, 13 Jul 2024 12:47:46 GMT
< Content-type: text/plain
<
Hey, this is WINstagram!
Your IP Address is: 100.100.15.21
* Closing connection
```
