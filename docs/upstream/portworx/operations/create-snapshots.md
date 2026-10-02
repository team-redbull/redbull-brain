# Create Snapshots in Portworx

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots (Portworx Enterprise 3.6)

Create Snapshots in Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This section describes how to create snapshots of Portworx volumes and how you can clone those snapshots to PVCs and use them with your applications.

The Snapshots feature in Portworx protects your data by creating point-in-time copies of persistent volumes (PVs). Snapshots help you quickly recover from accidental deletions, data corruption, or other unexpected failures. You can create, manage, and restore snapshots at the volume level without disrupting running workloads.

Portworx supports local and cloud snapshots, giving you flexibility to store backups on your cluster or offload them to remote cloud storage. This feature enables faster recovery, simplifies backup workflows, and helps meet your disaster recovery and compliance goals.

note

-
The suggested way to manage snapshots on Kubernetes is to use Stork. For information on how to create Portworx snapshots using PVC annotations, see the Create a PVC from a Snapshot section.

-
For multitenant FlashArray:

- When cloning a volume, the clone will inherit the storage class of the clone specification.

- If the clone should reside in the same pod configuration as the original volume, use the same storage class as the original.

- For different pod configurations:

- If the original volume is not in a pod but the clone should be, use a storage class with a pod for the clone.

- Conversely, if the original is in a pod but the clone should not be, use a StorageClass without a pod for the clone.

-
In airgapped bare metal environments, only local snapshots are supported. Cloud snapshots are not available.
