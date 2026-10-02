# 3D Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/snaps-3d (Portworx Enterprise latest)

3D Snapshots | Portworx Enterprise Documentation

A 3D Snapshot (3DSnap) is an application-consistent snapshot that captures the complete state of a running application and its underlying persistent storage. Unlike standard volume snapshots that only capture storage-layer data, 3DSnaps coordinate with the application to ensure data consistency, including for in-memory and database-driven workloads. For a 3DSnap, Portworx lets you specify pre- and post-rules that run on the application pods using the volumes. These rules allow you to quiesce the application before taking the snapshot and resume I/O afterward. Portworx runs the commands in the pods that use the PVC being snapshotted.

## Configuring 3D Snapshots​

For each of the snapshot types, Portworx supports specifying pre and post rules that are run on the application pods using the volumes being snapshotted. This allows users to quiesce the applications before the snapshot is taken and resume I/O after the snapshot is taken.

The high level workflow for configuring 3DSnaps involves creating rules and later on referencing the rules when creating the snapshots.

### Step 1: Create Rules​

A Stork `Rule` is a Custom Resource Definition (CRD) that allows to define actions that get performed on pods matching selectors. Below are the supported fields:

- podSelector: The actions will get executed on pods that only match the label selectors given here.

- actions: This contains a list of actions to be performed. Below are supported fields under actions:

- type: The type of action to run. Only type command is supported.

- background: If true, the action will run in background and will be terminated by Stork after the snapshot has been initiated. If false, the action will first complete and then the snapshot will get initiated.

- If background is set to true, add `${WAIT_CMD}` as shown in the examples below. This is a placeholder and Stork will replace it with an appropriate command to wait for the command is done.

- value: This is the actual action content. For example, the command to run.

- runInSinglePod: If true, the action will be run on a single pod that matches the selectors.

- container: specifies the container in which Stork will execute the action.

### Step 2: Create snapshots that reference the rules​

Once you have the rules applied in your cluster, you can reference them in the `VolumeSnapshot` or `GroupVolumeSnapshot` for individual and group snapshots respectively.

#### VolumeSnapshots​

Use following annotations on the VolumeSnapshot to specify pre and post rules.

- stork.rule/pre-snapshot: Stork will execute the rule which is given in the value of this annotation before taking the snapshot.

- stork.rule/post-snapshot: Stork will execute the rule which is given in the value of this annotation after taking the snapshot.

#### GroupVolumeSnapshots​

Use following fields in the GroupVolumeSnapshot spec to specify pre and post rules.

- preExecRule: Stork will execute the rule which is given in the value of this annotation before taking the group snapshot.

- postExecRule: Stork will execute the rule which is given in the value of this annotation after taking the snapshot.

### Examples​

This section covers examples of creating 3DSnapshots for various applications.

#### Specify the container in which Stork will execute the action​

The following example rule configures Stork to execute the action in a container named `<my_container>`:

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: mysql-pre-backup-rule

  namespace: mysql-1-pvc-mysql

  annotations:

    "stork/cmdexecutor-image": "openstorage/cmdexecutor:latest"

rules:

  - podSelector:

      app: mysql

    container: <my_container>

```

#### Hello world​

Below rule is a generic example on how to run an echo command on a single pod that matches the label selector app=foo.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: px-hello-world-rule

rules:

  - podSelector:

      app: foo

    actions:

    - type: command

      value: echo "hello world"

      runInSinglePod: true

```

#### Mysql​

Pre-snapshot rule

Below rule will flush tables on all mysql pods that match label app=mysql and take a read lock on the tables.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: px-presnap-rule

rules:

  - podSelector:

      app: mysql

    actions:

    - type: command

      background: true

      # this command will flush tables with read lock

      value: mysql --user=root --password=$MYSQL_ROOT_PASSWORD -Bse 'flush tables with read lock;system ${WAIT_CMD};'

```

Snapshot

Creating the below VolumeSnapshot will do the following:

-
Stork will run the px-presnap-rule rule on the pod that's using the mysql-data PVC.

-
Once the rule is executed, Stork will take a snapshot of the mysql-data PVC.

-
After the snapshot has been triggered, Stork will terminate any background actions that may exist in the rule px-presnap-rule.

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mysql-3d-snapshot

  annotations:

    stork.rule/pre-snapshot: px-presnap-rule

spec:

  persistentVolumeClaimName: mysql-data

```

#### MongoDB​

Pre-snapshot rule

Below pre-snapshot rule forces the mongod to flush all pending write operations to disk and locks the entire mongod instance to prevent additional writes until the user releases the lock with a corresponding db.fsyncUnlock() command. (See reference)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: px-mongodb-presnap-rule

rules:

  - podSelector:

      app: px-mongo-mongodb

    actions:

    - type: command

      value: mongo --eval "printjson(db.fsyncLock())"

```

Post-snapshot rule

Below post-snapshot rule reduces the lock taken by db.fsyncLock() on a mongod instance by 1. (See reference)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: px-mongodb-postsnap-rule

rules:

  - podSelector:

      app: px-mongo-mongodb

    actions:

    - type: command

      value: mongo --eval "printjson(db.fsyncUnlock())"

```

Snapshot

Creating the below VolumeSnapshot will do the following:

-
Stork will run the px-mongodb-presnap-rule rule on pod using the px-mongo-pvc PVC.

-
Once the rule is executed, Stork will take a snapshot of the px-mongo-pvc PVC.

-
After the snapshot has been triggered, Stork will run the px-mongodb-postsnap-rule rule on pod using the px-mongo-pvc PVC.

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mongodb-3d-snapshot

  annotations:

    stork.rule/pre-snapshot: px-mongodb-presnap-rule

    stork.rule/post-snapshot: px-mongodb-postsnap-rule

spec:

  persistentVolumeClaimName: px-mongo-pvc

```

#### Cassandra​

Pre-snapshot rule

Below rule flushes the tables from the memtable on all cassandra pods.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: cassandra-presnap-rule

rules:

  - podSelector:

      app: cassandra

    actions:

    - type: command

      value: nodetool flush

```

Snapshot

With this snapshot, Stork will run the cassandra-presnap-rule rule on all pods that are using PVCs that match labels app=cassandra. Hence this will be a group snapshot.

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: GroupVolumeSnapshot

metadata:

  name: cassandra-group-snapshot

spec:

  preExecRule: cassandra-presnap-rule

  pvcSelector:

    matchLabels:

      app: cassandra

```

### References​

- For information on how to restore a snapshot to a new PVC or the original PVC, see the Restore snapshots section.

- For information on how to create PVCs from group snapshots, see the Creating PVCs from group snapshots section.

In this topic:
