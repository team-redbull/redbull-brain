# FlashBlade and FlashArray env vars

Source: https://docs.portworx.com/portworx-enterprise/reference/pure-reference/spec-env-vars (Portworx Enterprise latest)

FlashBlade and FlashArray env vars | Portworx Enterprise Documentation

This section provides configuration details for setting FlashArray and FlashBlade environment variables in the `StorageCluster` object. All fields are objects under the `spec.env[]` list:

```

spec:

  env:

  - name: PURE_FLASHARRAY_SAN_TYPE

    value: "ISCSI"

  - name: PURE_DEFAULT_ENABLE_FB_NFS_SNAPSHOT

    value: "true"

```

NameValueTypeDefault

`PURE_FLASHARRAY_SAN_TYPE`Specifies the SAN transport protocol that Portworx CSI uses to communicate with FlashArray. Supported values are `ISCSI`, `NVMEOF-TCP`, `NVMEOF-RDMA`, and `FC`.`string``"ISCSI"`

`PURE_DEFAULT_ENABLE_FB_NFS_SNAPSHOT`Determines whether the .snapshot directory is enabled on FlashBlade filesystems or not.`enumerated string`: `true` or `false``"true"`

`PURE_ISCSI_LOGIN_TIMEOUT`Login timeout in seconds`string``"20"`

`PURE_ISCSI_ALLOWED_CIDRS`Use this in cases where the FlashArray has additional network interfaces not on your own subnet. Use commas as the separator, e.g. 10.0.0.0/24,10.1.0.0/16. An empty string means all enabled iSCSI interfaces will be connected to.`string``""` (empty string)
