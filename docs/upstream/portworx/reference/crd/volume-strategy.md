# VolumePlacementStrategy CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/volume-strategy (Portworx Enterprise latest)

VolumePlacementStrategy CRD reference | Portworx Enterprise Documentation

Portworx provides a CustomResourceDefinition (CRD) called `VolumePlacementStrategy`. The specification for this CRD is composed of 4 main sections:

- replicaAffinity

- Schema

- Example use cases

- replicaAntiAffinity

- Schema

- Example use cases

- volumeAffinity

- Schema

- Example use cases

- volumeAntiAffinity

- Schema

- Example use cases

Additional Information:

- topologyKey

- Templates

### replicaAffinity​
 Schema​

FieldDescriptionOptional?Default

enforcementSpecifies if the given rule is required (hard) or preferred (soft). Portworx will fail volume creation if it cannot provision volumes matching a rule with hard enforcement enabled.Yesrequired

matchExpressionsmatchExpressions is a list of label selector requirements. The requirements are ANDed.

The labels provided here are matched against the following:

- Kubernetes or OpenShift node labels

- PVC labels

- Portworx storage pool labels

Yes *

* required if topologyKey is emptyempty

topologyKeyKey for the node label that the system uses to denote a topology domain. The key can be for any node label that is present on the Kubernetes or OpenShift node.

NOTE: Using topologyKey requires nodes to be consistently labelled, i.e. every node in the cluster must have an appropriate label matching topologyKey. If some or all nodes are missing the specified topologyKey label, it can lead to unintended behavior.Yes*

* required if matchExpressions is emptyempty

weightSpecifies the weight of the rule. If more than one rule matches, then the rule with the highest weight is applied.Yes0

affected_replicasSpecifies the number of volume replicas affected by this rule.Yes0 (Interpreted as all volume replicas)

 Example use cases of replicaAffinity​

- Use SSD pools

- Use SSD and SATA and spread replicas evenly

- First replica SSD, others SATA

- Place volume on specific nodes, example infra etc

- Place volume only on racks 1, 2 and 3

By default, Portworx automatically adds the following labels to each of its storage pools. These can be used for replica affinity rules to target replicas on a specific storage pool type:

- `iopriority`

- `medium (Media Type)`

### replicaAntiAffinity​
 Schema​

FieldDescriptionOptional?Default

enforcementSpecifies if the given rule is required (hard) or preferred (soft). Portworx will fail volume creation if it cannot provision volumes matching a rule with hard enforcement enabled.Yesrequired

topologyKeyKey for the node label that the system uses to denote a topology domain. The key can be for any node label that is present on the Kubernetes or OpenShift node. Using topologyKey requires nodes to be consistently labelled, i.e. every node in the cluster must have an appropriate label matching topologyKey. If some or all nodes are missing the specified topologyKey label, it can lead to unintended behavior.Yes*

* required if matchExpressions is emptyempty

 Example use cases​

- Antiaffinity to data pools and spread across racks

- Antiaffinity to not use SATA pools

### volumeAffinity​
 Schema​

FieldDescriptionOptional?Default

enforcementSpecifies if the given rule is required (hard) or preferred (soft) Portworx will fail volume creation if it cannot provision volumes matching a rule with hard enforcement enabled.Yesrequired

topologyKeyKey for the node label that the system uses to denote a topology domain. The key can be for any node label that is present on the Kubernetes or OpenShift node.
Using topologyKey requires nodes to be consistently labelled, i.e. every node in the cluster must have an appropriate label matching topologyKey. If some or all nodes are missing the specified topologyKey label, it can lead to unintended behavior.Yesempty

matchExpressionsmatchExpressions is a list of label selector requirements. The requirements are ANDed.

The labels provided here are matched against the following:

- Kubernetes or OpenShift node labels

- PVC labels

- Portworx

- storage pool labels

Noempty

weightSpecifies the weight of the rule. If more than one rule matches, then the rule with the highest weight is applied.Yes0

 Example use cases​

- Collocate postgres volumes

- Place volume on DB type nodes or collocate with postgres volumes

### volumeAntiAffinity​
 Schema​

FieldDescriptionOptional?Default

enforcementSpecifies if the given rule is required (hard) or preferred (soft). Portworx will fail volume creation if it cannot provision volumes matching a rule with hard enforcement enabled.Yesrequired

topologyKeyKey for the node label that the system uses to denote a topology domain. The key can be for any node label that is present on the Kubernetes or OpenShift node.
Using topologyKey requires nodes to be consistently labelled, i.e. every node in the cluster must have an appropriate label matching topologyKey. If some or all nodes are missing the specified topologyKey label, it can lead to unintended behavior.Yesempty

matchExpressionsmatchExpressions is a list of label selector requirements. The requirements are ANDed.

The labels provided here are matched against the following:

- Kubernetes or OpenShift node labels

- PVC labels

- Portworx

- storage pool labels

Noempty

 Example use cases​
Do not collocate with other cassandra volumes

### topologyKey​

If `topologyKey` is not set, by default the rule will avoid/colocate volumes at the node level using built-in unique node identifiers.
 Portworx Built-in​
`topologyKey` can use the built-in key `portworx.io/pool` that is set automatically as a unique key/value on every Portworx pool. This can be used with volumeAffinity/volumeAntiAffinity to control volume placement at the pool level to work for individual pools.

### Templates​

Parameter values in `matchExpressions` may use predefined templates. The `VolumePlacementStrategy` will automatically resolve these templates at provision time as detailed below:

- key: `namespace`

- `${pvc.namespace}`

- Replaced with namespace of the `PersistentVolumeClaim` that triggered provisioning

- Example: Do not collocate with other app volumes within the same namespace

- key: `px/statefulset-pod`

- `${pvc.statefulset-pod}`

- Replaced with the `StatefulSet` pod name the `PersistentVolumeClaim` belongs to

- Matches corresponding label key/value applied to the volume

- Use this with multiple `volumeClaimTemplates` in a `StatefulSet` to relate volumes for the same replica pod to each other

- Works with `Immediate` binding mode

- Example: Collocate volumes that belong to the same StatefulSet pod

- key: `labelkey`

- `${pvc.labels.labelkey}`

- Portworx replaces any values in the template `${pvc.labels.labelkey}` with the `pvc.labels` value for `labelkey`.

- Example: Label the volumes dynamically based on the PVC label field

In this topic:
