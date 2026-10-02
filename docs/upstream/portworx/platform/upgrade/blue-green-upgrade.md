# Upgrade Portworx Cluster using the Blue-Green Method

Source: https://docs.portworx.com/portworx-enterprise/platform/upgrade/blue-green-upgrade (Portworx Enterprise latest)

Upgrade Portworx Cluster using the Blue-Green Method | Portworx Enterprise Documentation

This document explains how to upgrade your Portworx cluster using the blue-green method. The blue-green upgrade method may be automatically run by your cloud provider or Kubernetes management system, or you could also use this method to upgrade your cluster manually.

note

Portworx Operator does not support the Blue-green upgrade feature available in the Google Kubernetes Engine (GKE) dashboard.

Once you start the license expansion, the Portworx cluster's license will temporarily be extended to accommodate up to double the number of licensed nodes. While the existing nodes (blue nodes) serve production traffic, Portworx will expand the cluster by adding the new nodes (called green nodes) that have upgraded Linux OS or the new hardware.

Once the green nodes are added to the cluster, you must decommission the old nodes (blue nodes), and the application pods, storage volumes and their replicas are moved to the green nodes. Note that Portworx will automatically move cloud drives. For directly attached storage, contact the Portworx support team for assistance.

Once the upgrades are complete, decommission the blue nodes to avoid any issues after upgrades.

## Prerequisites​

- Portworx version 3.0.0 or newer.

- An active `PX-Enterprise` license.

- The `PX-Enterprise` license has not been expanded in 24 hours.

- During a blue-green upgrade, add the `portworx.io/suspend-storage-node-provisioning="true"` annotation to storageCluster metadata before starting the upgrade. Remove the annotation once the upgrade is complete. If Blue-Green License Expansion is enabled in Portworx, this annotation is not required. For more information, see the Manage storage nodes topic.

## Upgrade your cluster​

-
Run the following command to expand your `PX-Enterprise` license:

```

pxctl license expand --start

```

```

Successfully initiated license expansion

```

Once activated, the number of licensed nodes in the cluster will temporarily increase up to twice the original number for a period of seven days.
 All new nodes will operate with the same licensed features as the originally licensed nodes, which includes the ability to create new volumes, volume replicas, and snapshots.

-
Check the status of your Portworx license:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Healthy

Metering: Disabled or Unhealthy

License: PX-Enterprise VM+ Limited (expires in 7 days)

...

Cluster Summary

    Cluster ID: px-cluster-bglicense

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-aced4d3436e4

    Scheduler: kubernetes

    Total Nodes: 3 node(s) with storage (3 online), 1 node(s) without storage (1 online)

    IP		      ID	            				     SchedulerNodeName	Auth		StorageNode	Used	 Capacity	Status	StorageStatus	Version		      Kernel				        OS

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-a873327ac689	smxxxxxxx-30-3		Disabled	Yes		    12 GiB   397 GiB    Online	Up		        3.0.0.0-8c0abdb	  3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-47bc13d55961	smxxxxxxx-30-4		Disabled	Yes		    12 GiB   397 GiB	Online	Up		        3.0.0.0-8c0abdb   3.10.0-1160.80.1.el7.x86_64   CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-caf453d43549	smxxxxxxx-30-2		Disabled	Yes		    12 GiB   397 GiB	Online	Up (This node)	3.0.0.0-8c0abdb	  3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-13865e76d480	smxxxxxxx-30-1		Disabled	No		    0 B      0 B		Online  No Storage	    3.0.0.0-8c0abdb   3.10.0-1160.80.1.el7.x86_64   CentOS Linux 7 (Core)

      ...

```

You will notice that your Portworx cluster has been temporarily expanded, and this expansion will be valid for a period of 7 days. You can also see the blue nodes (`smxxxxxxx-30-2`, `smxxxxxxx-30-3`, and `smxxxxxxx-30-4`) that are storage nodes.

-
Add green nodes to the cluster (that have upgraded Linux OS or the new hardware) as storageless nodes.

-
Verify if these nodes are added as storageless nodes by running the following command:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Healthy

Metering: Disabled or Unhealthy

License: PX-Enterprise VM+ Limited (expires in 7 days ; NOTICE: License expansion expires in 6d, 23h, 53m)

...

Cluster Summary

    Cluster ID: px-cluster-bglicense

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-aced4d3436e4

    Scheduler: kubernetes

    Total Nodes: 3 node(s) with storage (3 online), 5 node(s) without storage (5 online)

    IP		     ID					                    SchedulerNodeName	Auth	   StorageNode    Used     Capacity	        Status  StorageStatus	   Version	        Kernel				         OS

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-a873327ac689	smxxxxxxx-30-3		Disabled	Yes		      12 GiB   397 GiB		    Online	Up		          3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-47bc13d55961	smxxxxxxx-30-4		Disabled	Yes		      12 GiB   397 GiB		    Online	Up		          3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-caf453d43549	smxxxxxxx-30-2		Disabled	Yes		      12 GiB   397 GiB		    Online	Up (This node)	  3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-f06bc091ee55	smxxxxxxx-30-8		Disabled	No		      0 B	   0 B		        Online  No Storage 	      3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-56dc7d48ef6c	smxxxxxxx-30-6		Disabled	No		      0 B	   0 B		        Online  No Storage	      3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-13865e76d480	smxxxxxxx-30-1		Disabled	No		      0 B	   0 B		        Online  No Storage	      3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-5d6953b7f35c	smxxxxxxx-30-7		Disabled	No		      0 B	   0 B		        Online  No Storage	      3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-368171233a4a	smxxxxxxx-30-5		Disabled	No		      0 B	   0 B		        Online  No Storage	      3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

...

```

You can see your blue and green nodes, and the newly added nodes (`smxxxxxxx-30-5`, `smxxxxxxx-30-6`, `smxxxxxxx-30-7`, and `smxxxxxxx-30-8`) are storageless nodes.

note

After deactivation of the license expansion period, you must reduce the number of nodes back to their original number. Otherwise, you will encounter the `invalid license: cluster over-allocated` error. This will result in failure to create new drives, volumes, and mount more than one volume per node. In order to fix this issue, you must manually decommission any extra nodes in your Portworx cluster. For instructions on decommissioning a node, see Decommission a Node.

### Move your cloud drives to green nodes​

Once you are confident that the green nodes are working correctly, perform the following steps to move your cloud drives from the blue nodes to the green nodes.

#### Get the drives​

Run the following command to list all cloud drives attached to your blue nodes:

```

pxctl cd list-drives

```

- Kubernetes

- Openshift

#### Move the drives​

Once you know which cloud drives are attached to your blue nodes, perform the following steps for each blue node to move them to green nodes:

-
Cordon a blue node:

```

kubectl cordon <blue-node>

```

-
Reschedule application pods using Portworx volumes on different nodes. Since application pods are expected to be managed by a controller like `Deployment` or `StatefulSet`, Kubernetes will spin up a new replacement pod on another node:

```

kubectl delete pod <pod-name> -n <application-namespace>

```

-
From your cloud provider’s console, detach the cloud drives from the blue node using the information from the previous section.

-
Restart a storageless green node:

```

kubectl label node <green-node> px/service=restart --overwrite

```

-
Run the `pxctl status` command to check if the green node is now a storage node:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Healthy

Metering: Disabled or Unhealthy

License: PX-Enterprise VM+ Limited (expires in 7 days ; NOTICE: License expansion expires in 6d, 6h, 40m)

...

Cluster Summary

    Cluster ID: px-cluster-bglicense

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-aced4d3436e4

    Scheduler: kubernetes

    Total Nodes: 3 node(s) with storage (3 online), 4 node(s) without storage (4 online)

    IP		      ID					                SchedulerNodeName    Auth	   StorageNode    Used      Capacity	Status	StorageStatus		   Version		    Kernel				         OS

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-a873327ac689	smxxxxxxx-30-3		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-47bc13d55961	smxxxxxxx-30-4		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-caf453d43549	smxxxxxxx-30-7		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-f06bc091ee55	smxxxxxxx-30-8		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-56dc7d48ef6c	smxxxxxxx-30-6		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-13865e76d480	smxxxxxxx-30-1		Disabled	No		      0 B	      0 B		Online	No Storage (This node) 3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-368171233a4a	smxxxxxxx-30-5		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

...

```

You will see that the green node (`smxxxxxxx-30-7`) is now a storage node and the blue node (`smxxxxxxx-30-1`) is a storageless node. Once the blue node is removed from the Kubernetes cluster, it will be automatically decommissioned from the Portworx cluster after a period of time (20 mins by default).

Once all green nodes are converted to storage nodes, use your cloud provider console to verify if the cloud drives are attached to the green nodes, then delete the blue node VMs.

#### Move the drives​

Once you know which cloud drives are attached to your blue nodes, perform the following steps for each blue node to move them to green nodes:

-
Cordon a blue node:

```

oc adm cordon <blue-node>

```

-
Reschedule application pods using Portworx volumes on different nodes. Since application pods are expected to be managed by a controller like `Deployment` or `StatefulSet`, Kubernetes will spin up a new replacement pod on another node:

```

oc delete pod <pod-name> -n <application-namespace>

```

-
From your cloud provider’s console, detach the cloud drives from the blue node using the information from the previous section.

-
Restart a storageless green node:

```

oc label node <green-node> px/service=restart --overwrite

```

-
Run the `pxctl status` command to check if the green node is now a storage node:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Healthy

Metering: Disabled or Unhealthy

License: PX-Enterprise VM+ Limited (expires in 7 days ; NOTICE: License expansion expires in 6d, 6h, 40m)

...

Cluster Summary

    Cluster ID: px-cluster-bglicense

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-aced4d3436e4

    Scheduler: kubernetes

    Total Nodes: 3 node(s) with storage (3 online), 4 node(s) without storage (4 online)

    IP		      ID					                SchedulerNodeName    Auth	   StorageNode    Used      Capacity	Status	StorageStatus		   Version		    Kernel				         OS

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-a873327ac689	smxxxxxxx-30-3		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-47bc13d55961	smxxxxxxx-30-4		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-caf453d43549	smxxxxxxx-30-7		Disabled	Yes		      31 GiB	397 GiB		Online	Up			           3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-f06bc091ee55	smxxxxxxx-30-8		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.xx.xx	xxxxxxxx-xxxx-xxxx-xxxx-56dc7d48ef6c	smxxxxxxx-30-6		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-13865e76d480	smxxxxxxx-30-1		Disabled	No		      0 B	      0 B		Online	No Storage (This node) 3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

    10.xx.x.xxx	xxxxxxxx-xxxx-xxxx-xxxx-368171233a4a	smxxxxxxx-30-5		Disabled	No		      0 B	      0 B		Online	No Storage		       3.0.0.0-8c0abdb	3.10.0-1160.80.1.el7.x86_64	CentOS Linux 7 (Core)

...

```

You will see that the green node (`smxxxxxxx-30-7`) is now a storage node and the blue node (`smxxxxxxx-30-1`) is a storageless node. Once the blue node is removed from the Kubernetes cluster, it will be automatically decommissioned from the Portworx cluster after a period of time (20 mins by default).

Once all green nodes are converted to storage nodes, use your cloud provider console to verify if the cloud drives are attached to the green nodes, then delete the blue node VMs.

In this topic:
