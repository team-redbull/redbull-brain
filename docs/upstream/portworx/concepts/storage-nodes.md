# Provisioning Storage Nodes in Portworx Cluster

Source: https://docs.portworx.com/portworx-enterprise/concepts/storage-nodes (Portworx Enterprise latest)

Provisioning Storage Nodes in Portworx Cluster | Portworx Enterprise Documentation

To provision nodes as storage nodes in a Portworx cluster, you can either use the `initialStorageNodes` parameter during the Portworx installation or apply the `portworx.io/provision-storage-node="true"` label to request provisioning of specific nodes as storage nodes.

In a standard installation scenario, when you don’t configure any parameters or labels in nodes, all nodes in a cluster are eligible to be storage nodes. Portworx automatically provisions storage nodes and distributes them evenly across the available zones.

In an installation scenario where you only want a limited number of storage nodes, you can use the `initialStorageNodes` parameter to automatically provision the specified number of nodes as storage nodes, evenly across zones. See: Limiting the number of storage nodes in a cluster during installation.

When you want to be very specific and provision certain nodes as storage nodes, you can add `portworx.io/provision-storage-node="true"` label to those nodes. See: Manually provisioning Storage Nodes in a Portworx cluster.

The parameters `maxStorageNodes`, `maxStorageNodesPerZone`, and `maxStorageNodesPerZonePerNodeGroup` are deprecated, and replaced with the `initialStorageNodes` parameter. When scaling a Portworx cluster, the `maxStorageNodesPerZone` parameter needed an increment to add more storage nodes. Instead of this, you can add new nodes and label them with `portworx.io/provision-storage-node="true"` to scale the cluster. In an environment where the cluster autoscaler is enabled, you can link the autoscaler to one or more 'nodePools' or 'machineSets'. To ensure that autoscaled nodes come up as storage nodes, preconfigure the node template by adding the `portworx.io/provision-storage-node="true"` label. This ensures that each node created from that template starts as a storage node automatically. See: Configuring the kubernetes cluster autoscaler to create new storage nodes automatically.

If you are upgrading the Portworx cluster, from version 3.4.x or earlier, any existing values for the deprecated parameters (`maxStorageNodes`, `maxStorageNodesPerZone`, and `maxStorageNodesPerZonePerNodeGroup`) will remain set in your configuration, but it will have no operational effect. These values persist only for backward compatibility. After upgrading, you cannot modify these parameters to new values. You can only unset them. Attempts to set or modify them (on both new and existing clusters) will result in an error.

### Limiting the number of storage nodes in a cluster during installation​

When installing Portworx Enterprise, you might want only a limited number of nodes in the cluster to be provisioned as storage nodes. In this case, you can use the `initialStorageNodes` parameter to set the limit. You can set the `initialStorageNodes` parameter either while generating a customized cluster specification in Portworx Central, or by adding the following to the generated spec:

```

spec:

  cloudStorage:

    deviceSpecs:

    ...

    initialStorageNodes: <custom-value> # Minimum value is 3

```

The Portworx Operator uses the `initialStorageNodes` parameter to determine the total number of storage nodes to create across zones and node pools. It then adds the `portworx.io/provision-storage-node="true"` label to the selected nodes. In a disaggregated setup, the Operator considers only nodes labeled with `portworx.io/node-type=storage` and adds the `portworx.io/provision-storage-node="true"` label to those nodes. After the nodes are provisioned as storage nodes, the `portworx.io/provision-storage-node-handled="true"` label is added to these storage nodes along with the `PortworxNewStorageNodeProvisioned` condition status as `true`.

For example, in a cluster with 3 zones and 3 nodes per zone, if you set `initialStorageNodes` to 6, Portworx will bring up two storage nodes in each zone and add the `portworx.io/provision-storage-node="true"` label to these storage nodes. The remaining nodes will be storageless. Operator ensures that storage nodes are distributed equally across zones. If equal distribution is not possible in at least two zones, the Portworx Operator will halt the installation.

If the `initialStorageNodes` parameter is set during initial deployment, the `portworx.io/provision-storage-node` label must not be present on any of the nodes. If the label is present, the operator will not proceed with Portworx installation.

Setting the `initialStorageNodes` parameter is optional, and is considered by the operator only during the initial installation. It does not affect any future operation.

If the `initialStorageNodes` parameter is not specified during installation, all nodes can come up as storage nodes during the initial deployment. To prevent this, you need to manually add the `portworx.io/provision-storage-node` label to a subset of nodes that need to be defined as storage nodes, and then only these labeled nodes will come up as storage nodes during the initial deployment.

### Manually provisioning storage nodes in a Portworx cluster​

If you want to control which nodes are provisioned as storage nodes, you need to add the `portworx.io/provision-storage-node="true"` label to the node and also remove the `portworx.io/provision-storage-node-handled="true"` label from the node, if it has been set.

Use the following command to perform these two operations at the same time :

```

kubectl label node <node-name> portworx.io/provision-storage-node="true" portworx.io/provision-storage-node-handled-

```

In a disaggregated setup, only nodes labeled with `portworx.io/node-type=storage` are eligible to become storage nodes. However, nodes with `portworx.io/node-type=storage` label are not automatically provisioned as storage nodes. To provision them, you must add the label `portworx.io/provision-storage-node="true"` to the nodes that already have the `portworx.io/node-type=storage` label.

### How nodes are provisioned as storage nodes​

The `portworx.io/provision-storage-node="true"` label for a node acts as a one time request for Portworx to provision the node as a new Portworx storage node. Portworx performs safety checks to ensure all storage nodes are online, and then automatically restarts the node to bring it up as a new storage node by adding the `portworx.io/provision-storage-node-handled="true"` label to the node.

In addition, the `PortworxNewStorageNodeProvisioned` condition is also added to the node object to indicate the result. If the condition status is `true`, the storage node is provisioned successfully. If the status is `false`, the node has not been provisioned as a storage node for the either of the following reasons depending on the status result:

- StoragelessInDisaggregatedSetup - Node must remain as a storageless node in a disaggregated setup.

- FoundExistingDriveset - Cannot provision a new storage node because the current driveset `<uuid>` (2 drives) is not empty.

- MaxProvisionAttemptsReached - Cannot provision a new storage node because the node has already attempted 20 times to provision a storage node.

- RecentDriveSetActivity - Cannot provision a new storage node because the drive set `<uuid>` was (re)attached less than 15 minutes ago.

- DriveSetAttachedToOfflineNode - Cannot provision a new storage node because drive set `<uuid>` is attached to an offline (`<node-status>`) node.

Setting `portworx.io/provision-storage-node="true"` does not guarantee that the node will remain a storage node permanently. If the node later goes down and its driveset fails over to a storageless node, the returning node will remain storageless when it comes back online. Portworx does not automatically reprovision another driveset on it because the node has already been marked as `portworx.io/provision-storage-node-handled="true"` This behavior is different from the deprecated `maxStorageNodesPerZone` parameter. While `maxStorageNodesPerZone` continuously attempted to maintain a target number of storage nodes per zone, the `portworx.io/provision-storage-node` labeling mechanism only triggers a one-time provisioning action, giving you finer control and preventing unwanted automatic rebalancing.

### Converting a KVDB storageless node into a storage node​

A storage node cannot be provisioned on a storageless node that hosts the KVDB. If you need to convert a KVDB storageless node into a storage node, follow this workaround:

- Migrate the KVDB to another node, by adding the `portworx.io/metadata-node=true` label to a different node and stopping the Portworx service on the current node. This will trigger KVDB migration.

- Once the KVDB has moved, restart the Portworx service on the original node. This removes the KVDB drive from the node.

- Convert the node to a storage node, by adding the `portworx.io/provision-storage-node="true"` label to the node. Portworx will perform safety checks and, if all conditions pass, provision storage on the node.

### Best Practices for Provisioning Storage Nodes​

-
If the `initialStorageNodes` parameter is set during initial deployment, the `portworx.io/provision-storage-node` label must not be present on any of the nodes. If the label is present, the operator will not proceed with Portworx installation.

-
To bring up autoscaled nodes as storageless, omit the `portworx.io/provision-storage-node="true"` label from the node pool's template. Do not set the `portworx.io/provision-storage-node` label as `false` in the node template. If the label is missing, the node comes up as a storageless node.

-
If you have a disaggregated setup, only the nodes with `portworx.io/node-type: storage` are eligible to become storage nodes. Add the `portworx.io/provision-storage-node="true"` label to the nodes with `portworx.io/node-type=storage` label. If a node already has the `portworx.io/provision-storage-node="true"` and `portworx.io/provision-storage-node-handled="true"` labels, and you clear the `portworx.io/provision-storage-node-handled` label, the effect is that of reapplying the `portworx.io/provision-storage-node` label.

-
When adding the `portworx.io/provision-storage-node="true"` label to a node, ensure that the `portworx.io/provision-storage-node-handled="true"` label is not set on that node, by using the following command:

```

kubectl label node <node-name> portworx.io/provision-storage-node="true" portworx.io/provision-storage-node-handled-

```

-
You must manually ensure even distribution of storage nodes across zones or node pools.

-
Do not make attempts to set or modify the deprecated parameters (`maxStorageNodes`, `maxStorageNodesPerZone`, and `maxStorageNodesPerZonePerNodeGroup`) in new or existing clusters, as it will result in an error.

-
If you are using the autoscaling feature, where the `portworx.io/provision-storage-node="true"` label is added to the node pool template and if you want to upgrade the Kubernetes platform using the surge nodes mechanism, add the `portworx.io/suspend-storage-node-provisioning="true"` annotation to the StorageCluster metadata before starting the upgrade, and remove the annotation after the upgrade is complete. This is to prevent orphaning of drivesets that might lead to Portworx clusters losing quorum.

In this topic:
