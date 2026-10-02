# Failover

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/acm-dr/failover (Portworx Enterprise 3.6)

Failover | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When a workload cluster becomes unavailable, you can fail over its protected resources to another operational workload cluster. Failover can serve as an emergency recovery action when the source cluster becomes inaccessible unexpectedly, or as a planned migration while the source cluster remains available. With ACM-based disaster recovery, failover occurs at the Protection Group level, meaning that all namespaces and resources included in a protection group fail over together to the destination cluster.

This topic explains how to trigger a failover using the Portworx MultiCluster Operator on the hub cluster.

For information about triggering a failover by using `kubectl`, see the Stork documentation.

## Prerequisites​

- A disaster recovery pair between the source and destination workload clusters.
For more information, see Configure a Disaster Recovery Pair.

- A protection group that references the DR pair and that has completed at least one successful migration.
For more information, see Manage Protection Groups.

## Perform a failover​

To perform a failover, complete the following steps:

- Sign in to the OpenShift web console.

- Switch to the multicluster management view (All Clusters on OpenShift 4.18 and 4.19, or Fleet management on 4.20 and later), and from the left navigation pane, select the Portworx option.

- Select Protection Groups.
 The system displays the Protection Groups page that lists all existing protection groups.

- Click the vertical ellipsis menu associated with the protection group to fail over, and select Initiate Failover.
The system displays the Failover window.

- In the Action Details page of the Failover window, perform the following:

- In the Failover Name field, enter a name for the failover action.

- (Optional) Under Skip source operations, select the Do not perform operations on the source cluster checkbox if the source cluster is unavailable and cannot participate in the failover process.

note

For failover actions on a unidirectional DR pair, always select the Do not perform operations on the source cluster checkbox.

- (Optional) Under Source cluster domain, select the Do not deactivate source cluster domain checkbox to keep the source cluster domain active during failover.

- Click Next.

- In the Choose Namespaces page that opens, do the following:

- Review the list of namespaces available for failover.
The list includes namespaces defined in the protection group, either through manual selection or label selectors.

- Select the checkbox associated with each namespace to fail over to the disaster recovery cluster.
Use the Name search field to locate a specific namespace.. By default, all namespaces associated with the protection group are available for selection. Clear any namespaces to not include in this failover operation.

important

You can fail over a protection group only once. Select all the namespaces that you want to include in the failover operation. After you initiate the failover, replication for the protection group stops, and you cannot fail over any namespaces that were excluded from the operation later.

- Click Next.

- In the Review page that opens, review the failover configuration details.

- Click Initiate to start the failover process.
The system initiates the failover and lists the failover action in the Disaster Recovery Actions page.

### What to do next​

- Ensure that the Status column for the failover event type in the Disaster Recovery Actions page displays Successful to confirm that the failover completed successfully.

- If the source cluster is unavailable, you must manually delete the protection group after the failover completes. For more information, see Delete a protection group.

In this topic:
