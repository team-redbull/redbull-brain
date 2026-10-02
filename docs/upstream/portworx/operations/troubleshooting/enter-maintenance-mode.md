# Enter Maintenance Mode

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/enter-maintenance-mode (Portworx Enterprise latest)

Enter Maintenance Mode | Portworx Enterprise Documentation

This guide describes a recommended workflow for putting a Portworx node in maintenance mode in your Kubernetes or OpenShift cluster.

### Step 1. Migrate application pods using Portworx volumes that are running on this node​

Before putting Portworx in maintenance mode on a node, applications running on that node using Portworx need to be migrated. If Portworx is in maintenance mode, existing application pods will end up with read-only volumes and new pods will fail to start.

Perform the following steps to migrate select pods:

- Kubernetes

- Openshift

-
Cordon the node using:

```

kubectl cordon <node>

```

-
Delete the application pods using Portworx volumes using:

```

kubectl delete pod <pod-name>

```

-
Cordon the node using:

```

oc adm cordon <node>

```

-
Delete the application pods using Portworx volumes using:

```

oc delete pod <pod-name>

```

Since application pods are expected to be managed by a controller like `Deployment` or `StatefulSet`, Kubernetes will spin up a new replacement pod on another node.

note

When a node is cordoned, the applications running on it are terminated, leading to the detachment of any ReadWriteOnce (RWO) volumes they were using. However, the same node might also serve as the coordinator for a ReadWriteMany (RWX) volume, where applications on other nodes are actively consuming the volume attached to this node.

If the node enters maintenance mode without properly draining the volume attachment, those remote applications might experience I/O disruptions or downtime.

To avoid this, before placing a node in maintenance mode, check whether any volumes—especially RWX volumes—are currently attached to it. If so, restart Portworx on the node first by running `px/service=restart` before proceeding with maintenance mode. This ensures that volumes capable of finding an alternate server can be safely reattached to another node without disrupting I/O operations.

### Step 2. Enter maintenance mode​

```

pxctl service maintenance --enter

```

This takes Portworx out of an “Operational” state for a given node. Perform whatever maintenance tasks are needed.

note

Entering maintenance mode makes the storage on that node temporarily unavailable. As a result, any active CloudSnap backup or Async DR migration that is processing a volume on the node can fail with a storage error, such as `Failed to get diff extents`.
Before entering maintenance mode, run `pxctl cloudsnap status` and check for operations in the `Backup-Active` or `Restore-Active` state on the node. Wait for any active operations to complete before proceeding. If an operation fails because the node enters maintenance mode, the operation is retried for the affected volumes at the next interval of the snapshot schedule or `MigrationSchedule`.

### Step 3. Exit maintenance mode​

Once you are done with maintenance tasks, run:

```

pxctl service maintenance --exit

```

This puts Portworx back in to “Operational” state for a given node.

### Step 4. Uncordon the node​

You can now uncordon the node using:

- Kubernetes

- Openshift

```

kubectl uncordon <node>

```

```

oc adm uncordon <node>

```

In this topic:
