# Install Portworx with Everpure Platforms

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage (Portworx Enterprise latest)

Install Portworx with Everpure Platforms | Portworx Enterprise Documentation

Portworx integrates with Everpure platforms such as FlashArray, FlashBlade, and Everpure Cloud Dedicated (formerly Cloud Block Store) to support multiple deployment models across Kubernetes environments.

## FlashArray​

FlashArray supports the most comprehensive set of features, including cloud drives, direct access volumes, PX-StoreV2, secure multi-tenancy using realms and pods, and ActiveCluster for synchronous replication.
 You can deploy Portworx with FlashArray in either a single-tenant or multi-tenant configuration, depending on your isolation and access requirements.

For installation instructions, see Installation of Portworx with FlashArray.

## FlashBlade​

FlashBlade provides NFS-based file storage and is supported as a direct access filesystem backend. It is ideal for shared file workloads such as AI/ML, analytics, or backup targets.

FlashBlade does not support Portworx system volumes, you must use FlashArray or local disks for Portworx system volumes (data drives, metadata, journal or KVDB).

For installation instructions, see Installation of Portworx with FlashBlade.

## Everpure Cloud Dedicated​

Everpure Cloud Dedicated extends FlashArray capabilities to the public cloud and supports both cloud drive and direct access volume models. It can also be used to store Portworx metadata and system volumes.

For installation instructions, see Installation of Portworx with Everpure Cloud Dedicated.

## Prerequisites​

Ensure that all the system requirements for Portworx are met.

In this topic:
