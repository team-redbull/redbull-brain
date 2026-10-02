# IBM Cloud Drives

Source: https://docs.portworx.com/portworx-enterprise/concepts/operate-ibm-cloud-drives (Portworx Enterprise 3.6)

IBM Cloud Drives | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page describes operations and troubleshooting for Portworx clusters on IBM VPC Gen2 Cloud with cloud drives.

## Operate​

### Provision storage nodes​

You can control which nodes are provisioned as storage nodes in the cluster by applying the `portworx.io/provision-storage-node="true"` label. This label directs Portworx to provision the labeled nodes as storage nodes when deploying or expanding your StorageCluster.

For more details, see Provisioning Storage Nodes in Portworx cluster.

### Scale down clusters​

A Portworx cluster on IBM VPC Gen2 with cloud drives can contain a mixture of storage and storageless nodes. When scaling down an IBM IKS/ROKS cluster, do not scale down the cluster size lower than the total number of storage nodes in the Portworx cluster.

You can find out the number of storage nodes by running `pxctl status` on any Portworx node. This lists all nodes in the cluster and specifies which ones are storage nodes.

### Node failure handling​

When Portworx initializes on a node at a high level, it looks for existing cloud drives that are available to use before creating new cloud drives. The creation of a new cloud drive initializes a brand new storage node in the cluster. If a node attaches an existing cloud drive, it will re-use that cloud drive set’s identity and disks. This results in the recovery of the node that was previously used to attach that cloud drive set.

The Portworx node recovery mechanism is essential in the following scenarios:

- A Portworx storage node is terminated and replaced. The reason for termination could be upgrading the OS or its packages, upgrading Kubernetes, or updating the node’s specs. In this case, when the new node comes up, it looks up the available cloud drive set and finds the drive set of the terminated storage node as available (because it’s no longer attached). It then attaches that drive set and resumes the identity of the removed node.

- A Portworx storage node is terminated permanently, or Portworx running on the storage node runs into a failure and does not come up.

In this case, if a storageless Portworx node is present, it detects that the storage node has gone down. The storageless node finds the cloud drive set of the terminated node as available and attaches it to gain the identity of the terminated storage node.

### Portworx storage pool expansion​

See Expand your storage pool size.

## Troubleshoot​

### Recover a node with a deleted VolumeAttachment​

If a VolumeAttachment gets deleted, the node will not boot and will return an error such as `cannot delete va, name: <va-name>`.

To recover from this state, perform a node replace operation from the IBM Cloud UI.

## Related topics​

- Install Portworx on IBM Cloud

- Install Portworx on OpenShift IBM Cloud

In this topic:
