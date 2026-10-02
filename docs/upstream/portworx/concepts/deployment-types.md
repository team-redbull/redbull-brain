# Portworx Deployment Types

Source: https://docs.portworx.com/portworx-enterprise/concepts/deployment-types (Portworx Enterprise latest)

Portworx Deployment Types | Portworx Enterprise Documentation

There are two approaches you can take when you architect Portworx Enterprise deployment:

- Disaggregated deployment - where the storage nodes and compute nodes are in separate groups.

- Converged deployment - where the compute and storage nodes are in the same group.

## Disaggregated Deployment - Separate Storage and Compute Node Groups​

In a disaggregated deployment, the storage nodes are in a separate storage node group (for ex, green above), and they have disks associated with them. The compute nodes are in a separate group (for ex, yellow above), and the application container workloads run on these storageless nodes. The Portworx Enterprise installation (for ex, indicated as orange above) spans across both node groups to provide a single storage fabric. The storage and compute node groups are part of the same orchestrator cluster (Single Kubernetes cluster).

If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the `portworx.io/node-type: storage` and `portworx.io/node-type: storageless` labels on Kubernetes nodes to determine their roles.

When using a managed Kubernetes cluster, you can add these label pairs when you create the node groups. This ensures that your cloud provider consistently applies the labels to all nodes. For existing node groups, if your cluster is already running, add or update the labels on your nodes using the Kubernetes command.

```

# for storage nodes

kubectl label node <node-name> portworx.io/node-type=storage

# for storageless nodes

kubectl label node <node-name> portworx.io/node-type=storageless

```

You can choose to deploy using a disaggregated model if you have a very dynamic compute environment, where the number of compute nodes can elastically increase or decrease based on workload demand. Some examples of what can cause this elasticity are:

- Autoscaling up or down due to increasing and decreasing demands. An example would be to temporarily increase the number of worker nodes from 30 to 50 to handle the number of PODs in the system.

- Instance upgrades due to reasons like kernel updates, security patches or more.

- Orchestrator upgrades (Example: Kubernetes upgrade)

Separating storage and compute clusters mean such scaling & management operations on the storage cluster don't interfere with the compute cluster, and vice versa.

note

Disaggregated deployment option is recommended in autoscaling cloud environments.

## Converged Deployment: Hyperconverged Storage and Compute clusters​

In a converged deployment, a single cluster consists of nodes providing both storage and compute. For example, a single Kubernetes cluster. The cluster might have certain nodes that don't have disks. These nodes can still run stateful applications.

Scaling and managing operations on this cluster affect both the storage and compute nodes. This approach is suitable for clusters that typically have the following characteristics:

- Hyperconverged compute and storage to achieve high performance benchmarks

- The instances in the cluster are mostly static. This means they don't get recycled very frequently.

- Scaling up and scaling down of the cluster is not that frequent

- The cluster admins don't want separation of concern between the Storage and Compute parts of the cluster.

In this topic:
