# Installation of Portworx to use FlashArray Direct Access volumes with ActiveCluster setup

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage/flasharray/install-flasharray-active-cluster-fada (Portworx Enterprise 3.6)

Installation of Portworx to use FlashArray Direct Access volumes with ActiveCluster setup | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports ActiveCluster with FlashArray direct access (FADA) volumes using either the iSCSI or FC protocol. Portworx doesn't support FlashArray cloud drives (FACD) with an ActiveCluster setup, and you must pre-provision drives before installing Portworx.

ActiveCluster is Everpure’s synchronous replication technology for FlashArray. It provides zero recovery point objective (RPO), ensuring that every write I/O is simultaneously acknowledged by both arrays in the cluster before it's committed. This setup allows two FlashArrays to operate as active-active peers and replicate storage volumes across availability zones or data centers.

When a volume resides in a stretched pod, any I/O written to one array is replicated in real time to the second array before being acknowledged. This configuration enables high availability, automatic failover, and seamless recovery in the event of outages.

note

- ActiveCluster is different from ActiveDR. ActiveDR is a near-synchronous disaster recovery feature that uses lightweight, snapshot-based replication to mirror data across arrays with a few seconds of lag.

- FlashArray Direct Access volumes in an ActiveCluster setup do not support CSI topology.

The ActiveCluster feature is useful for virtual machine (VM) workloads based on KubeVirt using FADA shared raw block (RWX) volumes. By enabling synchronous replication, this feature ensures high availability and data consistency for stateful VMs running in Kubernetes through KubeVirt.

For more information about ActiveCluster, see FlashArray ActiveCluster documentation.

important

Installing Portworx with the ActiveCluster feature on FlashArray supports only manually provisioned FlashArray volumes for the Portworx system volumes, such as metadata, journal, and KVDB.

If you plan to implement ActiveCluster with Portworx, Everpure recommends that you open a support case to ensure you receive appropriate guidance and support.

The following collection of tasks describe how to install Portworx with FlashArray ActiveCluster setup:

Complete all the tasks to install Portworx.

## How failover works​

In an ActiveCluster setup, if the two FlashArrays lose communication (due to network failure, array outage, or partitioning), each array attempts to contact the configured Mediator. The Mediator is a neutral third-party service that determines which array will remain active. Alternatively, you can use Pure1 Mediator instead of configuring your own.

- The array that wins quorum continues to serve I/O.

- The other array is marked as offline and ceases all volume operations.

- When connectivity is restored, the offline array enters a Resyncing state.

- Once it has replicated the missed I/O, the array resumes I/O and replication operations.

This automated mechanism ensures data integrity without requiring manual intervention.

## Prerequisites​

Before setting up ActiveCluster for Portworx volumes, verify the following:

- Two FlashArrays that support ActiveCluster and are properly licensed

- Connectivity to the Mediator from both arrays

- FlashArray pods must be created but must not use the secure multi-tenancy feature (realm)

For more information about compatibility and supported Purity versions, see:

- Supported Purity versions for Portworx

- Purity version requirements for the ActiveCluster feature

## Configure ActiveCluster on FlashArray​

For detailed instructions about configuring synchronous replication and stretched pods with ActiveCluster, refer to the FlashArray Administration Guide.

## Install Portworx​

Install Portworx, configured to use FlashArray Direct Access (FADA) volumes. For installation steps, see:

- Installation of Portworx with FlashArray using Portworx Central

- Installation of Portworx with FlashArray using Helm

note

Do not configure the volume’s backend pod inside a realm. ActiveCluster is not supported with secure multi-tenancy (realms).

## Configure Portworx for ActiveCluster​

After configuring ActiveCluster and creating a stretched pod, create a `StorageClass` in Kubernetes that references the stretched pod:

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: fada-activecluster-sc

provisioner: pxd.portworx.com

volumeBindingMode: Immediate

allowVolumeExpansion: true

parameters:

  backend: "pure_block"

  pure_fa_pod_name: "<your-stretched-pod-name>"

```

Then, create a `PersistentVolumeClaim` (PVC) using this storage class.

Portworx provisions a volume that is synchronously replicated across both FlashArrays using ActiveCluster.

## What to do next​

Create a PVC. For more information, see Configure FlashArray as a Direct Access volume.

In this topic:
