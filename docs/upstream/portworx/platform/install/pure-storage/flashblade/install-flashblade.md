# Installation of Portworx with FlashBlade using Portworx Central

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage/flashblade/install-flashblade (Portworx Enterprise 3.6)

Installation of Portworx with FlashBlade using Portworx Central | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise supports using FlashBlade to provide storage for workloads. However, Portworx requires a block device backend for system volumes, such as metadata, journal, and KVDB. You must configure a separate storage backend to support these components.

Choose a backend storage for Portworx system volumes:

- Use with FlashArray

- Use with local drives

If your cluster includes FlashArray, use it as the backend storage for Portworx system volumes. This configuration is recommended because it provides high-performance block storage for Portworx system volumes.

- Confirm that your environment meets the system requirements.

- Follow the steps in Prepare your environment for FlashBlade to configure the FlashBlade integration.

- Follow the steps in Install Portworx with FlashArray to deploy Portworx.

important

You must create a single `pure.json` file that includes configurations for both FlashArray and FlashBlade.

If your cluster does not include FlashArray, use local drives on each node to host Portworx system volumes.

- Confirm that your environment meets the system requirements.

- Follow the steps in Prepare your environment for FlashBlade to configure the FlashBlade integration.

- Follow the steps in Install Portworx on bare-metal to deploy Portworx.

## What to do next​

Create a PVC. For more information, see Configure FlashBlade as a Direct Access filesystem.

In this topic:
