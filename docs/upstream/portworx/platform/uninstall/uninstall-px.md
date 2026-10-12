# Uninstall Portworx from an IBM cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-px (Portworx Enterprise latest)

Uninstall Portworx from an IBM cluster | Portworx Enterprise Documentation

This guide provides instructions on how to uninstall Portworx from an IBM cluster, specifically for IBM Cloud Kubernetes Service (IKS) and OpenShift IBM clusters.

- IBM IKS Cluster

- OpenShift IBM Cluster

-
Stop all applications using Portworx volumes, delete the Portworx PVCs, and wait until all `Delete`-reclaim-policy PVs and their VolumeAttachments are fully removed from the cluster before proceeding.

warning

Do not proceed to the next step while volume cleanup is still in progress. Setting `ignoreVolumes: true` in the delete strategy bypasses this protection — use it only when you intentionally accept the risk that PV cleanup may not complete. If PVs are already stuck in `Released` state with CSI finalizers, contact Portworx Support.

-
Edit your Portworx StorageCluster:

```

kubectl -n <px-namespace> edit storagecluster <your-cluster-name>

```

-
Add the delete strategy to your YAML spec:

```

deleteStrategy:

    type: UninstallAndWipe

```

You may choose either `Uninstall`, `UninstallAndWipe`, or `UninstallAndDelete` based on your needs. For more details, refer to the Delete/Uninstall strategy.

-
Delete the StorageCluster:

```

kubectl -n <px-namespace> delete storagecluster <your-cluster-name>

```

-
Verify that all Portworx pods are deleted:

```

kubectl -n <px-namespace> get pods -l name=portworx

```

-
Once all Portworx-related pods have been removed, run the following command to delete the Portworx Helm deployment:

```

helm uninstall <px-helm-deployment>

```

This command removes all Kubernetes components associated with the chart and deletes the deployment.

-
Stop all applications using Portworx volumes, delete the Portworx PVCs, and wait until all `Delete`-reclaim-policy PVs and their VolumeAttachments are fully removed from the cluster before proceeding.

warning

Do not proceed to the next step while volume cleanup is still in progress. Setting `ignoreVolumes: true` in the delete strategy bypasses this protection — use it only when you intentionally accept the risk that PV cleanup may not complete. If PVs are already stuck in `Released` state with CSI finalizers, contact Portworx Support.

-
Edit your Portworx StorageCluster:

```

oc -n <px-namespace> edit storagecluster <your-cluster-name>

```

-
Add the delete strategy to your YAML spec:

```

deleteStrategy:

    type: UninstallAndWipe

```

You may choose either `Uninstall`, `UninstallAndWipe`, or `UninstallAndDelete` based on your needs. For more details, refer to the Delete/Uninstall strategy.

important

If you're running KubeVirt virtual machines (VMs), and your default storage class is set to a Portworx storage class, you must set `spec.deleteStrategy.ignoreVolumes` to `true` when uninstalling Portworx using the `UninstallAndWipe` or `UninstallAndDelete` strategy. Otherwise, the uninstall process fails. Use `ignoreVolumes: true` only when you intentionally accept the risk that PV cleanup may not complete.

This is because KubeVirt creates boot sources as PersistentVolumeClaims (PVCs) using the default storage class, which might be a Portworx storage class. In general, you can set `ignoreVolumes` to `true` if you are running KubeVirt VMs.

If the uninstall fails, check the `StorageCluster` conditions for more details.

-
Delete the StorageCluster:

```

oc -n <px-namespace> delete storagecluster <your-cluster-name>

```

-
Verify that all Portworx pods are deleted:

```

oc -n <px-namespace> get pods -l name=portworx

```

-
Once all Portworx-related pods have been removed, run the following command to delete the Portworx Helm deployment:

```

helm uninstall <px-helm-deployment>

```

This command removes all Kubernetes components associated with the chart and deletes the deployment.

### Remove storage objects from the IBM dashboard​

After deleting your Helm deployment, navigate to the IBM dashboard and follow these steps for housekeeping:

-
In the left pane of your dashboard, click Resource List.

-
Search for and select the Portworx resource in the Storage section associated with your Portworx installation.

-
Click the Delete option from the ellipsis menu to remove the resource as shown in the following figure:

In this topic:
