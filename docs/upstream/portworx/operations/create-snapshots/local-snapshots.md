# Local Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/local-snapshots (Portworx Enterprise 3.6)

Local Snapshots | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

A local snapshot is a user-triggered, point-in-time copy of a volume or group of volumes, stored within the same Kubernetes cluster. Portworx stores the local snapshot on the same physical node or storage backend as the source data. You can use local snapshots to capture the current state of your data without moving it outside the cluster. They are fast to create, lightweight, and ideal for short-term protection and quick recovery from accidental changes or data corruption.

important

For FlashArray Direct Access (FADA) and FlashBlade Direct Access (FBDA) volumes, create and restore local snapshots by using the CSI-based snapshot and restore method.

## Creating a Local Snapshot​

Create local snapshots of Portworx volumes and clone the snapshots to use in pods. With local snapshots, you can either snapshot individual PVCs one by one or snapshot a group of PVCs by using a label selector.

note

Use Stork to manage snapshots on Kubernetes. To create Portworx snapshots using PVC annotations, follow the instructions at Create a PVC from a snapshot.

### Prerequisites​

Ensure that you have Stork installed and running on your cluster.

note

If you fetched the Portworx specs from the Portworx spec generator in Portworx Central and used the default options, Stork is already installed.

### Local Snapshot of a Single PVC​

#### Creating snapshot within a single namespace​

-
If you have a PVC called jenkins-home-jenkins-master-0, in the jenkins namespace, you can create a snapshot for that PVC by using the following spec:

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: jenkins-home-jenkins-master-0

  namespace: jenkins

  annotations:

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  persistentVolumeClaimName: jenkins-home-jenkins-master-0

```

- Kubernetes

- OpenShift

-
Once you apply the above object, you can check the status of the snapshots using `kubectl`:

```

kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io -n jenkins

```

```

NAME                                                      AGE

jenkins-jobs-jenkins-master-0-snapshot-2019-03-20-snap1   6m

```

```

kubectl get volumesnapshotdatas.volumesnapshot.external-storage.k8s.io -n jenkins

```

```

NAME                                                       AGE

k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002   8m

```

-
Once you apply the above object, you can check the status of the snapshots using `oc`:

```

oc get -n jenkins volumesnapshot

```

```

NAME                                                      AGE

jenkins-jobs-jenkins-master-0-snapshot-2019-03-20-snap1   6m

```

```

oc get -n jenkins volumesnapshotdatas

```

```

NAME                                                       AGE

k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002   8m

```

-
The creation of the volumesnapshotdatas object indicates that the snapshot has been created.

- Kubernetes

- OpenShift

Portworx Volume Snapshot ID and the PVC for which the snapshot was created:

```

kubectl describe volumesnapshotdatas

```

```

Name:         k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

Namespace:

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshotData

Metadata:

    Creation Timestamp:  2019-03-20T22:22:37Z

    Generation:          1

    Resource Version:    56596513

    Self Link:           /apis/volumesnapshot.external-storage.k8s.io/v1/volumesnapshotdatas/k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

    UID:                 xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

Spec:

    Persistent Volume Ref:

    Kind:  PersistentVolume

    Name:  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

    Portworx Volume:

    Snapshot Id:    411710013297550893

    Snapshot Type:  local

    Volume Snapshot Ref:

    Kind:  VolumeSnapshot

    Name:  jenkins/jenkins-jobs-jenkins-master-0-snapshot-2019-03-20-snap1-xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

Status:

    Conditions:

    Last Transition Time:  2019-03-20T22:22:37Z

    Message:               Snapshot created successfully and it is ready

    Reason:

    Status:                True

    Type:                  Ready

    Creation Timestamp:      <nil>

Events:                    <none>

```

Portworx Volume Snapshot ID and the PVC for which the snapshot was created:

```

oc describe volumesnapshotdatas

```

```

Name:         k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

Namespace:

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshotData

Metadata:

    Creation Timestamp:  2019-03-20T22:22:37Z

    Generation:          1

    Resource Version:    56596513

    Self Link:           /apis/volumesnapshot.external-storage.k8s.io/v1/volumesnapshotdatas/k8s-volume-snapshot-xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

    UID:                 xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

Spec:

    Persistent Volume Ref:

    Kind:  PersistentVolume

    Name:  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

    Portworx Volume:

    Snapshot Id:    411710013297550893

    Snapshot Type:  local

    Volume Snapshot Ref:

    Kind:  VolumeSnapshot

    Name:  jenkins/jenkins-jobs-jenkins-master-0-snapshot-2019-03-20-snap1-xxxxxxxx-xxxx-xxxx-xxxx-0cc47ab5f9a2

Status:

    Conditions:

    Last Transition Time:  2019-03-20T22:22:37Z

    Message:               Snapshot created successfully and it is ready

    Reason:

    Status:                True

    Type:                  Ready

    Creation Timestamp:      <nil>

Events:                    <none>

```

-
You can use the `storkctl` command to verify that the snapshot was created successfully:

```

storkctl -n jenkins get snap

```

```

NAME                                                      PVC                             STATUS    CREATED               COMPLETED             TYPE

jenkins-jobs-jenkins-master-0-snapshot-2019-03-20-snap1   jenkins-jobs-jenkins-master-0   Ready     20 Mar 19 15:22 PDT   20 Mar 19 15:22 PDT   local

```

For details about how you can restore a snapshot to a new PVC or the original PVC, see the Restore snapshots section.

#### Creating snapshots across namespaces​

When creating snapshots, you can provide comma separated regexes with `stork.libopenstorage.org/snapshot-restore-namespaces` annotation to specify which namespaces the snapshot can be restored to. When creating PVC from snapshots, if a snapshot exists in another namespace, the snapshot namespace should be specified with `stork.libopenstorage.org/snapshot-source-namespace` annotation.

Let us take an example where we have two namespaces dev and prod. We create a PVC and snapshot in the dev namespace and then create a PVC in the prod namespace from the snapshot.

-
Create the namespaces

```

apiVersion: v1

kind: Namespace

metadata:

  name: dev

  labels:

    name: dev

---

apiVersion: v1

kind: Namespace

metadata:

  name: prod

  labels:

    name: prod

```

-
Create the PVC

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

  namespace: dev

  annotations:

    volume.beta.kubernetes.io/storage-class: px-mysql-sc

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

---

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-mysql-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

```

-
Create the snapshot

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mysql-snapshot

  namespace: dev

  annotations:

    stork.libopenstorage.org/snapshot-restore-namespaces: "prod"

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  persistentVolumeClaimName: mysql-data

```

-
Create a PVC in a different namespace from the snapshot

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: mysql-clone

  namespace: prod

  annotations:

    snapshot.alpha.kubernetes.io/snapshot: mysql-snapshot

    stork.libopenstorage.org/snapshot-source-namespace: dev

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  accessModes:

    - ReadWriteOnce

  storageClassName: stork-snapshot-sc

  resources:

    requests:

      storage: 2Gi

```

### Local Snapshot of a Group of PVCs​

#### Creating group snapshots​

To take group snapshots, you need to use the GroupVolumeSnapshot CRD object.
For example:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-groupsnapshot

  annotations:

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

```

The above spec takes a group snapshot of all PVCs that match labels `app=cassandra`.

The Examples section has a more detailed end-to-end example.

note

Above spec keeps all the snapshots local to the Portworx cluster. If you intend on backing up the group snapshots to cloud (S3 endpoint), refer to Create group cloud snapshots.

The `GroupVolumeSnapshot` object also supports specifying pre and post rules that are run on the application pods using the volumes being snapshotted. This allows users to quiesce the applications before the snapshot is taken and resume I/O after the snapshot is taken. For more information, see 3D Snapshots.

#### Checking status of group snapshots​

A new VolumeSnapshot object gets created for each PVC that matches the given `pvcSelector`.
For example, if the label selector `app: cassandra` matches three PVCs, you have three VolumeSnapshot objects.

You can track the status of the group volume snapshots using:

- Kubernetes

- OpenShift

```

kubectl describe groupvolumesnapshot <group-snapshot-name>

```

```

oc describe groupvolumesnapshot <group-snapshot-name>

```

This shows the latest status and also lists the VolumeSnapshot objects after it is complete.
Below is an example of the status section of the cassandra group snapshot.

```

Status:

  Stage:   Final

  Status:  Successful

  Volume Snapshots:

    Conditions:

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       1015874155818710382

    Parent Volume ID:      763613271174793816

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       1130064992705573378

    Parent Volume ID:      1081147806034223862

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       175241555565145805

    Parent Volume ID:      237262101530372284

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

You can see three VolumeSnapshots which are part of the group snapshot. The name of the VolumeSnapshot is in the Volume Snapshot Name field. For more details on the VolumeSnapshot:

- Kubernetes

- OpenShift

```

kubectl get volumesnapshot.volumesnapshot.external-storage.k8s.io/<volume-snapshot-name> -o yaml

```

```

oc get volumesnapshot.volumesnapshot.external-storage.k8s.io/<volume-snapshot-name> -o yaml

```

#### Snapshots across namespaces​

When creating a group snapshot, you can specify a list of namespaces to which the group snapshot can be restored. Below is an example of a group snapshot which can be restored into prod-01 and prod-02 namespaces.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-groupsnapshot

  annotations:

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

  restoreNamespaces:

   - prod-01

   - prod-02

```

#### Examples​
 Group snapshot for all cassandra PVCs​
In this example, we take a group snapshot for all PVCs in the default namespace and that have labels app: cassandra.
 Step 1: Deploy cassandra statefulset and PVCs​
The following spec creates a replica 3 cassandra statefulset. Each replica pod uses its own PVC.

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

After you see all three pods, you can also list the cassandra PVCs.

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

 Step 3: Take the group snapshot​
Apply the following spec to take the cassandra group snapshot. Portworx quiesce I/O on all volumes before triggering their snapshots.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-group-snapshot

  annotations:

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  pvcSelector:

    matchLabels:

      app: cassandra

```

- Kubernetes

- OpenShift

After you apply the above object you can check the status of the snapshots using `kubectl`:

```

kubectl describe groupvolumesnapshot cassandra-group-snapshot

```

After you apply the above object you can check the status of the snapshots using `oc`:

```

oc describe groupvolumesnapshot cassandra-group-snapshot

```

While the group snapshot is in progress, the status reflects InProgress. After the process is complete, the system displays the stage as Final and status as Successful.

```

Name:         cassandra-group-snapshot

Namespace:    default

Labels:       <none>

Annotations:  kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"stork.libopenstorage.org/v1alpha1","kind":"GroupVolumeSnapshot","metadata":{"annotations":{},"name":"cassandra-group-snapshot"

,"namespac...

API Version:  stork.libopenstorage.org/v1alpha1

Kind:         GroupVolumeSnapshot

Metadata:

  Cluster Name:

  Creation Timestamp:  2019-01-14T18:02:16Z

  Generation:          0

  Resource Version:    18184467

  Self Link:           /apis/stork.libopenstorage.org/v1alpha1/namespaces/default/groupvolumesnapshots/cassandra-group-snapshot

  UID:                 xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Spec:

  Options:             <nil>

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

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       1015874155818710382

    Parent Volume ID:      763613271174793816

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       1130064992705573378

    Parent Volume ID:      1081147806034223862

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

    Conditions:

      Last Transition Time:  2019-01-14T18:02:47Z

      Message:               Snapshot created successfully and it is ready

      Reason:

      Status:                True

      Type:                  Ready

    Data Source:

      Portworx Volume:

        Snapshot Id:       175241555565145805

    Parent Volume ID:      237262101530372284

    Task ID:

    Volume Snapshot Name:  cassandra-group-snapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7                  16s

```

Above we can see that creation of cassandra-group-snapshot created 3 volumesnapshots:

- cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

- cassandra-group-snapshot-cassandra-data-cassandra-1-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

- cassandra-group-snapshot-cassandra-data-cassandra-2-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

These correspond to the PVCs cassandra-data-cassandra-0, cassandra-data-cassandra-1 and cassandra-data-cassandra-2 respectively. You can also describe these individual volume snapshots using:

- Kubernetes

- OpenShift

```

kubectl describe volumesnapshot cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

```

oc describe volumesnapshot cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

```

```

Name:         cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Namespace:    default

Labels:       <none>

Annotations:  <none>

API Version:  volumesnapshot.external-storage.k8s.io/v1

Kind:         VolumeSnapshot

Metadata:

  Cluster Name:

  Creation Timestamp:  2019-01-14T18:02:47Z

  Owner References:

    API Version:     stork.libopenstorage.org/v1alpha1

    Kind:            GroupVolumeSnapshot

    Name:            cassandra-group-snapshot

    UID:             xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

  Resource Version:  18184459

  Self Link:         /apis/volumesnapshot.external-storage.k8s.io/v1/namespaces/default/volumesnapshots/cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

  UID:               xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Spec:

  Persistent Volume Claim Name:  cassandra-data-cassandra-0

  Snapshot Data Name:            cassandra-group-snapshot-cassandra-data-cassandra-0-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7

Status:

  Conditions:

    Last Transition Time:  2019-01-14T18:02:47Z

    Message:               Snapshot created successfully and it is ready

    Reason:

    Status:                True

    Type:                  Ready

  Creation Timestamp:      <nil>

Events:                    <none>

```

## Restoring a Local Snapshot​

After you create a snapshot, you can restore it to a new PVC or the original PVC.

note

When you restore a snapshot to a new PVC, Portworx skips `StorageClass` validation by default and raises a warning if it detects an infrastructure mismatch between the snapshot and the destination `StorageClass`. To change this behavior, see Configure `StorageClass` validation for clones.

### Restore a local snapshot or group snapshots to a new PVC​

The steps to restore a local snapshot to a new PVC depend on how the snapshot was created:

- Legacy VolumeSnapshot: Local snapshot created with VolumeSnapshot API (`volumesnapshot.external-storage.k8s.io/v1`), for example using the `portworx/snapshot-type` annotation, see Legacy VolumeSnapshot to restore a local snapshot to a new PVC.

- CSI VolumeSnapshot: Local snapshot created as a CSI `VolumeSnapshot` (`snapshot.storage.k8s.io/v1`), for example through a VolumeSnapshotSchedule for a CSI-provisioned PVC, see CSI VolumeSnapshot.

#### Legacy VolumeSnapshot​

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

- When using this storage class, the PVC is created with `delete` as the reclaim policy. However, if the source PVC has the policy as `retain`, then this is not inherited to the restored PVC. After the restore, you should manually verify the reclaim policy and change it if needed.

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: mysql-snap-clone

  annotations:

    snapshot.alpha.kubernetes.io/snapshot: mysql-snapshot

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  accessModes:

     - ReadWriteOnce

  storageClassName: stork-snapshot-sc

  resources:

    requests:

      storage: 2Gi

```

After you apply the above spec, Stork creates a PVC. This PVC is backed by a Portworx volume clone of the snapshot created above.

- Kubernetes

- OpenShift

```

kubectl get pvc

```

```

oc get pvc

```

```

NAMESPACE   NAME                                   STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                AGE

default     mysql-data                             Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447   2Gi        RWO            px-mysql-sc                 2d

default     mysql-snap-clone                       Bound     pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447   2Gi        RWO            stork-snapshot-sc           2s

```

#### CSI VolumeSnapshot​

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

- Restoring a snapshot always creates a new Portworx volume; the source volume is not affected.

### Restore a local snapshot to the original PVC​

When you perform an in-place restore to a PVC, Stork takes the pods using that PVC offline, restores the volume from the snapshot, then brings the pods back online.

important

In-place restore is not supported for CSI FADA snapshots. Restore CSI FADA snapshots by using the CSI restore method. For more information, see Manage local snapshots.

note

In-place restore using VolumeSnapshotRestore works only for applications deployed using the `stork` scheduler. If you're not using the Stork scheduler, Portworx displays the following error when describing the VolumeSnapshotRestore resource:

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

- The following annotations are required when PX-Security is enabled:

- openstorage.io/auth-secret-namespace: namespace where the Kubernetes secret holding the auth token resides

- openstorage.io/auth-secret-name: name of the Kubernetes secret which holds the auth token

The following example restores data from a snapshot called `mysql-snapshot` which was created in the `mysql-snap-restore-splocal` namespace to a PVC called `mysql-snap-inrestore` in the `default` namespace:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: VolumeSnapshotRestore

metadata:

  name: mysql-snap-inrestore

  namespace: default

  annotations:

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  sourceName: mysql-snapshot

  sourceNamespace: mysql-snap-restore-splocal

```

- Kubernetes

- OpenShift

-
Place the spec into a file called `mysql-cloud-snapshot-restore.yaml` and apply it:

```

kubectl apply -f mysql-cloud-snapshot-restore.yaml

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

You can also use the `kubectl describe` command to retrieve more detailed information about the status of the restore process.

Example:

```

kubectl describe volumesnapshotrestore mysql-snap-inrestore

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

-
Place the spec into a file called `mysql-cloud-snapshot-restore.yaml` and apply it:

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

## Delete a Snapshot​

To delete a local snapshot, you must delete the `VolumeSnapshot` object used to create the snapshot.

important

To avoid I/O pauses during deletion and to reclaim storage space on thin-provisioned backends, such as a storage area network (SAN) or a FlashArray, enable non-blocking device delete (NBDD), which performs discards in the background before deleting volumes or snapshots. For more information, see Non-Blocking Device Delete.

- Kubernetes

- OpenShift

```

kubectl delete volumesnapshot cassandra-snapshot

```

```

oc delete volumesnapshot cassandra-snapshot

```

To delete group snapshots, you must delete the `GroupVolumeSnapshot` used to create group snapshots. Stork deletes all other volumesnapshots that were created for this group snapshot.

- Kubernetes

- OpenShift

```

kubectl delete groupvolumesnapshot cassandra-group-snapshot

```

```

oc delete groupvolumesnapshot cassandra-group-snapshot

```

In this topic:
