# Single Data Center Deployment

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/deployment-arch/single-dc (Portworx Enterprise 3.6)

Single Data Center Deployment | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When you want to deploy applications in a Portworx cluster in a public cloud with availability zones (AZ), or in an on-premises data center with fault domains, you have the following two options:

- Option 1 - Dedicated Portworx storage cluster deployment

- Option 2 - Hyperconverged Portworx storage cluster deployment

With any of these options the Portworx volumes and replicas will automatically be placed across the boundaries to maximize high availability.

## Option 1- Dedicated Portworx storage cluster deployment​

Solves for these primary needs:

- Computing elasticity - When you have a dynamic computing environment, where computing nodes elastically increase or decrease based on workload demand. Reasons for this might include: increasing worker nodes to handle the number of pods in the system, instance upgrades due to kernel upgrades or patches and upgrades to your orchestrator (e.g., Kubernetes).

- Separation of computing and storage - You might want to separate computing and storage clusters so that scaling and resource utilization on the storage cluster and computing cluster don't interfere with each other.

Key constraints:

- This is a single data center with multiple AZ architecture. For multi-data center High Availability (HA) or Disaster Recovery (DR), this architecture can be used in combination with the architectures presented in the Multi Data Center Deployment section.

- There is potential for resource contention if stateful services are grouped onto few nodes. Plan for adequate computing capacity to avoid degraded application performance due to noisy neighbors. This can be easily solved, however, by scaling additional compute nodes.

- Increased latency from the computing cluster to the storage cluster, similar to what you would experience with a SAN or cloud block storage.

## Option 2- Hyperconverged Portworx storage cluster deployment​

Solves for these primary needs:

- High-performance applications - When computing and storage need to be on the same server to avoid any potential network latency.

- Cluster administrators who don’t want to separately manage the computing and storage clusters.

Key constraints:

- This is a single data center/multiple AZ architecture. For multi data center HA or DR, this architecture can be used in combination with the architectures presented in the Multi Data Center Deployment section.

- VM instances are mostly static. This means the VMs don’t get recycled very frequently.

- The cluster isn’t frequently scaled horizontally. Scaling your cluster out will mean adding new compute and storage nodes each time.

HYPERCONVERGED COMPUTE AND STORAGE CLUSTER

In this topic:
