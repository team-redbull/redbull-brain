# Using Stork as Scheduler for Applications

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/stateful-applications/stork (Portworx Enterprise latest)

Using Stork as Scheduler for Applications | Portworx Enterprise Documentation

Stork is Portworx's storage scheduler for Kubernetes that helps achieve tighter integration of Portworx with Kubernetes. It allows users to co-locate pods with their data, provides seamless migration of pods in case of storage errors, and makes it easier to create and restore snapshots of Portworx volumes. Stork consists of two components: the Stork scheduler and an extender. Both components run in HA mode with three replicas by default.

When you install Portworx using the Portworx Enterprise Cluster Spec from Portworx Central, Stork is installed by default.

```

kubectl get pods -n portworx

...

stork-56f7c6d4cb-6b4tf                      1/1     Running    0              21h

stork-56f7c6d4cb-qs25p                      1/1     Running    0              21h

stork-56f7c6d4cb-v7q6b                      1/1     Running    0              21h

stork-scheduler-78c6dc7c6-bkglp             1/1     Running    0              21h

stork-scheduler-78c6dc7c6-lt8ql             1/1     Running    0              21h

stork-scheduler-78c6dc7c6-vwbmn             1/1     Running    0              21h

...

```

## Using Stork as a scheduler for applications​

To take advantage of Stork's features, you must use it as the scheduler for your applications. On newer versions of Stork, this is enabled by default with the webhook controller.

If the `webhook-controller` is disabled, you need to specify Stork as the scheduler to be used when creating your applications. This can be done by adding `schedulerName: stork` to your application.

note

On Amazon EKS with hybrid nodes, the EKS control plane cannot reach the Stork admission webhook if the on-premises pod network is not routable from the virtual private cloud (VPC). In this case, keep Stork on the on-premises nodes and set `schedulerName: stork` on each workload that requires Stork scheduling. For more information, see Configure hyperconvergence for workloads.

The following example shows a MySQL deployment that uses Stork as the scheduler. The key field is `schedulerName: stork` in the Pod spec:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-data

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

provisioner: kubernetes.io/portworx-volume

parameters:

  repl: "2"

---

apiVersion: apps/v1

kind: Deployment

metadata:

  name: mysql

spec:

  selector:

    matchLabels:

      app: mysql

  strategy:

    rollingUpdate:

      maxSurge: 1

      maxUnavailable: 1

    type: RollingUpdate

  replicas: 1

  template:

    metadata:

      labels:

        app: mysql

        version: "1"

    spec:

      schedulerName: stork

      containers:

      - image: mysql:5.6

        name: mysql

        env:

        - name: MYSQL_ROOT_PASSWORD

          value: password

        ports:

        - containerPort: 3306

        volumeMounts:

        - name: mysql-persistent-storage

          mountPath: /var/lib/mysql

      volumes:

      - name: mysql-persistent-storage

        persistentVolumeClaim:

          claimName: mysql-data

```

## Taint-based scheduling with Stork​

Kubernetes schedules pods based on available compute resources and scheduling policies without considering whether workloads are stateful or stateless. Stork helps place pods that use Portworx volumes onto Portworx storage nodes. However, the default Kubernetes scheduler may still place non-Portworx workloads (typically stateless) on those same storage nodes if sufficient compute resources are available. This can result in Portworx pods being scheduled onto nodes without Portworx storage.

With taint-based scheduling, the Portworx Operator and Stork coordinate Kubernetes taints and tolerations to keep Portworx storage nodes reserved for Portworx-backed stateful workloads:

- Portworx storage nodes are tagged with a hard taint `node.portworx.io/px-storage=true:NoSchedule`, while Portworx storageless nodes are tagged with a soft taint `node.portworx.io/px-storageless=true:PreferNoSchedule`.

- Portworx system components and workloads that use Portworx volumes receive matching tolerations and can continue to run on those nodes.

- Application pods that don’t use Portworx volumes and therefore don’t receive these tolerations are prevented from being scheduled on Portworx nodes.

### Prerequisites​

Ensure that the following prerequisites are met:

- Stork is enabled in the `StorageCluster` (`spec.stork.enabled: true`).

- Stork version is 25.6.0 or later.

- Operator version is 25.5.1 or later.

### Enable taint-based scheduling​

To enable the feature, set `spec.taintBasedScheduling.enabled` to `true` in the `StorageCluster`:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: portworx

spec:

  stork:

    enabled: true

  taintBasedScheduling:

    enabled: true

```

When this field is set to `true`:

- The Portworx Operator adds the following taints to Portworx nodes:

- `node.portworx.io/px-storage="true": NoSchedule` on Portworx storage nodes

- `node.portworx.io/px-storageless="true": PreferNoSchedule` on Portworx storageless nodes

- The Operator adds matching tolerations to Portworx system pods, such as Portworx, Stork, and CSI, so they continue to run on tainted nodes.

- Stork adds matching tolerations to application pods that use Portworx volumes, through the Stork admission webhook.

As a result, non-Portworx workloads without these tolerations are prevented from scheduling on storage nodes and have lower scheduling priority on storageless nodes.

The Portworx Operator is deployed and managed independently from the `StorageCluster` custom resource. To ensure that it continues running on Portworx nodes after taints are applied, you must add tolerations to the Operator deployment for the `node.portworx.io/px-storage` and `node.portworx.io/px-storageless` taints. For example, add the tolerations to your Helm chart, OLM subscription, or GitOps manifests used to deploy the Operator.

note

If you want certain non-Portworx workloads (such as monitoring agents or other infrastructure services) to run on Portworx nodes, you can manually add tolerations for the `node.portworx.io/px-storage` and/or `node.portworx.io/px-storageless` taints to the pod specifications for those workloads. Do this only for workloads that can safely share resources with Portworx and Portworx-backed applications.

### Limitation​

DaemonSets using Portworx volumes

Stork does not automatically add tolerations to Pods created by DaemonSets. DaemonSets behave differently from regular Pods in Kubernetes. If no nodes are eligible to run a Pod in the DaemonSet (due to taints, node selectors, or other scheduling constraints), the DaemonSet controller doesn’t create any Pods.

The Stork mutating webhook operates on Pod creation requests. If no Pod is created, the webhook doesn’t receive a mutation event and can’t inject the required tolerations.

For any DaemonSet whose Pods use Portworx volumes, add the required Portworx node taint tolerations directly to the DaemonSet specification.

```

tolerations:

  - key: "node.portworx.io/px-storage"

    operator: "Equal"

    value: "true"

    effect: "NoSchedule"

  - key: "node.portworx.io/px-storageless"

    operator: "Equal"

    value: "true"

    effect: "PreferNoSchedule"

```

Without these tolerations, DaemonSet pods that use Portworx volumes may fail to schedule on Portworx nodes after you enable taint-based scheduling.

## Using Stork to take snapshots of your application volumes​

With Stork you can create and restore snapshots of Portworx volumes from Kubernetes. Instructions to perform these operations can be found here.

In this topic:
