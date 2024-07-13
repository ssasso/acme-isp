# ACME-ISP

**ACME ISP** Simulation - LAB exercises.

## repo structure

* **[T0-empty](T0-empty/README.md)**: This topology creates **only** the virtual devices and manages the addressing of the different interfaces, including the loopbacks. It can be used as a starting point if you want to configure everything else (i.e., OSPF, BGP) from scratch.

* **[T1-core-only](T1-core-only/README.md)**: This topology creates all the virtual devices, all the interfaces and related addressing. It configures OSPF and BGP on both Core Routers and *CORP-1*/*CORP-2*. It will allow you to configure BGP and related policies on **Customer-1 router**.

* **[T2-empty-acme](T2-empty-acme/README.md)**: This topology creates all the virtual devices, all the interfaces and related addressing. It configures BGP on **all the devices except ACME's**. It will allow you to configure on your own OSPF, BGP and related policies on the ACME devices.

* **[T3-full-cfg](T3-full-cfg/README.md)**: This topology creates the full lab configuration: virtual devices, addressing, OSPF and BGP configuration. You can use this as a reference deployment to check the full configuration.

## codespace

Start Github codespace: https://github.com/codespaces/new/ssasso/acme-isp
