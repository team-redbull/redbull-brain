# Install Portworx on Amazon Web Services

Source: https://docs.portworx.com/portworx-enterprise/platform/install/aws (Portworx Enterprise 3.6)

Install Portworx on Amazon Web Services | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise can be installed on both Amazon Web Services (AWS) Cloud and on-premises data centers. The installation process differs depending on whether you are using Amazon Elastic Kubernetes Service (EKS), EKS with hybrid nodes in your own data center, Red Hat OpenShift Service on AWS (ROSA), or a Gardener cluster on AWS.

## Prerequisites​

In addition to the System Requirements, ensure that your cluster meets the following requirements before installing Portworx Enterprise:

- Red Hat OpenShift Service on AWS

- Amazon Elastic Kubernetes Service

- You must have a ROSA cluster with a bring-your-own-VPC (BYO-VPC) configuration deployed on infrastructure that meets the Portworx System Requirements.

- Portworx recommends using at least m5.xlarge instances with three compute nodes across three availability zones.

- Your cluster must meet the AWS prerequisites for ROSA.

- Ensure that the OCP service is enabled from your AWS console.

- Ensure that AWS CLI is installed and configured, and that ROSA CLI is installed and configured.

- If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

- `portworx.io/node-type: storage`

- `portworx.io/node-type: storageless`

note

For Amazon EKS with hybrid nodes installation prerequisites, see Installation on an Amazon EKS Cluster with Hybrid Nodes.

- You must have an Amazon EKS cluster that meets the Portworx System Requirements.

- You must have the supported disk types.

- For production environments, Portworx by Everpure recommends three Availability Zones (AZs).

- If you are installing Portworx in an air-gapped environment, ensure that you meet the following prerequisites:

- A container registry accessible from the nodes on which Portworx will be deployed. If using ECR, you must have AWS CLI installed and configured on your client machine.

- An AWS user account identity that can push or pull images to the given container registry.

- If you intend to use the `sharedv4` feature, your host systems must be running the NFS service. For more information about installing the NFS service, refer to the installation article for air-gapped clusters.

- PX-StoreV1

- PX-StoreV2

- Recommended disk sizes:

- GP2: A 150-GB disk is the minimum IOPS requirement when running on AWS.

- GP3: Specify the required IOPS and throughput for the EBS volume.

- IO1: Specify the required IOPS for the EBS volume.

- For details about GP2, GP3, and IO1 performance characteristics, see the AWS documentation.

-
You must have a Kubernetes cluster deployed on infrastructure that meets the following minimum requirements for Portworx with PX-StoreV2:
Linux kernel version 4.20 or newer (minimum), 5.0 or newer (recommended), with the following packages:

- RHEL: device-mapper, mdadm, lvm2, device-mapper-persistent-data, augeas

- Debian: dmsetup, mdadm, lvm2, thin-provisioning-tools, augeas-tools

- SUSE: dmsetup, mdadm, lvm2, device-mapper-persistent-data, augeas

- Ubuntu: dmsetup, mdadm, lvm2, thin-provisioning-tools, augeas-tools

note

During installation, Portworx automatically tries to pull the required packages from distribution-specific repositories. This is a mandatory requirement, and installation will fail if this prerequisite is not met.

-
A minimum of 64-GB system metadata device on each node where you want to deploy Portworx. If you do not provide a metadata device, one is automatically added to the specification.

-
An SSD/NVME or GP3/IO1 drive type with more than 8 GB of memory per node. For details about GP3 and IO1 performance characteristics, see the AWS documentation.

-
For installation on EKS version 1.30 or later, increase the `HttpPutResponseHopLimit` to 3 for all nodes where Portworx will be installed by running the following command:

```

aws ec2 modify-instance-metadata-options --instance-id <instanceID> --http-put-response-hop-limit 3 --http-endpoint enabled

```

-
If you plan to have a disaggregated setup, designate your nodes as storage or storageless (compute) before installing Portworx. Portworx uses the following labels on Kubernetes nodes to determine their roles:

- `portworx.io/node-type: storage`

- `portworx.io/node-type: storageless`

-
Best practices to prevent accidental deletion: If your virtualization software has a feature to prevent accidental deletion, enable it for the instances hosting PX nodes. While PX is designed to handle the loss of some nodes without issue, losing a significant number of storage nodes due to instance deletion can result in a loss of quorum and an outage. For more information about preventing accidental deletion of instances, see Enable termination protection on Amazon EC2 instances.

## Installation Options for Portworx Enterprise on AWS Clusters​

You can install Portworx on Amazon Web Services with a PX-StoreV2 datastore, but there are some limitations, such as it being supported only with a fresh Portworx installation on Amazon EKS. Therefore, you cannot upgrade from a previous Portworx version to deploy PX-StoreV2 datastore with cloud drives and Red Hat OpenShift Service on AWS (ROSA) is not supported with PX-StoreV2 datastore. For more information about PX-StoreV2 datastore, see PX-StoreV2.

Depending on whether you want to deploy Portworx with Amazon EKS, EKS Hybrid Nodes, ROSA, or a Gardener cluster on AWS, proceed to one of the following topics:

- Installation on Non-Air-Gapped Amazon Elastic Kubernetes Service (EKS) Cluster

- Using Portworx Central

- Using AWS Marketplace

- Installation on Air-Gapped Amazon Elastic Kubernetes Service (EKS) Cluster

- Installation on an Amazon EKS Cluster with Hybrid Nodes

- Installation on Red Hat OpenShift Service on AWS (ROSA) Cluster

- Installation on an AWS Gardener Cluster

In this topic:
