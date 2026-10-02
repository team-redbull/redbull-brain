# Portworx node labels

Source: https://docs.portworx.com/portworx-enterprise/reference/node-labels (Portworx Enterprise latest)

Portworx node labels | Portworx Enterprise Documentation

Portworx service and node configuration can be managed through Kubernetes node labels, allowing control over where Portworx is installed, and whether specific nodes should be designated as storage or metadata nodes. Below is a list of common Kubernetes node labels used for managing Portworx service behavior and node designation.

LabelDescription

`px/enabled=false`Prevents Portworx from being installed on a node.

`px/enabled=true`Allows Portworx to be installed on the node. This is the default behavior if no label is applied.

`px/enabled=remove`Removes Portworx from a node. After Portworx is removed, the label is converted to `px/enabled=false`.

`px/service=stop`Stops the Portworx service on a node.

`px/service=start`Starts the Portworx service on a node.

`px/service=restart`Restarts the Portworx service on a node.

`px/metadata-node=true` or `false`Indicates whether a node is eligible to become a KVDB (metadata) node. It does not guarantee that the node will become one.

`portworx.io/node-type=storageless`For disaggregated installs, labels the node as part of the storageless node group.

`portworx.io/node-type=storage`For disaggregated installs, labels the node as part of the storage node group.

`portworx.io/provision-storage-node="true"`Requests provisioning of a new storage node by creating a new driveset and attaching it to this node. This acts as a one-time request. It does not indicate a permanent state of being a storage node nor does it cause a repeated driveset creation in future if node becomes a storageless node because its driveset was taken over by another node. See Provisioning Storage Nodes in Portworx cluster for more information.

`portworx.io/provision-storage-node-handled="true"`Indicates that Portworx has processed the request to provision a new storage node. The result is indicated in a condition added to the node object. See How nodes are provisioned as storage nodes for more information.
