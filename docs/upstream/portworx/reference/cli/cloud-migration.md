# Cloud migrations using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/cloud-migration (Portworx Enterprise latest)

Cloud migrations using pxctl | Portworx Enterprise Documentation

This document explains how to migrate Portworx volumes between clusters. In order to do this, we'll first have to pair up 2 clusters and then issue the migration command to Portworx.

note

The pairing is uni-directional. Say there are two clusters- C1 and C2. If you pair C1 with C2 you can only migrate volumes from C1 to C2.

With Portworx, there are two ways of migrating volumes between clusters:

- using `pxctl` or

- using `Stork` on `Kubernetes`

## Prerequisites​

### Configuring a secret store​

Before we begin, make sure you have configured a secret store on both clusters. This will be used to store the credentials for the objectstore.

## Pairing clusters​

The installation may take a while, depending on your Internet connection. Once the installation is finished we're going to want to pair our clusters.

First, let's get the cluster token of the destination cluster. Run the following command from one of the Portworx nodes in the destination cluster:

```

pxctl cluster token show

```

```

Token is 0795a0bcd46c9a04dc24e15e7886f2f957bfee4146442774cb16ec582a502fdc6aebd5c30e95ff40a6c00e4e8d30e31d4dbd16b6c9b93dfd56774274ee8798cd

```

Next, let's jump to the source cluster and create the cluster pair:

```

pxctl cluster pair create --ip <ip_of_source_destination_cluster_node> --token <token_from_2c>

```

Just to make sure our pairing was created, try running the following command on the second cluster:

```

pxctl cluster pair list

```

```

ClusterID                                               Name        IP              Port           CredID

xxxxxxxx-xxxx-xxxx-xxxx-10cbe9576427 (default)          mycluster   192.168.56.75   9001           xxxxxxxx-xxxx-xxxx-xxxx-c86a2554d71e

```

You can pair multiple clusters with each other. The first pair created will be listed as the default one.

You can delete a cluster pair by running the following command:

```

pxctl cluster pair delete --id <cluster_id>

```

## Migrating volumes​

Now that we've paired our clusters, the next step is to migrate our volume(s) between them by running `pxctl cloudmigrate`.

Run the `pxctl cloudmigrate` command with the `--help` flag to list the available subcommands and flags.

### Migrating volume​

To migrate a particular volume, try using:

```

pxctl cloudmigrate start --volume_id <volumeId> --cluster_id <cluster_id>

```

### Checking the migration status​

While Portworx migrates your volume(s), you can check the status by running the following command:

```

pxctl cloudmigrate status

```

```

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-10cbe9576427

VolumeId            VolumeName                                  Stage   Status      LastUpdate                          LastSuccess

1028723504085545761 pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 05 Sep 2018 03:04:10 UTC       Wed, 05 Sep 2018 03:04:10 UTC

1147613441858984344 pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 22 Aug 2018 23:56:19 UTC       Wed, 22 Aug 2018 23:56:19 UTC

228731158998208592  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 22 Aug 2018 21:18:44 UTC       Wed, 22 Aug 2018 21:18:44 UTC

280749584627774298  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 22 Aug 2018 21:18:44 UTC       Wed, 22 Aug 2018 21:18:44 UTC

580746088570435304  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 19 Sep 2018 03:21:38 UTC       Wed, 19 Sep 2018 03:21:38 UTC

775806166668776083  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 22 Aug 2018 23:56:19 UTC       Wed, 22 Aug 2018 23:56:19 UTC

873404678173271727  pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Restore Failed      Fri, 14 Sep 2018 19:18:07 UTC       InvalidTime

91307080409549411   pvc-xxxxxxxx-xxxx-xxxx-xxxx-0214683e8447    Done    Complete    Wed, 22 Aug 2018 21:18:44 UTC       Wed, 22 Aug 2018 21:18:44 UTC

```

The stages of a particular migration will progress from Backup→ Restore→ Done. If any stage fails the status will be marked as Failed.

If the migration is successful, you should see the volume(s) with the same name created on the destination cluster.

## Related topics​

For information about migrating Portworx volumes between clusters using Stork and Kubernetes, refer to the Migration page.

In this topic:
