# Failback

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/failback (Portworx Enterprise 3.6)

Failback | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Failback is the process of returning your resources and their data to the original source cluster after that cluster is restored and operational again. You perform a failback after you have failed over protected resources to a destination workload cluster and the source workload cluster becomes available. With ACM-based disaster recovery, failback occurs at the Protection Group level, meaning that all namespaces and resources included in a protection group return together to the source cluster.

This topic explains how to prepare for and initiate a failback using the Portworx MultiCluster Operator on the hub cluster.

For information about initiating a failback by using `kubectl`, see the Stork documentation.

## Prerequisites​

- A failover action that has completed successfully on the destination cluster.
For more information, see Failover.

## Prepare for failback​

Before you perform a failback operation, prepare the protection group for reverse migration. During this step, the system initializes the resources required to set up migrations from the destination cluster back to the primary cluster.

To prepare for failback, complete the following steps:

- Sign in to the OpenShift web console.

- Switch to the multicluster management view (All Clusters on OpenShift 4.18 and 4.19, or Fleet management on 4.20 and later), and from the left navigation pane, select the Portworx option.

- Select Protection Groups.
 The system displays the Protection Groups page that lists all existing protection groups.

- Click the vertical ellipsis menu associated with the protection group to fail back, and select Prepare Failback.
The system displays the Prepare for failback window.

- Review the failback scope, including:

- The number of namespaces successfully failed over.

- The number of namespaces that remain on the primary cluster.

- The namespaces eligible for failback.

- (Optional) Click Edit Settings to modify the protection group configuration used during failback. You can update:

- Resource protection rules

- Resource inclusion and exclusion settings

- Advanced synchronization settings

note

You cannot modify namespace selection during this stage.

- Click Prepare Failback.
The system starts the initial synchronization of data and resources from the destination cluster back to the primary cluster. After synchronization completes, the Protection State column for the protection group in the Protection Groups page displays Ready for Failback.

## Initiate a failback​

To initiate a failback, complete the following steps:

- Sign in to the OpenShift web console.

- Switch to the multicluster management view, and from the left navigation pane, select the Portworx option.

- Select Protection Groups.
 The system displays the Protection Groups page that lists all existing protection groups.

- Click the vertical ellipsis menu associated with the protection group to fail back, and select Initiate Failback.
The system displays the Failback window.

- In the Action Details page of the Failback window, perform the following:

- In the Failback Name field, enter a name for the failback action.

- Click Next.

- In the Choose Namespaces page that opens, do the following:

- Review the list of namespaces available for failback.
The list includes namespaces defined in the protection group, either through manual selection or label selectors.

- Select the checkbox associated with each namespace to failback to the primary cluster.
Use the Name search field to locate a specific namespace.. By default, all namespaces associated with the protection group are available for selection. Clear any namespaces to not include in this failback operation.

important

You can fail back a protection group only once. Select all the namespaces that you want to include in the failback operation. You cannot fail back any namespaces that were excluded from the operation later.

- Click Next.

- In the Review page that opens, review the failback configuration details.

- Click Initiate to start the failback process.
The system initiates the failback and lists the failback action in the Disaster Recovery Actions page.

### What to do next​

- Ensure that the Status column for the failback event type in the Disaster Recovery Actions page displays Successful to confirm that the failback completed successfully.

In this topic:
