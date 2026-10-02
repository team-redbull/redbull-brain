# Planning your Portworx Deployment

Source: https://docs.portworx.com/portworx-enterprise/platform/deployment-approach (Portworx Enterprise 3.6)

Planning your Portworx Deployment | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Before installing Portworx Enterprise, it’s important to evaluate your environment and make key architecture decisions based on your requirements The following aspects will influence how you deploy and manage your Portworx installation:

-
Type of Platform Support – Kubernetes, OpenShift and Provider Distributions: Portworx Enterprise integrates with majority of CNCF-certified Kubernetes distributions, including upstream Kubernetes and Red Hat OpenShift. It also supports the managed offerings from major cloud providers—Amazon EKS, Google Kubernetes Engine (GKE), Oracle Cloud Kubernetes (OKE), IBM Cloud Kubernetes Service, and others—so you can go for provider-specific optimizations and networking integrations. Furthermore, Portworx Enterprise runs on on-premises bare-metal clusters, giving you the flexibility to choose the any of the supported platform from bare metal to managed offerings.

-
Type of Installation Environment – Air-gapped or Non-air-gapped: Depending on your security and compliance requirements, Portworx Enterprise can be deployed in a fully air-gapped cluster (no external internet access) or in a standard connected environment. In air-gapped mode, you’ll need to mirror all container images and Helm charts into a private registry and pre-stage any CRDs or operator bundles. This ensures all binaries and dependencies reside within your secured perimeter. In non-air-gapped mode, Portworx Enterprise automatically pulls the necessary images and updates from public registries when external connectivity is allowed, without requiring any additional steps as part of the installation process.

-
Type of deployment - Disaggregated or Converged: By default, Portworx Enterprise is installed as a converged configuration, where compute and storage coexist on the same nodes. If you need a disaggregated setup, where compute and storage are on separate node groups, you must designate your nodes as storage and storageless (for compute) before installation. During deployment, you are required to add necessary labels to make sure Portworx identifies the disaggregated setup. These labels you can find in the environment specific installation steps.

-
Type of storage management - PX-StoreV1 or PX-StoreV2: Portworx offers two types of storage volume management solution - PX-StoreV1 that operates as a full filesystem, suitable for general-purpose storage needs, and PX-StoreV2 that focuses on high-performance volume management with optimized metadata handling and performance tracking while also enabling PX-Fast, a feature that provides an accelerated I/O path for volumes.
 By default, Portworx uses PX-StoreV2 as the datastore for all deployments on supported platforms.

-
Type of Disaster Recovery (DR): Portworx offers two DR options across clusters. Synchronous DR ensures zero recovery point objectives (RPO) with real-time replication but requires a shared external KVDB and a stretched cluster. Asynchronous DR uses scheduled snapshots, supports independent clusters, can tolerate higher latencies. Choose based on your recovery objectives (RTO & RPO), network setup, and operational needs.

## Reference architectures​

Reference architectures for Portworx Enterprise in the different environments are available to help you plan your deployment. These architectures provide guidance on how to set up Portworx in various scenarios, including:

- Portworx on Red Hat OpenShift with VMware vSphere

- Portworx on Google Distributed Cloud Anthos with VMware vSphere

- Portworx on Rancher Kubernetes Engine 2 with VMware

- Portworx on OCP Bare Metal OpenShift Virtualization Addendum

- Portworx on OCP Bare Metal

## What to do next​

### System Requirements

Learn about the system requirements for deploying Portworx Enterprise.

### Installing Portworx Enterprise

Learn how to install Portworx Enterprise on your infrastructure.

In this topic:
