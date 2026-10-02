# Scale your Portworx Cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster (Portworx Enterprise 3.6)

Scale your Portworx Cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

As your cluster usage increases and the data on your storage pools grows, you may start to run out of capacity. In order to handle this, you must use one of the two method.

- Expanding the storage pools with pxctl

- Using AutoPilot for dynamically achieving the same.

## Volume resize limitations​

This limitation is specific to the ext4 filesystem and does not apply to volumes using the XFS filesystem.

When using the ext4 filesystem with Portworx, there is a limitation on the maximum size to which a volume can be resized. This limitation is due to the inode constraints of the ext4 filesystem and not specific to Portworx.

#### ext4 default configuration limit​

For volumes formatted using the default ext4 configuration, where the bytes-per-inode ratio is 16384, the maximum size to which a volume can be resized is 65535 GiB. This restriction is due to the ext4 filesystem's maximum allowable inode count, which is capped at 2³² - 1 inodes.

#### Custom ext4 formatting limit​

If custom formatting options are used for the ext4 filesystem, the maximum volume size can vary based on the selected bytes-per-inode ratio. To determine whether a volume can be resized to a desired size with custom formatting, follow these steps:

- Use the `tune2fs` command on the Portworx device to retrieve the Inode count, Block size, and Block count:

```

tune2fs -l /dev/pxd/pxdxxx | grep "Inode count:"

tune2fs -l /dev/pxd/pxdxxx | grep "Block count:"

tune2fs -l /dev/pxd/pxdxxx | grep "Block size:"

```

- Calculate the bytes-per-inode ratio using the following formula:

```

bytesperinode = (blocksize * blockcount) / inodecount

```

- Calculate the number of inodes required for the desired volume size in bytes:

```

numofinodes = desiredvolumesizeinbytes / bytesperinode

```

- If the calculated number of inodes exceeds 2³² - 1, the volume cannot be resized to the desired size, and the requested size should be reduced. If the number of inodes is within the limit, the volume can be resized accordingly.

## 🗃Expand your Storage Pool Size

4 items

## 🗃Automate storage operations with Autopilot

5 items

## 📄️Scale with Cluster Autoscaler

Learn how to configure autoscaling of storage nodes in a Portworx cluster.

In this topic:
