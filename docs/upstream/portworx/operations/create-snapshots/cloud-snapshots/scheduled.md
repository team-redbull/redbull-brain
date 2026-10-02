# Scheduled Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/cloud-snapshots/scheduled (Portworx Enterprise latest)

Scheduled Snapshots | Portworx Enterprise Documentation

For PVCs provisioned by the Portworx CSI driver (`pxd.portworx.com`), the recommended way to schedule snapshots is with a `VolumeSnapshotClass` referenced from a `StorageClass` or `VolumeSnapshotSchedule`. See Associate a schedule policy using a CSI VolumeSnapshotClass. PVCs provisioned by the legacy in-tree Portworx driver use the VolumeSnapshotSchedule method instead.

## Prerequisites​

### Configuring cloud secrets​

To create cloud snapshots, you need to configure secrets with Portworx to connect and authenticate with the configured cloud provider.

Follow instructions on the create and configure credentials section to set up secrets.

### Storkctl​

important

Always use the latest `storkctl` binary tool by downloading it from the current running Stork container.

Perform the following steps to download `storkctl` from the Stork pod:

- Kubernetes

- OpenShift

-
Linux:

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
OS X:

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
Windows:

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(kubectl get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

-
Linux:

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
OS X:

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
Windows:

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(oc get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

## Create a schedule policy​

You can use a schedule policy to specify when Portworx should trigger a specific action.

-
Create a file named `daily-policy.yaml`, specifying the following fields and values:

-
apiVersion: with the version of the Stork scheduler (this example uses `stork.libopenstorage.org/v1alpha1`)

-
kind: with the `SchedulePolicy` value

-
metadata.name: with the name of the `SchedulePolicy` object (this example uses `daily`)

-
policy.daily.time: with the backup time (this example uses "10:14PM")

-
policy.retain: with the number of backups Portworx must retain (this example retains 3 backups)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: daily

policy:

  daily:

    time: "10:14PM"

    retain: 3

```

For more details about how you can configure a schedule policy, see the Schedule Policy reference page.

- Kubernetes

- OpenShift

```

kubectl apply -f daily-policy.yaml

```

```

schedulepolicy.stork.libopenstorage.org/daily created

```

```

oc apply -f daily-policy.yaml

```

```

schedulepolicy.stork.libopenstorage.org/daily created

```

```

schedulepolicy.stork.libopenstorage.org/daily created

```

-
You can check the status of your schedule policy by entering the `storkctl get schedulepolicy` command:

```

storkctl get schedulepolicy

```

```

NAME      INTERVAL-MINUTES   DAILY     WEEKLY             MONTHLY

daily     N/A                10:14PM   N/A                N/A

```

## Associate a schedule policy with a StorageClass or a Volume​

The following sections show how you can associate a schedule policy either with a `Volume` or a `StorageClass`.

note

In Azure AKS, if you associate a schedule policy with a storage class, you cannot use Stork to manage that schedule policy.

### Associate a schedule policy using a CSI VolumeSnapshotClass​

Starting with Stork 26.4.0 and Portworx Enterprise 3.6.2 or later, VolumeSnapshotSchedules for PVCs provisioned by the Portworx CSI driver (`pxd.portworx.com`) use CSI VolumeSnapshots (`snapshot.storage.k8s.io/v1`). This is the recommended method for scheduling snapshots for CSI-provisioned PVCs.

PVCs provisioned by the legacy in-tree Portworx driver continue to use the VolumeSnapshotSchedule.

To schedule CSI VolumeSnapshots:

- Create a `VolumeSnapshotClass` for each snapshot type you want (local or cloud with a specific credential).

- Reference that class from a `StorageClass` so Stork automatically creates a `VolumeSnapshotSchedule` for every PVC that uses it, or reference it directly from a `VolumeSnapshotSchedule` for a specific existing PVC.

note

For VolumeSnapshotSchedules created on CSI-provisioned PVCs before you upgraded Stork to 26.4.0 or later, Stork automatically creates a matching VolumeSnapshotClass (named `stork-auto-cloud-<sanitized-cred-id>`) from the schedule's legacy `portworx/snapshot-type` and `portworx/cloud-cred-id` annotations, so existing schedules keep working without modification. Stork creates this class only when it's absent and never patches it on subsequent reconciles. Only new snapshots created after the upgrade use the CSI VolumeSnapshot; snapshots created before the upgrade are not converted.

#### Create a VolumeSnapshotClass​

Create one `VolumeSnapshotClass` per snapshot type and reference it by name from your `StorageClass` or `VolumeSnapshotSchedule`.

The Portworx CSI driver reads the following parameters from the VolumeSnapshotClass:

ParameterTypeDefaultDescription

`csi.openstorage.org/snapshot-type`string`local`Snapshot type. Set to `cloud` for cloud backups.

`csi.openstorage.org/snapshot-credential-id`string—UUID of the Portworx cloud credential (`pxctl credentials list`). Required for cloud snapshots unless the cluster default credential is used.

`csi.openstorage.org/snapshot-incremental-count`stringcluster default (7)Number of incremental backups between full backups. `"0"` forces every backup to be a full backup.

important

When the SchedulePolicy's `retain` count is less than the cluster's Cloudsnap full backup frequency (default: 7), set `csi.openstorage.org/snapshot-incremental-count` on the VolumeSnapshotClass to a value no greater than `retain - 1`. This keeps every incremental's dependency chain inside the retain window and prevents snapshot deletion from being blocked by snapshots still referenced as a diff base.

For example, if your SchedulePolicy sets `retain: 3`, set `snapshot-incremental-count` to `"2"` or less.

Local VolumeSnapshotClass:

```

apiVersion: snapshot.storage.k8s.io/v1

kind: VolumeSnapshotClass

metadata:

  name: px-local-vsc

driver: pxd.portworx.com

deletionPolicy: Delete

```

Cloud VolumeSnapshotClass:

```

apiVersion: snapshot.storage.k8s.io/v1

kind: VolumeSnapshotClass

metadata:

  name: px-cloud-vsc

driver: pxd.portworx.com

deletionPolicy: Delete

parameters:

  csi.openstorage.org/snapshot-type: cloud

  csi.openstorage.org/snapshot-credential-id: <credential-uuid>

  csi.openstorage.org/snapshot-incremental-count: "6"

```

Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f volume-snapshot-class.yaml

```

```

oc apply -f volume-snapshot-class.yaml

```

#### Create a storage class​

Reference the VolumeSnapshotClass from a `StorageClass` using the `stork.libopenstorage.org/volume-snapshot-class-name` annotation inside a `snapshotschedule.stork.libopenstorage.org/<name>` parameter. Stork then automatically creates a `VolumeSnapshotSchedule` named `<pvc-name>-<name>` for every PVC that uses this `StorageClass`.

-
Create a file called `sc-with-snap-schedule.yaml` with the following content:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-sc-with-snap-schedules

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  snapshotschedule.stork.libopenstorage.org/daily-schedule: |

    schedulePolicyName: daily

    reclaimPolicy: Retain

    annotations:

      stork.libopenstorage.org/volume-snapshot-class-name: px-local-vsc

  snapshotschedule.stork.libopenstorage.org/weekly-schedule: |

    schedulePolicyName: weekly

    reclaimPolicy: Delete

    annotations:

      stork.libopenstorage.org/volume-snapshot-class-name: px-cloud-vsc

```

note

This example references two schedules:

- The `daily-schedule` backs up volumes to the local Portworx cluster daily, using the `px-local-vsc` VolumeSnapshotClass created above.

- The `weekly-schedule` backs up volumes to cloud storage every week, using the `px-cloud-vsc` VolumeSnapshotClass created above.

important

On auth-enabled (PX-Security) clusters, add the standard CSI provisioner secret parameters to the StorageClass so Portworx can authenticate volume provisioning, mounting, and resizing:

```

parameters:

  csi.storage.k8s.io/provisioner-secret-name: px-user-token

  csi.storage.k8s.io/provisioner-secret-namespace: portworx

  csi.storage.k8s.io/node-publish-secret-name: px-user-token

  csi.storage.k8s.io/node-publish-secret-namespace: portworx

  csi.storage.k8s.io/controller-expand-secret-name: px-user-token

  csi.storage.k8s.io/controller-expand-secret-namespace: portworx

```

These secrets are unrelated to snapshotting — they authenticate volume provisioning, mounting, and resizing. For snapshot operations on auth-enabled clusters, add `csi.storage.k8s.io/snapshotter-secret-name` and `csi.storage.k8s.io/snapshotter-secret-namespace` to the `VolumeSnapshotClass` instead of the StorageClass.

-
Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f sc-with-snap-schedule.yaml

```

```

oc apply -f sc-with-snap-schedule.yaml

```

#### Create a VolumeSnapshotSchedule directly​

Skip the StorageClass wiring above and create a `VolumeSnapshotSchedule` directly when you want to schedule snapshots for a specific existing PVC. Reference your VolumeSnapshotClass using the `stork.libopenstorage.org/volume-snapshot-class-name` annotation.

- Create a file called `volume-snapshot-schedule.yaml` specifying the following fields and values:

- metadata:

- name: with the name of this VolumeSnapshotSchedule policy

- namespace: the namespace in which this policy will exist

- annotations.stork.libopenstorage.org/volume-snapshot-class-name: with the name of the VolumeSnapshotClass to use

- spec:

-
schedulePolicyName: with the name of the schedule policy you defined in the steps above

-
suspend: with a boolean value specifying if the schedule should be in a suspended state

-
preExecRule: with the name of a rule to run before taking the snapshot

-
postExecRule: with the name of a rule to run after taking the snapshot

-
reclaimPolicy: with `Retain` or `Delete`, indicating what Portworx should do with the snapshots that were created using the schedule. Specifying the `Delete` value deletes the snapshots created by this schedule when the schedule is deleted.

-
template.spec.persistentVolumeClaimName: with the PVC you want this policy to apply to

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: VolumeSnapshotSchedule

metadata:

  name: mysql-snapshot-schedule

  namespace: mysql

  annotations:

    stork.libopenstorage.org/volume-snapshot-class-name: px-cloud-vsc

spec:

  schedulePolicyName: daily

  suspend: false

  reclaimPolicy: Delete

  preExecRule: testRule

  postExecRule: otherTestRule

  template:

    spec:

      persistentVolumeClaimName: mysql-data

```

-
Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f volume-snapshot-schedule.yaml

```

```

oc apply -f volume-snapshot-schedule.yaml

```

To restore a snapshot created by a VolumeSnapshotSchedule, see Restore a cloud snapshot to a new PVC

### VolumeSnapshotSchedule (for in-tree PVCs)​

note

Use this method only for PVCs provisioned by the legacy in-tree Portworx driver. PVCs provisioned by the Portworx CSI driver (`pxd.portworx.com`) should use the VolumeSnapshotClass-based flow described above instead.

Use a `VolumeSnapshotSchedule` to associate your schedule policy at the CRD level, and back up specific volumes according to a schedule you define.

- Create a file called `volume-snapshot-schedule.yaml` specifying the following fields and values:

- metadata:

- name: with the name of this VolumeSnapshotSchedule policy

- namespace: the namespace in which this policy will exist

- annotations:

- portworx/snapshot-type: with the `cloud` or `local` value, depending on what environment you want store your snapshots in

- portworx/cloud-cred-id: with your cloud environment credentials

- stork.libopenstorage.org/snapshot-restore-namespaces: with other namespaces snapshots taken with this policy can restore to

- The following annotations are required when PX-Security is enabled:

- openstorage.io/auth-secret-namespace: namespace where the Kubernetes Secret holding the auth token resides

- openstorage.io/auth-secret-name: name of the Kubernetes Secret which holds the auth token

- spec:

-
schedulePolicyName: with the name of the schedule policy you defined in the steps above

-
suspend: with a boolean value specifying if the schedule should be in a suspended state

-
preExecRule: with the name of a rule to run before taking the snapshot

-
postExecRule: with the name of a rule to run after taking the snapshot

-
reclaimPolicy: with `retain` or `delete`, indicating what Portworx should do with the snapshots that were created using the schedule. Specifying the `delete` value deletes the snapshots created by this schedule when the schedule is deleted.

-
template.spec.persistentVolumeClaimName: with the PVC you want this policy to apply to

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: VolumeSnapshotSchedule

metadata:

  name: mysql-snapshot-schedule

  namespace: mysql

  annotations:

    portworx/snapshot-type: cloud

    portworx/cloud-cred-id: <cred_id>

    stork.libopenstorage.org/snapshot-restore-namespaces: otherNamespace

    # Add the below annotations when PX-Security is enabled.

    #openstorage.io/auth-secret-namespace: <secret-namespace>

    #openstorage.io/auth-secret-name: <secret-name>

spec:

  schedulePolicyName: testpolicy

  suspend: false

  reclaimPolicy: Delete

  preExecRule: testRule

  postExecRule: otherTestRule

  template:

    spec:

      persistentVolumeClaimName: mysql-data

```

-
Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f volume-snapshot-schedule.yaml

```

```

oc apply -f volume-snapshot-schedule.yaml

```

### Legacy storage class (for in-tree PVCs)​

note

Use this method only for PVCs provisioned by the legacy in-tree Portworx driver.

Use a `StorageClass` to apply your schedule policy to all PVCs using that `StorageClass`.

-
Create a file called `sc-with-snap-schedule.yaml` with the following content:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-sc-with-snap-schedules

provisioner: pxd.portworx.com

parameters:

  # Add the below parameters when PX-Security is enabled.

  # openstorage.io/auth-secret-namespace: <secret-namespace>

  # openstorage.io/auth-secret-name: <secret-name>

  repl: "2"

  snapshotschedule.stork.libopenstorage.org/default-schedule: |

    schedulePolicyName: daily

    annotations:

      portworx/snapshot-type: local

  snapshotschedule.stork.libopenstorage.org/weekly-schedule: |

    schedulePolicyName: weekly

    annotations:

      portworx/snapshot-type: cloud

      portworx/cloud-cred-id: <credential-uuid>

```

note

This example references two schedules:

- The `default-schedule` backs up volumes to the local Portworx cluster daily.

- The `weekly-schedule` backs up volumes to cloud storage every week.

-
Apply the spec:

- Kubernetes

- OpenShift

```

kubectl apply -f sc-with-snap-schedule.yaml

```

```

oc apply -f sc-with-snap-schedule.yaml

```

### Specifying the cloud credential to use​

note

This applies only to the legacy VolumeSnapshotSchedule and StorageClass methods above. For the CSI-based flow, set the credential using the `csi.openstorage.org/snapshot-credential-id` parameter on the `VolumeSnapshotClass` instead — see Create a VolumeSnapshotClass.

note

Specifying the `portworx/cloud-cred-id` is required only if you have more than one cloud credentials configured. If you have a single one, by default, that credential is used.

List all available cloud credentials.

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl credentials list

```

```

PX_POD=$(oc get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

oc exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl credentials list

```

The command outputs the credentials required to authenticate with and access the object store. Pick the one you want to use for this snapshot schedule and specify it in the `portworx/cloud-cred-id` annotation in the StorageClass.

Apply your newly created storage class:

- Kubernetes

- OpenShift

```

kubectl apply -f sc-with-snap-schedule.yaml

```

```

storageclass.storage.k8s.io/px-sc-with-snap-schedules created

```

```

oc apply -f sc-with-snap-schedule.yaml

```

```

storageclass.storage.k8s.io/px-sc-with-snap-schedules created

```

## Create a PVC​

After you create the StorageClass, you can refer to it by name in your PVCs:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pvc-snap-schedules-demo

  annotations:

    volume.beta.kubernetes.io/storage-class: px-sc-with-snap-schedules

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

Paste the listing from above into a file named `pvc-snap-schedules-demo.yaml` and run:

- Kubernetes

- OpenShift

```

kubectl create -f pvc-snap-schedules-demo.yaml

```

```

persistentvolumeclaim/pvc-snap-schedules-demo created

```

```

oc create -f pvc-snap-schedules-demo.yaml

```

```

persistentvolumeclaim/pvc-snap-schedules-demo created

```

View your PVC:

- Kubernetes

- OpenShift

```

kubectl get pvc

```

```

NAME                      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                AGE

pvc-snap-schedules-demo   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7   2Gi        RWO            px-sc-with-snap-schedules   14s

```

```

oc get pvc

```

```

NAME                      STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS                AGE

pvc-snap-schedules-demo   Bound    pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7   2Gi        RWO            px-sc-with-snap-schedules   14s

```

This output shows that Portworx automatically created a volume named `pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7` and bound it to your PVC.

## Checking snapshots​

### Verifying snapshot schedules​

First, verify that the snapshot schedules are created correctly.

```

storkctl get volumesnapshotschedules

```

```

NAME                                       PVC                       POLICYNAME   PRE-EXEC-RULE   POST-EXEC-RULE   RECLAIM-POLICY   SUSPEND   LAST-SUCCESS-TIME

pvc-snap-schedules-demo-default-schedule   pvc-snap-schedules-demo   daily                                         Retain           false

pvc-snap-schedules-demo-weekly-schedule    pvc-snap-schedules-demo   weekly                                        Retain           false

```

You can see two snapshot schedules, one daily and one weekly.

### Verifying snapshots​

Verify that your cloud snapshots are created.

### Using storkctl​

You can use `storkctl` to verify that snapshots are created by running:

```

storkctl get volumesnapshots

```

```

NAME                                                                  PVC                       STATUS    CREATED               COMPLETED             TYPE

pvc-snap-schedules-demo-default-schedule-interval-2019-03-27-015546   pvc-snap-schedules-demo   Ready     26 Mar 19 21:55 EDT   26 Mar 19 21:55 EDT   local

pvc-snap-schedules-demo-weekly-schedule-interval-2019-03-27-015546    pvc-snap-schedules-demo   Ready     26 Mar 19 21:55 EDT   26 Mar 19 21:55 EDT   cloud

```

In this topic:
