# Cloud Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/cloud-snapshots (Portworx Enterprise latest)

Cloud Snapshots | Portworx Enterprise Documentation

A cloud snapshot is a point-in-time copy of a volume or group of volumes that Portworx uploads from the source storage system to a remote cloud storage location, such as a configured S3-compliant endpoint like AWS S3. You can use cloud snapshots to protect data against cluster-level failures and enable disaster recovery across regions or clusters. Cloud snapshots support long-term retention, off-site backups, and compliance with data protection policies.

By default, Portworx groups the backup data into 10 MB objects, compresses the objects, and uploads them to the cloud. You can increase the CloudSnap object size from the default 10 MB to 100 MB. Using larger object sizes improves the backup and restore performance for large volumes, particularly in environments using NFS backends. For information on how to increase the CloudSnap object size, see Increase the CloudSnap object size.

This topic describes how you can create cloud snapshots of Portworx volumes and how you can clone those snapshots to use them in pods.

important

For FlashArray Direct Access (FADA) volumes, create and restore cloud snapshots by using the CSI-based snapshot and restore method.

## Prerequisites​

-
Ensure that you have two running Portworx clusters.
For information on how to install Portworx on a cluster, see System Requirements.

-
Ensure that you have an Object store. Cloud snapshots work with Amazon S3, Azure Blob, Google Cloud Storage, or any S3 compatible object store. If you do not have an object store, Portworx by Everpure recommends using MinIO.
For information on how to install MinIO, see the MinIO Quickstart Guide.

-
Ensure that you have a secret store provider.
For information on how to configure a secret store provider, see Secret store management.

-
Ensure that Stork is installed and running on your cluster.

note

If you generated the Portworx specs using the default options in Portworx Central, Stork is already installed.

-
Set up secrets in Portworx to connect and authenticate with the configured cloud provider.
For more information, see the Create and Configure Credentials section.

-
To increase the CloudSnap object size to 100 MB, ensure that each node in your cluster has at least 16 core CPU and 16 GB of RAM.

## Limitations​

-
The following are the limitations of cloud snapshots on FADA volumes:

- Cloud snapshots on FADA volumes do not support group snapshots.

- Cloud snapshots on FADA volumes do not support schedules in Portworx. However, schedules through Stork is supported.

-
If a CloudSnap is created with a 100 MB object size, restoring it to a cluster configured with a 10 MB object size fails.

## (Optional) Increase the CloudSnap object size​

To increase the CloudSnap object size from the default 10 MB to 100 MB, use the `PX_CLOUDSNAP_LARGE_OBJECT_SUPPORT` environment variable in the PX configuration:

```

spec:

  env:

    - name: PX_CLOUDSNAP_LARGE_OBJECT_SUPPORT

      value: "true"

```

After applying this change, the Portworx cluster automatically restarts to apply the new setting.

## Create and Restore a Cloud Snapshot in the Same Cluster​

This section describes how to create a snapshot and restore it to the same Portworx cluster. You can either snapshot individual PVCs one by one or snapshot a group of PVCs.

note

You cannot use an older version of Portworx to restore a cloud snapshot created with a newer one. For example, if you are running Portworx 3.3, you cannot restore a cloud snapshot created with Portworx 3.4.

### Creating Cloud Snapshot of a Single PVC​

The cloud snapshot method supports the following annotations:

- portworx/snapshot-type: Indicates the type of snapshot. For cloud snapshots, the value should be cloud.

- portworx/cloud-cred-id (Optional): Specifies the credentials UUID if you have configured credentials for multiple cloud providers.

- portworx.io/cloudsnap-incremental-count: Specifies the number of incremental cloud snapshots after which a full backup is taken.

Example

Below, we create a cloud snapshot for a PVC called mysql-data backed by a Portworx volume.

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mysql-snapshot

  namespace: default

  annotations:

    portworx/snapshot-type: cloud

spec:

  persistentVolumeClaimName: mysql-data

```

After you apply the above object you can check the status of the snapshots using the `kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io/` command with the name of your snapshot appended:

- Kubernetes

- OpenShift

```

kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io/mysql-snapshot

```

```

oc get volumesnapshot.volumesnapshot.external-storage.k8s.io/mysql-snapshot

```

```

NAME                             AGE

volumesnapshots/mysql-snapshot   2s

```

- Kubernetes

- OpenShift

```

kubectl get volumesnapshotdatas

```

```

oc get volumesnapshotdatas

```

```

NAME                                                                            AGE

volumesnapshotdatas/k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-5a34ec89e61c    1s

```

The creation of the volumesnapshotdatas object indicates that the snapshot is created. If you describe the volumesnapshotdatas object you can see the Portworx Cloud Snapshot ID and the PVC for which the snapshot was created.

- Kubernetes

- OpenShift

```

kubectl describe volumesnapshotdatas

```

```

Name:         k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-5a34ec89e61c

Namespace:

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshotData

Metadata:

  Cluster Name:

  Creation Timestamp:             2018-03-08T03:17:02Z

  Deletion Grace Period Seconds:  <nil>

  Deletion Timestamp:             <nil>

  Resource Version:               29989636

  Self Link:                      /apis/volumesnapshot.external-storage.k8s.io/v1/k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-5a34ec89e61c

  UID:                            xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

Spec:

  Persistent Volume Ref:

    Kind:  PersistentVolume

    Name:  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

  Portworx Volume:

    Snapshot Id:  xxxxxxxx-xxxx-xxxx-xxxx-33c5ab8d4d8e/149813028909420894-125009403033610837-incr

  Volume Snapshot Ref:

    Kind:  VolumeSnapshot

    Name:  default/mysql-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

Status:

  Conditions:

    Last Transition Time:  <nil>

    Message:

    Reason:

    Status:

    Type:

  Creation Timestamp:      <nil>

Events:                    <none>

```

```

oc describe volumesnapshotdatas

```

```

Name:         k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-5a34ec89e61c

Namespace:

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshotData

Metadata:

  Cluster Name:

  Creation Timestamp:             2018-03-08T03:17:02Z

  Deletion Grace Period Seconds:  <nil>

  Deletion Timestamp:             <nil>

  Resource Version:               29989636

  Self Link:                      /apis/volumesnapshot.external-storage.k8s.io/v1/k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-5a34ec89e61c

  UID:                            xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

Spec:

  Persistent Volume Ref:

    Kind:  PersistentVolume

    Name:  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

  Portworx Volume:

    Snapshot Id:  xxxxxxxx-xxxx-xxxx-xxxx-33c5ab8d4d8e/149813028909420894-125009403033610837-incr

  Volume Snapshot Ref:

    Kind:  VolumeSnapshot

    Name:  default/mysql-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447

Status:

  Conditions:

    Last Transition Time:  <nil>

    Message:

    Reason:

    Status:

    Type:

  Creation Timestamp:      <nil>

Events:                    <none>

```

### Creating Cloud Snapshot of a Group of PVCs​

To take group snapshots, you need to use the `GroupVolumeSnapshot` CRD object and pass in portworx/snapshot-type as cloud. Here is a simple example:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-group-cloudsnapshot

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

  options:

    portworx/snapshot-type: cloud

```

The above spec takes a group snapshot of all PVCs that match labels `app=cassandra`.

The Examples section has a more detailed end-to-end example.

note

The above spec backs up the snapshots to a cloud S3 endpoint. If you intend on taking snapshots just local to the cluster, refer to Create local group snapshots.

The `GroupVolumeSnapshot` object also supports specifying pre and post rules that are run on the application pods using the volumes being snapshotted. This allows users to quiesce the applications before the snapshot is taken and resume I/O after the snapshot is taken. For more information, see 3D Snapshots.

#### Checking status of group cloud snapshots​

A new VolumeSnapshot object gets created for each PVC that matches the given `pvcSelector`.
For example, if the label selector `app: cassandra` matches three PVCs, you have three volumesnapshot objects.

You can track the status of the group volume snapshots using:

- Kubernetes

- OpenShift

```

kubectl describe groupvolumesnapshot <group-snapshot-name>

```

```

oc describe groupvolumesnapshot <group-snapshot-name>

```

This shows the latest status and lists the VolumeSnapshot objects after it is complete.
Below is an example of the status section of the cassandra group snapshot.

```

Status:

  Stage:   Final

  Status:  Successful

  Volume Snapshots:

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/763613271174793816-922960401583326548

        Snapshot Type:     cloud

    Parent Volume ID:      763613271174793816

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-66490f4172c7

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/1081147806034223862-518034075073409747

        Snapshot Type:     cloud

    Parent Volume ID:      1081147806034223862

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-b62951dcca0e

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/237262101530372284-299546281563771622

        Snapshot Type:     cloud

    Parent Volume ID:      237262101530372284

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-ee3b13f7c03f

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

-
You can see three volume snapshots which are part of the group snapshot. The name of the volume snapshot is in the Volume Snapshot Name field. For more details on the `volumesnapshot`, you can do:

- Kubernetes

- OpenShift

```

kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io/<volume-snapshot-name> -o yaml

```

```

oc get volumesnapshot.volumesnapshot.external-storage.k8s.io/<volume-snapshot-name> -o yaml

```

#### Retries of group cloud snapshots​

If a cloud `GroupVolumeSnapshot` fails to trigger, it is retried. However, by default, if a cloud `GroupVolumeSnapshot` fails after it has been triggered or started successfully, it is marked `Failed` and is not retried.

To change this behavior, you can set the `maxRetries` field in the spec. In below example, we perform three retries on failures.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-group-cloudsnapshot

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

  maxRetries: 3

  options:

    portworx/snapshot-type: cloud

```

When maxRetries are enabled, `NumRetries` in the status of the groupvolumesnapshot indicates the number of retries performed.

#### Snapshots across namespaces​

When creating a group snapshot, you can specify a list of namespaces to which the group snapshot can be restored.
Below is an example of a group cloud snapshot which can be restored into prod-01 and prod-02 namespaces.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-groupsnapshot

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

  options:

    portworx/snapshot-type: cloud

  restoreNamespaces:

   - prod-01

   - prod-02

```

#### Examples​
 Group cloud snapshot for all cassandra PVCs​
In below example, we take a group snapshot for all PVCs in the default namespace and that have labels app: cassandra and back it up to the configured cloud S3 endpoint in the Portworx cluster.
 Step 1: Deploy cassandra statefulset and PVCs​
Following spec creates a replica 3 cassandra statefulset. Each replica pod uses its own PVC.

```

##### Portworx storage class

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-repl2

provisioner: pxd.portworx.com

parameters:

  repl: "2"

---

apiVersion: v1

kind: Service

metadata:

  labels:

    app: cassandra

  name: cassandra

spec:

  clusterIP: None

  ports:

    - port: 9042

  selector:

    app: cassandra

---

apiVersion: "apps/v1"

kind: StatefulSet

metadata:

  name: cassandra

spec:

  selector:

    matchLabels:

      app: cassandra

  serviceName: cassandra

  replicas: 3

  template:

    metadata:

      labels:

        app: cassandra

    spec:

      containers:

      - name: cassandra

        image: gcr.io/google-samples/cassandra:v12

        imagePullPolicy: Always

        ports:

        - containerPort: 7000

          name: intra-node

        - containerPort: 7001

          name: tls-intra-node

        - containerPort: 7199

          name: jmx

        - containerPort: 9042

          name: cql

        resources:

          limits:

            cpu: "500m"

            memory: 1Gi

          requests:

           cpu: "500m"

           memory: 1Gi

        securityContext:

          capabilities:

            add:

              - IPC_LOCK

        lifecycle:

          preStop:

            exec:

              command: ["/bin/sh", "-c", "PID=$(pidof java) && kill $PID && while ps -p $PID > /dev/null; do sleep 1; done"]

        env:

          - name: MAX_HEAP_SIZE

            value: 512M

          - name: HEAP_NEWSIZE

            value: 100M

          - name: CASSANDRA_SEEDS

            value: "cassandra-0.cassandra.default.svc.cluster.local"

          - name: CASSANDRA_CLUSTER_NAME

            value: "K8Demo"

          - name: CASSANDRA_DC

            value: "DC1-K8Demo"

          - name: CASSANDRA_RACK

            value: "Rack1-K8Demo"

          - name: CASSANDRA_AUTO_BOOTSTRAP

            value: "false"

          - name: POD_IP

            valueFrom:

              fieldRef:

                fieldPath: status.podIP

          - name: POD_NAMESPACE

            valueFrom:

              fieldRef:

                fieldPath: metadata.namespace

        readinessProbe:

          exec:

            command:

            - /bin/bash

            - -c

            - /ready-probe.sh

          initialDelaySeconds: 15

          timeoutSeconds: 5

        # These volume mounts are persistent. They are like inline claims,

        # but not exactly because the names need to match exactly one of

        # the stateful pod volumes.

        volumeMounts:

        - name: cassandra-data

          mountPath: /cassandra_data

  # These are converted to volume claims by the controller

  # and mounted at the paths mentioned above.

  volumeClaimTemplates:

  - metadata:

      name: cassandra-data

      labels:

        app: cassandra

      annotations:

        volume.beta.kubernetes.io/storage-class: portworx-repl2

    spec:

      accessModes: [ "ReadWriteOnce" ]

      resources:

        requests:

          storage: 2Gi

```

 Step 2: Wait for all cassandra pods to be running​
List the cassandra pods:

- Kubernetes

- OpenShift

```

kubectl get pods -l app=cassandra

```

```

oc get pods -l app=cassandra

```

```

NAME          READY     STATUS    RESTARTS   AGE

cassandra-0   1/1       Running   0          3m

cassandra-1   1/1       Running   0          2m

cassandra-2   1/1       Running   0          1m

```

Once you see all the three pods, you can also list the cassandra PVCs.

- Kubernetes

- OpenShift

```

kubectl get pvc -l app=cassandra

```

```

oc get pvc -l app=cassandra

```

```

NAME                         STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS        AGE

cassandra-data-cassandra-0   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7   2Gi        RWO            stork-snapshot-sc   3m

cassandra-data-cassandra-1   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7   2Gi        RWO            stork-snapshot-sc   2m

cassandra-data-cassandra-2   Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7   2Gi        RWO            stork-snapshot-sc   1m

```

 Step 3: Take the group cloud snapshot​
Apply the following spec to take the cassandra group snapshot. Portworx quiesce I/O on all volumes before triggering their snapshots.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-group-cloudsnapshot

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

  options:

    portworx/snapshot-type: cloud

```

- Kubernetes

- OpenShift

After you apply the above object you can check the status of the snapshots using `kubectl`:

```

kubectl describe groupvolumesnapshot cassandra-group-cloudsnapshot

```

Once you apply the above object you can check the status of the snapshots using `oc`:

```

oc describe groupvolumesnapshot cassandra-group-cloudsnapshot

```

While the group snapshot is in progress, the status reflect as InProgress. After it is complete, the system displays a status stage as Final and status as Successful.

```

Name:         cassandra-group-cloudsnapshot

Namespace:    default

Labels:       <none>

Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"stork.libopenstorage.org/v1alpha1","kind":"GroupVolumeSnapshot","metadata":{"annotations":{},"name":"cassandra-group-cloudsnapshot","nam...

API Version:  stork.libopenstorage.org/v1alpha1

Kind:         GroupVolumeSnapshot

Metadata:

  Cluster Name:

  Creation Timestamp:  2019-01-14T20:30:13Z

  Generation:          0

  Resource Version:    18212101

  Self Link:           /apis/stork.libopenstorage.org/v1alpha1/namespaces/default/groupvolumesnapshots/cassandra-group-cloudsnapshot

  UID:                 xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Spec:

  Options:

    Portworx / Snapshot - Type:  cloud

  Post Snapshot Rule:

  Pre Snapshot Rule:

  Pvc Selector:

    Match Labels:

      App:  cassandra

Status:

  Stage:   Final

  Status:  Successful

  Volume Snapshots:

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/763613271174793816-922960401583326548

        Snapshot Type:     cloud

    Parent Volume ID:      763613271174793816

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-66490f4172c7

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/1081147806034223862-518034075073409747

        Snapshot Type:     cloud

    Parent Volume ID:      1081147806034223862

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-b62951dcca0e

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T20:30:49Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       xxxxxxxx-xxxx-xxxx-xxxx-4b6f09463a98/237262101530372284-299546281563771622

        Snapshot Type:     cloud

    Parent Volume ID:      237262101530372284

    Task ID:               xxxxxxxx-xxxx-xxxx-xxxx-ee3b13f7c03f

    Volume Snapshot Name:  cassandra-group-cloudsnapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Events:                    <none>

```

Above we can see that creation of cassandra-group-snapshot created 3 volumesnapshots:

- cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

- cassandra-group-cloudsnapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

- cassandra-group-cloudsnapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

These correspond to the PVCs cassandra-data-cassandra-0, cassandra-data-cassandra-1 and cassandra-data-cassandra-2 respectively.

You can also describe these individual volume snapshots using

- Kubernetes

- OpenShift

```

kubectl describe volumesnapshot cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

```

oc describe volumesnapshot cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

```

Name:         cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Namespace:    default

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshot

Metadata:

  Cluster Name:

  Creation Timestamp:  2019-01-14T20:30:49Z

  Owner References:

    API Version:     stork.libopenstorage.org/v1alpha1

    Kind:            GroupVolumeSnapshot

    Name:            cassandra-group-cloudsnapshot

    UID:             xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

  Resource Version:  18212097

  Self Link:         /apis/volumesnapshot.external-storage.k8s.io/v1/namespaces/default/volumesnapshots/cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

  UID:               xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Spec:

  Persistent Volume Claim Name:  cassandra-data-cassandra-0

  Snapshot Data Name:            cassandra-group-cloudsnapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Status:

  Conditions:

    Last Transition Time:  2019-01-14T20:30:49Z

    Message:               Snapshot created successfully and it is ready

    Reason:

    Status:                True

    Type:                  Ready

  Creation Timestamp:      <nil>

Events:                    <none>

```

### Restoring Cloud Snapshots in the same Cluster​

After you create a cloud snapshot, you can restore it to a new PVC or the original PVC.

#### Restore a cloud snapshot to a new PVC​

The steps to restore a cloud snapshot to a new PVC depend on how the snapshot was created:

- Legacy VolumeSnapshot: Cloud snapshot created with VolumeSnapshot API (`volumesnapshot.external-storage.k8s.io/v1`), for example using the `portworx/snapshot-type` annotation, see Legacy VolumeSnapshot to restore a cloud snapshot to a new PVC.

- CSI VolumeSnapshot: Cloud snapshot created as a CSI `VolumeSnapshot` (`snapshot.storage.k8s.io/v1`), for example through a VolumeSnapshotSchedule for a CSI-provisioned PVC, see CSI VolumeSnapshot.

 Legacy VolumeSnapshot​
When you install Stork, it also creates a storage class called stork-snapshot-sc. This storage class can be used to create PVCs from snapshots.

note

If you are using SUSE Harvester 1.6 or later, the `stork-snapshot-sc` StorageClass is not created by the Portworx Operator and you must create it manually. When creating the StorageClass, you must set the `cdi.harvesterhci.io/storageProfileVolumeModeAccessModes` annotation value to `{"<volume-mode>":["<access-mode>"]}`. For more information, see SUSE Harvester documentation.

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: stork-snapshot-sc

  annotations:

    cdi.harvesterhci.io/storageProfileVolumeModeAccessModes: '{"Block":["ReadWriteOnce"]}'

provisioner: stork-snapshot

reclaimPolicy: Delete

volumeBindingMode: Immediate

```

To create a PVC from a snapshot, add the `snapshot.alpha.kubernetes.io/snapshot` annotation to refer to the snapshot name. If the snapshot exists in another namespace, you should specify the snapshot namespace with the `stork.libopenstorage.org/snapshot-source-namespace` annotation in the PVC.

The Retain policy is important if you need to keep the volume in place, even after removing the Kubernetes objects from a cluster.

note

- As shown in the following example, the storageClassName should be the Stork StorageClass `stork-snapshot-sc`.

- When using this storage class the PVC is creating with `delete` as Retain policy. However, if the source PVC is having the policy as `retain`, then this will not be inherited to the restored PVC. After the restore, you should manually verify the retain policy and change it if needed.

-
Create a new PVC using the following spec:

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

   name: vdbench-restore

   namespace: vdbench-sv4-svc-autojournal

   annotations:

      snapshot.alpha.kubernetes.io/snapshot: vdbench-pvc-output-sv4-svc-schedule-interval-2024-01-10-225924

      stork.libopenstorage.org/snapshot-source-namespace: vdbench-sv4-svc-autojournal

spec:

  accessModes:

     - ReadWriteOnce

  storageClassName: stork-snapshot-sc

  resources:

    requests:

      storage: 10Gi

```

-
Once the above PVC specification is applied, verify that Stork has created a PVC that is backed by a clone of the specified Portworx volume snapshot(`vdbench-pvc-output-sv4-svc-schedule-interval-2024-01-10-225924`):

```

storkctl -n vdbench-sv4-svc-autojournal get volumesnapshot

```

```

NAME                                                             PVC                          STATUS   CREATED               COMPLETED             TYPE

vdbench-pvc-output-sv4-svc-schedule-interval-2024-01-10-225924   vdbench-pvc-output-sv4-svc   Ready    10 Jan 24 14:59 PST   10 Jan 24 14:59 PST   cloud

```

-
Verify that a cloud snapshot is restored to the PVC created above:

- Kubernetes

- OpenShift

```

kubectl get pvc -n vdbench-sv4-svc-autojournal

```

```

oc get pvc -n vdbench-sv4-svc-autojournal

```

```

NAME                         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS              AGE

vdbench-pvc-enc-sv4-svc      Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-a2959220f31b   50Gi       RWX            vdbench-sc-sv4-svc-auto   29m

vdbench-pvc-output-sv4-svc   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-ceda98f2ae06   5Gi        RWX            vdbench-sc-sv4-svc-auto   29m

vdbench-restore              Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-9916a6098418   10Gi       RWO            stork-snapshot-sc         4m46s

```

In the above example output, the `vdbench-restore` PVC is in a `Bound` status and is associated with the correct volume that represents the restored snapshot.

 CSI VolumeSnapshot​

-
List the CSI VolumeSnapshot objects in the namespace to find the name of the snapshot you want to restore:

- Kubernetes

- OpenShift

```

kubectl get volumesnapshot.snapshot.storage.k8s.io -n mysql

```

```

oc get volumesnapshot.snapshot.storage.k8s.io -n mysql

```

-
Create a PVC that references the snapshot as its `dataSource`:

note

Ensure that the target PVC uses the same storage class properties as the source PVC.

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: mysql-data-restore

  namespace: mysql

spec:

  storageClassName: px-sc-with-snap-schedules

  dataSource:

    name: <volumesnapshot-name>

    kind: VolumeSnapshot

    apiGroup: snapshot.storage.k8s.io

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 10Gi

```

note

- The referenced `VolumeSnapshot` must be `readyToUse: true` before the PVC binds.

- Restoring a cloud snapshot is an asynchronous operation. The PVC stays in a `Pending` state while the CSI provisioner polls until Portworx finishes downloading the data from the backup location.

- Restoring a snapshot always creates a new Portworx volume; the source volume is not affected.

For credential setup and other CSI VolumeSnapshot operations, see Manage cloud snapshots.

#### Restore a cloud snapshot to the original PVC​

When you perform an in-place restore to a PVC, Stork takes the pods using that PVC offline, restores the volume from the snapshot, then brings the pods back online.

important

-
In-place restore is not supported for FADA snapshots. Restore these snapshots by using the CSI restore method. For more information, see Manage cloud snapshots.

-
In-place restore using `VolumeSnapshotRestore` works only for applications deployed using the `stork` scheduler. If you're not using the Stork scheduler, Portworx displays the following error when describing the VolumeSnapshotRestore resource:

```

Events:

  Type     Reason  Age               From   Message

  ----     ------  ----              ----   -------

  Warning  Failed  5s (x2 over 15s)  stork  application not scheduled by stork scheduler

```

-
Create a `VolumeSnapshotRestore` YAML file specifying the following:

- apiVersion as `stork.libopenstorage.org/v1alpha1`

- kind as `VolumeSnapshotRestore`

- metadata.name with the name of the object that performs the restore

- metadata.namespace with the name of the target namespace

- spec.sourceName with the name of the snapshot you want to restore

- spec.sourceNamespace with the namespace in which the snapshot resides

The following example restores data from a snapshot called `mysql-snapshot` which was created in the `mysql-snap-restore-splocal` namespace to a PVC called `mysql-snap-inrestore` in the `default` namespace:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: VolumeSnapshotRestore

metadata:

  name: mysql-snap-inrestore

  namespace: default

spec:

  sourceName: mysql-snapshot

  sourceNamespace: mysql-snap-restore-splocal

```

-
Place the spec into a file called `mysql-cloud-snapshot-restore.yaml` and apply it:

- Kubernetes

- OpenShift

```

kubectl apply -f mysql-cloud-snapshot-restore.yaml

```

```

oc apply -f mysql-cloud-snapshot-restore.yaml

```

-
You can enter the following command to see the status of the restore process:

```

storkctl get volumesnapshotrestore

```

```

NAME                   SOURCE-SNAPSHOT   SOURCE-SNAPSHOT-NAMESPACE   STATUS          VOLUMES   CREATED

mysql-snap-inrestore   mysql-snapshot    default                     Successful      1         23 Sep 19 21:55 EDT

```

- Kubernetes

- OpenShift

You can also use the `kubectl describe` command to retrieve more detailed information about the status of the restore process.

Example:

```

kubectl describe volumesnapshotrestore mysql-snap-inrestore

```

You can also use the `oc describe` command to retrieve more detailed information about the status of the restore process.

Example:

```

oc describe volumesnapshotrestore mysql-snap-inrestore

```

```

Name:         mysql-snap-inrestore

Namespace:    default

Labels:       <none>

Annotations:  kubectl.kubernetes.io/last-applied-configuration:

                {"apiVersion":"stork.libopenstorage.org/v1alpha1","kind":"VolumeSnapshotRestore","metadata":{"annotations":{},"name":"mysql-snap-inrestore...

API Version:  stork.libopenstorage.org/v1alpha1

Kind:         VolumeSnapshotRestore

Metadata:

  Creation Timestamp:  2019-09-23T17:24:30Z

  Generation:          5

  Resource Version:    904014

  Self Link:           /apis/stork.libopenstorage.org/v1alpha1/namespaces/default/volumesnapshotrestores/mysql-snap-inrestore

  UID:                 xxxxxxxx-xxxx-xxxx-xxxx-000c295d6364

Spec:

  Group Snapshot:    false

  Source Name:       mysql-snapshot

  Source Namespace:  default

Status:

  Status:  Successful

  Volumes:

    Namespace:  default

    Pvc:        mysql-data

    Reason:     Restore is successful

    Snapshot:   k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-320ff611f4ca

    Status:     Successful

    Volume:     pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c295d6364

Events:

  Type    Reason      Age   From   Message

  ----    ------      ----  ----   -------

  Normal  Successful  0s    stork  Snapshot in-Place  Restore completed

```

## Create and Restore a Cloud Snapshot in a Different Cluster​

This section describes how to create a snapshot and restore it to a different Portworx cluster using the `pxctl` command-line utility.

note

You cannot use an older version of Portworx to restore a cloud snapshot created with a newer one. For example, if you are running Portworx 3.3, you cannot restore a cloud snapshot created with Portworx 3.4.

### Create your cloud snapshot credentials on the source cluster​

The options you use to create your cloud snapshot credentials differ based on which secret store provider you use. The steps in this document describe AWS KMS, but you can find instructions for creating other credentials in the CLI reference.

note

- If you use the workload identity feature, you can create credentials that use the workload identity feature. For more information, see Create Credentials using Workload Identity.

- If you use custom CA certificates with S3-compatible storage, secure them using the procedure described in Certificates as Kubernetes Secrets before creating cloud snapshots in your environment.

-
Enter the `pxctl credentials create` command, specifying the following:

- The `--provider` flag with the name of the cloud provider (`s3`).

- The `--s3-access-key` flag with your secret access key

- The `--s3-secret-key` flag with your access key ID

- The `--s3-region` flag with the name of the S3 region (`us-east-1`)

- The `--s3-endpoint` flag with the name of the endpoint (`s3.amazonaws.com`)

- The optional `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer

- The name of your cloud credentials

Example:

```

pxctl credentials create --provider s3 --s3-access-key <YOUR_ACCESS_KEY> --s3-secret-key <YOUR_SECRET_KEY> --s3-region us-east-1 --s3-endpoint <YOUR_ENDPOINT> --s3-storage-class <YOUR_STORAGE_CLASS> <YOUR_SOURCE_S3_CRED>

```

```

Credentials created successfully, UUIDU0d9847d6-786f-4ed8- b263-5cde5a5a12f5

```

-
You can validate your cloud snapshot credentials by entering the `pxctl credentials validate` command followed by the name of your cloud credentials:

```

pxctl cred validate <YOUR_SOURCE_S3_CRED>

```

```

Credential validated successfully

```

### Back up a volume​

-
Enter the following `pxctl volume list` command to list all volumes on the source cluster:

```

pxctl volume list

```

```

ID			NAME	SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	STATUS				SNAP-ENABLED

869510655149846346	testvol	1 GiB	1	no	no		HIGH		up - attached on X.X.X.123	no

186765995885697345	vol2	1 GiB	1	no	no		HIGH		up - attached on X.X.X.123	no

```

-
To back up a volume, enter the following `pxctl cloudsnap backup` command, specifying the name of your volume. The following example backs up a volume called `testvol`:

```

pxctl cloudsnap backup testvol

```

```

Cloudsnap backup started successfully with id: xxxxxxxx-xxxx-xxxx-xxxx-a46868cc6b5c

```

-
Enter the `pxctl cloudsnap status` command to display the status of your backup or restore operations:

```

pxctl cloudsnap status

```

```

NAME					SOURCEVOLUME		STATE		NODE		TIME-ELAPSED	COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-9bff6ea440eb	869510655149846346	Backup-Failed	X.X.X.153	80.915632ms	Wed, 22 Jan 2020 23:51:17 UTC

xxxxxxxx-xxxx-xxxx-xxxx-10458b7a8445	869510655149846346	Backup-Done	X.X.X.153	55.098204ms	Wed, 22 Jan 2020 23:52:15 UTC

xxxxxxxx-xxxx-xxxx-xxxx-f15839b26e76	186765995885697345	Backup-Failed	X.X.X.153	39.703754ms	Wed, 29 Jan 2020 18:17:30 UTC

xxxxxxxx-xxxx-xxxx-xxxx-2f4a504c01f9	186765995885697345	Backup-Done	X.X.X.153	60.439873ms	Wed, 29 Jan 2020 18:34:17 UTC

xxxxxxxx-xxxx-xxxx-xxxx-a46868cc6b5c	869510655149846346	Backup-Done	X.X.X.153	45.874676ms	Wed, 29 Jan 2020 22:32:30 UTC

```

-
To see more details about your backup operation, enter the `pxctl cloudsnap status` command specifying the following:

-
The `--json` flag

-
The `--name` flag with the task name of your backup.

Example:

```

pxctl --json cloudnsap status --name xxxxxxxx-xxxx-xxxx-xxxx-a46868cc6b5c

```

```

xxxxxxxx-xxxx-xxxx-xxxx-a46868cc6b5c

{

"xxxxxxxx-xxxx-xxxx-xxxx-a46868cc6b5c": {

"ID": "xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-1140911084048715440",

"OpType": "Backup",

"Status": "Done",

"BytesDone": 368640,

"BytesTotal": 0,

"EtaSeconds": 0,

"StartTime": "2020-01-29T22:32:30.258745865Z",

"CompletedTime": "2020-01-29T22:32:30.304620541Z",

"NodeID": "xxxxxxxx-xxxx-xxxx-xxxx-3c38a8c04736",

"SrcVolumeID": "869510655149846346",

"Info": [

""

],

"CredentialUUID": "xxxxxxxx-xxxx-xxxx-xxxx-5cde5a5a12f5",

"GroupCloudBackupID": ""

}

```

-
Run the `pxctl cloudsnap list` command, and look through the output to find the identifier of the cloud snapshot associated with your volume. You will use this to restore your cloud snapshot.

```

pxctl cloudsnap list

```

```

SOURCEVOLUME		SOURCEVOLUMEID			CLOUD-SNAP-ID										CREATED-TIME				TYPE		STATUS

testvol			869510655149846346		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-457116323485794032		Wed, 22 Jan 2020 23:52:15 UTC		Manual		Done

vol2			186765995885697345		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/186765995885697345-237744851553132030		Wed, 29 Jan 2020 18:34:17 UTC		Manual		Done

testvol			869510655149846346		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-1140911084048715440		Wed, 29 Jan 2020 22:32:30 UTC		Manual		Done

```

The `CLOUD-SNAP-ID` column is in the form of `<YOUR_SOURCE_CLUSTER_ID>/<YOUR_CLOUD_SNAP_ID>`. In this example, the identifier of the source cluster is `xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358`, and the identifier of the cloud snapshot is `869510655149846346-457116323485794032`.

### Create your cloud snapshot credentials on the destination cluster​

note

If you use the workload identity feature, you can create credentials that use the workload identity feature. For more information, see Create Credentials using Workload Identity.

-
Enter the `pxctl credentials create` command, specifying the following:

- The `--provider` flag with the name of the cloud provider (`s3`).

- The `--s3-access-key` flag with your secret access key

- The `--s3-secret-key` flag with your access key ID

- The `--s3-region` flag with the name of the S3 region (`us-east-1`)

- The `--s3-endpoint` flag with the name of the endpoint (`s3.amazonaws.com`)

- The optional `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer

- The name of your cloud credentials

Example:

```

pxctl credentials create --provider s3 --s3-access-key <YOUR_ACCESS_KEY> --s3-secret-key <YOUR_SECRET_KEY> --s3-region us-east-1 --s3-endpoint <YOUR_ENDPOINT> --s3-storage-class <YOUR_STORAGE_CLASS> <YOUR_DEST_S3_CRED>

```

```

Credentials created successfully, UUID:bb281a27-c2bb-4b3d-b5b9- efa0316a9561

```

### Restore cloud snapshot on the destination cluster​

-
On the destination cluster, verify that your cloud snapshot is visible. Enter the `pxctl cloudsnap list` command, specifying the `--cluster` flag with the identifier of the source cluster.

Example:

```

pxctl cloudsnap list --cluster 3f2fa12e-186f-466d- ac35-92cf569c9358

```

```

xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358

SOURCEVOLUME		SOURCEVOLUMEID			CLOUD-SNAP-ID										CREATED-TIME				TYPE		STATUS

testvol			869510655149846346		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-457116323485794032		Wed, 22 Jan 2020 23:52:15 UTC		Manual		Done

vol2			186765995885697345		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/186765995885697345-237744851553132030		Wed, 29 Jan 2020 18:34:17 UTC		Manual		Done

testvol			869510655149846346		xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-1140911084048715440		Wed, 29 Jan 2020 22:32:30 UTC		Manual		Done

```

-
To restore your volume, run the `pxctl cloudsnap restore` command specifying the `--snap` flag with the cloud snapshot identifier associated with your backup. Example:

```

pxctl cloudsnap restore --snap xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-1140911084048715440

```

```

Cloudsnap restore started successfully on volume: 1127186980413628688 with task name:xxxxxxxx-xxxx-xxxx-xxxx-a6b731f73983

```

-
To see the status of your restore operation, enter the following command:

```

pxctl cloudsnap status

```

```

NAME				                  	SOURCEVOLUME									STATE		NODE		TIME-ELAPSED	COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-dd77c14c00bc	79001397979145130								Backup-Done	X.X.X.94	44.634974ms	Wed, 29 Jan 2020 20:13:58 UTC

xxxxxxxx-xxxx-xxxx-xxxx-2aba15c5b300	xxxxxxxx-xxxx-xxxx-xxxx-92cf569c9358/869510655149846346-1140911084048715440	Restore-Done	X.X.X.94	53.527074ms	Wed, 29 Jan 2020 22:52:47 UTC

```

-
Run the `pxctl volume list` command to list all volumes on the destination cluster:

```

pxctl volume list

```

```

ID			NAME					SIZE	HA	SHARED	ENCRYPTED	IO_PRIORITY	STATUS		SNAP-ENABLED

1021141073379827532	Restore-869510655149846346-556794585	1 GiB	1	no	no		HIGH		up - detached	no

79001397979145130	samvol					1 GiB	1	no	no		HIGH		up - detached	no

```

### Naming scheme for cloud backups​

Cloud backups adhere to the following naming scheme: `<bucket-id>/<vol-id>-<snap-id>`.

Example:

- `xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463`

For incremental backups, Portworx adds the `-incr` suffix as follows: `<bucket-id>/<vol-id>-<snap-id>-incr`.

Example:

- `xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-951325819047337066-incr`

## Delete a Cloud Snapshot​

To delete a cloud snapshot, you must delete the `VolumeSnapshot` object used to create the snapshot.

important

To avoid I/O pauses during deletion and to reclaim storage space on thin-provisioned backends, such as a storage area network (SAN) or a FlashArray, enable non-blocking device delete (NBDD), which performs discards in the background before deleting volumes or snapshots. For more information, see Non-Blocking Device Delete.

- Kubernetes

- OpenShift

```

kubectl delete volumesnapshot cassandra-cloudsnapshot

```

```

oc delete volumesnapshot cassandra-cloudsnapshot

```

To delete group snapshots, you must delete the `GroupVolumeSnapshot` used to create group snapshots. Stork deletes all other volumesnapshots that were created for this group snapshot.

- Kubernetes

- OpenShift

```

kubectl delete groupvolumesnapshot cassandra-group-cloudsnapshot

```

```

oc delete groupvolumesnapshot cassandra-group-cloudsnapshot

```

In this topic:
