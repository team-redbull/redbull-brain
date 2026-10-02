# Encrypt Portworx Volumes using Vault Transit

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/vault-transit/vol-enc (Portworx Enterprise 3.6)

Encrypt Portworx Volumes using Vault Transit | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can use one of the following methods to encrypt Portworx volumes with Vault Transit, depending on how you provide the secret password to Portworx:

- Encrypt volumes using per volume secrets

- Encrypt volumes using a cluster-wide secret

## Encrypt volumes using per volume secrets​

-
Create an encrypted volume by entering the `pxctl volume create` command with the following parameters:

- `--secure`

```

pxctl volume create --secure enc_vol

```

```

Encrypted volume successfully created: 374663852714325215

```

With Portworx, you can create two types of encrypted volumes:

- Encrypted Volumes. You can access a regular volume from a single node.

- Shared Encrypted Volumes. You can access an encrypted sharedv4 volume from multiple nodes.

To create a shared encrypted volume, you must specify the `--sharedv4` parameter as follows:

```

pxctl volume create --sharedv4 --secure enc_shared_vol

```

```

Encrypted Shared volume successfully created: 77957787758406722

```

If you are using Vault Namespaces, and your secret key `key1` resides in a namespace called `ns1` then use the following command to create an encrypted volume:

```

pxctl volume create --secure --secret_options=vault-namespace=ns1 enc_vol

```

```

Encrypted volume successfully created: 374663852714325215

```

-
You can use the `pxctl volume list` command to list your volumes:

```

pxctl volume list

```

```

ID                      NAME        SIZE    HA SHARED   ENCRYPTED   IO_PRIORITY SCALE   STATUS

822124500500459627   enc_volume   10 GiB  1    no yes     LOW     1   up - detached

```

## Encrypt volumes using a cluster-wide secret​

A cluster wide secret key is a common key that can be used to encrypt all your volumes. This common key needs to be pre-created in Vault. Portworx will use this cluster-wide secret as a passphrase to encrypt your volume.

- Set the cluster-wide secret key. Run the following command specifying the `--secret` parameter with the secret name you created in Vault (this example uses `mysecret`):

```

pxctl secrets set-cluster-key --secret mysecret

```

```

Successfully set cluster secret key!

```

caution

You must set the cluster-wide secret only once. If you overwrite the cluster-wide secret, the volumes encrypted with the old secret will become unusable.

If you are using Vault Namespaces use the following command to set the cluster-wide secret key in a specific vault namespace (this example uses `ns1` as the vault namespace)

```

pxctl secrets set-cluster-key --secret_options=vault-namespace=ns1 --secret mysecret

```

- Create a new encrypted volume. Enter the `pxctl volume create` command, specifying the following arguments:

-
`--secure`

-
`--secret_key default` the default key used for cluster-wide secret

-
The size of your encrypted volume (this example use `10` GiB)

-
The name of the encrypted volume (this example uses `enc_vol`)

```

pxctl volume create --secure --secret_key default --size 10 enc_vol

```

```

Volume successfully created: 822124500500459627

```

With Portworx, you can create two types of encrypted volumes:

- Encrypted Volumes. You can access a regular volume from a single node.

- Shared Encrypted Volumes. You can access an encrypted sharedv4 volume from multiple nodes.

To create a shared encrypted volume, you must specify the `--sharedv4` parameter as follows:

```

pxctl volume create --sharedv4 --secure --secret_key default --size 10 enc_vol

```

```

Encrypted Shared volume successfully created: 77957787758406722

```

-
You can use the `pxctl volume list` command to list your volumes:

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

In this topic:
