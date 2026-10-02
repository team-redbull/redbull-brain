# Migrate KubeVirt VM Disks to a Different Kube Datastore

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/kubevirt-vms/migrate-vm-disks-to-kube-datastore (Portworx Enterprise 3.6)

Migrate KubeVirt VM Disks to a Different Kube Datastore | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

important

This feature is under Directed Availability. Please engage with your Portworx representative if you are interested and need to enable it in your environment under the current guidelines.

You can migrate KubeVirt virtual machine (VM) disks from one Kube Datastore (KDS) to another without recreating the VM. During storage migration, select the KDS-aware `StorageClass` associated with the destination KDS. OpenShift Virtualization copies the data to new persistent volumes provisioned through the selected `StorageClass` and updates the VM to use the new volumes.

You can migrate VM disks between Kube Datastores to:

- Rebalance storage capacity across FlashArrays.

- Move VM storage to a FlashArray that meets different performance or capacity requirements.

- Evacuate storage from a FlashArray before decommissioning it.

note

- You can keep the VM running during storage migration. OpenShift Virtualization might live migrate the VM as part of the storage migration workflow.

- OpenShift Virtualization performs a full copy of each migrated volume. Portworx Enterprise does not offload the copy operation to the FlashArray. VM I/O performance might be reduced while the migration is in progress.

## Prerequisites​

Before you migrate VM disks to another Kube Datastore, ensure that your cluster meets the following requirements:

- Has Portworx Enterprise 3.7.0 or later installed.

- Uses FlashArray Cloud Drive (FACD) as the storage backend.

- Has OpenShift Virtualization 4.18 or later installed.

- Has a node available for live migration. OpenShift Virtualization live migrates the VM to a different node as part of the storage migration.

- Has at least two Kube Datastores. To verify the available Kube Datastores, see List Kube Datastores.

- A KDS-aware `StorageClass` exists for the destination Kube Datastore. For more information, see Kube Datastore-aware StorageClasses.

- The VM is running. You can migrate the disks of one VM at a time.

- The destination Kube Datastore has sufficient available capacity for the VM disks. The source and destination volumes coexist until you delete the source PVCs.

- The destination Kube Datastore has enough storage pools on distinct nodes to satisfy the replication factor configured in the destination `StorageClass`.

- The VM uses the same RWX volume type for all its disks. For more information, see Manage KubeVirt VMs with Portworx.

## Identify the current Kube Datastore​

Before starting the migration, identify the Kube Datastore that contains the VM disks.

-
List the PVCs used by the VM and identify their StorageClasses:

```

oc get pvc -n <namespace>

```

-
Determine the Kube Datastore for each PVC:

-
If the PVC uses a KDS-aware `StorageClass`, use the `StorageClass` name or configuration to identify its Kube Datastore.

-
If the PVC does not use a KDS-aware `StorageClass`, inspect the Portworx volume to identify the storage pools that hold its replicas:

```

pxctl volume inspect <volume-name>

```

Then, inspect the storage pools:

```

pxctl service pool show

```

The `kube_datastore` label identifies the Kube Datastore associated with each pool.

## Migrate the VM disks​

Storage migration is an OpenShift Virtualization workflow. To migrate the VM disks, follow the procedure in Migrating VM disks to a different storage class in the Red Hat OpenShift Container Platform documentation.

When the workflow prompts you for the destination storage class, select the KDS-aware `StorageClass` associated with the Kube Datastore to migrate the disks to. For example, to migrate the disks to the `fa-c20-2c` Kube Datastore, select `px-rwx-block-kubevirt-fa-c20-2c`.

OpenShift Virtualization copies the volume data to persistent volumes provisioned through the selected `StorageClass`. After the migration completes, the VM uses the new volumes on the destination Kube Datastore.

note

To migrate the disks of multiple VMs in a single operation, see Migrating VMs in a single cluster to a different storage class in the Red Hat OpenShift Container Platform documentation. On OpenShift Virtualization versions earlier than 4.20.14, migrating multiple VMs requires Migration Toolkit for Containers (MTC).

## Verify the migration​

After the migration completes:

-
Verify that the VM is running and its disks are accessible.

-
Verify that the migrated PVCs use the KDS-aware `StorageClass` associated with the destination Kube Datastore:

```

oc get pvc -n <namespace>

```

-
Verify that the volume replicas reside on storage pools associated with the destination Kube Datastore:

```

pxctl volume inspect <volume-name>

```

Identify the replica pools, and then run:

```

pxctl service pool show

```

Verify that the `kube_datastore` labels for the replica pools identify the destination Kube Datastore.

-
Verify the Kube Datastore capacity:

```

pxctl kubedatastore list

```

Confirm that the destination Kube Datastore reflects the migrated storage.

## Delete the source PVCs​

OpenShift Virtualization does not delete the source PVCs after a storage class migration completes. Until you delete them, the source volumes continue to consume capacity in the source Kube Datastore.

After you verify that the migration completed successfully, delete each source PVC:

```

oc delete pvc <source-pvc-name> -n <namespace>

```

To confirm that the source Kube Datastore released the capacity, run the following command:

```

pxctl kubedatastore list

```

warning

Delete only the PVCs that the migration replaced. Verify that the VM uses the new volumes and that its disks are accessible before you delete any PVC.

## Related topics​

- Kube Datastore

- Kube Datastore-aware StorageClasses

- Manage Portworx RWX Block Volumes on OpenShift for KubeVirt VMs

- Troubleshooting, Known Issues, and Limitations for KubeVirt VMs

In this topic:
