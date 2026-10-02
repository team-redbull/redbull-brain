# Migrate from Portworx Essentials to Portworx Enterprise license

Source: https://docs.portworx.com/portworx-enterprise/platform/license/convert-px-essential-oem-to-px-enterprise-trial (Portworx Enterprise latest)

Migrate from Portworx Essentials to Portworx Enterprise license | Portworx Enterprise Documentation

With the discontinuation of Portworx Essentials, customers using the PX-Essentials license SKU will experience functionality restrictions when upgrading their Portworx release. Specifically, once the PX-Essentials license expires, users will no longer be able to:

- Create new volumes

- Take snapshots

- Perform new backups

To prevent service disruptions, users must transition from PX-Essentials to Portworx Enterprise.

important

- Migrating from Portworx Essentials to Portworx Enterprise starts a 30-day trial license. After this period, you must purchase a Portworx Enterprise license to continue using Enterprise features.

- You cannot roll back from Portworx Enterprise to PX-CSI. To migrate from Essentials to PX-CSI, contact Portworx Support for assistance.

### Switch from PX-Essentials to PX-Enterprise​

-
Modify the StorageCluster object by removing the `--oem esse` annotation from the `StorageCluster` object to disable the OEM Essentials mode.

```

kind: StorageCluster

apiVersion: core.libopenstorage.org/v1

metadata:

  annotations:

    portworx.io/misc-args: "--oem esse"  # Remove this line

```

-
Save and apply the changes to the cluster. The system will initiate a gradual, node-by-node transition to Portworx Enterprise.

-
Once the transition begins, Portworx will automatically switch to the Portworx Enterprise container image (`docker.io/portworx/px-enterprise`). This process will activate a 30-day Trial License for Portworx Enterprise.

In this topic:
