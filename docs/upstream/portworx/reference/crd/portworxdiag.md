# PortworxDiag CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/portworxdiag (Portworx Enterprise latest)

PortworxDiag CRD reference | Portworx Enterprise Documentation

PortworxDiag is the Schema for the portworxdiags API.

## PortworxDiag​

FieldDescriptionType

`apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`spec`PortworxDiagSpec is the spec used to define a portworx diag.`object`

`status`PortworxDiagStatus is the status of a portworx diag.`object`

### `spec` fields​

FieldDescriptionType

`spec.portworx`Configuration for diags collection of the main Portworx component.`object`

`spec.portworx.generateCore`Generates the core dump as well when collecting the node diags. Could be useful
to analyze the current state of the system.`boolean`

`spec.portworx.nodes`Nodes for which the diags need to be collected. If a volume selector is
also specified, then both the selectors will be honored and the selected
nodes will be a union of both selectors.`object`

`spec.portworx.nodes.all`Select all nodes in the Portworx cluster. If set to true, other selectors are ignored.`boolean`

`spec.portworx.nodes.ids`Ids of the nodes to be selected.`array`

`spec.portworx.nodes.labels`Labels of the nodes to be selected.`object`

`spec.portworx.podDiags`Collects all the pod diags. This includes diags for additional Kubernetes objects like ControllerRevisions, PersistentVolumeClaims (PVCs), PersistentVolumes (PVs), StorageClasses (SCs), CSINodes, CSIDrivers, VolumeAttachments, Deployments, DaemonSets, ReplicaSets, StatefulSets, Services, Endpoints, Secrets, and ConfigMaps.
Specify whether Pod diags need to be collected or not.`boolean`

`spec.portworx.volumes`Collects the diags for the nodes on which the selected volumes are attached.`object`

`spec.portworx.volumes.ids`Ids of the volumes to be selected.`array`

`spec.portworx.volumes.labels`Labels of the volumes to be selected.`object`

### `status` fields​

FieldDescriptionType

`status.clusterUuid`UUID of the Portworx cluster. This is useful to find the uploaded diags.`string`

`status.message`Optional message used to give the reason for any failure.`string`

`status.nodes`Status of the diags collection from all the selected nodes.`array`

`status.nodes.message`Optional message used to give the reason for any failure.`string`

`status.nodes.nodeId`ID of the node for which the diag status is reported.`string`

`status.nodes.status`One word status of the diags collection on the node.`string`

`status.phase`One word status of the entire diags collection job.`string`

`status.podDiags`Status of the diags collection from all the pods.`object`

`status.podDiags.message`Optional message used to give the reason for any failure.`string`

`status.podDiags.status`One word status of the pod diags collection.`string`

In this topic:
