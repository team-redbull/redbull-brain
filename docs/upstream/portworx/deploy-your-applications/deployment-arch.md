# Deployment Architectures for Kubernetes-Based Stateful Applications

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/deployment-arch (Portworx Enterprise latest)

Deployment Architectures for Kubernetes-Based Stateful Applications | Portworx Enterprise Documentation

Organizations leveraging Portworx have discovered how simple, reliable and secure it is to run Kubernetes-based stateful applications in production. Underneath this simplicity, however, there is a great degree of flexibility in how Portworx can be deployed. These deployment options, or architectures, vary along two primary dimensions:

- The degree to which they address application requirements around performance, elasticity, disaster recovery, and high availability

- Their ability to operate under different infrastructure constraints such as the number of data centers and network latency.

Portworx provides simple, reliable and secure ways to run Kubernetes-based stateful applications. Depending on the key requirements of the application, either of the following Portworx deployment architectures should be considered:

- Single on-premise data center or a public cloud across multiple availability zones: If your infrastructure is in an on-premise data center or is spread across multiple availability zone in a public cloud, Portworx can be deployed with either a dedicated Portworx storage cluster that is separate from the Portworx compute cluster, or in hyperconverged setup where storage and compute nodes are in the same Portworx cluster. For more information about which option is suitable based on application requirement, see Single data center Portworx deployment architecture.

- Multiple data center: For infrastructures spanning multiple data centers, Portworx offers deployment architectures that enable both high availability and granular disaster recovery. These architectures allow recovery at the container or namespace level in the event of failures. You can either deploy Portworx with synchronous disaster recovery and a single Portworx cluster across multiple data center or deploy Portworx with asynchronous disaster recovery with multiple Portworx clusters. If your infrastructure is spread across more than two data centers, you can deploy multi-site data center stretch Portworx cluster for high availability. For more information, see Multi data center deployment architecture.

note

Some of these deployment architectures are designed to be used together to solve multiple needs at once. You can pick one of the single data center Portworx deployment options and one of the disaster recovery (DR) and multi-site high availability (HA) architectures based on your requirements. For example, organizations can use the "synchronous Portworx DR" architecture along with the "hyperconverged" architecture to achieve DR for high-performance applications.
