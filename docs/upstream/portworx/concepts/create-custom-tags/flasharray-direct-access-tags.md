# Create Custom tags for FlashArray Direct Access

Source: https://docs.portworx.com/portworx-enterprise/concepts/create-custom-tags/flasharray-direct-access-tags (Portworx Enterprise latest)

Create Custom tags for FlashArray Direct Access | Portworx Enterprise Documentation

Portworx Enterprise enables users to tag volumes, clones, and snapshots stored on FlashArray Direct Access backend storage. Custom disk tags for a FADA can be:

- Added while creating Direct Access Volume

- Modified after Volume Provisioning

## Adding custom disk tags while creating Direct Access Volume​

You can specify custom tags as a `pure_backend_tags: <key1>:<value1>;<namespace>:<key2>:<value2>` pair using a parameter. The namespace is optional and is any user defined namespace. These are not Kubernetes namespace. If no namespace is provided while adding tags, Portworx uses the `default` namespace.

Here are some conditions for creating a custom tag:

- The `pure_backend_tags` parameter is mandatory.

- You can also specify only the key without a value.

- You cannot specify a custom tag without a key.

- A value cannot use `:` in the `value` text.

- Tag with a namespace is assigned the mentioned namespace.

- Tag without namespace is assigned the `default` namespace.

Based on your volume, select one of the following to create a custom disk tag for that volume.

- New Volume

- Cloned Volume

- Snapshot

### New Volume​

While creating direct access volumes, specify the custom tags in the `StorageClass` device spec for a new volume as:

```

pure_backend_tags: <namespace1>:<key1>:<value1>;<key2>:<value2>

```

This will create the volume with custom tags with the given key:value pair. For namespace1, the custom tag will be `<key1>:<value1>`. Custom tag `<key2>:<value2>` will go for the `default` namespace since no namespace was provided while adding custom tag.

### Cloned Volume​

Tags for volume clones will use the tags defined in the Storage Class of the clone. If the `pure_backend_tags` parameter is missing, the clone will have no tags. If the `pure_backend_tags` parameter is explicitly set to an empty string, the clone will have no tags. Otherwise, it will use the overwritten tags from the cloned Storage Class which can be defined as:

```

pure_backend_tags: <key1>:<value1>;<namespace>:<key2>:<value2>

```

You can also use `pxctl` to add a custom tag to a cloned volume:

```

pxctl volume clone --label pure_backend_tags="key1:value1;ns2:key2:value2" --name cloneName volName

```

This will update the custom tags for the cloned volume with the given `key:value` pair.

### Snapshot​

Specify the custom tags in `VolumeSnapshotClass` spec as:

```

pure_backend_tags: <key1>:<value1>;<key2>:<value2>

```

This will update the custom tags for a snapshot with the given key:value pair.

### Modifying custom disk tags after volume provision​

Custom tags for FlashArray Direct Access can be added or deleted after volume provisioning using `pxctl`.

-
Add a custom tag with the following command:

```

pxctl volume update --add_pure_tags "ns1:key1:val1;ns2:key2;key3:val3;key4:" volName

```

Any existing tag will be overwritten by the new ones with this command. The namespace is optional and is any user defined namespace. These are not Kubernetes namespace. If no namespace is provided while adding tags, Portworx uses the `default` namespace. In this example, custom tag for a FADA volume will be updated as mentioned below:

- For ns1 namespace, tag will `key1:val1`

- For ns2 namespace, tag will be `key2`

- For default namespace, tag will be `key3:val3` and `key4`g

-
Specify the tags that you want to delete with the following command:

```

pxctl volume update --del_pure_tags "ns1:key1;key2:" volName

```

In this example, custom tag for a FADA volume will be deleted as mentioned below:

- For ns1 namespace, tag `key1` will be deleted.

- For default namespace, tag `key2` will be deleted.

Deleting a key would mean the deletion of key:value pair.

## View the added custom tags​

Run the following command to view all the custom tags assigned to a FADA:

```

pxctl volume inspect volName

```

In this topic:
