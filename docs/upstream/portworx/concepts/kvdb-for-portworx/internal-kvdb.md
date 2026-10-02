# Internal KVDB for Portworx on Kubernetes

Source: https://docs.portworx.com/portworx-enterprise/concepts/kvdb-for-portworx/internal-kvdb (Portworx Enterprise 3.6)

Internal KVDB for Portworx on Kubernetes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx includes a built-in internal key-value database (KVDB) that eliminates the need for an external KVDB such as etcd. When you install Portworx through Portworx Central, the internal KVDB is enabled by default. Portworx automatically deploys, configures, and manages the internal KVDB cluster.

The internal KVDB runs on three nodes in the Kubernetes cluster and stores Portworx metadata required for cluster operations.

## Prerequisites​

The internal KVDB requires a dedicated drive for data storage. For PX-StoreV1, you can choose either a KVDB drive or a metadata drive. For PX-StoreV2, you must use the metadata drive.

### KVDB drive requirements​

- If IOPS are independent of disk size, Portworx recommends a minimum size of 32 GB and a minimum of 450 IOPS.

- If IOPS are dependent on disk size, Portworx recommends a size of 150 GB to ensure you get a minimum of 450 IOPS.

### Metadata drive requirements​

-
If IOPS are independent of disk size, Portworx recommends a minimum size of 64 GB and a minimum of 450 IOPS.

-
If IOPS are dependent on disk size, Portworx recommends a size of 150 GB to ensure you get a minimum of 450 IOPS.

note

If you use cloud-based storage, size the drive according to your cloud provider’s specifications to meet the minimum IOPS requirements.

## Control internal KVDB node placement​

The `px/metadata-node` label controls which nodes participate in the internal KVDB cluster. By default, Portworx selects the KVDB nodes automatically. To dedicate specific nodes to the internal KVDB, label those nodes with `px/metadata-node=true`.

- Kubernetes

- OpenShift

```

kubectl label nodes <list-of-node-names> px/metadata-node=true

```

```

oc label nodes <list-of-node-names> px/metadata-node=true

```

The following table describes how Portworx interprets the `px/metadata-node` label and its values:

Label configurationBehavior

`px/metadata-node=true`The node is eligible to run the internal KVDB and becomes part of the internal KVDB cluster.

`px/metadata-node=false`The node is excluded from the internal KVDB cluster.

Label not presentIf no other node in the cluster has `px/metadata-node=true`, the node is implicitly eligible to run the internal KVDB. If at least one node has `px/metadata-node=true`, the unlabeled node is excluded from the internal KVDB cluster.

Invalid label value (for example, `px/metadata-node=blah`)Portworx does not start the internal KVDB on the node.

Mixed labels (`px/metadata-node=false` on some nodes, no nodes labeled `px/metadata-node=true`)Nodes labeled `px/metadata-node=false` are excluded from the internal KVDB cluster. The remaining unlabeled nodes are implicitly eligible to run the internal KVDB.

note

For PX-StoreV2, every node requires a metadata disk. You can still use the `px/metadata-node` label to pin the internal KVDB to a selected set of nodes.

## Install Portworx with internal KVDB​

To use the internal KVDB during installation, log in to Portworx Central, select the Built-in option for etcd when creating your Portworx cluster.
Portworx automatically deploys and manages the internal KVDB cluster as part of the installation.

## Internal KVDB cluster recovery​

If a Portworx node that was previously part of the internal KVDB cluster becomes unavailable for more than three minutes, Portworx automatically attempts to restore cluster health by performing the following:

-
Removes the unresponsive node from the internal KVDB cluster.

note

The node remains part of the Portworx cluster.

-
Initializes the internal KVDB on an available Portworx storage node that is not currently part of the KVDB cluster.

-
Adds the new node to the internal KVDB cluster.

## Internal KVDB backup mechanism​

Portworx automatically creates periodic backups of the internal KVDB every two minutes and stores them in the `/var/lib/osd/kvdb_backup` directory on all Portworx nodes, retaining a rolling set of 10 backup files on the internal KVDB drive.

The following is an example of a backup file:

```

ls /var/lib/osd/kvdb_backup

```

```

pwx_kvdb_schedule_153664_2019-02-06T22:30:39-08:00.dump

```

Use these backup files to recover the internal KVDB in disaster recovery scenarios.

caution

Contact Portworx Technical Support to recover your Portworx cluster in the event of a cluster failure, such as:

- When all internal KVDB nodes and the corresponding drives where their data resides are lost and unrecoverable.

- When quorum is lost (two internal KVDB nodes are lost and are unrecoverable).

### Related topics​

- KVDB runtime options

In this topic:
