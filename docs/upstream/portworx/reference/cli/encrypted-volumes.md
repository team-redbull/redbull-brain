# Encrypted volumes using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/encrypted-volumes (Portworx Enterprise 3.6)

Encrypted volumes using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Encrypted Volumes​

This guide will give you an overview of how to use the encryption feature for Portworx volumes. Under the hood, Portworx uses the `libgcrypt` library to interface with the `dm-crypt` module for creating, accessing and managing encrypted devices. Portworx uses the `LUKS` format of `dm-crypt` and `AES-256` as the cipher with `xts-plain64` as the cipher mode.

All encrypted volumes are protected by a passphrase. Portworx uses this passphrase to encrypt the volume data at rest as well as in transit. It is recommended to store these passphrases in a secure secret store.

There are two ways in which you can provide the passphrase to Portworx:

-
Per volume secret: Use a unique secret for each encrypted volume

-
Cluster-wide secret: Use a default common secret for all encrypted volumes

note

Portworx does not allows creating encrypted volumes with a 512-byte block size. Instead, it automatically adjusts the block size to 4096 bytes.

To know more about the supported secret providers and how to configure them with Portworx, refer to the Setup Secrets Provider page.

## Creating and using encrypted volumes​

### Using a cluster-wide secret key​

A cluster-wide secret key is basically a key-value pair where the value part is the secret that Portworx uses as a passphrase to encrypt all your volumes.

note

Make sure the cluster-wide secret key is set when you are setting up Portworx with one of the supported secret endpoints.

Let's look at an example where we want to create and mount an encrypted volume that uses a cluster-wide secret key:

The first step is to create a new volume. Let's make it encrypted with the `--secure` flag:

```

/opt/pwx/bin/pxctl volume create --secure --size 10 encrypted_volume

```

```

Volume successfully created: 822124500500459627

```

Just to make sure our new encrypted volume was created, try running the following command:

```

pxctl volume list

```

```

ID	      	     		NAME		SIZE	HA SHARED	ENCRYPTED	IO_PRIORITY	SCALE	STATUS

822124500500459627	 encrypted_volume	10 GiB	1    no yes		LOW		1	up - detached

```

Next, you can attach the volume:

```

pxctl host attach encrypted_volume

```

```

Volume successfully attached at: /dev/mapper/pxd-enc822124500500459627

```

We're almost done. Let's mount the volume by running the following command:

```

pxctl host mount encrypted_volume /mnt

```

```

Volume encrypted_volume successfully mounted at /mnt

```

So, if a cluster-wide secret key is set, Portworx will use it as the default key for encryption. In the next section, you will learn how to specify per volume keys.

### Using per volume secret keys​

As mentioned, you can encrypt volumes using unique keys instead of the cluster-wide secret key. However, you are required to specify the key every time you create or attach a new volume.

Let's look at a simple example. First, we'll run `pxctl volume create` with the `--secret_key` flag like this:

```

pxctl volume create --secure --secret_key key1 enc_vol

```

```

Volume successfully created: 374663852714325215

```

Next, mount the `enc_vol` volume into the `mnt` directory as follows:

```

docker run --rm -it -v secret_key=key1,name=enc_vol:/mnt

```

You can get the same result by typing:

```

docker run --rm -it --mount src=secret_key=key1,name=enc_vol,dst=/mnt

```

note

Before running the above commands, make sure the secret `key1` exists in the secret endpoint.

## Encrypted Sharedv4 Volumes​

With Portworx, you can create encrypted sharedv4 volumes that can be accessed from multiple nodes.

The `--sharedv4` flag is used to indicate that we would want to share an encrypted volume:

```

pxctl volume create --sharedv4 --secure --size 10 encrypted_volume

```

```

Encrypted Shared volume successfully created: 77957787758406722

```

Try inspecting our new volume:

```

pxctl volume inspect encrypted_volume

```

```

Volume	:  77957787758406722

Name            	 :  encrypted_volume

Size            	 :  10 GiB

Format          	 :  ext4

HA              	 :  1

IO Priority     	 :  LOW

Creation time   	 :  Nov 1 17:22:59 UTC 2018

Shared          	 :  yes

Status          	 :  up

State           	 :  detached

Attributes      	 :  encrypted

Reads           	 :  0

Reads MS        	 :  0

Bytes Read      	 :  0

Writes          	 :  0

Writes MS       	 :  0

Bytes Written   	 :  0

IOs in progress 	 :  0

Bytes used      	 :  131 MiB

Replica sets on nodes:

	Set 0

		Node 		 : X.X.X.11 (Pool 0)

Replication Status	 :  Detached

```

You can enable or disable sharing during runtime by passing the `--sharedv4 on/off` flag.

Note that volumes must be detached to toggle the `sharedv4` flag during run-time.

The Portworx cluster must be authenticated to access the secret store for the encryption keys.

## Related topics​

- For information about encrypting your Portworx volumes using Kubernetes secrets, refer to the Using Kubernetes Secrets with Portworx section.

In this topic:
