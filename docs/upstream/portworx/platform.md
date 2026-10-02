# Install and Run Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/platform (Portworx Enterprise 3.6)

Install and Run Portworx Enterprise | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise allows you to build apps anywhere and run them at production scale with high availability, reliability, and security.

Listed below are the different workflows that you need to complete to have Portworx Enterprise up and running on your infrastructure and make storage available for your applications.

Get Started with Portworx Enterprise

-
Plan your Portworx Deployment based on your requirement: Choose the right architecture for your Portworx deployment, either the disaggregated model or the converged model. Determine the KVDB type, the storage backend format, and any other parameters that will influence your Portworx Enterprise set up in your environment.

-
Ensure that Systems Requirements are met: Ensure that your environment meets the requirements for deploying Portworx Enterprise like supported Kubernetes versions, CPU, memory, storage, and networking prerequisites. For additional information, refer to the platform-specific documentation.

-
Install Portworx Enterprise on your storage infrastructure: Prepare and deploy Portworx Enterprise by generating the installation spec from Portworx Central or using Helm. Based on the environment in which you are deploying Portworx, follow the installation instructions to ensure storage is ready for your applications.

-
Set Up Portworx Licenses: Portworx offers multiple license types to suit different deployment environments like Portworx Enterprise VM, designed for enterprise-grade storage in virtual machine environments, both on-premises and in the cloud or Portworx.

-
Secure your Portworx Setup: Enable encryption, configure role-based access control (RBAC), and enforce fine-grained access policies using JWT for API and volume security with Portworx Enterprise on your cluster.

-
Provision Storage for Application: Create and manage persistent storage for Kubernetes applications with Portworx Enterprise. Define storage classes, volumes, and ensure data locality for controlling application performance and resilience.

-
Upgrade Portworx Enterprise: When new versions of Portworx Enterprise are available, it is necessary to upgrade to stay current with supported versions and maintain cluster stability. Upgrade instructions vary for different environments like air-gapped clusters or for different methods like blue-green upgrades.

-
(Optional) Uninstall Portworx Enterprise: In case required to uninstall Portworx Enterprise from your Kubernetes environment. This would help to clean up associated resources to ensure cluster health and avoid orphaned volumes or configurations.
