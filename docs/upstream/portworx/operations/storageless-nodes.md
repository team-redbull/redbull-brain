# Storageless nodes with Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/operations/storageless-nodes (Portworx Enterprise 3.6)

Storageless nodes with Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise can be run in a client-only mode such that the storage available in a Portworx can be consumed by apps that are running on nodes that have no storage. This enables deployments to leverage the powerful Portworx Enterprise features from any node without having to rely on legacy protocols and adopt containerization faster.

## Add a new storageless node to your Portworx cluster​

### Display the status of your Portworx cluster​

```

pxctl status

```

```

Status: PX is operational

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-c9d0eb597668

	IP: X.X.X.185

 	Local Storage Pool: 1 pool

	Pool	IO_Priority	Size	Used	Status	Zone	Region

	0	LOW		100 GiB	1.0 GiB	Online	default	default

	Local Storage Devices: 1 device

	Device	Path				Media Type		Size	Last-Scan

	0:1	/dev/mapper/volume-a9e55549	STORAGE_MEDIUM_SSD	100 GiB08 Jan 17 23:15 UTC

	total					-			100 GiB

Cluster Summary

	Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

	Node IP: X.X.X.185 - Capacity: 1.0 GiB/100 GiB Online (This node)

	Node IP: 10.99.117.129 - Capacity: 1.2 GiB/100 GiB Online

	Node IP: X.X.X.197 - Capacity: 2.0 GiB/320 GiB Online

	Node IP: 10.99.119.1 - Capacity: 1.2 GiB/100 GiB Online

Global Storage Pool

	Total Used    	:  5.3 GiB

	Total Capacity	:  620 GiB

```

### Add a new node to this cluster with no storage​

As shown in the command below, a new node is added to the cluster by using the same cluster token which is formed by the cluster id of the existing cluster (which is `xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002` as shown above):

```

docker run --restart=always --name px-enterprise -d --net=host --privileged=true -v /run/docker/plugins:/run/docker/plugins \

-v /var/lib/osd:/var/lib/osd:shared -v /dev:/dev -v /etc/pwx:/etc/pwx -v /opt/pwx/bin:/export_bin:shared \

-v /var/run/docker.sock:/var/run/docker.sock -v /mnt:/mnt:shared -v /var/cores:/var/cores -v /usr/src:/usr/src \

portworx/px-enterprise -m team0:0 -d team0 -z

```

The `-z` option in the command above starts this node as a zero storage node.

note

If you already have `config.json` in `/etc/pwx/`, the `config.json` settings will take precedence over the `-z` option. If your deployment or automation scripts place the file on every node, make sure to remove it in order for `-z` option to take effect.

### Display the cluster node list​

```

pxctl cluster list

```

```

Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

Status: OK

Nodes in the cluster:

ID					DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION		STATUS

xxxxxxxx-xxxx-xxxx-xxxx-c9d0eb597668	X.X.X.185	0.625782	8.4 GB	8.0 GB		N/A		1.1.3-b33d4fa	Online

xxxxxxxx-xxxx-xxxx-xxxx-d3478c485a61	10.99.119.1	0.625		8.4 GB	8.0 GB		N/A		1.1.3-b33d4fa	Online

xxxxxxxx-xxxx-xxxx-xxxx-a74ee09030e3	X.X.X.55	16.20603	8.4 GB	8.0 GB		N/A		1.1.3-b33d4fa	Online

xxxxxxxx-xxxx-xxxx-xxxx-3e2b01cd0bc3	X.X.X.197	0.375469	8.4 GB	7.9 GB		N/A		1.1.3-b33d4fa	Online

xxxxxxxx-xxxx-xxxx-xxxx-dd5084dce208	10.99.117.129	0.749064	8.4 GB	8.0 GB		N/A		1.1.3-b33d4fa	Online

```

### Check node and cluster status​

The status below shows that the new node (X.X.X.55) is the zero storage node that has been added to the cluster

```

pxctl status

```

```

Status: PX is operational

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-a74ee09030e3

	IP: X.X.X.55

 	Local Storage Pool: 0 pool

	Pool	IO_Priority	Size	Used	Status	Zone	Region

	No storage pool

	Local Storage Devices: 0 device

	Device	Path	Media Type	Size		Last-Scan

	No storage device

	total		-	0 B

Cluster Summary

	Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

	Node IP: X.X.X.55 - Capacity: 0 B/0 B Online (This node)

	Node IP: X.X.X.197 - Capacity: 2.0 GiB/320 GiB Online

	Node IP: 10.99.117.129 - Capacity: 1.2 GiB/100 GiB Online

	Node IP: X.X.X.185 - Capacity: 1.0 GiB/100 GiB Online

	Node IP: 10.99.119.1 - Capacity: 1.2 GiB/100 GiB Online

Global Storage Pool

	Total Used    	:  5.3 GiB

	Total Capacity	:  620 GiB

```

In this topic:
