# Updating Volumes using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/updating-volumes (Portworx Enterprise 3.6)

Updating Volumes using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This section will walk you through the commands for updating your Portworx volumes. Run the `sudo /opt/pwx/bin/pxctl volume update` command with the `--help` flag to list the available subcommands and flags.

## Sharing and unsharing volumes​

You can use the `--sharedv4` flag to share or unshare a given volume across multiple namespaces.

Say we've created a volume named `clitest`. You can see its settings using this command:

```

pxctl volume inspect clitest

```

```

Volume	:  970758537931791410

	Name            	 :  clitest

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Shared          	 :  no

	Status          	 :  up

	State           	 :  detached

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  33 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  10.99.117.133

```

Note that the `shared` field is shown as `no`, indicating that `clitest` is not a sharedv4 volume.

Before turning on sharing, make sure no applications are actively using the volume. Kubernetes users can scale down their application pods so that the volume is in a detached state.

Next, let's turn on sharing:

```

pxctl volume update clitest --sharedv4=on

```

At this point, the volume's sharing settings should have been updated. We can easily check by running `pxctl volume inspect` on the volume again:

```

pxctl volume inspect clitest

```

```

Volume	:  970758537931791410

	Name            	 :  clitest

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Shared          	 :  v4

	Status          	 :  up

	State           	 :  detached

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  33 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  10.99.117.133

```

As shown above, the `shared` field is set to `v4` indicating that `clitest` is now a sharedv4 volume.

### Related topics​

- For more information about creating shared Portworx volumes through Kubernetes, refer to the Create sharedv4 PVCs page.

## Changing a volume's sticky option​

For adding the `--sticky` attribute to a volume, use the following command:

```

pxctl volume update clitest --sticky=on

```

Doing a subsequent inspect on the volume shows the `attributes` field set to `sticky`:

```

pxctl volume inspect clitest

```

```

Volume	:  970758537931791410

	Name            	 :  clitest

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Creation time   	 :  Feb 26 08:17:20 UTC 2017

	Shared          	 :  yes

	Status          	 :  up

	State           	 :  detached

	Attributes      	 :  sticky

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  33 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  10.99.117.133

```

## Increase volume size​

Here is an example of how to increase the size of an existing volume.

First, let’s create a volume with the default parameters (1 GiB):

```

pxctl volume create vol_resize_test

```

```

Volume successfully created: 485002114762355071

```

Next, we would want to inspect our new volume:

```

pxctl volume inspect vol_resize_test

```

```

Volume	:  485002114762355071

	Name            	 :  vol_resize_test

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Creation time   	 :  Apr 10 18:53:11 UTC 2017

	Shared          	 :  no

	Status          	 :  up

	State           	 :  detached

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  32 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  172.31.55.104

```

Note the default volume size - 1 GiB.

note

In order to update the size of a given volume, you should first mount it. If it’s a shared volume, then this operation can be done from any of the nodes where the volume is attached.

Now that we've created a new volume, let's attach it to resize it.

```

pxctl host attach vol_resize_test

```

```

Volume successfully attached at: /dev/pxd/pxd485002114762355071

```

With `vol_resize_test` attached, the next steps are to create a new directory:

```

sudo mkdir /var/lib/osd/mounts/voldir

```

and then mount the volume:

```

pxctl host mount --path /var/lib/osd/mounts/voldir vol_resize_test

```

```

Volume vol_resize_test successfully mounted at /var/lib/osd/mounts/voldir

```

Lastly, to update the size of this volume to 5 GB do:

```

pxctl volume update vol_resize_test --size=5

```

```

Update Volume: Volume update successful for volume vol_resize_test

```

Let's verify the size with the following command:

```

pxctl volume inspect vol_resize_test

```

```

Volume	:  485002114762355071

	Name            	 :  vol_resize_test

	Size            	 :  5.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Creation time   	 :  Apr 10 18:53:11 UTC 2017

	Shared          	 :  no

	Status          	 :  up

	State           	 :  Attached: xxxxxxxx-xxxx-xxxx-xxxx-293128e2d78b

	Device Path     	 :  /dev/pxd/pxd485002114762355071

	Reads           	 :  138

	Reads MS        	 :  108

	Bytes Read      	 :  974848

	Writes          	 :  161

	Writes MS       	 :  1667

	Bytes Written   	 :  68653056

	IOs in progress 	 :  0

	Bytes used      	 :  97 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  172.31.55.104

```

### Related topics​

For more information about dynamically resizing a volume (PVC) using Kubernetes and Portworx, refer to the Resize a Portworx PVC page.

## Update a volume's replication factor​

You can use the `pxctl volume ha-update` command to increase or decrease the replication factor for a given Portworx volume.

note

The maximum replication factor is 3.

### Increase the replication factor​

Follow the instructions below to increase a volume's replication factor and create replicas on a node or storage pool:

-
Identify a node or pool you want to create a replica on. The following example uses a node ID found using the `cluster list` command:

```

pxctl cluster list

```

```

Cluster ID: MY_CLUSTER_ID

Status: OK

Nodes in the cluster:

ID					DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION		STATUS

xxxxxxxx-xxxx-xxxx-xxxx-d816357f634b	10.99.117.133	0.5		8.4 GB	7.9 GB		N/A		1.1.6-a879596	Online

xxxxxxxx-xxxx-xxxx-xxxx-0dc1c09781d8	10.99.117.137	0.250313	8.4 GB	7.9 GB		N/A		1.1.6-a879596	Online

xxxxxxxx-xxxx-xxxx-xxxx-55c967d1a963	10.99.117.135	0.625782	8.4 GB	7.9 GB		N/A		1.1.6-a879596	Online

```

-
Begin replicating your volume to your target node or storage pool by entering the following `pxctl volume ha-update` command, specifying:

- `--repl=` with the new number of replicas you want to create. This must be equal to your volume's current replication factor plus one.

- `--node` with the node ID, node IP address, or pool UUID you want to create the replica(s) on.

- The volume you want to increase the replication factor for.

```

pxctl volume ha-update \

--repl=2 \

--node <node-ID|pool-uuid|node-IP>

<volume-name>

```

-
Monitor the replication operation by entering the following `pxctl alerts show` command:

```

pxctl alerts show --type volume

```

```

AlertID	VolumeID		Timestamp			Severity	AlertType			Description

25	970758537931791410	Feb 26 22:02:04 UTC 2017	NOTIFY		Volume operation success	Volume (Id: 970758537931791410 Name: exampleVolume) HA updated from 1 to 2

```

-
Once the replication completes and the new node is added to the replication set, enter the `pxctl volume inspect` command to verify the new replica exists:

```

pxctl volume inspect <volume-name>

```

```

Volume	:  970758537931791410

	Name            	 :  exampleVolume

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  2

	IO Priority     	 :  LOW

	Creation time   	 :  Feb 26 08:17:20 UTC 2017

	Shared          	 :  yes

	Status          	 :  up

	State           	 :  detached

	Attributes      	 :  sticky

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  33 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  10.99.117.133

			Node 	 :  10.99.117.137

```

### Decreasing the replication factor​

The `ha-update` command can be used to reduce the replication factor as well. Follow the instructions below to decrease a volume's replication factor and remove replicas from a node or storage pool:

-
Begin removal of your volume's replica from your target node or storage pool by entering the following `pxctl volume ha-update` command, specifying:

- `--repl=` with the new number of replicas. This must be equal to your volume's current replication factor minus one.

- `--node` with the node ID, node IP address, or pool UUID you want to remove a replica from.

- The volume you want to decrease the replication factor for.

```

pxctl volume ha-update  \

--repl=1 \

--node <node-ID|pool-uuid|node-IP> \

<volume-name>

```

```

Update Volume Replication: Replication update started successfully for volume exampleVolume

```

-
Monitor the replication operation by entering the following `pxctl alerts show` command:

```

pxctl alerts show --type volume

```

```

26	970758537931791410	Feb 26 22:58:17 UTC 2017	NOTIFY		Volume operation success	Volume (Id: 970758537931791410 Name: exampleVolume) HA updated

```

-
Once the replica reduction completes, enter the `pxctl volume inspect` command to verify the target replica has been removed:

```

pxctl volume inspect exampleVolume

```

```

Volume	:  970758537931791410

	Name            	 :  exampleVolume

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Creation time   	 :  Feb 26 08:17:20 UTC 2017

	Shared          	 :  yes

	Status          	 :  up

	State           	 :  detached

	Attributes      	 :  sticky

	Reads           	 :  0

	Reads MS        	 :  0

	Bytes Read      	 :  0

	Writes          	 :  0

	Writes MS       	 :  0

	Bytes Written   	 :  0

	IOs in progress 	 :  0

	Bytes used      	 :  33 MiB

	Replica sets on nodes:

		Set  0

			Node 	 :  10.99.117.133

```

## Update a volume's group ID​

To update or a new group ID to a volume, enter the `pxctl volume update` command with the `--group` option and the new group name:

```

pxctl volume update --group <groupName> <volumeName>

```

```

Update Volume: Volume update successful for volume exampleVolume

Warning: Updating group field will not affect the replica placement of already provisioned volumes.

```

## Access a sharedv4 volume from additional IP addresses​

By default, `sharedv4` volumes can be accessed from the specific data interface IPs on Portworx nodes. To specify additional IP addresses, add the `allow_ips` label to the volume you want to allow access to, specifying a semicolon-separated list of IP addresses.

```

pxctl volume update <vol_name> --label "allow_ips=<Kubernetes-IP-1>;<Kubernetes-IP-2>"

```

You can also specify `allow_ips` as a parameter in a StorageClass.

For example:

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: px-sharedv4-ipv6-example

parameters:

  repl: "2"

  allow_ips: "allow_ips=<Kubernetes-IP-1>;<Kubernetes-IP-2>"

...

```

## Enable NFSv4 for a sharedv4 volume​

By default, sharedv4 volumes use the NFSv3 protocol. You can instruct Portworx to use NFSv4 for a specific sharedv4 volume by adding the following label:

```

pxctl volume update <vol_name> --label nfs_v4=true

```

In this topic:
