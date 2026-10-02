# Uninstall Portworx installed using AWS Marketplace

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-marketplace (Portworx Enterprise 3.6)

Uninstall Portworx installed using AWS Marketplace | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Uninstall Portworx​

Perform the following steps to uninstall Portworx:

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
