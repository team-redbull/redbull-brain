# FlashArray Direct Access

Source: https://docs.portworx.com/portworx-enterprise/concepts/fada (Portworx Enterprise latest)

FlashArray Direct Access | Portworx Enterprise Documentation

In the Direct Access model, Portworx provisions volumes directly from FlashArray, bypassing the storage pool. When a PVC is created, Portworx provisions a FlashArray volume, mounts it directly to the pod, and writes data to the array.

### Features​

FlashArray Direct Access volumes support:

- Basic operations: create, mount, expand, clone, unmount, delete

- Mount options for file system configuration

- Volume snapshots

- Quality of Service (QoS) settings (requires FlashArray with Purity 5.3.0 or later and REST API 1.17 or later)

- ActiveCluster

- Secure Multitenancy (SMT)

- Realm through StorageClass (requires Portworx 3.7.0 or later)

note

Portworx recommends deploying FlashArray cloud drives before using Direct Access volumes.

### Limitations​

- CSI ephemeral volumes and volume import operations are not supported

- `CreateOperations` settings are not honored by Portworx

- Volume groups are not supported

- FlashArray host sharing with realms must be explicitly configured as it is not supported by default under Secure Multi-Tenancy (SMT). Do not mix hosts within a realm with hosts outside a realm on the same node.

In this topic:
