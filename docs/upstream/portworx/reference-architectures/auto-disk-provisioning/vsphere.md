# Manage storage nodes on VMware vSphere

Source: https://docs.portworx.com/portworx-enterprise/reference-architectures/auto-disk-provisioning/vsphere (Portworx Enterprise 3.6)

Manage storage nodes on VMware vSphere | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Availability across failure domains​

Since Portworx is a storage overlay that automatically replicates your data, Portworx by Everpure recommends using multiple availability zones when creating your VMware vSphere based cluster. Portworx automatically detects regions and zones that are populated using known Kubernetes node labels. You can also label nodes with custom labels to inform Portworx about region, zones and racks. Refer to the Cluster Topology awareness page for more details.

In this topic:
