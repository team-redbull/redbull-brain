# GCP cloud drive encryption with customer managed encryption keys

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/encrypt-cloud-drives/gcp (Portworx Enterprise 3.6)

GCP cloud drive encryption with customer managed encryption keys | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page describes how to encrypt Google Cloud Platform (GCP) cloud drives with customer managed keys using Google Key Management Service (KMS).

## Create a disk encryption key​

### Create a KMS key ring​

- Navigate to Key Management in the Google Cloud console.

- Click Create Key Ring.

- Provide a Key Ring name, choose your region, and click Create.

note

Choose either the same region as your cluster or the Multi-region global region. Keys from different regions should not be used for disk encryption.

### Create a symmetric key​

-
Click the Key Ring that you created in the previous section.

-
Click Create key.

-
Provide a key name, choose Symmetric encrypt/decrypt for Purpose, select an automatic rotation policy, and click Create.

-
To get the name of the resource that you need to provide for disk encryption, click the Actions menumore_vert for your key, then click Copy resource name.

The key is in the following format:

```

projects/<projectName>/locations/<region>/keyRings/<keyRing>/cryptoKeys/<keyName>

```

caution

Google KMS lets you set an automatic key rotation policy for your KMS key, and it creates a new key version at each scheduled rotation. Do not disable or delete old key versions after key rotation is complete.

If you mark a key for deletion, the key version stays scheduled for destruction for a default period of 24 hours or a configured duration, after which it is automatically destroyed. Any data encrypted with this key version is not recoverable.

## Enable a KMS account for disk encryption​

A service account is required for performing encryption operations with Google KMS.

This service account must have the Cloud KMS CryptoKey Encrypter/Decrypter (`roles/cloudkms.cryptoKeyEncrypterDecrypter`) role. You can either make a separate service account that is responsible for disk encryption and decryption operations, or you can add the role to the default service account managing Portworx.

### Use a separate KMS service account​

#### Create and configure a KMS service account​

- Navigate to the Service Accounts page of the Google Cloud console.

- Click Create service account.

- Under Service account details, provide an ID for your service account, then click Create and continue.

- Under Grant this service account access to project, in the Select a role menu, select the Cloud KMS CryptoKey Encrypter/Decrypter role, then click Continue.

- Under Grant users access to this service account, in the Service account users role field, enter the default service account that you use to manage Portworx, then click Done.

note

A KMS service account that has been used to encrypt a disk must be enabled for the life cycle of that disk. If a KMS service account is deactivated or deleted, any data that was encrypted with that particular KMS service account cannot be retrieved.

#### Modify your StorageCluster spec​

In your StorageCluster spec, specify your KMS key in front of every cloud drive as follows:

```

cloudStorage:

    deviceSpecs:

    - type=pd-standard,size=150,kms=<kms-key>,kmsAccount=<kmsServiceAccount>

```

Where:

-
`<kms-key>` is the key resource name in the following format:

```

projects/<projectName>/locations/<region>/keyRings/<keyRing>/cryptoKeys/<keyName>

```

-
`<kmsServiceAccount>` is the name of the new service account that you created, in the following format:

```

<serviceAccountName>@<project>.iam.gserviceaccount.com

```

### Use the default Portworx service account​

-
Navigate to the IAM page of the Google Cloud console.

-
Under View by principals, select the default service account that you use to manage Portworx.

-
Click Edit principals edit.

-
Under Assign roles, click Add a role or Add another role and choose the Cloud KMS CryptoKey Encrypter/Decrypter role, then click Save.

-
In your StorageCluster spec, specify your KMS key in front of every cloud drive as follows:

```

cloudStorage:

    deviceSpecs:

    - type=pd-standard,size=150,kms=<kms-key>

```

Where `<kms-key>` is the resource name in the following format:

```

projects/<projectName>/locations/<region>/keyRings/<keyRing>/cryptoKeys/<keyName>

```

## Verify your drive encryption​

There are two ways to check the encryption for your cloud drives.

### From pxctl​

Execute the following command:

```

pxctl clouddrive list

```

```

px-cloud-drive-xxxxxxxx-xxxx-xxxx-xxxx-29330f3de598(data)(cmk)

```

Disks which are encrypted with customer managed keys include `(cmk)`, as in the above output.

### From the Google Cloud console​

-
Navigate to the Compute Engine page of the Google Cloud console.

-
Click the name of any of the nodes in your cluster that should have attached disks that are encrypted with CMEK.

Under Additional disks, in the Encryption column, disks which are encrypted with customer managed keys show as Customer-managed.

In this topic:
