# Encrypt Portworx Volumes using AWS KMS

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/aws-kms/vol-enc (Portworx Enterprise 3.6)

Encrypt Portworx Volumes using AWS KMS | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can use one of the following methods to encrypt Portworx volumes with AWS Key Management Service (KMS), depending on how you provide the secret password to Portworx:

- Encrypt volumes using per volume secrets

- Encrypt volumes using named secrets

- Encrypt volumes using a cluster-wide secret

## Encrypt volumes using per volume secrets​

Use per-volume secrets to encrypt each volume with a unique encryption key. With this approach, every volume uses its own passphrase, improving security isolation between volumes.
Portworx uses AWS KMS APIs to generate the data encryption key.

Run the `pxctl volume create` command with the `--secure` flag to create an encrypted volume:

```

pxctl volume create --secure  enc_vol

```

This example creates an encrypted volume named `enc_vol`.

## Encrypt volumes using named secrets​

You can use a named secret to specify the secret Portworx uses to encrypt and decrypt your volumes.

note

You cannot use named secrets to create a cloud backup of an encrypted volume or to migrate encrypted volumes between two different Portworx clusters.

To encrypt a volume using a named secret, follow these steps:

-
List your named secrets:

```

pxctl secrets aws list-secrets

```

-
Generate a new AWS KMS data key and associate it with a unique name:

```

pxctl secrets aws generate-kms-data-key --secret_id <name of the data key>

```

-
Create a new encrypted volume by specifying the following arguments:

- `--secure`

- `--secret-key` with the name of your named secret (this example uses `my-unique-secret`)

- The name of the encrypted volume (this example uses `enc_vol`)

```

pxctl volume create --secure --secret_key my-unique-secret enc_vol

```

-
Attach your volume by running the command with the following arguments:

- The name of your encrypted volume (this example uses `enc_vol`)

- The `--secret-key` flag with the `default` value

```

pxctl host attach enc_vol --secret_key default

```

```

Volume successfully attached at: /dev/mapper/pxd-enc822124500500459627

```

-
Mount the volume by running the command with the following parameters:

- The name of your encrypted volume (this example uses `enc_vol`)

- The mount point (this example uses `mnt`)

```

pxctl host mount enc_vol /mnt

```

```

Volume enc_vol successfully mounted at /mnt

```

## Encrypt volumes using a cluster-wide secret​

Set the default cluster-wide secret, and use it to encrypt your volumes.

Starting with version 2.1, cluster-wide secrets have been deprecated. However, any volume encrypted with a cluster-wide secret can still be used in newer versions of Portworx.

To create new encrypted volumes using your existing cluster-wide secret, follow these steps:

-
Generate a new AWS KMS data key and associate it with a unique name. Enter the following `pxctl secrets aws generate-kms-data-key` command, specifying the `--secret_id` flag with the name of the data key, which must be unique (this example uses `my-unique-secret`):

```

pxctl secrets aws generate-kms-data-key --secret_id my-unique-secret

```

-
Enter the `pxctl secrets set-cluster-key` command, specifying the name of your new KMS data key (this example uses `my-unique-secret`):

```

pxctl secrets set-cluster-key my-unique-secret

```

-
Create a new volume by following the steps in the Encrypt volumes using named secrets section.

note

You can not use a cluster-wide secret to create a cloud backup of an encrypted volume or to migrate encrypted volumes between two different Portworx clusters.

In this topic:
