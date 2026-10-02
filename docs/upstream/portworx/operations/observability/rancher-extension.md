# Monitor Portworx Clusters on Rancher

Source: https://docs.portworx.com/portworx-enterprise/operations/observability/rancher-extension (Portworx Enterprise latest)

Monitor Portworx Clusters on Rancher | Portworx Enterprise Documentation

You can use the Portworx extension in the Rancher UI to monitor your cluster directly within the Rancher platform. This extension simplifies cluster management and provides actionable insights by integrating Portworx storage monitoring directly into the Rancher dashboard.

important

Portworx Rancher extension is not supported on PX-Security enabled clusters.

## Prerequisites​

- Kubernetes version 1.16.0 or later

- Rancher version 2.7.0 or later

- Ensure you are logged in as an admin to add and install the Portworx extension to the Rancher dashboard. Admin privileges are required to access the necessary settings and permissions for a successful installation and integration.

## Install Portworx extension​

To install the Portworx Rancher extension, follow these steps:

note

For air-gapped environments, clone the extension repository into a private repository registry accessible to the Rancher cluster.

- Navigate to ☰ > Extensions in the Rancher UI.

- In the top-right corner, click ⋮ > Manage Repositories > Create.

- Provide the following details:

- Name: Enter a name for your Portworx Rancher repository.

- Select the Target as Git repository containing Helm chart or cluster template definitions.

- Git Repo URL: `https://github.com/portworx/px-rancher-extension.git`

- Git Branch: `main`

- Click Create to add the repository.

- Go to the Available tab and locate the Portworx extension.

- Click Install on the desired version.

- After installation, click the Reload page button to update the UI.

## Monitor Portworx cluster​

After the cluster is installed, navigate to any cluster where Portworx is installed and select the Portworx dashboard to monitor the Portworx cluster.

### Portworx dashboard​

The Portworx dashboard provides comprehensive insights into the Portworx cluster, including:

- Cluster Details: Information such as Portworx version, Operator version, Stork version, status, number of nodes, license status, and more.

- Resources Section: Details about volumes, drives, and pools.

- Node Summary: Information on all nodes within the cluster.

### PersistentVolumeClaim (PVC)​

From the Portworx dashboard, you can select a PersistentVolumeClaim (PVC) to view detailed insights, including size, replication factor, replicas, labels, and volume consumers.

## Update Portworx extension​

Follow the steps below to update your Portworx Rancher extension:

- Navigate to ☰ > Extensions in the Rancher UI.

- Go to the Updates tab.

- Click Update if a new version is available.
 Alternatively, check the Available tab for the extension. If an update is available, an Update button will appear on its card.

- After upgrading, click the Reload page button to update the UI.

## Uninstall Portworx extension​

Follow the steps below to remove the Portworx Rancher extension:

- Navigate to ☰ > Extensions in the Rancher UI.

- Under the Installed tab, find the Portworx extension.

- Click Uninstall.

- After the extension is removed, click the Reload page button to refresh the UI.

In this topic:
