# Enable or Upgrade Portworx OpenShift Dynamic Plugin

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/enable-ocp-plugin (Portworx Enterprise 3.6)

Enable or Upgrade Portworx OpenShift Dynamic Plugin | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The Portworx OpenShift Dynamic plugin is an OpenShift console plugin that provides integrated storage observability and management directly within the OpenShift console. It simplifies observability, monitoring, and troubleshooting for Portworx storage clusters, Kubernetes applications, and OpenShift integrations such as KubeVirt.

When enabled, the plugin adds:

- A Portworx option in the left navigation pane of the OpenShift console, allowing you to access details of your Portworx cluster.

- A Portworx tab on the KubeVirt VirtualMachine page, allowing you to view and manage PVCs or Disks for KubeVirt VMs.
For more information, see Observing Portworx PVCs and Disks for KubeVirt VMs.

- Portworx tabs on other storage-related pages such as StorageClasses and PersistentVolumeClaims, allowing you to view detailed information about your Portworx-backed resources.

This topic describes the steps to enable the Portworx OpenShift Dynamic plugin from the OpenShift console. It also explains how to upgrade the plugin installed on your cluster.

## Prerequisites​

Ensure that your cluster meets the following prerequisites before you enable Portworx OpenShift Dynamic plugin:

- Portworx version 3.4.0 or later installed.

- Portworx Operator version 25.3.1 or later installed.

note

For Portworx OpenShift Dynamic Plugin version 2.2.0 or later, you must install Portworx Operator version 25.6.0 or later.

- Run OpenShift version 4.16 or later.

## Enable Portworx OpenShift Dynamic Plugin​

To enable the Portworx OpenShift Dynamic plugin, follow these steps:

-
Sign in to the OpenShift Container Platform web console.

-
From the left navigation pane, click Installed Operators.

-
Click Portworx Operator.

-
In the Console plugin section, click the pencil icon.
 The system displays the Console plugin enablement window.

-
Select Enable and click Save.
 The system enables the plugin and displays the Portworx option in the left navigation pane.

## Upgrade Portworx OpenShift Dynamic Plugin​

To upgrade the plugin and ensure your Portworx deployment is using the latest recommended components, follow the appropriate procedure based on your setup:

### Automatic Upgrade of the Plugin​

When you upgrade Portworx Enterprise, Portworx OpenShift Dynamic Plugin is automatically upgraded. The updated plugin version is aligned with the Portworx Enterprise version you are upgrading to.

### Manual Upgrade of the Plugin using Storage Cluster​

To upgrade the plugin to a version aligned with a specific Portworx Enterprise release, without upgrading Portworx Enterprise, use the `StorageCluster` specification as follows:

Add the `autoUpdateComponents` field to the `StorageCluster`spec:

```

kind: StorageCluster

spec:

  autoUpdateComponents: Once

```

This prompts the Portworx Operator to reconcile all components and retrieve the latest images corresponding to the Portworx Enterprise version.

note

To upgrade only the plugin, you must create a ConfigMap to scope the update; otherwise, all components are upgraded.

### Manual Upgrade of the Plugin using a ConfigMap​

To upgrade the plugin to a version aligned with a specific Portworx Enterprise release, without upgrading Portworx Enterprise, by using a ConfigMap, follow these steps:

-
Download the latest Portworx version manifest:

```

curl -o versions.yaml "https://install.portworx.com/$<portworx-version>/version?kbver=$<kubernetes-version>&opver=$<operator-version>"

```

Replace:

- `<portworx_version>` with the Portworx version you want to use.

- `<kubernetes-version>` with the Kubernetes version you want to use.

- `<operator-version>` with the Operator version you want to use.

-
Update the px-versions configmap with the downloaded version manifest:

```

kubectl -n <px-namespace> delete configmap px-versions

kubectl -n <px-namespace> create configmap px-versions --from-file=versions.yaml

```

-
Add the `autoUpdateComponents` field to the storage cluster specification:

```

kind: StorageCluster

spec:

  autoUpdateComponents: Once

```

This prompts the Portworx Operator to reconcile all components and retrieve the latest images from the configmap if available, or download them from the manifest if not.

### Manual Upgrade of the Plugin to a Custom Version using Storage Cluster​

To upgrade the plugin to a custom version, without upgrading Portworx Enterprise, use the StorageCluster specification as follows:

Add the `pluginImage`, `proxyImage`, and `cacheAgentImage` field to the storage cluster specification:

```

kind: StorageCluster

spec:

  ocpDynamicPlugin:

    pluginImage: "portworx/portworx-dynamic-plugin:<dynamic-plugin-version>"

    cacheAgentImage: "portworx/px-cache-agent:<cache-agent-version>"

    proxyImage: "nginxinc/nginx-unprivileged:alpine-slim"

```

Replace:

- `<dynamic-plugin-version>` with the version of OpenShift Dynamic Plugin you want to upgrade to.

- `<cache-agent-version>` with the Portworx cache agent version.

This prompts the Portworx Operator to reconcile the components mentioned in the `StorageCluster` and retrieve the corresponding images.

### Manual Upgrade of the Plugin to a Custom Version using a ConfigMap​

To upgrade the plugin to a custom version, without upgrading Portworx Enterprise, by using a ConfigMap, follow these steps:

To upgrade the plugin to a custom version, without upgrading Portworx Enterprise, by using a ConfigMap, follow these steps:

-
Update the `configmap/px-versions` with the desired custom plugin image.

-
Add the `autoUpdateComponents` field to the storage cluster specification:

```

kind: StorageCluster

spec:

  autoUpdateComponents: Once

```

This prompts the Portworx Operator to reconcile all components and retrieve the latest images from the configmap if available, or download them from the manifest if not.

In this topic:
