# Uninstall Portworx from an IBM cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-px (Portworx Enterprise 3.6)

Uninstall Portworx from an IBM cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This guide provides instructions on how to uninstall Portworx from an IBM cluster, specifically for IBM Cloud Kubernetes Service (IKS) and OpenShift IBM clusters.

- IBM IKS Cluster

- OpenShift IBM Cluster

- Edit your Portworx StorageCluster:

```

kubectl -n <px-namespace> edit storagecluster <your-cluster-name>

```

- Add the delete strategy to your YAML spec:

```

deleteStrategy:

    type: UninstallAndWipe

```

 You may choose either `Uninstall`, `UninstallAndWipe`, or `UninstallAndDelete` based on your needs. For more details, refer to the Delete/Uninstall strategy.

- Delete the StorageCluster:

```

kubectl -n <px-namespace> delete storagecluster <your-cluster-name>

```

- Verify that all Portworx pods are deleted:

```

kubectl -n <px-namespace> get pods -l name=portworx

```

- Once all Portworx-related pods have been removed, run the following command to delete the Portworx Helm deployment:

```

helm uninstall <px-helm-deployment>

```

 This command will remove all Kubernetes components associated with the chart and delete the deployment.

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

If you're running KubeVirt virtual machines (VMs), and your default storage class is set to a Portworx storage class, you must set `spec.deleteStrategy.ignoreVolumes` to `true` when uninstalling Portworx using the `UninstallAndWipe` or `UninstallAndDelete` strategy. Otherwise, the uninstall process fails.

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

This command will remove all Kubernetes components associated with the chart and delete the deployment.

### Remove storage objects from the IBM dashboard​

After deleting your Helm deployment, navigate to the IBM dashboard and follow these steps for housekeeping:

-
In the left pane of your dashboard, click Resource List.

-
Search for and select the Portworx resource in the Storage section associated with your Portworx installation.

-
Click the Delete option from the ellipsis menu to remove the resource as shown in the following figure:

In this topic:
