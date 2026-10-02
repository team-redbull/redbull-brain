# Uninstall Portworx using Helm

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-portworx-helm (Portworx Enterprise 3.6)

Uninstall Portworx using Helm | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page provides instructions on how to uninstall Portworx using Helm.

## Prerequisites​

- You must have installed Portworx using Helm.

- This guide is applicable to the following platforms:

- FlashArray

- OpenShift vSphere

## Uninstall Portworx​

By default, Portworx is installed in the `kube-system` namespace. If you have installed it in a different namespace, use the `-n <namespace>` flag. In this example, you uninstall Portworx that was installed in the `portworx` namespace.

To uninstall Portworx with the release name `px-release`, follow the steps below:

-
(Optional) If you want to uninstall Portworx and wipe data, ensure that the `deleteStrategy` parameter is set to `UninstallAndWipe`. If this parameter was not set during the initial installation, you need to add it to the `px_install_values.yaml` file.

note

- You can also set the `deleteStrategy` parameter to `UninstallAndDelete`. Delete operation permanently removes all data from your disks, including Portworx metadata, and deletes the cloud drive.

- Supported on vSphere, AWS, GKE, and Azure with Portworx version 3.5.0 or later and Operator version 25.5.0 or later.

- Supported on Oracle Cloud Infrastructure, IBM Cloud, and FlashArray cloud drives with Portworx version 3.6.2 or later and Operator version 26.3.0 or later.

- If you're running KubeVirt virtual machines (VMs), and your default storage class is set to a Portworx storage class, you must set `spec.deleteStrategy.ignoreVolumes` to `true` when uninstalling Portworx using the `UninstallAndWipe` or `UninstallAndDelete` strategy. Otherwise, the uninstall process fails. This is because KubeVirt creates boot sources as PersistentVolumeClaims (PVCs) using the default storage class, which might be a Portworx storage class. In general, you can set `ignoreVolumes` to `true` if you are running KubeVirt VMs.
If the uninstall fails, check the `StorageCluster` conditions for more details.

```

deleteStrategy:

  type: UninstallAndWipe

```

-
Apply the updated delete strategy using the following command:

```

helm upgrade <px-release> portworx/portworx -n <portworx> -f px_install_values.yaml

```

```

Release "px-release" has been upgraded. Happy Helming!

NAME: px-release

LAST DEPLOYED: Thu Sep 26 06:15:16 2024

NAMESPACE: portworx

STATUS: deployed

REVISION: 2

TEST SUITE: None

NOTES:

Your Release is named "px-release"

Portworx Pods should be running on each node in your cluster.

Portworx would create a unified pool of the disks attached to your Kubernetes nodes.

No further action should be required and you are ready to consume Portworx Volumes as part of your application data requirements.

```

-
Verify that the new values have taken effect.

```

helm get values <px-release> -n <portworx>

```

```

USER-SUPPLIED VALUES:

deleteStrategy:

    type: UninstallAndWipe

```

-
Uninstall Portworx using the following command.

```

helm uninstall <px-release> -n <portworx>

```

```

release "px-release" uninstalled

```

In this topic:
