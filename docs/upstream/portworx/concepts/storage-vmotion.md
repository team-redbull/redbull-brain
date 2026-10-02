# Storage vMotion

Source: https://docs.portworx.com/portworx-enterprise/concepts/storage-vmotion (Portworx Enterprise latest)

Storage vMotion | Portworx Enterprise Documentation

Portworx supports VMware's Storage vMotion feature, allowing for the live migration of virtual disk files (.vmdk) between datastores without any downtime. This capability is particularly useful for rebalancing storage consumption across new and existing datastores managed by Portworx. It is important to note that Portworx only supports vSphere-based cloud drives that were created directly by the Portworx itself.

## Limitations​

The following operations are not supported while vMotion is in progress for the associated VMDKs:

- Pool expansion

- VM deletion

- Cloud-drive detachment

## Prerequisites​

The Storage vMotion feature requires the Container Storage Interface (CSI) to be enabled.

When you generate the StorageCluster specification using Portworx Central, CSI is enabled by default. If CSI is disabled, you can enable it by adding the following configuration to your StorageCluster spec:

```

spec:

  csi:

    enabled: true

```

## How Portworx manages Storage vMotion​

Portworx tracks vSphere cloud drives using their UUIDs, which serve as unique identifiers stored in a configmap. Unlike disk paths, which change when a drive is moved, the UUID remains constant, allowing Portworx to reliably identify and update the new paths when Storage vMotion occurs.

When Storage vMotion is initiated, Portworx automatically detects the migration and updates the disk paths. This ensures seamless functionality even after cloud drives are relocated to different datastores. Since Storage vMotion is a live process, the drives remain attached to the VM throughout the migration.

- Portworx uses the UUID of virtual disks to uniquely identify cloud drives, avoiding issues caused by changing paths.

- Portworx is informed of Storage vMotion through the `WaitForUpdatesEx` function, which notifies the coordinator node of a path change for a specific UUID. The coordinator then updates the cloud-drive configmap with the new paths.

- Once the paths are updated, Portworx generates a `SvMotionMonitoringSuccess` alert, indicating the success or failure of the vMotion detection.

note

- After every Storage vMotion event, wait for the `SvMotionMonitoringSuccess` alert before performing the following operations:

- Pool expansion

- Platform upgrades

- VM deletion

- Detaching cloud drives

- It may take several minutes for Portworx to recognize Storage vMotion, as vSphere could be under heavy load, causing a delay before Portworx receives the callback from vSphere.

Alternatively, if Portworx is restarted after a Storage vMotion event, it will detect the path changes upon startup and update them automatically.

The following diagram shows how a vmdk3 is moved from Datastore 1 to Datastore 2. This migration happens in the background while VM3 continues to function normally, ensuring no disruption in service.

In this topic:
