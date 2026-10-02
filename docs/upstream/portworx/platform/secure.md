# Securing your Portworx Setup

Source: https://docs.portworx.com/portworx-enterprise/platform/secure (Portworx Enterprise 3.6)

Securing your Portworx Setup | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

To help secure your Portworx Kubernetes cluster setup, consider the following approaches:

-
Enable PX-Security - Enable PX-Security to enforce role-based access control (RBAC) for authentication, authorization, and ownership. For more information, see Configure PX-Security on your Cluster.

-
After you enable PX-Security and the cluster is running, a cluster administrator must configure a `pxctl context` on each node to interact with the system. For more information, see Use pxctl with security enabled.

-
To restrict access to specific volumes, enable authorization on PVCs. For more information, see Enable authorization in Portworx.

-
Set up a secret store and enable volume encryption - To secure Portworx volumes and use features like cloud snapshots, you must configure a secret store provider. The secret store is needed for managing the passphrases that Portworx uses for the encryption keys required for encrypting and decrypting volume data at rest and in transit. For more information on how to encrypt volumes, see Set Up Key Management and Encrypt Portworx Volumes.

-
Configure multiple secret providers - You can configure multiple secret providers in a single Portworx deployment and assign a different secret store provider to each feature. For example, use Kubernetes Secrets for volume encryption and Vault for storing cloud provider credentials such as vSphere or FlashArray access tokens. For more information, see Configure multiple secrets providers.

-
Encrypt Cloud Drives - You can configure your Portworx storage clusters to use cloud provider specific encryption for the underlying storage (cloud drives). This ensures that data is encrypted at the storage layer using keys managed by your cloud provider (like Google Cloud KMS or Oracle disk encryption). For more information, see Encrypt Cloud Drives.

-
Enable TLS certificate verification for vCenter - On vSphere, Portworx connects to the vCenter API to provision and manage cloud drives. You can configure Portworx to verify the vCenter certificate when establishing this connection. If vCenter uses a certificate signed by a private certificate authority (CA), provide the CA certificate to Portworx. For more information, see Enable TLS Certificate Verification for vCenter.

-
Enable SSL certificate verification for Everpure arrays - Portworx communicates with FlashArray and FlashBlade through their REST management APIs. By default, Portworx encrypts this traffic but does not verify the certificates presented by the management endpoints. Enable SSL certificate verification to have Portworx validate the identity of each endpoint before sending API requests. For more information, see Enable SSL Certificate Verification for FlashArray and FlashBlade.
