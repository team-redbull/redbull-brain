# FlashBlade Direct Access

Source: https://docs.portworx.com/portworx-enterprise/concepts/fbda (Portworx Enterprise latest)

FlashBlade Direct Access | Portworx Enterprise Documentation

Portworx supports FlashBlade as a Direct Access volume provider. When a PVC is created, Portworx provisions an NFS filesystem on FlashBlade, maps it to the PVC, and mounts it to the pod. Once mounted, Portworx writes data directly to FlashBlade.

This model bypasses storage pools and provides high-performance shared file storage for Kubernetes workloads.

### Features​

FlashBlade Direct Access supports:

- Filesystem operations: create, mount, expand, unmount, delete

- NFS export rules for access control

- Mount options for NFS configuration

- NFS v3 and v4.1

You can specify mount options in the `mountOptions` field of the StorageClass. If not specified, Portworx uses the client’s default NFS settings. Options depend on the host OS and Purity//FB version.

For more details, see the FlashBlade User Guides.

### Limitations​

- Subpaths are not supported

- PX-Autopilot does not support FlashBlade volumes

### Differences between FlashBlade Direct Access and proxy volumes​

- Direct Access: Portworx dynamically creates and manages filesystems on FlashBlade.

- Proxy volumes: You must manually create filesystems on FlashBlade before Portworx can use them.

## Unsupported parameters for FlashBlade Direct Access​

- `shared`

- `sharedv4`

- `secure`

- `repl`

- `scale` (must be `0`)

- `aggregation_level` (must be less than `2`)

In this topic:
