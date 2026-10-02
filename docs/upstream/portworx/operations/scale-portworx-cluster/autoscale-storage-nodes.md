# Configure Kubernetes Cluster Autoscaler to Autoscale Storage Nodes

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autoscale-storage-nodes (Portworx Enterprise latest)

Configure Kubernetes Cluster Autoscaler to Autoscale Storage Nodes | Portworx Enterprise Documentation

To enable automatic provisioning of storage nodes when autoscaling with Cluster Autoscaler, you need to preconfigure the node template and add the `portworx.io/provision-storage-node="true"` label.

Note: Auto-scaling down is not supported. When using Kubernetes Cluster Autoscaler, make sure that auto-scaling down is disabled. Otherwise, drivesets might get orphaned and Portworx might lose quorum.

## Prerequisites for Cluster Autoscaler​

Before configuring autoscaling for storage nodes, ensure that your Cluster Autoscaler and node pool configuration meet the following prerequisites.

-
Dedicated node pools or node groups are required only on cloud-managed clusters such as Google Kubernetes Engine, Amazon Elastic Kubernetes Service, and Azure Kubernetes Service. These new node pools are needed because you can apply the `portworx.io/provision-storage-node="true"` label only to these new node pools, so that only the new nodes receive this label. You must ensure that the Cluster Autoscaler is set to balance similar node groups to ensure that nodes scale evenly across different node pools. The configuration of this setting varies by cloud provider.

- In Google Kubernetes Engine cluster, set the `--location-policy` flag with the value `BALANCE` in the node pool configuration.

- In Amazon Elastic Kubernetes Service cluster, set the `balance-similar-node-groups` flag to `true` in the Cluster Autoscaler configuration.

- In Azure Kubernetes Service cluster, deploy the Cluster Autoscaler with the `--balance-similar-node-groups` argument.

-
OpenShift cluster does not require creating separate node pools for autoscaling Portworx storage nodes, but you must enable the `balanceSimilarNodeGroups` setting in the Cluster Autoscaler configuration to distribute new nodes evenly across zones so that each zone contains approximately the same number of nodes.

### Configure Kubernetes Cluster Autoscaler to create new storage nodes automatically​

In an environment where the Cluster Autoscaler is enabled, you can link the autoscaler to one or more `nodePools` or `machineSets`. To ensure that autoscaled nodes come up as storage nodes, preconfigure the node template by adding the `portworx.io/provision-storage-node="true"` label. This ensures that each node created from that template starts as a storage node by triggering the creation of a new driveset.
 If the `portworx.io/provision-storage-node="true"` label is present on the autoscaled node, the node initially comes up as a storageless node. After the initial wait time, Portworx performs safety checks. If the checks pass, Portworx creates a new driveset and provisions the node as a storage node.

To bring up autoscaled nodes as storageless, omit the label from the node pool's template. Do not set the `portworx.io/provision-storage-node` label as `false` in the node template. If the label is missing, the node comes up as a storageless node and remains that way. To convert the node to a storage node, you must manually add the `portworx.io/provision-storage-node="true"` label to the node.

You can also increase the number of storage nodes manually by adding the `portworx.io/provision-storage-node="true"` label to existing storageless nodes. This operation skips the wait time. Portworx performs safety checks to ensure that all existing storage nodes are online, then automatically restarts the node, creates a driveset, and brings it up as a storage node.

Note: In vSphere Cloud Drive setups, when a node is down (but not marked unhealthy), any new node added by the Cluster Autoscaler may remain storage-less due to Portworx safety checks. Since vSphere drives stay attached to the down node, the new node cannot attach those drives and will not convert to a storage node.

### Considerations when upgrading the Kubernetes platform using the surge nodes mechanism​

If you are using the autoscaling feature, where the `portworx.io/provision-storage-node="true"` label is added to the node pool template and if you upgrade the Kubernetes platform using the surge nodes mechanism, the new surge nodes will inherit the `portworx.io/provision-storage-node="true"` label. The addition of this label on the new nodes acts as a one time request for Portworx to provision them as new storage nodes. Portworx waits for 15 minutes and performs a safety checks. During this interval, if the older nodes do not go down, the safety checks will pass and the new surge nodes instead of picking up the drivesets of the old nodes, will be provisioned as new storage nodes. This might lead to orphaning of drivesets and Portworx clusters losing quorum.

To prevent this issue, add the `portworx.io/suspend-storage-node-provisioning="true"` annotation to the StorageCluster metadata before starting the upgrade, and remove the annotation after the upgrade is complete.

In this topic:
