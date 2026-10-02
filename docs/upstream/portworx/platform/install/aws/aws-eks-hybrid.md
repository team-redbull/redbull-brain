# Installation on an Amazon EKS Cluster with Hybrid Nodes

Source: https://docs.portworx.com/portworx-enterprise/platform/install/aws/aws-eks-hybrid (Portworx Enterprise 3.6)

Installation on an Amazon EKS Cluster with Hybrid Nodes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Amazon EKS Hybrid Nodes lets you attach on-premises hosts as worker nodes to an Amazon Elastic Kubernetes Service (EKS) cluster whose control plane runs in AWS. Portworx Enterprise runs on the on-premises nodes while AWS manages the Kubernetes control plane.

The Amazon EKS control plane must be able to reach the webhook endpoints required by Portworx Enterprise. Before installing Portworx Enterprise, configure one of the following networking configurations:

-
Routable pod network: Make the on-premises pod network reachable from the virtual private cloud (VPC) so that the EKS control plane can reach webhook endpoints running on the hybrid nodes. For more information, see Amazon EKS Hybrid Nodes gateway.

-
Webhooks on cloud nodes: If the on-premises pod network is not routable from the VPC, configure the required webhook components to run on cloud nodes that the EKS control plane can reach. For more information, see Configure webhooks for hybrid nodes.

This topic provides instructions for installing Portworx Enterprise for either networking configuration.

## Prerequisites​

In addition to the System Requirements, ensure that your environment meets the following requirements:

- An Amazon EKS cluster with hybrid nodes attached and a Kubernetes version listed in Supported Kubernetes Versions.

- Network connectivity from the Amazon EKS control plane to the webhook endpoints required by Portworx Enterprise, through either a routable pod network or webhook components running on reachable cloud nodes.

- Portworx Enterprise 3.7.0 or later and Portworx Operator 26.3.2 or later.

- On-premises nodes that meet the PX-StoreV2 requirements described in the Amazon Elastic Kubernetes Service tab of the AWS prerequisites, including the required kernel version and packages and a minimum 64-GB system metadata device on each node.

- Local drives, vSphere cloud drives, FlashArray Cloud Drives (FACD), or pre-provisioned FlashArray volumes for Portworx storage.

important

-
Always configure `spec.storage` or `spec.cloudStorage` explicitly in the `StorageCluster` if the cluster contains an AWS node because the Portworx Operator treats the cluster as an Amazon EKS cluster and uses Amazon Elastic Block Store (EBS) `gp3` volumes as the default storage.

-
Outbound connectivity from the on-premises nodes to the EKS control plane does not confirm that the EKS control plane can reach on-premises pods. Admission webhooks, certificate issuance, and aggregated APIs require connectivity from the EKS control plane to the pod network.

-
To verify connectivity between the EKS control plane and the on-premises pod network, deploy a test pod on an on-premises node and confirm that the EKS control plane can reach the pod IP address on the ports required by admission webhooks.

## Install Portworx Enterprise​

Generate the Portworx Enterprise specification and install Portworx Enterprise by following the installation procedure for the storage used by your on-premises nodes:

On-premises storageInstallation procedure

Local drivesInstallation on a Non-Air-Gapped Bare Metal Kubernetes Cluster

vSphere cloud drivesInstallation on Non-Air-Gapped vSphere Kubernetes Cluster

FlashArray Cloud Drives (FACD) or pre-provisioned FlashArray volumesInstallation of Portworx with FlashArray

important

When generating the specification, select the platform that corresponds to the storage used by your on-premises nodes: DAS/SAN, vSphere, or Pure FlashArray. Do not select AWS. Selecting AWS configures Amazon EBS cloud drives, which cannot be attached to on-premises nodes.

With a routable pod network, the following capabilities are available after you install Portworx Enterprise:

- KVDB TLS certificate issuance through cert-manager without additional component placement. For more information, see How to enable TLS for Internal KVDB.

- Hyperconverged, data-local pod placement through Stork scheduling and the Stork mutating webhook. For more information, see Run Hyper Converged Using Stork.

- Asynchronous disaster recovery (DR) through the Amazon S3 cluster pair path without additional network infrastructure. For more information, see Asynchronous Disaster Recovery.

If the on-premises pod network is not routable from the VPC, complete the additional configuration described in Configure Portworx Enterprise with a non-routable pod network.

## Configure Portworx Enterprise with a non-routable pod network​

If the on-premises pod network is not routable from the VPC, the EKS control plane cannot directly reach Portworx webhook endpoints running on the hybrid nodes. Additional configuration is required for cert-manager, Stork scheduling, and the Portworx Operator.

note

Kubernetes components and add-ons that require control plane connectivity to pods on hybrid nodes might not work with a non-routable pod network. These include Metrics Server on hybrid nodes, horizontal pod autoscaling that depends on Metrics Server, custom resource definition (CRD) conversion webhooks, and Amazon Managed Service for Prometheus managed collectors.

### Enable TLS for the internal KVDB​

The EKS control plane must be able to reach the cert-manager webhook to issue certificates for internal KVDB TLS.

If the on-premises pod network is not routable from the VPC, use one of the following methods:

- Deploy and manage cert-manager separately on nodes that the EKS control plane can reach.

- Use the Portworx-managed cert-manager and pin its workloads to cloud nodes.

#### Use an externally managed cert-manager​

-
Deploy cert-manager so that the EKS control plane can reach its webhook. For more information, see Configure webhooks for hybrid nodes.

-
Set `spec.certManager.enabled` to `false` in the `StorageCluster` so that the Portworx Operator does not manage cert-manager.

#### Use the Portworx-managed cert-manager​

Set `spec.certManager.enabled` to `true` in the `StorageCluster`. Then, pin the cert-manager workloads to cloud nodes that the EKS control plane can reach by creating the following `ComponentK8sConfig` custom resource:

```

apiVersion: core.libopenstorage.org/v1

kind: ComponentK8sConfig

metadata:

  name: eks-hybrid-cert-manager-placement

  namespace: portworx

spec:

  components:

    - componentNames:

        - Cert Manager

      workloadConfigs:

        - workloadNames:

            - cert-manager

            - cert-manager-cainjector

            - cert-manager-webhook

          placement:

            nodeAffinity:

              requiredDuringSchedulingIgnoredDuringExecution:

                nodeSelectorTerms:

                  - matchExpressions:

                      - key: eks.amazonaws.com/compute-type

                        operator: NotIn

                        values:

                          - hybrid

```

note

- Component names are case-sensitive. Use `Cert Manager` and the workload names listed in Mapping of components to workloads, pods, and containers.

- Do not patch the cert-manager deployments directly. The Portworx Operator reverts direct changes during reconciliation.

- If the cloud nodes have a taint, add the corresponding toleration under `placement.tolerations`.

For more information, see Configure Portworx Pods and Containers and the ComponentK8sConfig CRD reference.

#### Configure DNS resolution​

If you pin cert-manager to cloud nodes, the cert-manager workloads require DNS resolution from those nodes. If CoreDNS runs only on the on-premises nodes, configure DNS to serve both cloud and hybrid nodes.

-
Label each hybrid node with a topology zone:

```

kubectl label node <hybrid-node> topology.kubernetes.io/zone=onprem

```

-
Run at least one CoreDNS replica on the cloud nodes. Ensure that the replica uses the `k8s-app=kube-dns` label so that it joins the existing Kubernetes DNS service.

-
Configure the Kubernetes DNS service to prefer zone-local traffic:

```

kubectl patch svc kube-dns -n kube-system --type=merge \

  -p '{"spec":{"trafficDistribution":"PreferClose"}}'

```

-
If you use Cilium as the CNI, enable service topology:

```

cilium config set enable-service-topology true

```

### Configure Stork scheduling for workloads​

If the EKS control plane cannot reach the Stork mutating webhook on the on-premises nodes, hyperconverged, data-local pod placement is not available for workloads.

To configure Stork scheduling with a non-routable pod network:

-
Keep Stork on the on-premises nodes. Do not move Stork to cloud nodes.

-
(Optional) Set `spec.stork.args.webhook-controller` to `"false"` in the `StorageCluster`.

note

Disabling the webhook controller introduces an approximately 10-millisecond scheduling delay.

-
Add `schedulerName: stork` to the deployment template (manifest) of each workload that requires Stork scheduling:

```

spec:

  template:

    spec:

      schedulerName: stork

```

For more information, see Using Stork as Scheduler for Applications.

note

Setting `schedulerName: stork` configures the workload to use Stork for scheduling, but does not provide hyperconverged, data-local pod placement with a non-routable pod network.

### Configure the Portworx Operator​

If you use the Amazon EKS Hybrid Nodes gateway and the Portworx Operator cannot reach the Kubernetes API server, the Operator cannot create the required custom resource definitions (CRDs).

Configure the Portworx Operator to use the host network so that its traffic reaches the Kubernetes API server through the node network instead of the pod network:

```

kubectl patch deployment portworx-operator -n <px-namespace> --type=json \

  -p='[

    {"op":"add","path":"/spec/template/spec/hostNetwork","value":true},

    {"op":"add","path":"/spec/template/spec/dnsPolicy","value":"ClusterFirstWithHostNet"}

  ]'

```

Replace `<px-namespace>` with the namespace where the Portworx Operator is installed.

Apply this patch before you apply the `StorageCluster` specification:

```

kubectl apply -f <portworx-stc>.yaml

```

## Unsupported configurations​

Portworx Enterprise does not support the following configurations and features on Amazon EKS with hybrid nodes:

- `vault` and `aws-kms` secret store providers

- Workload identity

- External KVDB

- PX-StoreV1

- Proxy configurations

- IPv6 and dual-stack networking

- Air-gapped installations

## What to do next​

After Portworx Enterprise is running:

- If you enabled TLS for the internal KVDB, verify that TLS is active. For more information, see How to enable TLS for Internal KVDB.

- Configure asynchronous DR as needed. For more information, see Asynchronous Disaster Recovery.

In this topic:
