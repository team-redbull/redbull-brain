# Multi Data Center Deployment Architectures for HA and DR

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/deployment-arch/dr-and-multi-site (Portworx Enterprise 3.6)

Multi Data Center Deployment Architectures for HA and DR | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx offers multiple options for Disaster Recovery (DR) and multi-data center High Availability (HA) beyond what is provided with the single data center/multiple AZ deployment options. For more on why you cannot simply use your traditional DR system for Kubernetes applications, see the Limits of traditional DR for Kubernetes applications section.

- Option 1- Synchronous DR over a MAN using multiple Kubernetes clusters with a single Portworx stretch cluster

- Option 2- Asynchronous DR over a WAN using multiple Kubernetes clusters with multiple Portworx clusters

- Option 3- Multi-site data center stretch cluster for HA

## Option 1- Synchronous DR over a MAN using multiple Kubernetes clusters with a single Portworx stretch cluster​

Solves for these primary needs:

- Container- or Namespace-granular DR.

- RPO zero data protection and low RTO in the case of losing an entire data center.

- Data and Kubernetes objects are replicated across both sites, simplifying and speeding up application failover

Key constraints:

- Requires two data centers.

- Round trip latency between data centers must be < 10 ms. This can usually be accomplished using different cloud providers in the same geographical region, colocating an on-premises data center in the same region as a cloud provider or operating a campus or metropolitan area network.

## Option 2- Asynchronous DR over a WAN using multiple Kubernetes clusters with multiple Portworx clusters​

Solves for these primary needs:

- Container- or Namespace-granular Disaster Recovery.

- RPO levels are as low as 15 minutes and RTO under one minute in the case of losing an entire data center.

- Data and Kubernetes objects are replicated across both sites, simplifying and speeding up application failover

Key constraints:

-
Requires two data centers.

-
S3-compatible object store is available to move data.

### Summary of Synchronous vs. Asynchronous PX-DR Options​

Application and infrastructure requirementsSynchronous PX-DRAsynchronous PX-DR

Number of Portworx clusters12

Needs an S3-compatible object store to move dataNoYes

Max round trip latency between data centers10 msNo limit

Data guaranteed to be available at both sites (zero RPO)YesNo

Kubernetes objects replicated between data centersYesYes

Low RTOYesYes

## Option 3- Multi-site data center stretch cluster for HA​

Solves for these primary needs:

- High availability of data services across multiple data centers.

- Zero RPO data protection.

Key constraints:

- Requires three data centers.

- Max round trip latency between data centers of under 10 ms.

In this topic:
