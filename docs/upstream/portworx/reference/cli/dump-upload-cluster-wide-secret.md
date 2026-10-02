# Dump and Upload cluster-wide secrets

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/dump-upload-cluster-wide-secret (Portworx Enterprise latest)

Dump and Upload cluster-wide secrets | Portworx Enterprise Documentation

Portworx provides the capability to encrypt volumes using cluster-wide secrets. A cluster-wide secret is a unique secret for a cluster that can be used as a default key for encrypting your volumes. However, this poses a problem while migrating such volumes across clusters. The destination cluster needs to have the same cluster-wide secret in order to use the migrated encrypted volume.

The following set of commands will help you dump the cluster-wide secret from one cluster and upload the same secret to a different cluster. Once the cluster-wide secret is uploaded to the destination cluster, encrypted volumes using the cluster-wide secret can be migrated to the destination cluster.

### Dumping cluster-wide secret​

Run the following command to dump the cluster-wide secret:

```

pxctl secrets  dump-cluster-wide-secret

```

```

Following are the details about the cluster-wide secret for this cluster:

Secret ID (--secret_id): demo_secret_id

Secret value (--secret_value): XXXX

Run the following command on the destination cluster:

 /opt/pwx/bin/pxctl secrets upload-cluster-wide-secret --secret_id demo_secret_id --secret_value XXXX

```

The `dump` command also spits out the corresponding upload command that needs to be executed on the destination cluster.

### Upload cluster-wide secret​

The `dump-cluster-wide-secret` command outputs an `upload-cluster-wide-secret` command. Use this command on the destination cluster to upload the cluster-wide secret:

```

pxctl secrets upload-cluster-wide-secret --secret_id demo_secret_id --secret_value XXXX

```

```

Successfully uploaded cluster-wide secret.

```

note

The cluster-wide secret dump and upload utility is only supported for AWS KMS secret store.

In this topic:
