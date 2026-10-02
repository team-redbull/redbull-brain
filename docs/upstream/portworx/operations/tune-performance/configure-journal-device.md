# Add a dedicated journal device to a node

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance/configure-journal-device (Portworx Enterprise 3.6)

Add a dedicated journal device to a node | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

A journal device is a dedicated storage component used to improve the performance and reliability of write operations. It logs write operations before they are finalized in the main storage volumes. This page outlines how to configure a Portworx StorageCluster to add a journal device to a new or existing node.

## Prerequisites​

Before proceeding, ensure that:

-
The chosen journal device matches or surpasses the performance of the data pool devices.

-
The selected device or a partition on the selected device is not being used by any other service or applications.

## Check your current journal device configuration​

Before you begin, you may already have a journal device configured for your cluster. If you're unsure, you can check the current journal device configuration by running the `pxctl status` command and finding the `Journal Device` section:

```

pxctl status

```

```

...

	Journal Device:

	1	/dev/sdb1	STORAGE_MEDIUM_SSD	3.0 GiB

    ...

```

## Add a journal device to a new node automatically​

You can add a journal device to a new node automatically by editing your Portworx `StorageCluster`. Using this method, Portworx creates a partition from the existing storage pool drives:

```

storage:

    useAll: true

    journalDevice: auto

```

caution

You cannot use this method to add a journal device existing nodes.

## Add journal device manually​

You can use this method to add a journal device to a new or existing node manually. Done in this way, Portworx creates a journal device out of a drive, cloud drive, or partition you provide it.

### Add journal device to a new node​

Follow the steps in this section to edit your Portworx StorageCluster to add the size and type of the journal device you want to add for your environment.

-
Run the command to edit your Portworx StorageCluster:

- Kubernetes

- Openshift

```

kubectl edit stc <px-cluster-ID> -namespace <px-namespace>

```

```

oc edit stc <px-cluster-ID> -namespace <px-namespace>

```

-
Add the `journalDeviceSpec` parameter and specify the type and size of the device:

```

spec:

    cloudStorage:

        deviceSpecs:

        - type=pd-standard,size=150

        journalDeviceSpec: type=<device-type>,size=<device-size>

```

-
After you add a storage node, run the following command on a node to verify that a journal device is added:

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-6ccfb5c6b80a

   IP: 10.13.158.150

   Local Storage Pool: 1 pool

   POOL	   IO_PRIORITY	   RAID_LEVEL	USABLE	USED	STATUS	ZONE	REGION

   0	HIGH		raid0		384 GiB	12 GiB	Online	default	default

   Local Storage Devices: 3 devices

   Device	Path		Media Type		    Size		Last-Scan

   0:1	   /dev/sdf	   STORAGE_MEDIUM_SSD	128 GiB		31 Jan 24 02:26 UTC

   0:2	   /dev/sdd	   STORAGE_MEDIUM_SSD	128 GiB		31 Jan 24 02:26 UTC

   0:3	   /dev/sde	   STORAGE_MEDIUM_SSD	128 GiB		31 Jan 24 02:26 UTC

   total			-			384 GiB

   Cache Devices:

   * No cache devices

   Journal Device:

   1	/dev/sdb1	STORAGE_MEDIUM_SSD	3.0 GiB

   Metadata Device:

   1	/dev/sdc	STORAGE_MEDIUM_SSD	64 GiB

Cluster Summary

   Cluster ID: PX-xxx-0377

   Cluster UUID: 847373dd-xxxx

   Scheduler: none

   Total Nodes: 3 node(s) with storage (3 online)

   IP		    ID					                  SchedulerNodeName	  Auth		StorageNode	   Used	   Capacity	    Status	StorageStatus   Version		        Kernel				          OS

   10.xx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-4c988d5af111	N/A			     Disabled	       Yes		12 GiB	384 GiB		Online	Up		        3.1.0.0-0a8098d	  3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

   10.xx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-b06882d44629	N/A			     Disabled	       Yes		12 GiB	384 GiB		Online	Up		        3.1.0.0-0a8098d	  3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

   10.xx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-6ccfb5c6b80a	N/A			     Disabled	       Yes		12 GiB	384 GiB		Online	Up (This node)	3.1.0.0-0a8098d	  3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

```

You will see the journal device details in the status.

### Add a journal device to an existing node​

important

This workflow is not supported in a disaggregated cloud deployment. Contact the support team if your setup is disaggregated in a cloud environment.

To add a journal device to an existing node, follow the steps in this section:

-
Switch the node to pool maintenance mode:

```

pxctl service pool maintenance --enter

```

```

This is a disruptive operation, PX will restart in maintenance mode.

Are you sure you want to proceed ? (Y/N): Y

```

Respond with `Y` when prompted.

-
Confirm that the node is in pool maintenance mode:

```

pxctl status

```

```

Status: PX storage in pool maintenance

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: PX-Enterprise (floating) (lease renewal in 6h, 4m)

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-f739ed673990

    IP: 10.xx.xxx.xxx

    Local Storage Pool: 1 pool

    POOL	IO_PRIORITY	RAID_LEVEL	USABLE	USED	STATUS		ZONE	REGION

    0	HIGH		raid0		2.0 TiB	1.0 TiB	In Maintenance	default	default

    Local Storage Devices: 2 devices

    Device	Path		Media Type		Size			Last-Scan

    0:1	/dev/sdc	STORAGE_MEDIUM_SSD	1021 GiB		15 Dec 23 15:02 UTC

    0:2	/dev/sdd	STORAGE_MEDIUM_SSD	1.0 TiB			15 Dec 23 15:02 UTC

    total			-			2.0 TiB

Cluster Summary

    Cluster ID: PX-xxx

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-2b9a5f67ba0e

    Scheduler: none

    Total Nodes: 9 node(s) with storage (8 online)

    IP		        ID					                   SchedulerNodeName	Auth		StorageNode	Used		Capacity	Status			StorageStatus		  Version		    Kernel				         OS

    10.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-e4e9916fcde5	N/A			        Disabled	Yes		    879 GiB		2.0 TiB		Online			Up			          3.1.0.0-4375431	4.20.13-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    10.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-746abe26a72b	N/A			        Disabled	Yes		    531 GiB		2.0 TiB		Online			Up			          3.1.0.0-4375431	4.20.13-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    10.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-f739ed673990	N/A			        Disabled	Yes		    20 GiB	    350 GiB	    In Pool Maintenance	Down (This node)  3.1.0.0-4375431	4.20.13-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    10.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-312cb721e64f	N/A			        Disabled	Yes		    1.0 TiB		2.0 TiB		Online			Up			          3.1.0.0-4375431	4.20.13-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    ...

```

You should see a status output indicating that the node is in pool maintenance mode.

-
Add the journal device. It is recommended to use an SSD/NVME for this purpose:

```

pxctl service drive add --drive /dev/nvme01 --journal

```

```

Successfully added journal device /dev/nvme010p1

```

-
Exit the pool maintenance mode:

```

pxctl service pool maintenance --exit

```

In this topic:
