# Create Custom tags for Cloud Drives

Source: https://docs.portworx.com/portworx-enterprise/concepts/create-custom-tags/cloud-drive-tags (Portworx Enterprise 3.6)

Create Custom tags for Cloud Drives | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Custom tags to cloud drives can be added during:

- Portworx Installation

- Storage Pool Expansion

note

- Custom tags are supported for cloud-drives provisioned on AWS, Azure, GCP, Oracle cloud platforms and FlashArray.

- vSphere, FlashBlade, and IBM platforms do not support cloud-drive tags.

- For FlashArray cloud drive (FACD), custom tags can not be created after storage provisioning.

You can specify custom tags as a `key:value` pair. To specify more than one `key:value` pairs, use a `;` separator. For example, `tags=tenant:fin;bu:finance;env:prod`.

Here are some conditions for creating a custom tag:

- A custom tag can also be a `key:` without a `value`.

- A custom tag can not exist without a `key`.

- A `value` cannot use `:` since it is used as a separator with key.

## Add custom disk tags while installing Portworx​

While installing Portworx, specify the custom tags in the `StorageCluster` device spec:

```

cloudStorage:

    deviceSpecs:

    -type=<device-type>,size=<volume-size>,tags=<custom-tags>

```

For example:

```

tags=tenant:fin;bu:finance;env:prod

```

Run the following command to view all the custom tags assigned to a cloud-drive:

```

pxctl clouddrive inspect --node <node-id>

```

In the output, locate the `Labels` field:

```

Drive Set Configuration

    Number of drives in the Drive Set:  1

    NodeID:  <node-id>

    NodeIndex:  3

    InstanceID:  <instance-id>

    Zone:  us-central1-a

    State:  In Use

    Labels:  -

Drive  0

    ID:  <drive-id>

    Type:  <URL>

    Size:  150 Gi

    Iops:  0

    Path:  <drive-location>

    Used for:  data

    Labels:  apps=px,bu=eng

```

note

The `Labels` field displays custom tags that you specify in the `pxctl sv drive add -s "type=<custom-tags>"` command. For example, `pxctl sv drive add -s "type=apps=px,bu=eng"`

## Add custom tags during pool expansion​

You can also add custom tags when expanding the storage pool, using the following command:

```

pxctl sv drive add -s

```

For example:

```

pxctl sv drive add -s "type=pd-ssd,size=150,tags=apps:px;bu:eng"

```

Run the `pxctl sv pool show` command to display the added drive and its configuration. Then, run the `pxctl clouddrive inspect --node <drive-UUID>` to view the specified custom tags. Example output for the above commands:

```

pxctl sv drive add -s "type=pd-ssd,size=150,tags=apps:px;bu:eng"

Drive add done

pxctl sv pool show

PX drive configuration:

Pool ID: 0

    Type:  Default

    UUID:  <UUID>

    IO Priority:  MEDIUM

    Labels:

    Size: 147 GiB

    Status: Online

    Has metadata:  Yes

    Balanced:  Yes

    Drives:

    1: <drive1-location>, Total size 147 GiB, Online

    Cache Drives:

    No Cache drives found in this pool

Journal Device:

    1: <drive1-location>, STORAGE_MEDIUM_SSD

pxctl clouddrive inspect --node <node-id>

Drive Set Configuration

    Number of drives in the Drive Set:  1

    NodeID:  <node-id>

    NodeIndex:  3

    InstanceID:  <instance-id>

    Zone:  us-central1-a

    State:  In Use

    Labels:  -

Drive  0

    ID:  <drive-id>

    Type:  <URL>

    Size:  150 Gi

    Iops:  0

    Path: <drive0-location>

    Used for:  data

    Labels:  apps=px,bu=eng

```

note

During pool expansion, following is the behavior of custom tags:

- `resize-drive` option: the disk will continue to include existing custom disk tags.

- `add-drive` option: the new disk will inherit common custom tags from existing disks of the storage pool. This option can be used only if you are not using PX-StoreV2 as your backend.

Each individual data disk, `kvdb` disk, metadata disk, journal disk can have their own set of custom tags. Any node failures and subsequent node restarts does not have an impact on the custom tags.

## Unsupported custom disk tag formats:​

You cannot specify the following keys, Portworx reserves them for internal use.

- `name`

- `pwx_cluster_id`

- `pxtype`

- `portworx.io/flasharray-name`

- `portworx.io/flasharray-id`

- `portworx.io/flasharray-management-endpoint`

- `sc`

In this topic:
