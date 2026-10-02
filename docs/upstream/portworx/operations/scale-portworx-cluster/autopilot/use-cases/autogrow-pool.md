# Automatically expand Portworx storage pools

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/use-cases/autogrow-pool (Portworx Enterprise 3.6)

Automatically expand Portworx storage pools | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can use Autopilot to expand Portworx storage pools automatically when they begin to run out of space. Autopilot monitors the metrics in your cluster (e.g., via Prometheus) and detects high usage conditions. Once high usage conditions occur, Autopilot communicates with Portworx to resize the pool.

Autopilot uses Portworx APIs to expand storage pools, and these APIs currently support the following cloud providers:

- Azure

- AWS

- VMware vSphere

- FlashArray

- Google Cloud Platform

note

The `add-drive` operation is not supported with PX-StoreV2.

## Prerequisites​

- Portworx cloud drives: Your Portworx installation must use one of the supported cloud drives where Portworx provisions the backing drives using the cloud provider

- Autopilot version: 1.2.13 and later

## Example spec​

You can use the `auto` scale type to automatically expand the Portworx storage pool. You can also specify the `add-drive` or `resize-drive` scale type based on your specific use case.

important

PX-StoreV2 supports scaling using only the `resize-drive` method. The `add-drive` method is not supported. If you select the `auto` scaling method, Portworx automatically uses `resize-drive` to scale the storage pool.

The following example Autopilot rules use the different scale types supported to resize all Portworx storage pools in the cluster until each pool exceeds 400 GiB. For more information about scale types, refer to `openstorage.io.action.storagepool/expand`.

- Auto

- Add drive

- Resize drive

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate. All conditions are AND'ed.

  conditions:

    expressions:

    # Pool available capacity is less than 50%

    - key: "100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)"

      operator: Lt

      values:

        - "50"

    # Total pool capacity should not exceed 400 GiB

    - key: "px_pool_stats_total_bytes / (1024 * 1024 * 1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when conditions are true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # Auto-scale the pool by a percentage of its current size

        scalepercentage: "50"

        # When scaling, use auto-scaling logic

        scaletype: "auto"

```

### Key Sections in the Spec

-
The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains two formulas:

- `100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)`:

- This calculates the percentage of available capacity in the pool.

- The `Lt` (less than) operator sets a condition that the pool’s available capacity percentage must be less than 50%.

- `px_pool_stats_total_bytes / (1024 * 1024 * 1024)`:

- This calculates the total pool capacity in GiB.

- The Lt operator limits the pool size to a maximum of 400 GiB.

These conditions are combined using logical operator `AND`, meaning all conditions must be true for the rule to trigger.

-
The `actions` section specifies the operation that Portworx performs when the conditions are met. Action parameters control the behavior of the action, and different actions include different parameters. In this example, the actions section directs Portworx to:

- Increase the pool size by 50% of its current size (`scalepercentage: "50"`).

- The `auto` scale type is used, allowing Autopilot to either add new drives or resize existing ones automatically, based on available resources and configuration.

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate. All conditions are AND'ed.

  conditions:

    expressions:

    # Pool available capacity is less than 50%

    - key: "100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)"

      operator: Lt

      values:

        - "50"

    # Total pool capacity should not exceed 400 GiB

    - key: "px_pool_stats_total_bytes / (1024 * 1024 * 1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when conditions are true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # Add a new drive to the pool by a percentage of its current size

        scalepercentage: "50"

        # When scaling, add a new drive to the pool

        scaletype: "add-drive"

        # skip wait for clean volumes before resize

        dontWaitForCleanVolumes: "false" #WARNING: Might cause downtime for single-replica (repl1) volumes.

```

### Key Sections in the Spec

-
The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains two formulas:

- `100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)`:

- This calculates the percentage of available capacity in the pool.

- The `Lt` (less than) operator sets a condition that the pool’s available capacity percentage must be less than 50%.

- `px_pool_stats_total_bytes / (1024 * 1024 * 1024)`:

- This calculates the total pool capacity in GiB.

- The Lt operator limits the pool size to a maximum of 400 GiB.

These conditions are combined using logical operator `AND`, meaning all conditions must be true for the rule to trigger.

-
The `actions` section specifies the operation that Portworx performs when the conditions are met. Action parameters control the behavior of the action, and different actions include different parameters. In this example, the actions section directs Portworx to:

- Increase the pool size by 50% of its current size (`scalepercentage: "50"`).

- The `add-drive` scale type is used, explicitly instructing Portworx to expand the pool by attaching new drives rather than resizing existing ones.

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate. All conditions are AND'ed.

  conditions:

    expressions:

    # Pool available capacity is less than 50%

    - key: "100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)"

      operator: Lt

      values:

        - "50"

    # Total pool capacity should not exceed 400 GiB

    - key: "px_pool_stats_total_bytes / (1024 * 1024 * 1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when conditions are true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # Resize the pool by a percentage of its current size

        scalepercentage: "50"

        # When scaling, resize the existing disks in the pool

        scaletype: "resize-drive"

        # skip wait for clean volumes before resize

        dontWaitForCleanVolumes: "false" #WARNING: Might cause downtime for single-replica (repl1) volumes.

```

### Key Sections in the Spec

-
The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains two formulas:

- `100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)`:

- This calculates the percentage of available capacity in the pool.

- The `Lt` (less than) operator sets a condition that the pool’s available capacity percentage must be less than 50%.

- `px_pool_stats_total_bytes / (1024 * 1024 * 1024)`:

- This calculates the total pool capacity in GiB.

- The Lt operator limits the pool size to a maximum of 400 GiB.

These conditions are combined using logical operator `AND`, meaning all conditions must be true for the rule to trigger.

-
The `actions` section specifies the operation that Portworx performs when the conditions are met. Action parameters control the behavior of the action, and different actions include different parameters. In this example, the actions section directs Portworx to:

- Increase the pool size by 50% of its current size (`scalepercentage: "50"`).

- The `resize-drive` scale type is used, instructing Portworx to expand the pool by resizing the existing drives, ensuring no new drives are added.

note

When you expand your storage pool using the `add-drive` scale type, Autopilot increases your pool storage capacity by adding new drives to the pool based on the scale percentage. The new drives will match the capacity of the existing ones because the storage pool consists of drives of equal size. For example, if your current pool consists of 100 GiB drive, with `add-drive` scale type, a 100 GiB drive is added to your pool, thus expanding it by 100%. In such cases, scale percentage represents the minimum percentage by which Portworx will scale up the pool. This note is only applicable if you are not using PX-StoreV2 as your backend.

## Define and add Autopilot rule​

Perform the following steps to deploy the above example.

### Create application and PVC specs​

note

The specs below create an application that writes 300 GiB of data to a 400 GiB volume. If your Storage pools are larger than that, you must change these numbers to ensure the capacity condition triggers.

First, create the storage and application spec files:

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

spec:

  storageClassName: postgres-pgbench-sc

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 400Gi

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
Create `postgres-app.yaml` and place the following content inside it.

The application in this example is a PostgreSQL database with a pgbench sidecar. The `SIZE` environment variable in this spec instructs pgbench to write 300GiB of data to the volume. Since the volume is 400GiB in size, Autopilot will resize the storage pool when the `conditions` threshold is crossed.

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

              value: "300"

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

### AutopilotRule spec​

Once you've created your storage and application specs, you can create an AutopilotRule that controls them.

Use the example spec and create a YAML spec for the autopilot rule named `autopilotrule-pool-expand-example.yaml`.

### Apply specs​

Once you've designed your specs, deploy them.

- OpenShift

- Kubernetes

```

oc apply -f autopilotrule-pool-expand-example.yaml

oc apply -f postgres-sc.yaml

oc apply -f postgres-vol.yaml

oc apply -f postgres-app.yaml

```

```

kubectl apply -f autopilotrule-pool-expand-example.yaml

kubectl apply -f postgres-sc.yaml

kubectl apply -f postgres-vol.yaml

kubectl apply -f postgres-app.yaml

```

### Monitor​

Observe how the pgbench pod starts filling up the pgbench-data PVCs and, by extension, the underlying Portworx storage pools. As the pool usage exceeds 50%, Autopilot resizes the storage pools.

You can enter the following command to retrieve all the events generated for the `pool-expand` rule:

- OpenShift

- Kubernetes

```

oc get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=pool-expand --all-namespaces --sort-by .lastTimestamp

```

```

kubectl get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=pool-expand --all-namespaces --sort-by .lastTimestamp

```

In this topic:
