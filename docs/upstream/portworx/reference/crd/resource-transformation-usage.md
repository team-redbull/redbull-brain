# ResourceTransformation

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/resource-transformation-usage (Portworx Enterprise latest)

ResourceTransformation | Portworx Enterprise Documentation

Metro and asynchronous disaster recovery (DR) involves migrating Kubernetes resources from a source cluster to a destination cluster. To ensure applications can come up correctly on the destination clusters, you may need to modify resources such as `Service`, `ServiceAccount`, or `ConfigMap` to work as intended on your destination cluster. The ResourceTransformation feature allows you to define a set of rules that modify the Kubernetes resources before they are migrated to the destination cluster.

ResourceTransformation is a custom resource (CR) that accepts change rules that Stork follows to modify resources from a source cluster before applying them onto a destination cluster.

## ResourceTransformation schema​

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

`specs`ResourceTransformationSpec is used to update k8s resources
before migration/restore`object`

### ResourceTransformation spec​

FieldDescriptionType

`specs.transformSpecs.paths`Paths collection of resource path to update`array`

`specs.transformSpecs.paths.operation`Operation to be performed on path
add/modify/delete/replace/jsonPatch`string`

`specs.transformSpecs.paths.path`Path k8s resource for operation`string`

`specs.transformSpecs.paths.type`Type of value specified int/bool/string/slice/keypair`string`

`specs.transformSpecs.paths.value`Value for given k8s path`string`

`specs.transformSpecs.resource`Resource is GroupVersionKind for k8s resources
should be in format `group/version/kind"`string`

`specs.transformSpecs.selectors`Selectors label selector to filter out resource for
patching`object`

-
Path: the YAML path for a given Kubernetes resource you want to perform an operation on. Provide this in dot notation, e.g. `metadata.labels`.

Starting from Stork version 25.4.0, paths support array indexing, which allows you to modify fields within specific elements of arrays. For example, to modify the first container’s image in a Pod, use a path like `spec.containers[0].image`.

important

Transformations on entire array elements or objects (e.g. `spec.ports[0]`) are not supported. You can only transform individual fields within an array element, such as `spec.ports[0].name` or `spec.ports[0].nodePort`.

-
Value: the value you want to set at the selected path. For example, if the path is `spec.replicas`, you can specify a value of `4`.

-
Type: the supported data type you want to update values to. Type can be one of the following:

TypeValueExample

KeyPairComma separated key value pair for patching map type in resource specsa:b,c:d,e:f,g:h
 <key1:value1>, <key2:value2>, … <keyN:valueN>

ListComma separated array element list for patching resource specs[a,b,c,d]
 <val1,val2,…,valN>

IntInteger type value for updating resources0

StringString type values“new-val”

BoolBoolean values for setting path valueTrue, False

note

Complex types such as Array of KeyPairs is not supported.

-
Operations What operation you want to perform on the given `path` in an unstructured Kubernetes object:

- Add: sets a new nested `path` in an unstructured object specification with `value`. If `path` already exists, this will replace the existing value.

- Modify: updates a nested path in an unstructured resource object with `value`. If the value is a `KeyPair` or `List` type, this will append `value` to the existing path.

- Delete: removes the specified nested spec path from an unstructured object.

note

You can specify multiple paths for the same resource and multiple resources in single ResourceTransformation CR.

## Examples​

The example in this topic modifies all Kubernetes services in the `mysql` namespace on the destination cluster during the migration based on the migration schedule.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind : ResourceTransformation

metadata:

  name: name-of-transform-rules

specs:

 transformSpecs:

 - paths:

     - path: <spec-path-of-k8s-resources-to-modify>

       value: <value-to-be-updated-at-above-path>

       type: <type-of-value->

       operation: <operation-to-perform>

     - path: <spec-path-of-k8s-resources-to-modify>

       value: <value-to-be-updated-at-above-path>

       type: <type-of-value->

       operation: <operation-to-perform>

   resource: <k8s-resource-version/kind-format>

```

### Define the source service object​

This `Service` spec defines the source service object. Note the following:

- There's currently no `metadata.annotations` defined in the following service object. Secondly the `type` of service being used is `ClusterIP`.

- `metadata.labels` contains only the `app: mysql` key value pair.

```

apiVersion: v1

kind: Service

metadata:

 name: mysql-service

 labels:

   app: mysql

spec:

  type: ClusterIP

 selector:

   app: mysql

 ports:

   - name: transport

     port: 3306

```

### Create a ResourceTransformation spec​

You must create the `ResourceTransformation` CRD in the source namespace. The `ResourceTransformation` spec does the following when it's called:

- Changes the type from `service` to `LoadBalancer`.

- Updates `metadata.labels`, adding the `handler: project` key value pair to it and replacing `app: mysql` with `app:mysql-2`.

- Adds new `metadata.annotations` to the service object.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind : ResourceTransformation

metadata:

  name: mysql-service-transform

  namespace: mysql

specs:

 transformSpecs:

 - paths:

     - path: "spec.type"

       value: "LoadBalancer"

       type: "string"

       operation: "modify"

     - path: "metadata.labels"

       value: "handler:project,app:mysql-2"

       type: "keypair"

       operation: "modify"

     - path: "metadata.annotations"

       value: "handler:project,app:mysql-2"

       type: "keypair"

       operation: "add"

   resource: "/v1/Service"

```

note

The resource field in the above example is the combination of `apiVersion` and `kind` fields from the Kubernetes service object. You can get these values from the source object for which you are creating `ResourceTransformation` spec.

When migrated, Portworx will use the rules defined in this ResourceTransformation spec to modify the object it creates on the destination cluster.

### Use the ResourceTransformation Spec​

A `MigrationSchedule` references the `ResourceTransformation` defined above in the `spec.template.spec.transformSpecs` field. When it triggers, the `MigrationSchedule` uses the `ResourceTransformation` defined above to change the object it deploys on the destination cluster:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: MigrationSchedule

metadata:

 name: mysql-migration-transform-interval

 Namespace: mysql

spec:

 schedulePolicyName: migrate-every-5m

 template:

   spec:

     # This should be the name of the cluster pair

     clusterPair: remoteclusterpair

     # If set to false this will migrate only the volumes. No PVCs, apps, etc will be migrated

     includeResources: true

     # If set to false, the deployments and stateful set replicas will be set to

     # 0 on the destination. There will be an annotation with

     # "stork.openstorage.org/migrationReplicas" to store the replica count from the source

     startApplications: false

     # Update service resource as per transformation specs

     transformSpecs:

     - mysql-service-transform

     namespaces:

     - mysql-1-pvc-mysql-migration-transform-interval

```

### Using array indexing in `path`​

This example demonstrates how to update a field within a specific element of an array using indexed paths. In this case, the `nodePort` field of the first port in a `Service` object is modified.

While array indexing is supported in the `path` field (e.g., `spec.ports[0].nodePort`), you must target a specific subfield within the array element. You cannot transform or replace the entire array element (such as `spec.ports[0]`) itself. For example, setting a complete port object at `spec.ports[0]` is not supported.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: ResourceTransformation

metadata:

  name: service-port-array-transform

specs:

  transformSpecs:

  - paths:

      - path: "spec.ports[0].nodePort"

        value: "30080"

        type: "int"

        operation: "modify"

    resource: "/v1/Service"

```

In this topic:
