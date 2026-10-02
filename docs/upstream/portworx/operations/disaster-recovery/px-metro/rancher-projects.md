# Use Rancher Projects with ClusterPair

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/rancher-projects (Portworx Enterprise latest)

Use Rancher Projects with ClusterPair | Portworx Enterprise Documentation

note

If you are not using Rancher, skip to the Schedule your migration section.

Rancher has a concept of Projects that allow grouping of resources and Kubernetes or OpenShift namespaces. Depending on the resource and how it is created, Rancher adds the following label or annotation:

```

field.cattle.io/projectID: <project-short-UUID>

```

The ClusterPair with these project mappings will ensure that Rancher projects are effectively managed and associated during the migration process.

The `projectID` uniquely identifies the project, and the annotation or label on the Kubernetes or OpenShift object provides a way to tie an object back to a Rancher project.

Stork allows you to map projects from the source cluster to the destination cluster during migration. It will ensure that the following are transformed when migrating Kubernetes or OpenShift resources to a destination cluster:

- Labels and annotations for projectID `field.cattle.io/projectID` on any Kubernetes or OpenShift resource on the source cluster are transformed to their respective projectIDs on the destination cluster.

- The transformation of Namespace Selectors on a NetworkPolicy object that reference the `field.cattle.io/projectID` label to use the correct projectIDs on the destination cluster.

- The transformation of Namespace Selectors on a Pod object (Kubernetes version 1.24 or newer) that reference the `field.cattle.io/projectID` label to the correct projectIDs on the destination cluster.

## Prerequisites​

- All Rancher projects are created on both the source and the destination cluster.

## Create project mapping​

While creating the ClusterPair, use the argument `--project-mappings` to indicate how projectIDs on the source cluster should map to projectIDs on the destination cluster. Project mappings are provided as comma-separated key-value pairs.

For example:

```

storkctl generate clusterpair -n <migrationnamespace> <remotecluster> --project-mappings  <projectID-A1>=<projectID-A2>,<projectID-B1>=<projectID-B2>

```

In this example, `projectID-A1` on the source cluster maps to `projectID-A2` on the destination cluster, while `projectID-B1` on the source cluster maps to `projectID-B2` on the destination cluster.

### Include ClusterIDs in project mappings (Optional)​

For the projectIDs, you can also include clusterID prefixes in project mappings. Including clusterID prefixes ensures precise mapping, especially in scenarios with multiple clusters.

For example:

```

storkctl generate clusterpair \

-n <migrationnamespace> <remotecluster> \

--project-mappings \

p-58q4n=p-jjk2q c-m-wthc7l5q:p-58q4n=c-m-5sftdjns:p-jjk2q

```

In the above example, there are two mappings:

- A mapping with clusterIDs: `c-m-wthc7l5q:p-58q4n` containing the source clusterID `c-m-wthc7l5q` will map to `c-m-5sftdjns:p-jjk2q` containing the destination clusterID `c-m-5sftdjns`.

- A mapping without the clusterIDs: `p-58q4n` will map to `p-jjk2q`.

To view the information, click on the respective tabs, which provide details on how the projectIDs on the source cluster correlate with projectIDs on the destination cluster during resource migration.

- Source cluster

- Destination cluster

```

spec:

 platformOptions:

  rancher:

    projectMappings:

        c-m-wthc7l5q:p-58q4n: c-m-5sftdjns:p-jjk2q

        c-m-wthc7l5q:p-dmx28: c-m-5sftdjns:p-6nk5r

        c-m-wthc7l5q:p-hvxqm: c-m-5sftdjns:p-7cx4c

        c-m-wthc7l5q:p-fkth5: c-m-5sftdjns:p-w5z2s

        p-58q4n: p-jjk2q

        p-dmx28: p-6nk5r

        p-hvxqm: p-7cx4c

        p-xz4pd: p-fg5sd

```

```

spec:

 platformOptions:

  rancher:

    projectMappings:

        c-m-5sftdjns:p-jjk2q: c-m-wthc7l5q:p-58q4n

        c-m-5sftdjns:p-6nk5r: c-m-wthc7l5q:p-dmx28

        c-m-5sftdjns:p-7cx4c: c-m-wthc7l5q:p-hvxqm

        c-m-5sftdjns:p-w5z2s: c-m-wthc7l5q:p-fkth5

        p-jjk2q: p-58q4n

        p-6nk5r: p-dmx28

        p-7cx4c: p-hvxqm

        p-fg5sd: p-xz4pd

```

In this topic:
