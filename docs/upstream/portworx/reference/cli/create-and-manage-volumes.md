# Create and manage volumes using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/create-and-manage-volumes (Portworx Enterprise 3.6)

Create and manage volumes using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This topic explains how to create and manage volumes using the `pxctl` CLI tool. To view a list of the `pxctl` commands, run one of the following from a worker node:

```

export PATH=$PATH:/opt/pwx/bin

pxctl volume --help

```

```

/opt/pwx/bin/pxctl volume --help

```

Alternatively, you can run the following commands anywhere you can access your Kubernetes cluster. First, set an environment variable containing the name of one of your Portworx worker nodes:

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

```

Then you can run `pxctl` commands through `kubectl exec` as follows:

```

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl volume --help

```

The following sections explain the individual `pxctl` commands.

## Create volumes​

Portworx creates volumes from the global capacity of a cluster. You can expand the capacity and throughput of your cluster by adding new nodes to the cluster. Portworx protects your volumes from hardware and node failures through automatic replication.

Consider the following capabilities of Portworx when creating a new volume using the `pxctl` CLI:

- Durability: Set the replication level through policy, using the `High Availability` setting. For more information, see storage policy.

- Portworx synchronously replicates each write operation to a quorum set of nodes.

- Portworx uses an elastic architecture. This allows you to add capacity and throughput at every layer, at any time.

- Volumes are thinly provisioned. They only use as much storage as needed by the container.

- You can expand and contract the maximum size of a volume, even after you write data to the volume.

To create a volume, run the `pxctl volume create` command and provide the volume name. The following example creates the `myVol` volume:

```

pxctl volume create myVol

```

```

3903386035533561360

```

note

Portworx controls the throughput at per-container level and can be shared. Volumes have fine-grained control, set through policy.

Before proceeding to the next sections, understand the following concepts:

- Throughput is set by the IO Priority setting. Throughput capacity is pooled.

- If you add a node to the cluster, you expand the available throughput for read and write operations.

- Portworx selects the best node to service read operations, no matter that the operation is from local storage devices or the storage devices attached to another node.

- Read throughput is aggregated, where multiple nodes can service one read request in parallel streams.

- Fine-grained controls: Policies are specified per volume and provide full control to storage.

- Policies enforce how the volume replicates across the cluster, IOPs priority, filesystem, blocksize, and additional parameters described below.

- Policies are specified at create time, and you can apply them to the existing volumes.

The `pxctl` CLI tool provides options for setting the policies on a volume. Run the `pxctl volume create ` command with the `--help` flag to view the available options.

note

You can also pass these options through the scheduler.

### Create volumes with a specific filesystem formatting​

You can use the `pxctl volume create` command with the `--fs` option to specify your desired filesystem (ext4 or xfs) and `--fs_format_options` to specify your desired filesystem formatting options for the specified filesystem.

Use it only for volumes that are formatted with either ext4 or xfs filesystems.

Here are a few examples for specifying different filesystems and filesystem formatting options for a volume:

- EXT4: `pxctl volume create vol3 --fs ext4 --fs_format_options "-i 8192"`. To see all the formatting options for ext4, see the mkfs man page.

- EXT4: `pxctl volume create vol2 --fs ext4 --fs_format_options "-N 128000"`. To see all the formatting options for ext4, see the mkfs.ext4 man page.

- XFS: `pxctl volume create vol9 --fs xfs --fs_format_options "-q -i size=1024"`. To see all the formatting options for ext4, see the [mkfs.xfs man page](: https://linux.die.net/man/8/mkfs.xfs).

Alternatively, run `man mkfs.ext4` or `man mkfs.xfs` on linux terminal to see the man page details.

### Place a replica on a specific node​

Use the `--nodes=LocalNode` flag to create a volume and place at least one replica of the volume on the node where the command is run. This is useful when you use a script to create a volume locally on a node.

note

You can provide a node ID, node IP address, or pool UUID to the `--nodes` flag.

For example, run the following command to create the `localVolume` volume and place a replica of the volume on the local node:

```

pxctl volume create --nodes=LocalNode localVolume

```

```

Volume successfully created: 756818650657204847

```

The following command helps you to check if the replica of the volume is on the node where the command was run:

```

pxctl volume inspect localVolume

```

```

Volume  :  756818650657204847

        Name                     :  localVolume

        Size                     :  1.0 GiB

        Format                   :  ext4

        HA                       :  1

        IO Priority              :  LOW

        Creation time            :  Mar 20 00:30:05 UTC 2019

        Shared                   :  no

        Status                   :  up

        State                    :  detached

        Reads                    :  0

        Reads MS                 :  0

        Bytes Read               :  0

        Writes                   :  0

        Writes MS                :  0

        Bytes Written            :  0

        IOs in progress          :  0

        Bytes used               :  340 KiB

        Replica sets on nodes:

                Set 0

                  Node           : X.X.X.90 (Pool 1)

        Replication Status       :  Detached

```

note

The replicas are visible in the `Replica sets on nodes` section of the command output.

```

pxctl volume list --name opt_example

```

```

ID			NAME		SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	STATUS		SNAP-ENABLED

282820401509248281	opt_example	1 GiB	1	no	no		LOW		up - detached	no

```

The `pxctl` CLI utility supports the following key-value pairs:

```

IO priority      - io_priority=[high|medium|low]

Volume size      - size=[1..9][G|M|T]

HA factor        - repl=[1,2,3]

Block size       - bs=[4096...]

Shared volume    - shared=true

File System      - fs=[xfs|ext4]

Encryption       - passphrase=secret

snap_schedule    - "periodic=mins#k;daily=hh:mm#k;weekly=weekday@hh:mm#k;monthly=day@hh:mm#k" where k is the number of snapshots to retain.

```

## The global namespace​

Through sharedv4 volumes (also known as a global namespace), a single volume’s filesystem is concurrently available to multiple containers running on multiple hosts.

note

- There is no inherent limit imposed by Portworx on the number of pods that can be attached to a sharedv4 service-based volume. However, the actual limit is dependent on factors such as cluster size and available resources. Pod scaling may also be constrained by the maximum number of pods allowed per node, as dictated by Kubernetes. It is important to monitor and optimize cluster resources to ensure stable performance at higher pod counts.

- Portworx does not support Kerberos with sharedv4 volumes.

- You do not need to use sharedv4 volumes to have your data accessible on any host in the cluster. Any Portworx volumes can be exclusively accessed from any host as long as they are not simultaneously accessed. Sharedv4 volumes are for providing simultaneous (concurrent or shared) access to a volume from multiple hosts at the same time.

- You do not necessarily need a replication factor of greater than 1 on your volume in order for it to be shared. Even a volume with a replication factor of 1 can be shared on as many nodes as there are in your cluster.

- IOPS might be misleading when using sharedv4 volumes due to batching of small blocksize I/Os into a larger one before I/O reaches the `pxd` device. Bandwidth is more consistent.

- When multiple pods on the same node mount the same Sharedv4 (NFS) volume, Portworx traditionally performs a separate NFS mount for each pod. This can lead to several issues, including redundant NFS connections, an increased number of mount table entries, higher kernel overhead, and more complex unmount operations. To address these limitations, Portworx uses sentinel mounts which creates a single, shared NFS mount per volume per node. For more information, see Configure sentinel mount cleanup interval and timeout.

A typical pattern is for a single container to have one or more volumes. Conversely, many scenarios would benefit from multiple containers being able to access the same volume, possibly from different hosts. Accordingly, the shared volume feature enables a single volume to be read/write accessible by multiple containers. Example use cases include:

- A technical computing workload sourcing its input and writing its output to a sharedv4 volume.

- Scaling a number of Wordpress containers based on load while managing a single sharedv4 volume.

- Collecting logs to a central location.

note

Usage of sharedv4 volumes for databases is not recommended because they have a small metadata overhead. Additionally, typical databases do not support concurrent writes to the underlying database at the same time.

## Sharedv4 failover and failover strategy​

When the node which is exporting the sharedv4 or sharedv4 service volume becomes unavailable, there is a sharedv4 failover. After failover, the volume is exported from another node which has a replica of the volume.

Failover is handled slightly differently for sharedv4 volumes than for sharedv4 service volumes:

- When a sharedv4 volume fails over, all of the application pods are restarted.

- For sharedv4 service volumes, only a subset of the pods need to be restarted. These are the pods that were running on the 2 nodes involved in failover: the node that became unavailable, and the node that started exporting the replica of the volume. The pods running on the other nodes do not need to be restarted.

The failover strategy determines how quickly the failover will start after detecting that the node exporting the volume has become unavailable. The `normal` strategy waits for a longer duration than the `aggressive` strategy.

### Sharedv4 volumes​

The default failover strategy for sharedv4 volumes is `normal`. This gives the unavailable node more time to come back up after a transient issue. If the node comes back up during the grace period allowed by the `normal` failover strategy, there is no need to restart the application pods.

If an application with a sharedv4 volume is able to recover quickly after a restart, it may be more appropriate to use the `aggressive` failover strategy even for a sharedv4 volume.

### Sharedv4 service volumes​

A sharedv4 service volume is mounted through a Kubernetes service (ClusterIP) rather than through the address of a specific node. The ClusterIP is a stable front end: Portworx maps it to the data IP of the node that is currently exporting the volume. Because the ClusterIP itself does not change when the export moves to a different node, application pods keep their mounts across a failover.

This seamless failover depends on NFS version 4.0, which is the default protocol version for sharedv4 service volumes. NFS 4.1 and 4.2 clients consolidate connections to the same server: if two sharedv4 service volumes have two different ClusterIPs that currently resolve to the data IP of the same exporting node, a 4.1 or 4.2 client collapses both mounts into a single connection to that one server. NFS 4.0 does not apply this optimization; it resolves each ClusterIP independently.

That consolidation breaks during a failover. If the exporting node becomes unavailable and the two volumes fail over to two different nodes, their ClusterIPs must now resolve to two different data IPs, but the client is still using the single consolidated connection. For this reason, seamless failover is not possible over NFS 4.1 or 4.2.

The default failover strategy for sharedv4 service volumes is `aggressive`, because these volumes are able to fail over without restarting all the application pods.

These defaults can be changed in the following ways:

-
Setting a value for `sharedv4_failover_strategy` in StorageClass before provisioning a volume.

-
Using a `pxctl volume update` command if a volume has been provisioned already. For example:

```

pxctl volume update --sharedv4_failover_strategy=normal <volume_ID>

```

### Sharedv4 service volume hyperconvergence​

When you set the `stork.libopenstorage.org/preferRemoteNode` parameter in the StorageClass as `false`, Stork will deactivate anti-hyperconvergence for sharedv4 service volumes generated with this StorageClass, and the value of the `stork.libopenstorage.org/preferRemoteNodeOnly` parameter will be ignored.

note

- The `stork.libopenstorage.org/preferRemoteNode` parameter is supported from the Stork 23.11.0 and newer versions, and the default setting for this parameter is `true`.

- If you want to update the `stork.libopenstorage.org/preferRemoteNode` parameter after creating sharedv4 PVCs, you can update the volume labels using `pxctl volume update --label` command.

### Sharedv4 service pod anti-hyperconvergence​

If you want to prevent pods from needing to bounce upon NFS server failover for `sharedv4` service volumes, you would have to use NFS mountpoints on nodes instead of having pods running on the node with the volume attached as a direct bind mount.

By default, the Stork scheduler places application pods on nodes where `sharedv4` volume replicas do not exist, if such nodes are available. This configuration is known as anti-hyperconvergence, meaning that pods are positioned on different nodes from their volume replicas. In other words, this can be described as the pods using `sharedv4` volumes being anti-hyperconverged with respect to their volume replicas.

note

- You can force a pod using sharedV4 service volumes to be scheduled only on non replica nodes by specifying `stork.libopenstorage.org/preferRemoteNodeOnly: "true"` as a StorageClass parameter. This parameter will strictly enforce this behavior, and application pods will not come up if a valid node is not found.

- If you want to update the `stork.libopenstorage.org/preferRemoteNodeOnly` parameter after creating sharedv4 PVCs, you can update the volume labels using `pxctl volume update --label` command.

### Related topics​

- For information about creating shared Portworx volumes through Kubernetes, refer to the ReadWriteMany and ReadWriteOnce section.

## Delete volumes​

You can delete a specific volume using the `pxctl volume delete ` command. For example, the following command deletes the `myOldVol` volume:

```

pxctl volume delete myOldVol

```

```

Delete volume 'myOldVol', proceed ? (Y/N): y

Volume myOldVol successfully deleted.

```

important

To avoid I/O pauses during deletion and to reclaim storage space on thin-provisioned backends, such as a storage area network (SAN) or a FlashArray, enable non-blocking device delete (NBDD), which performs discards in the background before deleting volumes or snapshots. For more information, see Non-Blocking Device Delete.

## Import volumes​

You can import files from a directory into an existing volume. The existing files on the volume are retained or overwritten.

For example, the following command imports files from the `/path/to/files` directory into `myVol`:

```

pxctl volume import --src /path/to/files myVol

```

```

Starting import of  data from /path/to/files into volume myVol...Beginning data transfer from /path/to/files myVol

Imported Bytes :   0% [>---------------------------------------------------------------------------------------------------------------------------------------] 14ms

Imported Files :   0% [>---------------------------------------------------------------------------------------------------------------------------------------] 16ms

Volume imported successfully

```

## Inspect volumes​

For more information about inspecting your Portworx volumes, see:
 Inspect volumes

## List volumes​

The following command lists all volumes within a cluster:

```

pxctl volume list

```

```

ID			NAME		SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	STATUS				SNAP-ENABLED

951679824907051932	objectstorevol	10 GiB	1	no	no		LOW		up - attached on 192.168.99.101	no

810987143668394709	testvol		1 GiB	1	no	no		LOW		up - detached			no

1047941676033657203	testvol2	1 GiB	1	no	no		LOW		up - detached			no

800735594334174869	testvol3	1 GiB	1	no	no		LOW		up - detached			no

```

## List volumes in a drive​

The following command displays details about volumes that are located on a specific drive:

```

pxctl volume list --cloud-drive-id "[datastore-xxxxx] fcd/<file-name.vmdk>"

```

```

ID                NAME      SIZE      HA    SHARED  ENCRYPTED   PROXY-VOLUME    IO_PRIORITY   STATUS          SNAP-ENABLED

<volume-id>	testvol   10 GiB    2     no      no          no              LOW           up - attached   no

```

This functionality is useful for administrators who need to audit, manage, or troubleshoot storage resources by correlating volumes with their physical or logical storage locations.

## List volumes in trash can​

When the trash can is enabled, you can list volumes in the trash can with the following command:

```

pxctl volume list --trashcan

```

This displays output similar to the following:

```

DELETE TIME                   ID                  NAME                  SIZE   HA  SHARED  ENCRYPTED  IO_PRIORITY  STATUS         DELETE_TIMER

Tue Mar 29 21:51:16 UTC 2022  780196670250220779  newvol-tc-1648590676  1 GiB  1   no      no         LOW          up - detached  9m33s

```

In the sample output above, the trash can volume name is in the format `<original-vol-name>-tc-<original-vol-id>`.

### Related topics​

- To learn how to enable the volume trash can feature on a cluster, see Volume trash can.

## Locate volumes​

The `pxctl volume locate` command displays the mounted location of a volume in the containers running on the node:

```

pxctl volume locate 794896567744466024

```

```

host mounted:

  /directory1

  /directory2

```

In the above example, the `794896567744466024` volume is mounted in two containers through the `/directory1` and `/directory2` mount points.

## Create volume snapshots​

Snapshots are efficient, point-in-time, read-only copies of volumes. You can use snapshots to read data, restore a volume, or create clones.

Portworx supports different snapshot implementations based on the datastore:

- PX-StoreV1: Uses the copy-on-write (CoW) technique.

- PX-StoreV2: Uses the redirect-on-write (RoW) technique.

The redirect-on-write (RoW) technique is generally more efficient than copy-on-write (CoW) for snapshot management because it reduces write overhead and improves storage efficiency.

You can create snapshots in one of the following ways:

- Manually, by running the `pxctl volume snapshot create` command (referred to as user-created snapshots).

- Automatically, by configuring a snapshot schedule for the volume.

Here's an example of how to create a snapshot:

```

pxctl volume snapshot create --name mysnap --label color=blue,fabric=wool myvol

```

```

Volume snap successful: 234835613696329810

```

The string of digits in the output is the volume ID of the new snapshot. You can use this ID(`234835613696329810`) or the name(`mysnap`), to refer to the snapshot in subsequent `pxctl` commands.

The label values allow you to tag the snapshot with descriptive information of your choosing. You can use them to filter the output of the `pxctl volume list` command.

There is an implementation limit of 64 snapshots per volume.

Snapshots are read-only. To restore a volume from a snapshot, use the `pxctl volume restore` command.

### Related topics​

- For information about creating snapshots of your Portworx volumes through Kubernetes, refer to the Create and use snapshots page.

## Clone volumes​

Use the `pxctl volume clone` command to create a volume clone from a volume or snapshot.

To view the in-built help, run the `pxctl volume clone` command with the `--help` flag.

For example, the following command creates the `myvol_clone` clone from the parent `myvol` volume:

```

pxctl volume clone --name myvol_clone myvol

```

```

Volume clone successful: 55898055774694370

```

### Related topics​

- For information about creating a clone from a snapshot through Kubernetes, see the Create Snapshots in Portworx page.

## Restore a volume​

In order to restore a volume from snapshot use the `pxctl volume restore` command:

```

/opt/pwx/bin/pxctl volume restore -h

```

```

Restore volume from snapshot

Usage:

  pxctl volume restore [flags]

Aliases:

  restore, r

Examples:

pxctl volume restore [flags] volName

Flags:

  -h, --help              help for restore

  -s, --snapshot string   snapshot-name-or-ID

Global Flags:

      --ca string            path to root certificate for ssl usage

      --cert string          path to client certificate for ssl usage

      --color                output with color coding

      --config string        config file (default is $HOME/.pxctl.yaml)

      --context string       context name that overrides the current auth context

  -j, --json                 output in json

      --key string           path to client key for ssl usage

      --output-type string   use "wide" to show more details

      --raw                  raw CLI output for instrumentation

      --ssl                  ssl enabled for portworx

```

In the below example parent volume `myvol` is restored from its snapshot `mysnap`. Make sure volume is detached in order to restore from the snapshot.

```

pxctl volume restore --snapshot mysnap myvol

```

```

Successfully started restoring volume myvol from mysnap.

```

To restore a volume from the trash can, specify the --trashcan flag:

```

pxctl volume restore --trashcan trashedvol myvol

```

```

Successfully started restoring volume myvol from trashedvol.

```

### Related topics​

- To learn how to enable the volume trash can feature on a cluster, see Volume trash can.

- For information about restoring a Portworx volume with data from a snapshot through Kubernetes, refer to the Restore snapshots page.

## Update the snap interval of a volume​

Please see the documentation for [snapshots] (/reference/cli/snapshots) for more details.

### Related topics​

- For information about creating scheduled snapshots of a Portworx volume through Kubernetes, refer to the Scheduled snapshots page.

## Show volume stats​

The `pxctl volume stat` command displays the real-time read/write IO throughput:

```

pxctl volume stats mvVol

```

```

TS			Bytes Read	Num Reads	Bytes Written	Num Writes	IOPS		IODepth		Read Tput	Write Tput	Read Lat(usec)	Write Lat(usec)

2019-3-4:11 Hrs		0 B		0		0 B		0		0		0		0 B/s		0 B/s		0		0

```

## Manage volume access rules​

Using `pxctl`, you can manage your volume access rules. See the volume access page for more details.

## Update the replication factor of a volume​

You can use the `pxctl volume ha-update` to increase or decrease the replication factor of a Portworx volume. Refer to the update volumes page for more details.

## Update the settings of a volume​

Using the `pxctl volume update` command, you can update the settings of your Portworx volumes. Refer to the updating volumes page for additional details.

## Volume usage​

To get more information about the usage of your Portworx volumes, run the `pxctl volume usage` command with the name or the ID of your volume:

```

pxctl volume usage 13417687767517527

```

## Understand copy-on-write features​

By default, Portworx uses features present in the underlying file system to take snapshots through copy-on-write and checksum storage blocks.

When using the copy-on-write feature to take snapshots, overwriting a block does not update it in place. Instead, every overwrite allocates or updates a new block, and the filesystem metadata is updated to point to this new block. This technique is called redirect-on-write. When using this feature, a block overwrite almost always involves block updates in multiple areas:

- the target block

- any linked indirect file blocks

- filesystem metadata blocks

- filesystem metadata indirect file blocks

In a background process, separate from the overwrite operation, the old block is freed only if it is not referred by a snapshot or clone. In addition to copy-on-write, the file system checksums all blocks to detect lost writes and stores the checksum values in a different location away from their associated data.

While these combined features increase the integrity of the data stored on the filesystem, they also increase the read and write overhead on the drives that use them. This slows down performance and increases latency during file operations.

Depending on your use-case, you can trade off the integrity copy-on-write features offer for increased performance and lower latency. You can do this on a per-volume basis using the `pxctl` command.

In this topic:
