# Set up FlashArray NVMe-oF RDMA

Source: https://docs.portworx.com/portworx-enterprise/reference/pure-reference/nvme-roce (Portworx Enterprise latest)

Set up FlashArray NVMe-oF RDMA | Portworx Enterprise Documentation

This document explains setup and configuration steps for using Portworx version 2.13.0 or newer on FlashArray NVMe-oF RDMA (RDMA over Converged Ethernet). Using this feature, you can attach FlashArray volumes using the NVMe-oF RDMA protocol. Follow the steps in this document when you set up and install Portworx.

NVMe-oF RDMA can be used with FlashArray Cloud Drives (FACD) or FlashArray Direct Access (FADA) volumes. When you select NVME-oF RDMA during StorageCluster spec generation or specify the protocol in the spec manually, Portworx recognizes that you want to use the NVMe-oF RDMA protocol and uses it to communicate with the FlashArray.

note

- QoS (IOPS and bandwidth) limits are not supported with NVMe volumes.

- In-place upgrades from iSCSI or Fibre Channel to NVMe are not supported. Changing the SAN type might result in unpredictable attachment behavior.

## Prerequisites​

- Check that your setup meets the requirements in the NVMe-oF RDMA Support Matrix.

- Make sure that your Linux kernel supports NVMe. You need to load the `nvme-fabrics` and `nvme-rdma` modules on boot or include them when you compile the kernel.

- Install the `nvme-cli` package.

- Ensure that all nodes have unique NQN (`/etc/nvme/hostnqn`) and host ID (`/etc/nvme/hostid`) entries.

## Configure hardware​

Configure your Cisco, Juniper, or Arista switch for use with Pure FlashArray NVMe-oF RDMA.

## Configure software​

To configure your software settings, follow the steps in Linux Recommended Settings, with the following change.

When you set up your `multipath.conf` file, add a `blacklist` section as shown in the following example:

```

blacklist {

        devnode "^pxd[0-9]*"

        devnode "^pxd*"

        device {

          vendor "VMware"

          product "Virtual disk"

        }

}

defaults {

        polling_interval       10

        find_multipaths        on

}

devices {

    device {

        vendor                      "NVME"

        product                     "Pure Storage FlashArray"

        path_selector               "queue-length 0"

        path_grouping_policy        group_by_prio

        prio                        ana

        failback                    immediate

        fast_io_fail_tmo            10

        user_friendly_names         no

        no_path_retry               0

        features                    0

        dev_loss_tmo                60

    }

    device {

        vendor                   "PURE"

        product                  "FlashArray"

        path_selector            "service-time 0"

        hardware_handler         "1 alua"

        path_grouping_policy     group_by_prio

        prio                     alua

        failback                 immediate

        path_checker             tur

        fast_io_fail_tmo         10

        user_friendly_names      no

        no_path_retry            0

        features                 0

        dev_loss_tmo             600

    }

}

```

## Install Portworx​

Perform the steps in one of the following documents to install Portworx version 2.13.0 or newer on your FlashArray setup, then return to this document.

- Provision Cloud Drives on Pure Storage FlashArray

- Configure Pure Storage FlashArray as a Direct Access volume

## Configure the adapter as a PCI device​

Configure the NVMe-oF RDMA adapter installed in ESXi as a PCI device. For example, on vSphere, follow the steps in Enable Passthrough for a Network Device on a host from the VMware documentation.

Once the NVMe-oF RDMA adapter is set up as a PCI device, the VM can mount as a PCI device and access external storage directly.

## Use NVMe-oF RDMA in a VM​

If you are using a VM, you also need to perform additional steps to enable and configure PCI passthrough.

The following examples illustrate how to perform these steps for vSphere. Your environment might require different steps.

### Enable RoCE as PCI passthrough​

After you install a physical adapter, the NVMe-oF RDMA adapter should be listed in PCI Devices.

-
Navigate to a host in the vSphere Client navigator.

-
Select the Configure tab, then under Hardware, select PCI devices.

-
Select all of the NVMe adapters that you have added, then select Toggle passthrough.

When passthrough configurations complete successfully, the device is listed in the Passthrough-enabled devices tab.

### Configure PCI passthrough in a VM​

-
In the vSphere client, select the VM you want to add the PCI passthrough card to from the list of VMs. Right click the VM, then select Edit settings.

-
Click Add new device, then select PCI device.

-
Select DirectPathIO, then select any of the RoCE adapter interfaces.

Add as many PCI devices for RoCE adapters as you need for the VM. Multiple ports on the FlashArray will provide redundant connections, but for extra redundancy you should add two or more PCI devices in case one device fails.

## Further considerations​

Before upgrading NVMe software, Portworx by Everpure recommends putting Portworx in maintenance mode.

In this topic:
