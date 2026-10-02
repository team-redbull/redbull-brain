# Locking Azure Cloud Drives

Source: https://docs.portworx.com/portworx-enterprise/concepts/azure-disk-lock (Portworx Enterprise latest)

Locking Azure Cloud Drives | Portworx Enterprise Documentation

When you install Portworx Enterprise on an Azure cluster, it provisions Azure-managed cloud drives (disks) to provide persistent storage for your workloads. Because these cloud drives store application data, deleting a cloud drives can cause application downtime and potential data loss.

To protect cloud drives from accidental or external deletion, you can enable cloud drive locking in Portworx Enterprise. Portworx Enterprise integrates with Azure Resource Manager (ARM) resource locks to secure cloud drives. When you enable cloud drive locking, Portworx Enterprise automatically applies a `CanNotDelete` lock to each Azure cloud drives that it creates. This lock prevents deletion of the cloud drive while still allowing normal read and update operations.

Lock creation occurs as part of the drive provisioning process. To avoid affecting application availability, drive provisioning continues even if the lock cannot be created. In such cases, Portworx Enterprise generates an alert and later attempts to apply the lock again during reconciliation. If you modify or remove a lock that Portworx Enterprise creates, Portworx reconciles the lock and restores it to its original state.

When you delete a Portworx-managed Azure cloud drive with drive locking enabled, Portworx Enterprise first removes the associated `CanNotDelete` lock. If Portworx Enterprise successfully removes the lock, the system proceeds with deleting the cloud drive. If the lock cannot be removed, Portworx Enterprise raises an alert and stops the deletion process. This approach ensures consistency between Portworx and Azure. Portworx does not assume that a cloud drive is deleted unless Azure confirms successful lock removal and cloud drive deletion.

When you uninstall Portworx Enterprise using the `Uninstall` or `UninstallAndWipe` strategy, the system removes cloud drive locks to allow administrators to manually clean up the cloud drives. When you uninstall Portworx Enterprise using the `UninstallAndDelete` strategy, the system removes the cloud drive locks and then deletes the cloud drives to ensure the cleanup operation completes successfully.

## Prerequisites​

Ensure that your cluster meets the following requirements before you enable cloud drive locking:

-
Have Portworx Enterprise 3.6.0 or later installed.

-
Have either `Microsoft.Authorization/*` or `Microsoft.Authorization/locks/*` permission.
When you create a custom role during installing Portworx Enterprise on an Azure cluster, add either of these permissions to the custom role. For more information, see Create an Azure Cluster.

For example, the following role can be created to allow Portworx access to azure locking operations:

```

az role definition create --role-definition

'{

"Name": "<your-role-name>",

"Description": "",

"AssignableScopes": [

    "/subscriptions/<your-subscription-id>"

],

"Actions": [

    "Microsoft.ContainerService/managedClusters/agentPools/read",

    "Microsoft.Compute/disks/delete",

    "Microsoft.Compute/disks/write",

    "Microsoft.Compute/disks/read",

    "Microsoft.Compute/virtualMachines/write",

    "Microsoft.Compute/virtualMachines/read",

    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/write",

    "Microsoft.Compute/virtualMachineScaleSets/virtualMachines/read",

    "Microsoft.Authorization/locks/*"

],

"NotActions": [],

"DataActions": [],

"NotDataActions": []

}'

```

## Enable Cloud Drives Locking​

To enable cloud drive locking:

```

pxctl cluster options update --cloud-drive-locking=true

```

When you enable cloud drive locking, Portworx Enterprise locks all existing managed cloud drives and automatically locks newly created cloud drives.

## Disable Cloud Drive Locking​

To permanently disable cloud drive locking:

```

pxctl cluster options update --cloud-drive-locking=false

```

When you disable cloud drive locking, Portworx Enterprise removes locks from all managed cloud drives and stops applying locks to new cloud drives.

## Temporarily Disable Cloud Drive Locking​

When Azure cloud drives managed by Portworx are protected with `CanNotDelete` locks, platform upgrades fail with the following error:

```

Operation status: Failed

Code: ResourceGroupLocked

Message: Preflight validation check for resource(s) for container service failed.

Resource group 'MC_XXXXXX_XXXXXXX_eastus' is locked, please remove lock and retry.

```

To avoid upgrade failure you can temporarily disable cloud drive locking before performing Kubernetes platform upgrades or node group operations.

To temporarily disable cloud drive locking:

```

pxctl cluster options update --cloud-drive-locking-disable-for-hours <duration>

```

Replace `<duration>` with the number of hours to temporarily disable locking the drives.

note

You can set the disable duration for a minimum of 1 hour and a maximum of 168 hours (7 days).

When you disable cloud drive locking temporarily, Portworx Enterprise removes locks from all managed cloud drives and stops applying locks to new cloud drives for the specified duration. After the specified duration expires, Portworx Enterprise reapplies locks to all managed cloud drives and resumes locking newly created cloud drives.

In this topic:
