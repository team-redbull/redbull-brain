# Oracle disk encryption

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/encrypt-cloud-drives/oracle-disk-encryption (Portworx Enterprise latest)

Oracle disk encryption | Portworx Enterprise Documentation

The Oracle Block Volume service is a cloud-based storage service provided by Oracle Cloud Infrastructure (OCI) that enables you to create and manage block volumes, which are high-performance, persistent storage devices that can be attached to an instance in OCI.

Using the Oracle disk encryption feature, you can pass your own managed keys to Portworx, which will encrypt your cloud drives using those keys. The Oracle Block Volume service allows encrypting block volumes at rest (not active or being accessed by a compute instance), using the Advanced Encryption Standard (AES) algorithm with 256-bit encryption. To achieve this, you should:

- Create a custom encryption key.

- Use the key to encrypt disks.

## Create a custom encryption key​

To create a custom disk encryption key stored in the Vault service:

-
Follow this procedure to create Oracle Vault service.

-
Create a master encryption key using symmetric Advanced Encryption Standard (AES) algorithm with 256-bit encryption. Oracle Block Volume service only allows the AES algorithm for encrypting block devices. For more information, see Securing Block Volume.

-
Create an IAM policy so that the Oracle Block Volume service can access the master encryption key stored in the Vault service. For more information, see Common Policies. For example, create an IAM policy with the following policy statement, replacing the `target.key.id` value with the OCID of your master encryption key.

```

Allow service blockstorage, oke to use keys in compartment dev where target.key.id = 'ocid1.key.oc1.iad.b5r5xcpzaaazi.***'

```

## Associate the encryption key with your StorageCluster​

After creating the disk encryption key, perform the following procedure during Portworx installation:

-
Create the `ociapikey` Kubernetes secret in the namespace, which you want to install Portworx:

```

kubectl create secret generic ociapikey \

--namespace kube-system \

--from-file=oci_api_key.pem=oci_api_key.pem \

--from-literal=PX_ORACLE_user_ocid="***" \

--from-literal=PX_ORACLE_fingerprint="***”

```

-
Specify the encryption key in the StorageCluster device spec:

```

cloudStorage:

    deviceSpecs:

    - type=pv-10,size=150,kms=<ocid-of-encr-key>

```

-
(Optional) Verify if the disks are encrypted with your managed keys:

```

pxctl cloudrive list

```

The (`cmk`) label in the output confirms that the specified disk is encrypted:

```

px-do-not-delete-xxxxxxxx-xxxx-xxxx-xxxx-29330f3de598(data)(cmk)

```

note

If you provide an incorrect `kms` encryption key, Portworx installation will fail.

In this topic:
