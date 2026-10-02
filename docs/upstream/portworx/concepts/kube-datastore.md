# Kube Datastore

Source: https://docs.portworx.com/portworx-enterprise/concepts/kube-datastore (Portworx Enterprise latest)

Kube Datastore | Portworx Enterprise Documentation

important

This feature is under Directed Availability. Please engage with your Portworx representative if you are interested and need to enable it in your environment under the current guidelines.

Portworx Kube Datastore (KDS) groups storage pools from the same FlashArray into a logical datastore in a FlashArray Cloud Drive (FACD) deployment. In environments with multiple FlashArrays, Portworx Enterprise creates a separate KDS for each FlashArray. This model allows you to manage and control storage capacity and volume placement at the KDS level.

Portworx Enterprise creates and manages Kube Datastores automatically. You cannot manually create, update, or delete a KDS.

A KDS includes all storage pools associated with its FlashArray, including pools created in earlier versions. It can contain dynamic pools, which support pool failover, and static pools, which do not support pool failover.

When you add a FlashArray and create the first storage pool on it, Portworx Enterprise creates a KDS for that FlashArray. Additional pools created on the same FlashArray are automatically added to the existing KDS.

Portworx Enterprise automatically applies the following labels to pools in a KDS. These labels are managed by Portworx and cannot be added, modified, or removed manually:

LabelValueDescription

`kube_datastore`FlashArray nameIdentifies the KDS associated with the pool. Portworx Enterprise uses this value as the KDS display name.

`kube_datastore_id`FlashArray UUIDUniquely identifies the KDS associated with the pool. Portworx Enterprise uses this value in placement rules to place volumes on a specific KDS.

## Create a Kube Datastore on a specific FlashArray​

Portworx Enterprise creates a Kube Datastore when the first storage pool is provisioned on a FlashArray. To control which FlashArray Portworx uses for a storage pool, specify the `storage_backend` field in the device specification. Set the value to the FlashArray name or management endpoint.

### Create pools from multiple FlashArrays during installation​

To provision a separate storage pool from each FlashArray on every storage node, add a device specification for each FlashArray to the `cloudStorage` section of the `StorageCluster`:

```

spec:

  cloudStorage:

    deviceSpecs:

      - size=100,storage_backend=<fa1-name>

      - size=100,storage_backend=<fa2-management-endpoint>

      - size=200,storage_backend=<fa3-name>

```

This configuration provisions three separate storage pools on each storage node, one from each FlashArray. Portworx creates a separate Kube Datastore for each FlashArray when its first pool is provisioned.

Pool provisioning honors CSI topology. If a device specification includes the `pod` field, Portworx also honors the specified FlashArray pod placement.

note

Portworx Enterprise applies `deviceSpecs` only when provisioning a new storage node. Changes to `deviceSpecs` do not affect existing storage nodes. Similarly, changes that you make to storage pools on an existing node by using `pxctl` are not reflected in the `StorageCluster` specification.

### Create a pool on a FlashArray added to an existing cluster​

To create a storage pool on a FlashArray that you added to an existing Portworx cluster, run the following command on each storage node where you want to create the pool:

```

pxctl service drive add --newpool --spec size=<size>,storage_backend=<fa-name>

```

Replace:

- `<size>` with the pool size.

- `<fa-name>` with the name of the FlashArray.

Portworx Enterprise creates a Kube Datastore for the FlashArray when the first storage pool is provisioned on it. Additional pools provisioned on the same FlashArray are automatically associated with the existing Kube Datastore.

## Kube Datastore affinity​

Kube Datastore affinity lets you place volumes created from a `StorageClass` on a specific KDS. Configure KDS affinity by setting the `kube_datastore_affinity` parameter in the `StorageClass` to the name of the target KDS. Portworx Enterprise then provisions volumes created from that `StorageClass` on pools that belong to the specified KDS.

KDS affinity acts as a placement rule similar to a volume placement strategy (VPS). Portworx honors the KDS affinity during initial volume provisioning and subsequent storage rebalancing operations.

If a volume has other placement rules, including the internal volume affinity rule that Portworx uses to colocate disks for a KubeVirt VM, Portworx combines the rules by using a logical AND.

note

The `kube_datastore_affinity` parameter accepts only one KDS name. You cannot configure a volume with affinity to multiple Kube Datastores.

### How volumes map to Kube Datastores​

KDS affinity specifies where Portworx should place a volume, while the current replica locations indicate where its data resides. Therefore, KDS affinity and current KDS membership might differ.

Portworx considers a volume to be associated with a KDS when either of the following conditions is true:

- The volume has affinity to the KDS through a `replicaAffinity` rule.

- At least one volume replica resides on a pool in the KDS.

A volume can therefore be associated with multiple Kube Datastores. For example:

-
A volume can have affinity to one KDS while its replicas reside on another KDS. The behavior differs by volume type:

- KubeVirt VM disks: Portworx periodically re-evaluates replica placement and moves replicas to pools in the KDS specified by the affinity rule.

- Other volumes: Portworx does not automatically relocate existing replicas. The affinity rule applies only to new and replacement replicas. To move an existing volume to the target KDS, migrate its data to a PVC that uses a StorageClass with affinity to that KDS.

-
A volume has no KDS affinity and has replicas on pools that belong to different Kube Datastores.

### Create a KDS-aware StorageClass​

To place volumes on a specific KDS, create a `StorageClass` and set `kube_datastore_affinity` to the KDS name.

The following example places volumes on the `fa-x90-1a` KDS:

StorageClass

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: px-kds-fa-x90-1a

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  kube_datastore_affinity: "fa-x90-1a"

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

To find the KDS names available in your cluster, see List Kube Datastores. For information about supported `StorageClass` parameters, see Portworx Enterprise StorageClass.

note

- For KubeVirt VMs, you do not need to create KDS-aware StorageClasses manually. The Portworx Operator generates a KDS-aware version of each default KubeVirt `StorageClass` for every KDS in the cluster. For more information, see Kube Datastore-aware StorageClasses.

- If you rename a FlashArray, the name of the KDS associated with it also changes. Recreate any `StorageClass` that references the previous KDS name, and update any user-defined VPS rules that reference that name.

## Migrate VM disks to a different Kube Datastore​

You can use KDS-aware StorageClasses to migrate existing KubeVirt VM disks between Kube Datastores. During storage migration, select the KDS-aware `StorageClass` associated with the destination KDS.

For more information, see Migrate KubeVirt VM disks to a different Kube Datastore.

## List Kube Datastores​

To list the Kube Datastores in your Portworx cluster, run the following command:

```

pxctl kubedatastore list

```

You can also use the `kds` alias:

```

pxctl kds list

```

Example output:

```

NAME            SIZE            AVAILABLE       USED    PROVISIONED     NUMBER OF POOLS

ph530-a25       882 GiB         838 GiB         44 GiB  0 B             6

```

For more information, see pxctl kubedatastore.

note

The `AVAILABLE` value represents the total available capacity across all pools in the KDS. Because this capacity is distributed across multiple pools, the maximum size of an individual volume can be smaller than the reported `AVAILABLE` value.

## Limitations​

Consider the following when you use Kube Datastore:

-
Kube Datastore supports only the FlashArray CloudDrive (FACD) backend.

-
Portworx Enterprise creates a KDS for a new FlashArray only after at least one storage pool is created on that FlashArray.

-
A pool associated with a KDS cannot include drives from another FlashArray.

-
Because KDS affinity requires all replicas of a volume to reside in the same Kube Datastore, the target KDS must have enough storage pools on distinct nodes to satisfy the volume's replication factor.

If the target KDS does not have enough eligible pools on distinct nodes, volume provisioning fails with the following error:

```

could not find enough nodes to provision volume

```

-
The `pxctl kds list` command reports only the current KDS capacity. To monitor historical KDS capacity and performance trends, use the Kube Datastore metrics.

## Related topics​

- Dynamic Pools for Volumes with Replication Factor 1

- Storage pools

- Volume Placement Strategies

- Migrate KubeVirt VM disks to a different Kube Datastore

In this topic:
