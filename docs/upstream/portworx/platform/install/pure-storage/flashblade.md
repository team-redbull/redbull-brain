# Installation of Portworx with FlashBlade

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage/flashblade (Portworx Enterprise 3.6)

Installation of Portworx with FlashBlade | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports FlashBlade as a Direct Access filesystems. When a PersistentVolumeClaim (PVC) is created, Portworx provisions an NFS filesystem on FlashBlade, maps it to the PVC, and mounts it to the pod. Once mounted, Portworx writes data directly to FlashBlade. This approach bypasses storage pools and provides high-performance shared file storage for workloads. For more information on Direct Access volumes, see FlashBlade Direct Access.

To install Portworx Enterprise with FlashBlade, follow these steps:

- Prepare your environment for installing Portworx with FlashBlade

- Install Portworx with FlashBlade using Portworx Central

note

After you install Portworx Enterprise, you can enable SSL certificate verification for FlashBlade connections to have Portworx validate the FlashBlade identity before sending management API requests. For more information, see Enable SSL Certificate Verification for FlashArray and FlashBlade.
