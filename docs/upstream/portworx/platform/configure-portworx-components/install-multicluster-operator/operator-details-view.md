# Portworx MultiCluster Operator Details View

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/install-multicluster-operator/operator-details-view (Portworx Enterprise 3.6)

Portworx MultiCluster Operator Details View | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

After you install the Portworx MultiCluster Operator, the Installed Operators page in the OpenShift console lists the Portworx Multi-Cluster Operator. Select the operator to open its details page, where you can view installation information and inspect or manage the disaster recovery custom resources that the operator provides.

The operator details page contains several tabs. The Details, YAML, Subscription, Events, and All instances tabs are standard Operator Lifecycle Manager (OLM) tabs that provide information about the operator. The Cluster, Disaster Recovery Action, Protection Group, and Disaster Recovery Pair tabs correspond to the custom resources managed by the operator and allow you to create, view, and manage instances of each resource.

note

Use the operator details page for advanced inspection and direct management of custom resources. For guided disaster recovery workflows, use the Portworx dashboards in the multicluster management view (All Clusters in OpenShift 4.18 and 4.19, or Fleet Management in OpenShift 4.20 and later). For more information, see Portworx ACM Dynamic Console Plugin Dashboards.

## Access the operator details page​

To access the operator details page, complete the following steps:

- Sign in to the OpenShift web console.

- From the left navigation pane, select Operators > Installed Operators.
The system displays the Installed Operators page that lists the installed operators.

- From the Project dropdown, select the portworx project in which you installed the operator.

- Click the Portworx Multi-Cluster Operator item.
The system opens the operator details page with multiple tabs.

## Operator details page attributes​

The following table lists the tabs on the operator details page and the attributes that each tab displays.

AttributesDescription

Details Tab

Provided APIsDisplays the custom resource types that the operator provides: Cluster, Disaster Recovery Action, Protection Group, and Disaster Recovery Pair. Click Create instance under an API to create a custom resource of that type.

ProviderDisplays the provider of the operator.

Created atDisplays the date and time when the operator was installed.

Console pluginDisplays whether the Portworx console plugin is enabled. The plugin adds the Portworx option and the disaster recovery dashboards to the OpenShift console.

LinksDisplays the documentation and support links for the operator.

MaintainersDisplays the maintainer name and contact email for the operator.

DescriptionDisplays an overview of the operator, including its features, prerequisites, and getting started steps.

ClusterServiceVersion detailsDisplays metadata about the installed operator version, including its name, namespace, labels, annotations, managed namespaces, creation time, and owner. It also displays the installation Status and status reason, the operator deployments, the operator service accounts, and the operator group.

ConditionsDisplays a table of the operator lifecycle conditions, including the Phase, the time it was last Updated, the Reason, and a descriptive Message.

YAML Tab

YAML editorDisplays the full `ClusterServiceVersion` manifest of the installed operator in an editor. You can view and edit the operator configuration, and then save, reload, cancel, or download the manifest.

Subscription Tab

Update channelDisplays the channel from which the operator receives updates.

Update approvalDisplays whether updates are applied automatically or require manual approval.

Upgrade statusDisplays whether the operator is up to date, along with the number of installed and installing versions.

NameDisplays the name of the operator subscription.

NamespaceDisplays the namespace where the subscription is created.

LabelsDisplays the labels applied to the subscription.

Created atDisplays the date and time when the subscription was created.

OwnerDisplays the owner of the subscription, if any.

Installed versionDisplays the currently installed `ClusterServiceVersion` (CSV).

Starting versionDisplays the version from which the operator started, if any.

CatalogSourceDisplays the catalog source that provides the operator, along with its health status.

InstallPlanDisplays the install plan associated with the subscription.

ConditionsDisplays a table of subscription conditions, including the Type, Status, last Updated time, Reason, and Message.

Events Tab

Streaming eventsDisplays a real-time stream of events related to the operator and the resources it manages.

All instances Tab

NameDisplays the name of the custom resource instance. Click the name to view the resource details.

KindDisplays the kind of the custom resource instance, such as Cluster, DisasterRecoveryAction, ProtectionGroup, or DisasterRecoveryPair.

StatusDisplays the status of the custom resource instance for a disaster recovery action.

LabelsDisplays the labels applied to the custom resource instance.

Last updatedDisplays the date and time when the custom resource instance was last updated.

Create newClick Create new and select a resource type such as Cluster, Disaster Recovery Action, Protection Group, or Disaster Recovery Pair to create a new instance of that type.

Cluster Tab

NameDisplays the name of the Cluster custom resource. Click the name to view the resource details.

KindDisplays the resource kind, which is Cluster.

StatusDisplays the status of the custom resource.

LabelsDisplays the labels applied to the custom resource.

Last updatedDisplays the date and time when the custom resource was last updated.

Create ClusterClick Create Cluster to create a new Cluster custom resource.

Disaster Recovery Action Tab

NameDisplays the name of the DisasterRecoveryAction custom resource. Click the name to view the resource details.

KindDisplays the resource kind, which is DisasterRecoveryAction.

StatusDisplays the status of the action, such as Successful or Failed.

LabelsDisplays the labels applied to the custom resource.

Last updatedDisplays the date and time when the custom resource was last updated.

Create DisasterRecoveryActionClick Create DisasterRecoveryAction to create a new DisasterRecoveryAction custom resource.

Protection Group Tab

NameDisplays the name of the ProtectionGroup custom resource. Click the name to view the resource details.

KindDisplays the resource kind, which is ProtectionGroup.

StatusDisplays the status of the custom resource.

LabelsDisplays the labels applied to the custom resource.

Last updatedDisplays the date and time when the custom resource was last updated.

Create ProtectionGroupClick Create ProtectionGroup to create a new ProtectionGroup custom resource.

Disaster Recovery Pair Tab

NameDisplays the name of the DisasterRecoveryPair custom resource. Click the name to view the resource details.

KindDisplays the resource kind, which is DisasterRecoveryPair.

StatusDisplays the status of the custom resource.

LabelsDisplays the labels applied to the custom resource.

Last updatedDisplays the date and time when the custom resource was last updated.

Create DisasterRecoveryPairClick Create DisasterRecoveryPair to create a new DisasterRecoveryPair custom resource.

In this topic:
