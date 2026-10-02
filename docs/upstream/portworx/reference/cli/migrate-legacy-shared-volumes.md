# Migrate legacy volumes to sharedv4 service volumes

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/migrate-legacy-shared-volumes (Portworx Enterprise latest)

Migrate legacy volumes to sharedv4 service volumes | Portworx Enterprise Documentation

Before adopting NFS to support `ReadWriteMany` volumes, Portworx utilized a `shared=true` approach to create shared volumes, which functioned even without NFS installed.

As these volumes are considered legacy, Portworx by Everpure advises converting them to `sharedv4` service volumes. This ensures a standardized method to achieve RWX mode and avoids issues when Portworx is restarted on a node (for example, during an upgrade). Additionally, an application container using legacy shared volumes also needs to be restarted, which may encounter compatibility issues with newer versions.

caution

This operation is disruptive. Applications using legacy shared volumes will experience downtime, and new attachments to these volumes will be blocked until the migration is complete. Portworx by Everpure recommends scheduling a maintenance window for this migration.

### Migrate the Legacy Shared Volumes​

After scheduling the maintenance window, proceed with the following steps:

- Install the NFS service on Portworx nodes and open the required ports.

- Execute the command below to enable `MigrateLegacySharedToSharedv4Service`:

```

pxctl cluster options update --migrate-legacy-shared-to-sharedv4-service=true

```

Once all the pods that were using the volume have been terminated, the last detachment of the volume, will update the KVDB. This update changes the volume fields from `shared=true` to `Shared-V4-Service: True`. After this update, new attachments will use the SharedV4-Service (NFS mount) method rather than the legacy method for mounting the volume.

In this topic:
