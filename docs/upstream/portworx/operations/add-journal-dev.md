# Adding journal device to existing Portworx nodes

Source: https://docs.portworx.com/portworx-enterprise/operations/add-journal-dev (Portworx Enterprise latest)

Adding journal device to existing Portworx nodes | Portworx Enterprise Documentation

## Adding Journal Device to an existing node.​

This section illustrates how to add a journal device to an existing node.

### 1. Enter maintenance mode​

In order to add journal device to a node, the node must be put in maintenance mode:

```

pxctl service maintenance --enter

```

```

This is a disruptive operation, PX will restart in maintenance mode.

Are you sure you want to proceed ? (Y/N): Y

```

Check if the node is in maintenance mode:

```

pxctl status

```

```

PX is in maintenance mode.  Use the service mode option to exit maintenance mode.

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-c9d0eb597668

	IP: X.X.X.185

 	Local Storage Pool: 0 pool

	Pool	IO_Priority	Size	Used	Status	Zone	Region

	No storage pool

	Local Storage Devices: 0 device

	Device	Path	Media Type	Size		Last-Scan

	No storage device

	total		-	0 B

Cluster Summary

	Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

	Node IP: X.X.X.185 - Node ID: xxxxxxxx-xxxx-xxxx-xxxx-c9d0eb597668 In Maintenance

Global Storage Pool

	Total Used    	:  0 B

	Total Capacity	:  0 B

AlertID	Resource	ResourceID				Timestamp	Severity	AlertType		Description

39	CLUSTER		xxxxxxxx-xxxx-xxxx-xxxx-3e2b01cd0bc3	Jan 8 06:01:22 UTC 2017	ALARM		Node state change	Node xxxxxxxx-xxxx-xxxx-xxxx-3e2b01cd0bc3 has an Operational Status: Down

48	NODE		xxxxxxxx-xxxx-xxxx-xxxx-c9d0eb597668	Jan 8 21:45:25 UTC 2017	ALARM		Cluster manager failure	Cluster Manager Failure: Entering Maintenance Mode because of Storage Maintenance Mode

```

### 2. Add the journal device to the node​

A journal device is recommended to be an SSD/NVME:

```

pxctl service drive add --drive /dev/nvme01 --journal

```

```

Successfully added journal device /dev/nvme010p1

```

note

The journal device is expected to not have any filesystem on it, This can be verified by running `blkid /dev/nvme01`. If it has a filesystem on it and you still want to use it as a journal device, the filesystem should be removed by running `wipefs -a /dev/nvme01`.

### 3. Exit maintenance mode​

```

pxctl service maintenance --exit

```

In this topic:
