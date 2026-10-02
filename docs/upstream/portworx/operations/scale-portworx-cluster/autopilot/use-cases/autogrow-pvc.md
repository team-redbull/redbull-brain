# Automatically grow PVCs

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/use-cases/autogrow-pvc (Portworx Enterprise latest)

Automatically grow PVCs | Portworx Enterprise Documentation

## Using Autopilot to Autogrow PVCs​

You can use Autopilot to expand PVCs automatically when they begin to run out of space. Autopilot monitors the metrics in your cluster (e.g., via Prometheus) and detects high usage conditions. Once high usage conditions occur, Autopilot talks with your cluster to resize the PVC.

Autopilot does not support resizing FlashBlade Direct Access (FBDA) volumes. If you are using FBDA volumes, use the `kubectl edit pvc <pvc-name>` command and update the volume size in the `spec.resources.requests.storage` field to resize such volumes.

An AutopilotRule has 4 main parts:

- PVC Selector Matches labels on the PVCs.

- Namespace Selector Matches labels on the Kubernetes namespaces the rule should monitor. This is optional, and the default is all namespaces.

- Metric conditions on the PVC to monitor.

- PVC resize action to perform once the metric conditions are met.

The following example section shows the actual YAML for this.

## Example​

The following example Autopilot rule expands Postgres PVCs by 100% whenever their usage exceeds 50% up to a maximum size of 400GiB:

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

 name: volume-resize

spec:

  ##### selector filters the objects affected by this rule given labels

  selector:

    matchLabels:

      app: postgres

  ##### namespaceSelector selects the namespaces of the objects affected by this rule

  namespaceSelector:

    matchLabels:

      type: db

  ##### conditions are the symptoms to evaluate. All conditions are AND'ed

  conditions:

    # volume usage should be less than 50%

    expressions:

    - key: "100 * (px_volume_fs_usage_bytes / px_volume_capacity_bytes)"

      operator: Gt

      values:

        - "50"

  ##### action to perform when condition is true

  actions:

  - name: openstorage.io.action.volume/resize

    params:

      # resize volume by scalepercentage of current size

      scalepercentage: "100"

      # volume capacity should not exceed 400GiB

      maxsize: "400Gi"

```

Consider the key sections in this spec.

- `selector` and `namespaceSelector`

- `conditions`

- `action`

The `selector` determines what objects are acted on by the Autopilot rule by looking for PVCs with the `app: postgres` label. Similarly, the `namespaceSelector` filters PVCs by namespaces and only includes PVCs from namespaces that contain the `type: db` label. Hence, this rule applies only to PVCs running Postgres in the DB namespaces.

note

You can also use `matchExpressions` with `selector` and `namespaceSelector`. For more information, refer to `selector` and `namespaceSelector`.

The `conditions` section determines the threshold criteria dictating when the rule has to perform its action. In this example, that criteria has the following formula:

`100 * (px_volume_fs_usage_bytes / px_volume_capacity_bytes)` gives the volume usage percentage and the `Gt` operator puts a condition that volume usage percentage has exceeded 50%.

Conditions are combined using AND logic, requiring all conditions to be true for the rule to trigger.

The `actions` section specifies what action Portworx performs when the conditions are met. Action parameters modify action behavior, and different actions contain different action parameters.

Perform the following steps to deploy this example:

### Create specs​

#### Application and PVC specs​

First, create the storage and application spec files:

-
Create `namespaces.yaml` and place the following content inside it.

```

apiVersion: v1

kind: Namespace

metadata:

  name: pg1

  labels:

    type: db

---

apiVersion: v1

kind: Namespace

metadata:

  name: pg2

  labels:

    type: db

```

-
Create `postgres-sc.yaml` and place the following content inside it.

```

##### Portworx storage class

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: postgres-pgbench-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

allowVolumeExpansion: true

```

-
Create `postgres-vol.yaml` and place the following content inside it.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pgbench-data

  labels:

    app: postgres

spec:

  storageClassName: postgres-pgbench-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 10Gi

---

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pgbench-state

spec:

  storageClassName: postgres-pgbench-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 1Gi

```

-
Create`postgres-app.yaml` and place the following content inside it.

The application in this example is a PostgreSQL database with a pgbench sidecar. The `SIZE` environment variable in this spec instructs pgbench to write 70GiB of data to the volume. Since the PVC is only 10GiB in size, Autopilot must resize the PVC when needed.

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: pgbench

  labels:

    app: pgbench

spec:

  selector:

    matchLabels:

      app: pgbench

  strategy:

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 1

    type: RollingUpdate

  replicas: 1

  template:

    metadata:

      labels:

        app: pgbench

    spec:

      schedulerName: stork

      containers:

        - image: postgres:9.5

          name: postgres

          ports:

          - containerPort: 5432

          env:

          - name: POSTGRES_USER

            value: pgbench

          - name: POSTGRES_PASSWORD

            value: superpostgres

          - name: PGBENCH_PASSWORD

            value: superpostgres

          - name: PGDATA

            value: /var/lib/postgresql/data/pgdata

          volumeMounts:

          - mountPath: /var/lib/postgresql/data

            name: pgbenchdb

        - name: pgbench

          image: portworx/torpedo-pgbench:latest

          imagePullPolicy: "Always"

          env:

            - name: PG_HOST

              value: 127.0.0.1

            - name: PG_USER

              value: pgbench

            - name: SIZE

              value: "70"

          volumeMounts:

          - mountPath: /var/lib/postgresql/data

            name: pgbenchdb

          - mountPath: /pgbench

            name: pgbenchstate

      volumes:

      - name: pgbenchdb

        persistentVolumeClaim:

          claimName: pgbench-data

      - name: pgbenchstate

        persistentVolumeClaim:

          claimName: pgbench-state

```

#### AutopilotRule spec​

Once you've created your storage and application specs, you can create an AutopilotRule that controls them.

important

It is recommended to set up only one Autopilot rule for each PVC, because Autopilot does not support more than one rule per PVC.

Create a YAML spec for the autopilot rule named `autopilotrule-example.yaml` and place the following content inside it:

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: volume-resize

spec:

  ##### selector filters the objects affected by this rule given labels

  selector:

    matchLabels:

      app: postgres

  ##### namespaceSelector selects the namespaces of the objects affected by this rule

  namespaceSelector:

    matchLabels:

      type: db

  ##### conditions are the symptoms to evaluate. All conditions are AND'ed

  conditions:

    # volume usage should be less than 50%

    expressions:

    - key: "100 * (px_volume_fs_usage_bytes / px_volume_capacity_bytes)"

      operator: Gt

      values:

        - "50"

  ##### action to perform when condition is true

  actions:

  - name: openstorage.io.action.volume/resize

    params:

      # resize volume by scalepercentage of current size

      scalepercentage: "100"

      # volume capacity should not exceed 400GiB

      maxsize: "400Gi"

```

### Apply specs​

Once you've designed your specs, deploy them.

- OpenShift

- Kubernetes

```

oc apply -f autopilotrule-example.yaml

oc apply -f namespaces.yaml

oc apply -f postgres-sc.yaml

oc apply -f postgres-vol.yaml -n pg1

oc apply -f postgres-vol.yaml -n pg2

oc apply -f postgres-app.yaml -n pg1

oc apply -f postgres-app.yaml -n pg2

```

```

kubectl apply -f autopilotrule-example.yaml

kubectl apply -f namespaces.yaml

kubectl apply -f postgres-sc.yaml

kubectl apply -f postgres-vol.yaml -n pg1

kubectl apply -f postgres-vol.yaml -n pg2

kubectl apply -f postgres-app.yaml -n pg1

kubectl apply -f postgres-app.yaml -n pg2

```

### Monitor​

Notice that the pgbench pods in the `pg1` and `pg2` namespace will start filling up the pgbench-data PVCs. As the PVC usage starts exceeding 50%, Autopilot will resize the PVCs.

You can use the following command to get all the events generated for the `volume-resize` rule:

- OpenShift

- Kubernetes

```

oc get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=volume-resize --all-namespaces --sort-by .lastTimestamp

```

```

NAMESPACE   LAST SEEN   TYPE     REASON       KIND            MESSAGE

default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

default     9m52s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

default     9m48s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

```

```

kubectl get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=volume-resize --all-namespaces --sort-by .lastTimestamp

```

```

NAMESPACE   LAST SEEN   TYPE     REASON       OBJECT                        MESSAGE

default     3m47s       Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-177eeb59-c8e6-42fe-8bc4-4dadd4bsb310-volume-resize transition from  => Initializing

default     3m47s       Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from  => Initializing

default     3m37s       Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-177eeb59-c8e6-42fe-8bc4-4dadd4bsb310-volume-resize transition from Initializing => Normal

default     3m37s       Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from Initializing => Normal

default     66s         Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from Normal => Triggered

default     23s         Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from Triggered => ActiveActionsPending

default     22s         Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from ActiveActionsPending => ActiveActionsInProgress

default     18s         Normal   Transition   autopilotrule/volume-resize   rule: volume-resize:pvc-4ba4539c-4349-4216-90f0-351ddsd7422b-volume-resize transition from ActiveActionsInProgress => ActiveActionsTaken

```

In this topic:
