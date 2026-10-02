# Encrypt Portworx volumes using Google Cloud KMS

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/gcloud-kms/vol-enc (Portworx Enterprise latest)

Encrypt Portworx volumes using Google Cloud KMS | Portworx Enterprise Documentation

You can use one of the following methods to encrypt Portworx volumes with Google Cloud KMS, depending on how you provide the secret password to Portworx:

- Encrypt volumes using per volume secrets

- Encrypt volumes using named secrets

- Encrypt volumes using a cluster-wide secret

## Encrypt volumes using per volume secrets​

Use per-volume secrets to encrypt each volume with a unique encryption key. With this approach, every volume uses its own passphrase, improving security isolation between volumes.

Run the `pxctl volume create` command with the `--secure` flag to create an encrypted volume:

```

pxctl volume create --secure  enc_vol

```

This example creates an encrypted volume named `enc_vol`.

## Encrypt volumes using a cluster-wide secret​

Set the default cluster-wide secret, and specify the secret name as `default`. Portworx will use the cluster-wide secret as a passphrase to encrypt your volume.

-
Set the cluster-wide secret key.
Enter the following `pxctl secrets set-cluster-key` command, specifying the `--secret` parameter with your secret passphrase (this example uses `mysecretpassphrase`):

```

pxctl secrets set-cluster-key --secret mysecretpassphrase

```

```

Successfully set cluster secret key!

```

caution

You must set the cluster-wide secret only once. If you overwrite the cluster-wide secret, the volumes encrypted with the old secret will become unusable.

If you have specified your cluster-wide secret key in the `config.json` file, the `pxctl secrets set-cluster-key` command will overwrite it. Even if you restart your cluster, Portworx will use the key you passed as an argument to the `pxctl secrets set-cluster-key` command.

-
Create a new encrypted volume.
Enter the `pxctl volume create` command, specifying the following arguments:

- `--secure`

- `--secret-key` with the `default` value

- The name of the encrypted volume (this example uses `enc_vol`)

```

pxctl volume create --secure --secret_key default enc_vol

```

-
List your volumes using the `pxctl volume list` command:

```

pxctl volume list

```

```

ID                      NAME        SIZE    HA SHARED   ENCRYPTED   IO_PRIORITY SCALE   STATUS

822124500500459627   enc_vol   10 GiB  1    no yes     LOW     1   up - detached

```

-
Attach your volume by entering the `pxctl host attach` command with the following arguments:

- The name of your encrypted volume (this example uses `enc_vol`)

- The `--secret-key` flag with the `default` value

```

pxctl host attach enc_vol --secret_key default

```

```

Volume successfully attached at: /dev/mapper/pxd-enc822124500500459627

```

-
Mount the volume by entering the `pxctl host mount` command with the following parameters:

- The name of your encrypted volume (this example uses `enc_vol`)

- The mount point (this example uses `mnt`)

```

pxctl host mount enc_vol /mnt

```

```

Volume enc_vol successfully mounted at /mnt

```

If you want to migrate encrypted volumes created through this method between two different Portworx clusters, then you must:

- Create a secret with the same name. You can use the `--secret-id` flag to specify the name of your secret, as shown in step 1.

- Make sure you provide the same passphrase while generating the secret.

## Encrypt volumes using named secrets​

Use a named secret to specify the secret Portworx uses to encrypt and decrypt your volumes.

-
List your named secrets by running the following command:

```

pxctl secrets gcloud list-secrets

```

-
Generate a new secret and associate it with a unique name.
Enter the following `pxctl secrets gcloud create-secret` command specifying the following:

- The `--secret_id` flag with the name of your secret, which must be unique (this example uses `my-unique-secret`):

- The `--passphrase` flag with your secret passphrase (this example uses `mysecretpassphrase`)

```

pxctl secrets gcloud create-secret --secret_id my-unique-secret --passphrase mysecretpassphrase

```

Note that Portworx uses Google Cloud KMS to encrypt your passphrase, and stores it in its internal metadata store. To encrypt and decrypt volumes using this passphrase, you must specify the secret ID when you create or attach volumes.

-
Create a new encrypted volume.
Enter the `pxctl volume create` command, specifying the following arguments:

- `--secure`

- `--secret-key` with the name of your named secret (this example uses `my-unique-secret`)

- the name of the encrypted volume (this example uses `enc_vol`)

```

pxctl volume create --secure --secret_key my-unique-secret enc_vol

```

-
List your volumes using the `pxctl volume list` command:

```

pxctl volume list

```

```

ID                      NAME        SIZE    HA SHARED   ENCRYPTED   IO_PRIORITY SCALE   STATUS

822124500500459627   enc_volume   10 GiB  1    no yes     LOW     1   up - detached

```

-
Attach your volume by entering the `pxctl host attach` command with the following arguments:

- The name of your encrypted volume (this example uses `enc_vol`)

- The `--secret-key` flag with the `default` value

```

pxctl host attach enc_vol --secret_key default

```

```

Volume successfully attached at: /dev/mapper/pxd-enc822124500500459627

```

-
Mount the volume by entering the `pxctl host mount` command with the following parameters:

- The name of your encrypted volume (this example uses `enc_vol`)

- The mount point (this example uses `mnt`)

```

pxctl host mount enc_vol /mnt

```

```

Volume enc_vol successfully mounted at /mnt

```

If you want to migrate encrypted volumes created through this method between two different Portworx clusters, then you must:

- Create a secret with the same name. You can use the `--secret-id` flag to specify the name of your secret, as shown in step 1.

- Make sure you provide the same passphrase while generating the secret.

In this topic:
