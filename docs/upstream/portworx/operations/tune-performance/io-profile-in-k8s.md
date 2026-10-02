# Configure IO profiles for Portworx volumes

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance/io-profile-in-k8s (Portworx Enterprise latest)

Configure IO profiles for Portworx volumes | Portworx Enterprise Documentation

Portworx volumes on your cluster can use different IO profiles to optimize the Portworx volumes' performance for specific use-cases. For information about what IO profiles are, as well as the different profiles available, see the IO profiles concept section.

note

By default, Portworx uses an `auto` IO profile, which automatically applies an IO profile that is most appropriate for the data patterns it sees.

## Manually configure IO profiles​

You can direct a group of volumes to use a specific IO profile by defining it at the storageClass level and referencing that storageClass in your PVCs:

-
Create and configure a storageClass as desired. Add the `parameters.io_profile` field with the IO profile you want to specify:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-io-profile

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  io_profile: "db_remote"

allowVolumeExpansion: true

```

-
In your PVCs, reference the storageClass you just created to apply your IO profile to volumes:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: px-db-remote-pvc

  annotations:

    volume.beta.kubernetes.io/storage-class: portworx-io-profile

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 10Gi

```

## Configure IO profile using pxctl​

Portworx optimizes performance for specific application access patterns using IO profiles. You can set these IO profiles by using one of the following options:

### Option 1: Change the default IO profile for the cluster​

Change the default IO profile for the cluster without changing the `io_profile` annotation using the cluster option `--default-io-profile`. The same profile will be inherited by all the volumes by default if they do not have `io_profile` StorageClass annotation.

For example, using the following command will assign the `none` IO profile to any volumes created within the cluster that do not have the `io_profile` StorageClass annotation:

```

pxctl cluster options update --default-io-profile none

```

Verify the profile set using the following command:

```

pxctl cluster options list | grep -i profile

```

```

Default IO Profile                                      : none

```

### Option 2: Set IO profile of new volume​

Set `io_profile` option while creating the volume. Check the command usage and available options.

```

pxctl volume create --help | grep profile

```

```

--io_profile string  IO Profile (Valid Values: [db_remote auto none journal auto_journal use_cluster_default]) (default "use_cluster_default")

```

note

The `auto_journal` value is deprecated. Use `journal` instead.

For example, using the following command will assign the `journal` io_profile to the `demovolume` volume.

```

pxctl volume create --size=10 --repl=3 --io_profile=journal demovolume

```

### Option 3: Change IO profile of existing volume​

Change the IO profile of an existing volume using the following command. Check the command usage and available options.

```

pxctl volume update --help | grep profile

```

```

--io_profile string  IO Profile (Valid Values: [db_remote auto none journal auto_journal use_cluster_default]) (default "use_cluster_default")

```

note

The `auto_journal` value is deprecated. Use `journal` instead.

## Related topics​

- Performance optimization options in the IO path

In this topic:
