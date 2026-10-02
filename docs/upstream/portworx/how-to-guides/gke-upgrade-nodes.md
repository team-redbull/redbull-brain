# Migrate Google Kubernetes Engine cluster nodes to a different machine type

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/gke-upgrade-nodes (Portworx Enterprise 3.6)

Migrate Google Kubernetes Engine cluster nodes to a different machine type | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

warning

Upgrading a GKE VM instance from `C2` to `C3` machine series with a `pd-standard` disk type is not supported.

If you're running Portworx on GKE and want to migrate to nodes with more resources, you can do this by adding new nodes and retiring old ones. Perform the following steps to migrate nodes:

note

This upgrade method only works if you're using an internal KVDB.

-
Add a new node pool containing your desired node type.

-
Ensure that all nodes in the new node pool have Portworx in storageless mode.

-
Disable auto scaling in the old pool.

-
Choose a node from your old node pool that you want to remove:

```

pxctl cluster list

```

```

Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

Status: OK

Nodes in the cluster:

ID					DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION		STATUS

xxxxxxxx-xxxx-xxxx-xxxx-4782959264bc	X.X.X.243	0.125078	34 GB		33 GB		N/A		1.1.4-6b35842	Online

xxxxxxxx-xxxx-xxxx-xxxx-de2699fa39b4	X.X.X.171	0.187617	34 GB		33 GB		N/A		1.1.4-6b35842	Online

xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5	X.X.X.189	0.125078	34 GB		33 GB		N/A		1.1.4-6b35842	Online

```

-
Once you've chosen a node ID, enter the following `kubectl` command to drain the node, replacing `<node-id>` with the ID of the node that you want to remove:

```

kubectl drain <node-id> --ignore-daemonsets --delete-emptydir-data

```

-
Drain volume attachments:

```

pxctl service node drain-attachments submit --node <node-id>

```

-
Delete the node from Kubernetes:

```

kubectl delete node <node>

```

-
In the GKE console, find the node by name and delete the instance.

-
Choose a storageless node and restart Portworx so that it becomes a storage node:

```

kubectl label <node> px/service=restart --overwrite

```

Wait until the storage node is back up before proceeding.

-
Re-enable attachments on the node:

```

pxctl service node uncordon-attachments --node <node-id>

```

Repeat steps 4 through 10 for each remaining node in your cluster that you want to remove.
