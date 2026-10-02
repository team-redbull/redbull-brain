# ClusterPair CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/clusterpairs (Portworx Enterprise 3.6)

ClusterPair CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

ClusterPair represents pairing with other clusters.

## ClusterPair​

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

`spec`ClusterPairSpec is the spec to create the cluster pair`object`

`status`ClusterPairStatus is the status of the cluster pair`object`

### `spec` fields​

FieldDescriptionType

`spec.config`Config holds the configuration to connect to the remote cluster`object`

`spec.config.apiVersion`Legacy field from pkg/api/types.go TypeMeta.`string`

`spec.config.clusters`Clusters is a map of referencable names to cluster configs`object`

`spec.config.contexts`Contexts is a map of referencable names to context configs`object`

`spec.config.current-context`CurrentContext is the name of the context that you would like to use by default`string`

`spec.config.extensions`Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields`object`

`spec.config.kind`Legacy field from pkg/api/types.go TypeMeta.`string`

`spec.config.preferences`Preferences holds general information to be use for cli interactions`object`

`spec.config.preferences.extensions`Extensions holds additional information. This is useful for extenders so that reads and writes don't clobber unknown fields`object`

`spec.config.users`AuthInfos is a map of referencable names to user configs`object`

`spec.options`Options is a map of referenceable keys to values used for the cluster pair
For example, backuplocation, mode etc`object`

`spec.platformOptions`PlatformOptions are kubernetes platform provider related
options.`object`

`spec.platformOptions.rancher`Rancher configuration`object`

`spec.platformOptions.rancher.projectMappings`ProjectMappings allows a cluster pair to migrate namespaces between different
Rancher projects. The key in the map is the source project while the value
is the destination project. Specify this only if you have not provided
API key to stork for creating the project on the target cluster.`object`

### `status` fields​

FieldDescriptionType

`status.remoteStorageId`ID of the remote storage which is paired`string`

`status.schedulerStatus`Status of the pairing with the scheduler`string`

`status.storageStatus`Status of pairing with the storage driver`string`

In this topic:
