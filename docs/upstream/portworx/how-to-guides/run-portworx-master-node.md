# Run Portworx on master nodes

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/run-portworx-master-node (Portworx Enterprise 3.6)

Run Portworx on master nodes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

By default, Portworx is deployed on Kubernetes worker nodes. However, in some environments, especially those with constrained resources or unique scheduling requirements, you might need to run Portworx on master nodes. This ensures that all workloads have access to persistent storage, regardless of their scheduling location.

For example:

- In a bare metal cluster where KubeVirt hosts virtual machines (VMs) on the master node to maximize hardware resource utilization. In such configurations, Portworx must run on the master node to provide persistent storage access to VMs scheduled there.

- In a three-node edge cluster hosting applications on all nodes. In such configurations, Portworx must run on the master node to provide persistent storage access to applications scheduled on those nodes.

important

When running Portworx on master or control-plane nodes, there might be port conflicts if the PVC controller is scheduled on these nodes. This can result in errors such as:

```

"failed to create listener: failed to listen on 0.0.0.0:10257: listen tcp 0.0.0.0:10257: bind: address already in use"

```

To resolve this issue, you must configure custom ports by adding the following annotations in the StorageCluster (STC):

- `portworx.io/pvc-controller-port: "10261"`

- `portworx.io/pvc-controller-secure-port: "10262"`

## Run Portworx on master nodes using annotations​

### Fresh install​

For a fresh install, if you want to run Portworx on master nodes without providing any placement strategy in the StorageCluster, add the `portworx.io/run-on-master: "true"` annotation.

This automatically applies the following placement strategy:

```

spec:

  placement:

    nodeAffinity:

      requiredDuringSchedulingIgnoredDuringExecution:

        nodeSelectorTerms:

        - matchExpressions:

          - key: px/enabled

            operator: NotIn

            values:

            - "false"

    tolerations:

    - effect: NoSchedule

      key: node-role.kubernetes.io/master

      operator: Exists

    - effect: NoSchedule

      key: node-role.kubernetes.io/control-plane

      operator: Exists

```

Portworx will run on all nodes that do not have the `px/enabled: "false"` label. Nodes that have no label or have the `px/enabled` label set to a value other than `"false"` will also run Portworx.

### Update an existing cluster​

If Portworx is already running and you want to include master or control-plane nodes, edit your StorageCluster (STC), remove the `spec.placement` field, and add the `portworx.io/run-on-master: "true"` annotation.

The Portworx Operator will apply the configuration during the next reconciliation.

## Run Portworx on master nodes using custom node affinity and tolerations​

You can also provide custom `nodeAffinity` and `tolerations` based on your cluster configuration. For example, if your master nodes have the following taint:

```

spec:

  taints:

  - effect: NoSchedule

    key: node-role.kubernetes.io/master

```

You can configure the StorageCluster specification to ensure Portworx runs only on master and control-plane nodes:

```

spec:

  placement:

    nodeAffinity:

      requiredDuringSchedulingIgnoredDuringExecution:

        nodeSelectorTerms:

        - matchExpressions:

          - key: node-role.kubernetes.io/master

            operator: Exists

          - key: node-role.kubernetes.io/control-plane

            operator: Exists

    tolerations:

    - effect: NoSchedule

      key: node-role.kubernetes.io/master

      operator: Exists

```

note

You can customize `nodeAffinity` rules according to your node labels and add more keys in `matchExpressions` to ensure Kubernetes schedules pods on the desired nodes.

In this topic:
