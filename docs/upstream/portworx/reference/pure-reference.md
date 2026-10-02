# Portworx with FlashArray and FlashBlade reference

Source: https://docs.portworx.com/portworx-enterprise/reference/pure-reference (Portworx Enterprise latest)

Portworx with FlashArray and FlashBlade reference | Portworx Enterprise Documentation

The following sections provide reference information for using Portworx with FlashArray and FlashBlade:

## 📄️FlashBlade and FlashArray JSON

Portworx uses a single secret for both FlashArray and FlashBlade configuration. If you are planning on using both together, specify all of your FlashBlade and FlashArray entries in a single JSON file.

## 📄️Set up FlashArray NVMe-oF RDMA

Setup items related to FlashArray NVMe-oF RDMA.

## 📄️FlashBlade and FlashArray env vars

This section provides configuration details for setting FlashArray and FlashBlade environment variables in the StorageCluster object. All fields are objects under the spec.env[] list:

## FlashArray and FlashBlade reference​

When the FA/FB driver is enabled, the following references apply to FlashArray and FlashBlade Direct Access volumes:

ReferenceDescription

StorageClass referenceDescribes the supported `StorageClass` parameters.

pure.json referenceDescribes the backend configuration, including FlashArray VLAN binding, FlashBlade multi-tenancy servers, and Purity realms.

PersistentVolumeClaim referenceDescribes the PVC fields and annotations supported by the FA/FB driver.

Custom resource definitionsDescribes `PureVolume`, `PureSnapshot`, `PureStorageCluster`, and related custom resources.

PX-CSI CLI referenceDescribes the `kubectl px csi` commands for cluster status, images, diagnostics, backend credentials, volumes, and snapshots.

In this topic:
