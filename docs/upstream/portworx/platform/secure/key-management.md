# Set Up Key Management and Encrypt Portworx Volumes

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management (Portworx Enterprise latest)

Set Up Key Management and Encrypt Portworx Volumes | Portworx Enterprise Documentation

This topic provides an overview of how to configure a secret store in Portworx Enterprise and to encrypt volumes using secrets.
Under the hood, Portworx uses the `libgcrypt` library to interface with the `dm-crypt` module for creating, accessing and managing encrypted devices. Portworx uses the `LUKS` format of `dm-crypt` and `AES-256` as the cipher with `xts-plain64` as the cipher mode.

note

Encryption is not supported for Portworx raw block devices.

All encrypted volumes are protected by a passphrase. Portworx uses this passphrase to encrypt the volume data at rest as well as in transit. It is recommended to store these passphrases in a secure secret store. There are two ways in which you can provide the passphrase to Portworx:

- Per volume secret: Use a unique secret for each encrypted volume

- Cluster-wide secret: Use a default common secret for all encrypted volumes

Depending on your choice of secret provider, follow the instructions to first configure a secret store with Portworx Enterprise to store your passphrases, and then encrypt the PVCs by using the secrets and passphrases.

Secret ProviderStep 1: Set Up a Secret StoreStep 2: Encrypt Volumes Using Secrets

AWS KMSSet up AWS KMS

- Encrypt Kubernetes PVCs with AWS KMS

- Encrypt Portworx Volumes using AWS KMS

Azure Key VaultSet up Azure Key VaultEncrypting volumes using named secrets is not supported with Azure Key Vault. To encrypt volumes, follow the steps in Encrypting Kubernetes PVCs with Google Cloud KMS.

Google Cloud KMSSet up Google Cloud KMS

- Encrypt Kubernetes PVCs with Google Cloud KMS

- Encrypt Portworx volumes using Google Cloud KMS

IBM key management servicesSet Up IBM key management services

- Encrypt Kubernetes PVCs with IBM key management services

- Encrypt Portworx Volumes using IBM Key Protect

Kubernetes SecretsSet up Kubernetes Secrets

- Encrypt PVCs using annotations with Kubernetes Secrets

- Encrypt PVCs using CSI and Kubernetes

- Encrypt PVCs using StorageClass with Kubernetes Secrets

VaultSet up Vault

- Encrypt Kubernetes PVCs with Vault

- Encrypt Portworx Volumes using Vault

Vault TransitSet Up Vault Transit

- Encrypt Kubernetes PVCs with Vault Transit

- Encrypt Portworx Volumes using Vault Transit
