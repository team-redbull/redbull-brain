# Install Portworx MultiCluster Operator

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/install-multicluster-operator (Portworx Enterprise latest)

Install Portworx MultiCluster Operator | Portworx Enterprise Documentation

The Portworx MultiCluster Operator provides enterprise-grade disaster recovery and multi-cluster management capabilities for Portworx Enterprise storage clusters.

The Portworx MultiCluster Operator provides the following features:

- Portworx Fleet Visibility: Centrally view multiple Portworx clusters from a single OpenShift Hub cluster. You can view Portworx installation status, cluster health status, platform, and capacity information.

- Fleet-wide Disaster Recovery Management: Declarative DR management using custom Kubernetes resources, enabling consistent DR policies across your entire fleet.

- Red Hat ACM Integration: Native integration with Red Hat Advanced Cluster Management (RHACM) for seamless multi-cluster operations.

The Portworx MultiCluster Operator extends Red Hat Advanced Cluster Management (ACM) by enabling asynchronous DR between workload clusters directly from the OpenShift console. This integration removes the need to perform the standalone Stork-based Async DR cluster pairing workflow through multiple CLI steps. For more information on Red Hat ACM, see Red Hat documentation.

This topic describes the steps to install the Portworx MultiCluster Operator on the hub cluster from the OpenShift console.

## Prerequisites​

Ensure that your cluster meets the following prerequisites before you install Portworx MultiCluster Operator:

- The cluster is running OpenShift version 4.18 or later.

- The cluster is running Portworx Enterprise version 3.5.0 or later.

- The cluster is running Portworx Operator version 26.2.0 or later.

- Red Hat Advanced Cluster Management (ACM) is installed on the cluster. For more information, see Red Hat documentation.

## Install Portworx MultiCluster Operator​

To install the Portworx MultiCluster Operator, follow these steps:

-
Sign in to the OpenShift Container Platform web console.

-
From the left navigation pane, go to the OpenShift operator catalog.

-
Search for Portworx MultiCluster Operator, and from the search results, select Portworx MultiCluster Operator.

-
Click Install.
The system initiates the Portworx MultiCluster Operator installation and displays the Install Operator page.

-
In the Installation mode section, select A specific namespace on the cluster.

-
From the Installed Namespace dropdown, choose Select a Namespace, and from the dropwdown menu, select Create Project.
The system displays the Create Project window.

-
Provide the name `portworx` and click Create to create a namespace called portworx.

-
In the Console plugin section, select Enable to manage your Portworx cluster using the Portworx dashboard within the OpenShift console.

-
Click Install to install the Portworx Multi-Cluster Operator in the `portworx` namespace.
The installation also deploys the Portworx ACM Dynamic Console Plugin. After the installation completes, the Portworx option appears in the left navigation pane of the multicluster management view (All Clusters in OpenShift 4.18 and 4.19, or Fleet Management in OpenShift 4.20 and later).
The Portworx menu includes the Clusters, Disaster Recovery Pairs, Protection Groups, and Disaster Recovery Actions pages, which you can use to configure, manage, and monitor multicluster disaster recovery operations for your Portworx clusters. For information about the dashboards and the attributes they display, see Portworx ACM Dynamic Console Plugin Dashboards.

### What to do next​

- Review the operator details page to confirm a successful installation and to manage the disaster recovery custom resources directly. For more information, see Portworx MultiCluster Operator Details View.

- Set up Multi Cluster disaster recovery. For more information, see Multi Cluster Disaster Recovery with Red Hat Advanced Cluster Management.

- Configure ACM Multicluster Observability to collect and centralize Portworx metrics from your workload clusters on the hub cluster. For more information, see Configure ACM Multicluster Observability for Portworx metrics.

In this topic:
