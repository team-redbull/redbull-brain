# System Requirements

Source: https://docs.portworx.com/portworx-enterprise/platform/prerequisites (Portworx Enterprise 3.6)

System Requirements | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Before installing Portworx Enterprise, ensure your environment meets the minimum requirements for a stable and supported deployment. A Portworx cluster must include at least three nodes, each meeting specific hardware, software, and network requirements.

## Hardware requirements​

Each node in the Portworx cluster must meet baseline hardware specifications. These vary slightly depending on whether you're using PX-StoreV1 or PX-StoreV2. Requirements include CPU, RAM, disk space, and storage drive configuration to ensure optimal operation.

- PX-StoreV1

- PX-StoreV2

HardwareRequirements

CPUMinimum 4 Cores | Recommended 8 Cores

RAMMinimum 4GB | Recommended 8GB

Disk
- `/var` - Recommended 30GB Free

- `/opt` - Minimum 3.5GB Free

Backing driveMinimum 8GB
 Recommended 128GB

Operating system root partition
- Minimum 64GB is required for the root filesystem, which contains the operating system.

- Recommended 128GB

Storage drivesStorage drives must be unmounted block storage: raw disks, drive partitions, LVM, or cloud block storage.

Network connectivity
Bandwidth:

- 10 Gbps recommended

- 1 Gbps minimum

Latency requirements for synchronous replication: less than 10ms between nodes in the cluster.

Node typeBare metal and virtual machine (VM)

HardwareRequirements

CPUMinimum 8 Cores | Recommended 16 Cores

RAMMinimum 8GB | Recommended 16GB

Disk
- `/var` - Recommended 20GB Free

- `/opt` - Minimum 3.5GB Free | Recommended 20GB Free

Backing driveMinimum 8GB
 Recommended 128GB

Operating system root partitionIf `/opt` and `/var` are created as separate disks, then 64 GB is sufficient for root partition. Otherwise, minimum 128GB is required.

Storage drivesStorage drives must be unmounted block storage: raw disks, drive partitions, or cloud block storage.

Network connectivity
Bandwidth:

- 10 Gbps recommended

- 1 Gbps minimum

Latency requirements for synchronous replication: less than 10ms between nodes in the cluster.

Node typeBare metal and virtual machine (VM)

## Software requirements​

Each node in the Portworx cluster must meet the necessary software requirements, including a supported Linux kernel version, container runtime, and key-value store configuration. Portworx also depends on specific system utilities and settings, such as having swap disabled and NTP enabled, to ensure reliable and consistent cluster behavior.

- PX-StoreV1

- PX-StoreV2

SoftwareRequirements

Linux kernel and distro
Kernel version 4.18 or greater.
 To check if your Linux distro and kernel are supported, see Supported Kernels.

DockerVersion 1.13.1 or greater.

Key-value store
Portworx needs a key-value store to perform its operations. As such, install a clustered key-value database (`kvdb`) with a three-node cluster.

 You can also use Internal KVDB during installation. In this mode, Portworx creates and manages an internal key-value store (KVDB) cluster.

 If you plan to use your own KVDB, refer to KVDB for Portworx for details on recommendations for installing and configuring a KVDB cluster.

Disable swap
Disable swap on all nodes that will run the Portworx software. Ensure that the swap device is not automatically mounted on server reboot.

Network Time Protocol (NTP)
All nodes in the cluster should be in sync with NTP time. Any time drift between nodes can cause unexpected behavior, impacting services.

Key Management Service (KMS)
If you plan to use a KMS to store encryption keys, secrets, or credentials for features such as CloudSnap, volume encryption, or cloud provider credentials during Portworx Enterprise installation, you must first configure Portworx Enterprise to authenticate with the selected KMS. For more information, see Set Up Key Management and Encrypt Portworx Volumes.

SoftwareRequirements

Linux kernel and distro
Linux kernel version: 4.20 or newer (minimum), 5.0 or newer (recommended). During installation, Portworx automatically pulls the `dmsetup`, `mdadm`, `lvm2`, `thin-provisioning-tools`, `augeas-tools` packages from distribution-specific repositories. This is a mandatory requirement and installation will fail if this prerequisite is not met.
To check if your Linux distro and kernel are supported, see Supported Kernels.

DockerVersion 1.13.1 or greater.

Key-value store
Portworx needs a key-value store to perform its operations. As such, install a clustered key-value database (`kvdb`) with a three-node cluster.

 You can also use Internal KVDB during installation. In this mode, Portworx creates and manages an internal key-value store (KVDB) cluster.

 If you plan to use your own KVDB, refer to KVDB for Portworx for details on recommendations for installing and configuring a KVDB cluster.

Disable swap
Disable swap on all nodes that will run the Portworx software. Ensure that the swap device is not automatically mounted on server reboot.

Network Time Protocol (NTP)
All nodes in the cluster should be in sync with NTP time. Any time drift between nodes can cause unexpected behavior, impacting services.

Key Management Service (KMS)
If you plan to use a KMS to store encryption keys, secrets, or credentials for features such as CloudSnap, volume encryption, or cloud provider credentials during Portworx Enterprise installation, you must first configure Portworx Enterprise to authenticate with the selected KMS. For more information, see Set Up Key Management and Encrypt Portworx Volumes.

## Supported hypervisor versions​

HypervisorSupported Versions

VMware vSphere

- Version 7.0

- Version 8.0

## OpenShift Virtualization​

Portworx Enterprise supports deployment on virtual clusters (hosted clusters) created on top of KubeVirt VMs running in OpenShift Virtualization. For installation instructions, see How to deploy OpenShift hosted clusters with Portworx.

## Network requirements​

Portworx runs as a Pod in a Kubernetes cluster and requires specific ports to be open for node communication, storage operations, and telemetry. These vary slightly between Kubernetes and OpenShift environments.

### East-to-West (Internal Communication Ports)​

KubernetesOpenShiftDescription

900117001Portworx management port [REST]

900217002Portworx node-to-node port [gossip]/UDP
Required to open when using external KVDB

900317003Portworx storage data port

900417004Portworx namespace [RPC]

901217009Portworx node-to-node communication port [gRPC]

901317010Portworx namespace driver [gRPC]

901417011Portworx diags server port [gRPC]

901817015Portworx KVDB peer-to-peer port [gRPC]

901917016Portworx KVDB client service [gRPC]

902017017Portworx gRPC SDK server [REST]

902117018Portworx gRPC SDK gateway [REST]

902217019Portworx health monitor [REST]

902417021Telemetry log uploader (Portworx version 2.13.7 and earlier) [gRPC]

902917021Telemetry log uploader (Portworx version 2.13.8 and later) [gRPC]

900617024Portworx node liveness service [TCP]
Required when Kube Datastore (KDS) dynamic pools are enabled.

1200120001Telemetry metrics collector [gRPC]

1200220002Telemetry phone home [HTTP]

23792379External KVDB (etcd) port [gRPC]
Open only if you run an external etcd cluster

### Outbound​

TypeTCP Port(s)ScopeDestination host(s)Description

Install / Upgrade443PX install & version updatesinstall.portworx.com,
 mirrors.portworx.comRetrieves install spec, helper scripts, and downloads PX kernel modules.

License activation443PAYG licensingrest.zuora.comUsage reporting & license retrieval.
Not applicable for air-gapped deployments.

443PAYG licensingflex1327.compliance.flexnetoperations.comFor licensing to work.
Not applicable for air-gapped deployments.

Telemetry443Cluster registration & metricspxessentials.portworx.com,
 register.cloud-support.purestorage.com,
 rest.cloud-support.purestorage.comRegisters cluster and uploads usage metrics.

443 / 80Event log uploadslogs-01.loggly.comSends PX log events to Portworx Support.

Snapshots / Backups443CloudSnaps, backups, restoresYour S3 or S3-compatible endpointPersists snapshots & object data.

## Supported Kubernetes versions​

For information on the Kubernetes versions supported by Portworx, see Supported Kubernetes Versions.

## What to do next​

Install Portworx in your environment. For more information, see Installing Portworx Enterprise.

In this topic:
