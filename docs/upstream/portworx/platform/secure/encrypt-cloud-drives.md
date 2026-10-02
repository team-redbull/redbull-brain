# Encrypt Cloud Drives

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/encrypt-cloud-drives (Portworx Enterprise 3.6)

Encrypt Cloud Drives | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This section provides instructions on how to encrypt cloud drives in Portworx. While Portworx provides volume-level encryption, you may also want to encrypt the underlying cloud storage media using your cloud provider's key management services.

Disk encryption configurations can vary based on the cloud provider you are using. The following cloud providers are supported for encrypting cloud drives in Portworx:

- Google Cloud: Encrypt cloud drives using Customer-Managed Encryption Keys (CMEK) with Google Key Management Service (KMS).

- Oracle Cloud Infrastructure: Encrypt Oracle Block Volumes using custom encryption keys managed in the OCI Vault.

## 📄️GCP cloud drive encryption with CMEK

Learn how to encrypt GCP cloud drives with customer managed keys.

## 📄️Oracle disk encryption

Learn how to encrypt Oracle disks by passing your own managed keys.
