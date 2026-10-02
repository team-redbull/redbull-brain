# Register Application CRDs for Stork Disaster Recovery

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/stateful-applications/application-registration (Portworx Enterprise latest)

Register Application CRDs for Stork Disaster Recovery | Portworx Enterprise Documentation

Stork uses ApplicationRegistration custom resources to register your application CRDs for cluster-to-cluster migration and disaster recovery failover and failback. When Stork knows about your custom CRDs, it can migrate, scale down, and stash them appropriately during DR operations.

## Fetch default ApplicationRegistrations​

By default, Stork supports several CRDs for common applications. List the existing defaults by entering the `storkctl get applicationregistrations` command:

```

storkctl get applicationregistrations

```

```

NAME                           KIND                           CRD-NAME                   VERSION    SUSPEND-OPTIONS     KEEP-STATUS

adminnetworkpolicy             AdminNetworkPolicy             policy.networking.k8s.io   v1alpha1                       false

alertmanager                   Alertmanager                   monitoring.coreos.com      v1                             false

alertmanagerconfig             AlertmanagerConfig             monitoring.coreos.com      v1alpha1                       false

bgpconfiguration               BGPConfiguration               crd.projectcalico.org      v1                             false

bgpfilter                      BGPFilter                      crd.projectcalico.org      v1                             false

bgppeer                        BGPPeer                        crd.projectcalico.org      v1                             false

blockaffinity                  BlockAffinity                  crd.projectcalico.org      v1                             false

caliconodestatus               CalicoNodeStatus               crd.projectcalico.org      v1                             false

clusterinformation             ClusterInformation             crd.projectcalico.org      v1                             false

felixconfiguration             FelixConfiguration             crd.projectcalico.org      v1                             false

globalnetworkpolicy            GlobalNetworkPolicy            crd.projectcalico.org      v1                             false

globalnetworkset               GlobalNetworkSet               crd.projectcalico.org      v1                             false

hostendpoint                   HostEndpoint                   crd.projectcalico.org      v1                             false

ipamblock                      IPAMBlock                      crd.projectcalico.org      v1                             false

ipamconfig                     IPAMConfig                     crd.projectcalico.org      v1                             false

ipamhandle                     IPAMHandle                     crd.projectcalico.org      v1                             false

ippool                         IPPool                         crd.projectcalico.org      v1                             false

ipreservation                  IPReservation                  crd.projectcalico.org      v1                             false

kubecontrollersconfiguration   KubeControllersConfiguration   crd.projectcalico.org      v1                             false

networkpolicy                  NetworkPolicy                  crd.projectcalico.org      v1                             false

networkset                     NetworkSet                     crd.projectcalico.org      v1                             false

podmonitor                     PodMonitor                     monitoring.coreos.com      v1                             false

portworxdiag                   PortworxDiag                   portworx.io                v1                             false

probe                          Probe                          monitoring.coreos.com      v1                             false

prometheus                     Prometheus                     monitoring.coreos.com      v1         spec.replicas,int   false

prometheusrule                 PrometheusRule                 monitoring.coreos.com      v1                             false

servicemonitor                 ServiceMonitor                 monitoring.coreos.com      v1                             false

thanosruler                    ThanosRuler                    monitoring.coreos.com      v1                             false

tier                           Tier                           crd.projectcalico.org      v1                             false

volumeplacementstrategy        VolumePlacementStrategy        portworx.io                v1beta2                        false

volumeplacementstrategy        VolumePlacementStrategy        portworx.io                v1beta1                        false

volumesnapshot                 VolumeSnapshot                 snapshot.storage.k8s.io    v1                             false

volumesnapshot                 VolumeSnapshot                 snapshot.storage.k8s.io    v1beta1                        false

volumesnapshotclass            VolumeSnapshotClass            snapshot.storage.k8s.io    v1                             false

volumesnapshotclass            VolumeSnapshotClass            snapshot.storage.k8s.io    v1beta1                        false

volumesnapshotcontent          VolumeSnapshotContent          snapshot.storage.k8s.io    v1                             false

volumesnapshotcontent          VolumeSnapshotContent          snapshot.storage.k8s.io    v1beta1                        false

```

## Register a new CRD with Stork​

To register a new CRD with Stork, perform these steps:

- Create an `applicationregistration` spec, specifying the following:

-
metadata.name: the name of the spec

-
resources.PodsPath: (Optional) the path which stores the pods created by the CR. These will be deleted when scaling down the migration.

-
resources.group: The group of the CRD being registered.

-
resources.version: The version of the CRD being registered.

-
resources.kind: The kind of the CRD being registered.

-
resources.keepStatus: (Optional) If you don't want to save the resource's status after migration, set this value to `false`.

-
resources.suspendOptions.path: (Optional) With the path in the CRD spec which contains the option to suspend the application.

-
resources.suspendOptions.type: (Optional) With the type of the field that is used to suspend the operation. For example, `int`, if the field contains the replica count for the application.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: ApplicationRegistration

metadata:

  name: myappname

resources:

- PodsPath: <POD_PATH>

  group: <CRD_GROUP_NAME>

  version: <CRD_VERSION>

  kind: <CR_KIND>

  keepStatus: false

  # To disable CR on migration,

  # CR spec path for disable

  suspendOptions:

    path: <spec_path>

    type: <type_of_value_to_set> (can be "int"/"bool")

```

The following ApplicationRegistration example allows Stork to migrate a `datastax/cassandra` operator during cluster-to-cluster migration and DR operations:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: ApplicationRegistration

metadata:

  name: cassandra

resources:

- PodsPath: ""

  group: cassandra.datastax.com

  version: v1beta1

  kind: CassandraDatacenter

  keepStatus: false #cassandra datacenter status will not be migrated

  suspendOptions:

    path: spec.stopped #path to disable cassandra datacenter

    type: bool #type of value to be set for spec.stopped

```

- Apply the spec:

- Kubernetes

- Openshift

```

kubectl apply -f <application-registration-spec>.yaml

```

```

oc apply -f <application-registration-spec>.yaml

```

Once you've applied the spec, you can verify it by entering the following `storkctl get` command, specifying your own application name:

```

storkctl get appreg <app-name>

```

```

NAME        KIND                  CRD-NAME                 VERSION   SUSPEND-OPTIONS     KEEP-STATUS

cassandra   CassandraDatacenter   cassandra.datastax.com   v1beta1   spec.stopped,bool   false

```

note

If you register your CRD with Stork using an applicationRegistration CRD, you do not need to modify the migration spec.

## Managing application migrations with Stork​

Migration of applications controlled by operators in Stork can be conducted with either asynchronous or synchronous DR methods. When the `startApplications` parameter is set to `false` for migrations, it is expected that the application pods will not be running in the destination cluster once the migration is completed. For DR scenarios, the `startApplications` flag is by default set to `false` since the applications need to be in a scale down state on the destination cluster.

Different applications may require specific scaling down procedures by modifying certain parameters in their Custom Resource (CR) specifications. Stork provides support for modifying the CR spec to scale down these applications, utilizing the options provided by the `ApplicationRegistration`'s `suspendOptions`. See here for the list of options.

### Safeguarding application pods during migration with Stork's stash strategy​

For certain applications controlled by clusterwide operators that do not support scaling down via CR spec modifications, the pods related to these applications may become active in the destination namespace after migration. This can be problematic if the intention is to avoid starting the application in the destination cluster before performing the actual failover.

To prevent the application pods from becoming active prematurely, Stork offers a feature known as the "Stash Strategy". This feature allows the CR content to be stashed in a config map during migration on the destination cluster. The actual CR spec is created on the destination cluster only when the applications failover to the destination cluster using `storkctl`.

note

The `stashStrategy` feature is only available starting from Stork version 23.8.0. Moreover, do not define any suspend options for application registrations with the `stashStrategy` enabled.

Here is an example of an application registration for Elasticsearch with the stash strategy enabled. Modifications need to be made in both the source and destination clusters before initiating the migration:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: ApplicationRegistration

metadata:

  name: elasticsearch

resources:

- group: elasticsearch.k8s.elastic.co

  keepStatus: false

  kind: Elasticsearch

  stashStrategy:

    stashCR: true

  version: v1

- group: elasticsearch.k8s.elastic.co

  keepStatus: false

  kind: Elasticsearch

  stashStrategy:

    stashCR: true

  version: v1beta1

- group: elasticsearch.k8s.elastic.co

  keepStatus: false

  kind: Elasticsearch

  stashStrategy:

    stashCR: true

  version: v1alpha1

```

note

When configuring Disaster Recovery (DR) setups in OpenShift, it's crucial to maintain consistency in the operator's namespace scope. Mixing namespaced and clusterwide operators on different sides of the replication process can lead to operational issues and unexpected behavior. To ensure a smooth and reliable DR deployment, make a deliberate choice between using either namespaced or clusterwide operators, and avoid combining them within the same DR setup. Consistency in the operator's scope simplifies management, troubleshooting, and maintenance of your disaster recovery solution.

In this topic:
