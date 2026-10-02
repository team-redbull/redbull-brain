# Uninstall Portworx from a Kubernetes cluster using the Operator

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-operator (Portworx Enterprise latest)

Uninstall Portworx from a Kubernetes cluster using the Operator | Portworx Enterprise Documentation

Using the Portworx Operator, you can efficiently uninstall Portworx from your clusters by updating the `StorageCluster` object. You have the option to either keep the data on your drives or wipe it completely.

- Uninstall: Removes the Kubernetes objects, Portworx `systemctl` service, `/etc/pwx` and `/opt/pwx` directories, and all traces of Portworx on the nodes. The drives are not formatted and Portworx Metadata in the KVDB is not deleted. You may need to uninstall Portworx if you installed it in the wrong namespace.

- Uninstall and wipe: Removes all of the resources listed in the "Uninstall" procedure, and also removes (formats) all data from your disks permanently, including the Portworx metadata. You may want to perform an uninstall and wipe when you decommission a cluster.

- Uninstall and delete: Delete operations permanently remove all data from your disks, including Portworx metadata, and delete the cloud drive.

- Supported on vSphere, AWS, GKE, and Azure with Operator version 25.5.0 or later and Portworx Enterprise version 3.5.0 or later.

- Supported on Oracle Cloud Infrastructure, IBM Cloud, and FlashArray cloud drives with Operator version 26.3.0 or later and Portworx Enterprise version 3.6.2 or later.

## Prerequisites​

- A successfully deployed Portworx Operator on your cluster.

## Uninstall Portworx​

- Kubernetes

- Openshift

-
Display the Portworx StorageCluster:

Use the `kubectl get` command to display the name of your Portworx storage cluster:

```

kubectl get -n <px-namespace> storagecluster <storagecluster-name>

```

-
Edit the StorageCluster:

Modify your storage cluster to initiate the uninstall process:

```

kubectl edit -n <px-namespace> storagecluster <storagecluster-name>

```

Update the `deleteStrategy` field in the `StorageCluster` object:

note

If PersistentVolumeClaims (PVCs) referencing a Portworx storage class are present on your cluster, the uninstall is blocked until all Portworx volumes are removed. To allow the uninstall to proceed, set `spec.deleteStrategy.ignoreVolumes` to `true` when using the `UninstallAndWipe` or `UninstallAndDelete` strategy.

-
For uninstall only:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  deleteStrategy:

    type: Uninstall

```

-
For uninstall and wipe:
 Wipe operations remove all data from your disks permanently, including the Portworx metadata. Use caution when applying the `deleteStrategy` spec.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  deleteStrategy:

    type: UninstallAndWipe

```

-
Uninstall and delete:
 Delete operations permanently remove all data from your disks, including Portworx metadata, and delete the cloud drive. Use caution when applying the `deleteStrategy` spec.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  deleteStrategy:

    type: UninstallAndDelete

```

-
Delete the StorageCluster:

Execute the following command, specifying your `StorageCluster` object:

```

kubectl delete StorageCluster <storagecluster-name> -n <px-namespace>

```

This operation can take several minutes to complete.

-
Remove the Portworx Operator:

Finally, delete the Portworx Operator deployment:

```

kubectl delete deployment -n <px-namespace> portworx-operator

```

-
Display the Portworx StorageCluster:

Enter the `oc get` command to display the name of your Portworx storage cluster and specify your namespace:

```

oc get -n portworx storagecluster <storagecluster-name>

```

-
Edit the StorageCluster: Enter the `oc edit` command to modify your storage cluster and specify your namespace:

```

oc edit -n portworx storagecluster <storagecluster-name>

```

Modify your `StorageCluster` object by adding the `deleteStrategy` field with one of the following types: `Uninstall`, `UninstallAndWipe`, or `UninstallAndDelete`.

important

If you're running KubeVirt virtual machines (VMs), and your default storage class is set to a Portworx storage class, you must set `spec.deleteStrategy.ignoreVolumes` to `true` when uninstalling Portworx using the `UninstallAndWipe` or `UninstallAndDelete` strategy. Otherwise, the uninstall process fails.

This is because KubeVirt creates boot sources as PersistentVolumeClaims (PVCs) using the default storage class, which might be a Portworx storage class. In general, you can set `ignoreVolumes` to `true` if you are running KubeVirt VMs.

If the uninstall fails, check the `StorageCluster` conditions for more details.

-
Uninstall Portworx only:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: portworx

spec:

  deleteStrategy:

    type: Uninstall

```

-
Uninstall Portworx and wipe all drives:
 Wipe operations remove all data from your disks permanently, including the Portworx metadata. Use caution when applying the `deleteStrategy` spec.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: portworx

spec:

  deleteStrategy:

    type: UninstallAndWipe

```

-
Uninstall and delete:
 Delete operations permanently remove all data from your disks, including Portworx metadata, and delete the cloud drive.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  deleteStrategy:

    type: UninstallAndDelete

```

-
Delete the StorageCluster:

Enter the `oc delete` command, specifying your `StorageCluster` object name and namespace:

```

oc delete StorageCluster <your-storagecluster-name> -n portworx

```

note

This operation can take several minutes to complete.

-
Remove the Portworx Operator:

Finally, delete the Portworx Operator deployment:

```

oc delete deployment -n <px-namespace> portworx-operator

```

In this topic:
