# Performance Tuning

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/tuning (Portworx Enterprise 3.6)

Performance Tuning | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx has best practices for both global container level optimization, as well as volume granular optimization.

## Global performance tuning​

Portworx by Everpure recommends you use a journal device to absorb Portworx metadata writes. Journal writes are small with frequent syncs and therefore only SSD/NVME should be configured as a journal device.

The journal device should be 3GB. Using a larger device will not help, since Portworx will only use these amounts of storage. You can specify the journal device using the `-j` option during installation.

note

- You must ensure that the journal device is at least as fast as the fastest storage device on the node allocated for Portworx. If the journal device is slower than the actual storage drive, your overall performance will decrease to match the lower of the two devices.

- Cloud providers match the drive's performance based on its size. So if you select a small sized journal device, your performance will be worse. For a cloud drive, provide a partition from the larger storage drive as your journal device.

- Portworx by Everpure recommends using the `-j auto` option. This allows Portworx to create its own journal partition on the best drive.

## Tune volume performance with pxctl​

Portworx optimizes performance for specific application access patterns using IO profiles. You can set these IO profiles by providing the `io_profile` option while creating the volume. For example:

```

pxctl volume create --size=10 --repl=3 --io_profile=db_remote demovolume

```

or

```

docker volume create -d pxd io_priority=high,size=10G,repl=3,io_profile=db_remote,name=demovolume

```

### Change the default IO profile using pxctl​

You can change the default IO profile for volumes created without the `io_profile` annotation using the cluster option `--default-io-profile`. For example, using the following command will assign the `none` IO profile to any volumes created within the cluster that do not have the `io_profile` StorageClass annotation:

```

pxctl cluster options update --default-io-profile none

```

## Related topics​

- IO profiles

- Performance optimization options in the IO path

In this topic:
