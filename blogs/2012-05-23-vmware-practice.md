---
layout: post
category : virtualization
tags : [cloud, tutorial]
title: VMWare vSphere Practice
---

VMware vSphere Practice
------------------------

### ABSTRACT
As we all know, VMware vSphere has become the most popular virtualization infrastructure in the world. VMware vSphere virtualizes and aggregates the underlying physical hardware resources across multiple systems and provides pools of virtual resources for the datacenter. The current VMware vSphere 4 includes two critical subsystems: ESX and vCenter Server. The article mainly discusses VMware vSphere 4 practice for performance tuning.

### 1.Introduction
As a cloud virtualization infrastructure, VMware vSphere manages large collections of infrastructures (such as CPUs, storages, and networking ) as a seamless and dynamic operating environment, and also manages the complexity of a datacenter. The following component layers make up VMware vSphere.
 
#### VMware vSphere includes the following main components:

- ESX and ESXi: A virtualization-customized OS running on physical servers/hosts that abstracts processors,memories, storages, and resources into multiple virtual machines.
- vCenter Server: A central point for configuring, provisioning, and managing virtualized IT environments.
- vSphere Client: An interface that allows users to connect remotely to vCenter Server or ESX/ESXi from any Windows PC. This component is the main configuration tool for the vSphere infrastructure.
- vSphere Web Access: A Web interface that enables you to manage virtual machines and access remote consoles. The VMWare Lab Manger product is designed by vSphere Web Access.
- VirtualMachine File System(VMFS): A high performance cluster file system for ESX/ESXi virtual machines.
- VMotion and Storage VMotion: VMware VMotion enables the live migration of running virtual machines from one physical server to another with zero down time, continuous service availability, and complete transaction integrity. Storage VMotion enables the migration of virtual machine files from one datastore to another without service interruption.

Since VMware vCenter Server is the main vSphere management component, we also need to introduce the structure of vCenter Server in general. The vCenter Server manages ESX/ESXi servers on which virtual machines (VMs) are running. The vCenter Server uses a database to store and organize inventory data. Clients are connected to vCenter Server to manage and view the inventory. vCenter Server, the database, and the clients can either run on physical machines or inside virtual machines. Our best practice is that the vCenter products mentioned above run inside virtual machines because vCenter itself provides VM Backup/Disaster Recovery/High Availability/Fault Tolerance advance features. 
Figure 2: High level architecture of VMware vCenter
 
### 2.Hardware consideration with VMware vSphere 
Firstly, the hardware needs to be validated before we install ESX or vCenter Server on it. 
All hardware in the system is on the hardware compatibility list for the VMware ESX version
you will be running. We also need to make sure that your hardware meets the minimum configuration supported by  the VMware ESX version you will be running. 

- CPU considerations: Many recent processors from both Intel and AMD include hardware features to assist virtualization. You can enable the hardware-assisted virtualization features on BIOS. Dell PowerEdge series servers adopt the hardware-assisted virtualization CPU.
- Storage Considerations: Storage performance issues are most often the result of configuration issues with underlying storage devices and are not specific to vSphere. It depends on workload, hardware, vendor, RAID level, cache size, stripe size, and so on. According to my experience, many VM workloads are very sensitive to the latency of I/O operations between storage and ESX.
- Network Considerations: The server-class/physical network interface cards (NICs) should be considered for the best performance. The network infrastructure between the source and destination NICs couldn’t be bottlenecks such as the same network speed in all cables and switches. VMware vSphere adopts virtual switches (vSwitch) to configure virtual networks. You could see VMware Virtual Networking Concepts for more information.

### 3.ESX and Virtual Machines Consideration
The general consideration is based on the proper configuration of ESX and Virtual Machine physics and virtual hardware. The following two points are very important for ESX and Virtual Machine.

- Allocate only as much virtual hardware as required for each virtual machine. 
- Disconnect or disable unused or unnecessary physical/virtual hardware devices.

Same as the hardware section above, ESX and Virtual Machine best practice relates to CPU, Memory, Storage and Network.

#### ESX CPU considerations:
When configuring virtual machines, the total CPU resources needed by the virtual machines running on the system should not exceed the CPU capacity of the host. We suggest using as fewer virtual CPUs (vCPUs) as possible when creating VM. But we could monitor all of the behaviors on every VM users. For the best practice, we recommend that you limit the CPU resources for them in order to prevent the host CPU capacity from being overloaded. 
For the VM vSphere Administration, it is a good idea to periodically monitor the CPU usage of the host. This can be done through the vSphere Client or by using esxtop or resextop. 
Hyper-threading technology (called symmetric multithreading, or SMT) is enabled on ESX server for best performance if both the processors and the BIOS support this feature. It allows a single physical processor core to behave like two logical processors, essentially allowing two independent threads to run simultaneously.

#### ESX Memory considerations:
Virtualization causes an increase in the amount of physical memory required due to the extra memory needed by ESX for its own code and for data structures. This additional memory requirement can be separated into two components:

- A system-wide memory space overhead for the service console (typically 272MB) and for the VMkernel (typically about 100MB).
- An additional memory space overhead for each virtual machine.

We recommend that you carefully select the amount of memory you allocate to your virtual machines, so that you can minimize swapping, and avoid over-allocating memory. Allocating more memory than needed increases the virtual machine memory overhead.
ESX uses three memory management mechanisms — page sharing, ballooning, and swapping — to dynamically reduce the amount of machine physical memory required for each virtual machine. The three mechanisms above are enabled on ESX automatically. The VMware administrator could investigate memory overcommit issues according to these three values in the vSphere Client Performance Chart if it affects the performance of a virtual machine.
In addition to the usual 4KB memory pages, ESX also makes 2MB memory pages available as the large page. The use of large pages results in reduced memory management overhead, and thus it increases hypervisor performance.

#### ESX Storage Considerations:
The ESX storage consideration relates to so many system-level designs so that the common user doesn’t have to know them deeply. In here, we just introduce the main features on ESX storage. 
ESX supports three virtual disk modes: Independent persistent, Independent nonpersistent, and Snapshot.

- Independent persistent – Changes are immediately written to the disk, so this mode provides the best performance.	
- Independent nonpersistent – Changes to the disk are discarded when you power off or revert to a snapshot.
- Snapshot – A snapshot captures the entire state of the virtual machine. This includes the memory and disk states as well as the virtual machine settings.

ESX supports multiple disk types:

- Thick – Thick disks, which have all their space allocated at creation time, are further divided into two types: eager zeroed and lazy zeroed.
- Thin – Space required for a thin-provisioned virtual disk is allocated and zeroed upon demand, as opposed to upon creation.

The alignment of the file system partitions can impact performance. So we recommend that you create VMFS partitions to avoid this problem since it automatically aligns the partitions along the 64KB boundary.
Multiple heavily-used virtual machines concurrently accessing the same VMFS volume, or multiple VMFS volumes backed by the same LUNs, can result in decreased storage performance.
I/O latency statistics can be monitored using esxtop (or resxtop), which reports device latency, time spent in the kernel, and latency seen by the guest.
Disk I/O bandwidth can be unequally allocated to virtual machines by using the vSphere Client.

#### ESX Networking Considerations:
Because insufficient CPU resources will reduce maximum throughput, it is important to monitor the CPU utilization of high-throughput workloads for networking. We suggest observing the status of CPU resources through the vSphere client regularly.
If the virtual machines are connected to different virtual switches, traffic will go through wires and incur unnecessary CPU and network overhead.
If the switch is configured with a specific speed and duplex setting, however, the administrator must force the network driver to use the same speed and duplex setting.

### 4.Virtual Infrastructure Management 
The following suggestions included in this section can be implemented using the vSphere Client connected to a VMware vCenter server or an individual ESX host. Resource management configurations can have a significant impact on virtual machine performance.

- If you expect frequent changes to the total available resources, use Shares, instead of Reservation, to allocate resources fairly across virtual machines.
- Use Reservation to specify the minimum acceptable amount of CPU or memory, instead of the amount you would like to have.
- Use resource pools for delegated resource management. To fully isolate a resource pool, set the resource pool type to Fixed and use Reservation and Limit.
- Group virtual machines for a multi-tier service into a resource pool. This allows resources to be assigned for the service as a whole.


### 5.vSphere Case Study
The following solutions are shown for vSphere System management. They include the most common issues that occurred in the practical work for IIG Platform team. 

#### 1. How to upgrade ESX Server to 4.0.4 (the latest version) properly

> 1.	Download the Update package “update-from-esx4.0-4.0_update04.zip”.
> 2.	Transfer the update package file (update-from-esx4.0-4.0_update04.zip) onto the ESX server (make sure the ESX server has a few gigabytes of available space, or the upgrade will fail).
> 3.	In Lab Manager, undeploy all the VMs that are running on the host.
> 4.	In Lab Manager, go to the Resources link -> Hosts tab -> Highlight the host -> Disable (this will prevent any new configurations from deploying onto the host).
> 5.	In Lab Manager, go to the Resources link -> Hosts tab and unprepare Host (It could cut off the connection between LabManger and vCenter Server).
> 6.	In the Virtual Center, put the host into maintenance mode.
> 7.	Ssh into the ESX host and run this command in the same directory where the zip file locates :
esxupdate update --bundle update-from-esx4.0-4.0_update04.zip
> 8.	After the command finishes, it will prompt you to reboot the server.  After rebooting, it will be upgraded to ESX 4.0 Update 4.
> 9.	In Virtual Center, go back to the host and exit maintenance mode
> 10.	In Lab Manager, prepare Host and enable the host again.
> 11.	In Lab Manager, reset Physical Network if necessary. 

#### 2. How to resolve the full disk space issue and purge SqlServer database for vCenter Server
> 1.	Shut down the vCenter Server services.
> 2.	Shrink the Database of vCenter Server. 
(Please refer to [link](http://msdn.microsoft.com/en-us/library/ms189035.aspx) )
> 3.	Run the purge scripts from VMWare to purge the performance data. 
(Please refer to [link](http://kb.vmware.com/selfservice/microsites/search.do?cmd=displayKC&externalId=1025914) )
> 4.	Reduce the size of the VirtualCenter database manually when the rollup scripts take a long time to run. You must run the specific delete sql statements manually on database.
(Please refer to [link](http://kb.vmware.com/selfservice/microsites/search.do?cmd=displayKC&externalId=1007453) )
> 5.	If the above operation still couldn’t reduce the size of database effectively. You have to detach the data files of database in the current disk and move the data to a larger disk. After that, you could attach the data files of database in a new disk. 

#### 3. How to allocate the resources on Lab Manager to improve performance
> 1.	Create a workspace for each Lab Manager User.
> 2.	Allocate the specific resource to the specific user as required.
> 3.	Restrict the access privileges in case of performance limitation.
> For more information about how to migrate VMs and allocate the resource effectively, refer to the following IIG Platform xPlore team sample:
 
#### 4. How to resolve NIC's connected status modified issue on Lab Manager
The following errors will be thrown when you deploy a configuration of 20 or more virtual machines in Lab Manager, if the physical network is configured to use a Distributed Virtual Switch.
NIC's connected status modified
<date stamp> <time stamp>
Network Interface: NIC <n>
NIC's connected status was modified in vCenter.
The resolution is to set Default Local vNetwork Distributed Switch Ports to X+1 where X is the number of virtual machines in the configuration. Make sure the version of Lab Manager is larger than 4.0.2. The change takes effect only in configurations that are deployed after the change is made or after you redeploy the current configurations that generated a related error.

(Please refer to [link](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1020450) )

#### 5. How to resolve the issue Powering off a virtual machine fails with the error
An error message that resembles the following may occur in the console of the vSphere client when you power off a virtual machine. For example, Cannot power Off: Another task is already in progress.
You could resolve this issue using the following steps.

> 1.	Open the .vmx file of the virtual machine using a text editor.
> 2.	Comment this line:
 #log.fileName = "/vmfs/volumes/4b8bd18f-c1f89b5a-1914-002219c8e7a3/vmware.log"
> 3.	Restart the virtual machine for the changes to take effect.
 # vmware-vim-cmd vmsvc/getallvms
 This command returns the VMID.
 # vmware-vim-cmd vmsvc/reload <VMID>
> (Please refer to [link](http://kb.vmware.com/selfservice/microsites/search.do?cmd=displayKC&docType=kc&externalId=1027040&sliceId=1&docTypeID=DT_KB_1_1&dialogID=286943832&stateId=0%200%20286949092) )

#### 6. How to troubleshoot virtual machine performance issues
As the team develops, the virtual machine performance issues will become the bottleneck of work efficiency. The following tips from VMWare Knowledge Base website could help improve the performance of VM.
[Link](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1008360)
The performance tuning of VMs is the main task for every VMWare System Administrator. Actually so many factors could impact the performance of VM and we are still seeking for the better performance of VMs so far.  

#### 7. How to troubleshoot virtual machine performance issues

##### Symptom:
The configuration you are trying to deploy requires consolidation of one or more virtual machines. You can consolidate either the configuration or the virtual machine "CS70C18DFS". 
This is due to the limit on the number of hosts that can simultaneously access the same storage. 

#### 8. How to delete  virtual machine file on SAN storage

##### Symptom:
Cannot delete file [SANFS] chnservices-lm/-17162

#### 9. VMware vCenter Best Practices
Large numbers of managed hosts, managed virtual machines, and connected VMware vSphere Clients can impact the performance of a vCenter server. Exceeding the supported maximums, though it might work, is even more likely to impact vCenter performance. Currently, vCenter Server in IIG Platform team manages over 40 ESX hosts and over 1500 VMs. We should migrate the vCenter Server on more powerful server for the best performance. Besides that, the following tips could help improve vCenter performance.

- Disconnect VMware vSphere Clients from the vCenter server when they are no longer needed.
- Avoid overly-aggressive vCenter alarm settings. Each time an alarm condition is met the vCenter server must take appropriate actions.
- The VMWare user should consider running VMware vCenter Update Manager and vCenter Converter on its own system and providing it with a dedicated database.
- We recommend that the user select Microsoft Windows Server 2008 64-bit operating system for vCenter installations with no more than 300 hosts or 3000 virtual machines.

#### 10. VMWare Lab Manager Best Practice
> 1.	Install vCenter Server/Lab Manager on VM env for DRS/FailOver 
> 2.	VM Name Definition and improve Reusability
> 3.	Power off VMs in idle time 
> 4.	Using virtual networks in case of network conflict 
> 5.	Using Organization/Workspace to manage resource
> 6.	Install VM tool
> 7.	Don’t snapshot in Lab Manager and using Library on Configuration.
> 8.	Using Linked Clone not Full Clone for VM
> 9.	Limit VM numbers/Configuration numbers
> 10.	Limit CPU/Memory sizes
> 11.	Use Storage Leases
> 12.	The shared storage/vCenter are the main bottlenecks not LM
> 13.	Upgrade vSphere(ESX/vCenter/LabManager) timely
> 14.	Backup vCenter/Lab Manager database periodically  

### 6.Conclusion
The VMware vSphere performance tuning is very important and complicated for every VMware administrator. The performance consideration includes CPUs, Memories, Storages and Networking configurations on multiple layers (Hardware/ESX/Virtual Machine). So the understanding of vSphere design and concept is essential. And vSphere client as the common and useful vSphere management tool should be mastered proficiently for the best performance. VMware community on VMware official website also could help the VMware users find out the solution to resolve all kinds of VMware vSphere issues.

### 7.Reference

- [Performance Best Practices for VMware vSphere 4.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere4.0.pdf)
- [Performance Troubleshooting for VMware vSphere 4](http://www.vmware.com/resources/techresources/10066)
- [Understanding Memory Resource Management in ESX.pdf](http://www.vmware.com/files/pdf/perf-vsphere-memory_management.pdf)

