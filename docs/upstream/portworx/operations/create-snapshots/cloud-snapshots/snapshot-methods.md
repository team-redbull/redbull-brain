# Storing and Comparing Cloud Snapshots

Source: https://docs.portworx.com/portworx-enterprise/operations/create-snapshots/cloud-snapshots/snapshot-methods (Portworx Enterprise 3.6)

Storing and Comparing Cloud Snapshots | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx features two methods for storing and comparing cloudsnaps before they're uploaded:

- Extent-based snapshots

- Local snapshots

In both modes, Portworx uses extents to perform the diff. For Local snapshots, Portworx keeps the snapshot locally (which implicitly also keeps the extents locally). For Extent-based snapshots, Portworx uploads the extent information for the snapshot and then deletes the local snapshot.

By default, Portworx chooses the most efficient snapshot method automatically in an effort to minimize the amount of data retained on local storage for incremental cloud snapshots. Although, you can override the defaults if you have specific configuration needs.

### Extent-based snapshots​

Under the extent-based mode, Portworx compares block metadata, called extents, to determine the difference between the local snapshot and the previously uploaded cloud snapshot.

Portworx uses this metadata to calculate the difference between snapshots for upload and does not need to store previous snapshots for comparison. As Portworx reduces the footprint of the locally stored cloud snapshot data significantly. However, Portworx must also upload this metadata to the cloud alongside the cloudsnap data, resulting in slightly larger uploads.

When taking extent-based snapshots, Portworx does the following:

- Takes a snapshot

- Downloads extent data for the previous snapshot from the cloud

- Compares extents, looking for changed blocks or generations

- Uploads the changes and new snapshot metadata

- Deletes the local snapshot

note

Portworx defaults to extent-based snapshots.

### Local snapshots​

Under the local snapshot operation mode, Portworx takes a full snapshot of a volume and then uploads only the incremental difference between the local snapshot and the previously uploaded cloud snapshot.

Portworx calculates this difference by comparing the current local snapshot with the previously taken local snapshot before uploading only the changed blocks to the cloud. While this minimizes the amount of data transmitted to the cloud storage provider, Portworx must store the latest snapshot locally so that it can compare it the future snapshot. These locally held snapshots can take up a lot of extra space, filling storage pools unnecessarily.

When taking local snapshots, Portworx does the following:

- Takes a snapshot

- Compares it with a previously saved snapshot

- Uploads the changes

- deletes the old snapshot and keeps the latest for future comparison

## Configure snapshot modes​

Portworx contains an optional toggle that allows you to change how cloud-snaps are stored and compared before they’re uploaded.

### Configure limits​

If the default limits don't work for you, you can configure Portworx to switch between snapshot modes based on criteria you define. Do this by configuring the following cluster options:

- `cloudsnap-metadata-upload-mb-bytes-limit`: if metadata size is over this limit, Portworx will not upload the extent-based metadata and will use the local snapshot operation mode.

- `cloudsnap-metadata-upload-percent-limit`: If the metadata is larger than this defined percent limit when compared to the data to upload, Portworx will not upload extent-based metadata and will use the local snapshot operation mode.

Enter the `pxctl cluster options update` command to change the threshold values. The following example sets the upload limits:

```

pxctl cluster options update --cloudsnap-metadata-upload-mb-bytes-limit 40

```

### Disable extent-based snapshots​

You can disable extent-based snapshots entirely by entering the following `pxctl` command:

```

pxctl cluster options update --cloudsnap-using-metadata-enabled off

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

Successfully updated cluster-wide options

```

In this topic:
