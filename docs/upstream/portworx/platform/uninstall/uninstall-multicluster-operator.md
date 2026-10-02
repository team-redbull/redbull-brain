# Uninstall the Portworx MultiCluster Operator

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-multicluster-operator (Portworx Enterprise 3.6)

Uninstall the Portworx MultiCluster Operator | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When you no longer need ACM-based disaster recovery, uninstall the Portworx MultiCluster Operator from the ACM hub cluster. Uninstalling the operator also disables and removes the Portworx ACM Dynamic Console Plugin.

To uninstall the Portworx MultiCluster Operator, complete the following steps:

- Sign in to the OpenShift web console.

- From the left navigation pane, go to Operators > Installed Operators.
The system displays the Installed Operators page that lists the installed operators.

- From the Project dropdown, select the namespace or project in which you installed the operator.

- In the Portworx Multi-Cluster Operator row, click the vertical ellipsis menu, and then select Uninstall Operator.

- In the Uninstall Operator? window, review the list of custom resources managed by the operator, such as Cluster, DisasterRecoveryPair, ProtectionGroup, and DisasterRecoveryAction.

- (Optional) Select the Delete all operand instances for this operator checkbox to delete all custom resource instances managed by the operator.

- Click Uninstall.
The system removes the operator from the `portworx` namespace and disables and removes the Portworx ACM Dynamic Console Plugin.

note

Uninstalling the Portworx MultiCluster Operator does not remove the disaster recovery resources created on the managed clusters, such as `ClusterPair`, backup locations, and `MigrationSchedule` resources. These resources continue to run and must be removed manually if they are no longer required.
