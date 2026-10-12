# Uninstall Portworx installed using AWS Marketplace

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-marketplace (Portworx Enterprise latest)

Uninstall Portworx installed using AWS Marketplace | Portworx Enterprise Documentation

## Uninstall Portworx​

Perform the following steps to uninstall Portworx:

-
Stop applications and clean up volumes before deleting the StorageCluster to prevent PVs from getting permanently stuck with CSI finalizers:

- Stop all applications using Portworx volumes.

- Delete the Portworx PVCs.

- Wait until all `Delete`-reclaim-policy PVs and their VolumeAttachments are fully removed from the cluster.

warning

Do not proceed to the next step while volume cleanup is still in progress. Setting `ignoreVolumes: true` in the delete strategy bypasses this protection — use it only when you intentionally accept the risk that PV cleanup may not complete. If PVs are already stuck in `Released` state with CSI finalizers, contact Portworx Support.

-
Edit the storage cluster:

```

kubectl -n <namespace> edit storagecluster <yourclustername>

```

-
Add the following lines to your YAML `spec` section:

note

- If you are running Portworx version 3.5.0 or later on vSphere, AWS, GKE, and Azure platforms with Operator version 25.5.0 or later, you can also set the `deleteStrategy` parameter to `UninstallAndDelete`. Delete operation permanently removes all data from your disks, including Portworx metadata, and deletes the cloud drive.

- If you're running KubeVirt virtual machines (VMs), and your default storage class is set to a Portworx storage class, you must set `spec.deleteStrategy.ignoreVolumes` to `true` when uninstalling Portworx using the `UninstallAndWipe` or `UninstallAndDelete` strategy. Otherwise, the uninstall process fails. This is because KubeVirt creates boot sources as PersistentVolumeClaims (PVCs) using the default storage class, which might be a Portworx storage class. In general, you can set `ignoreVolumes` to `true` if you are running KubeVirt VMs.
If the uninstall fails, check the `StorageCluster` conditions for more details.

```

deleteStrategy:

  type: UninstallAndWipe

```

-
Save the spec and exit.

-
Delete the storagecluster:

```

kubectl -n <namespace> delete storagecluster <yourclustername>

```

-
Once all the Portworx-related pods are gone, uninstall or delete the `my-release` deployment:

```

helm uninstall my-release

```

This command removes all the Kubernetes components associated with the chart and deletes the release.

In this topic:
