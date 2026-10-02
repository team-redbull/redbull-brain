# Run-flat mode

Source: https://docs.portworx.com/portworx-enterprise/concepts/run-flat (Portworx Enterprise latest)

Run-flat mode | Portworx Enterprise Documentation

Portworx requires a key-value database such as etcd for configuring storage. A highly available clustered etcd with persistent storage is preferred. You can setup an external etcd and configure Portworx to use it, or you can let Portworx spin up its own key-value database by using the internal KVDB.

An always available key-value database is essential to keep Portworx running smoothly. However, if the external etcd or internal KVDB nodes go offline, Portworx goes into run-flat mode.

In run-flat mode, all the existing volumes which are attached and in use by applications will continue to be online, but no new volume creations, attachments, detachments, or deletions will be honored. Existing volumes don't see an I/O interruption as long as all the replicas of the volume are online. This has the following implications for external and internal KVDB:

-
External KVDB: As long as all the Portworx nodes continue to stay up, all the volume replicas stay online and there is no I/O interruption. However, if any node has been down or goes down, volumes with a replica on the downed nodes will see an I/O interruption.

-
Internal KVDB: If the KVDB is down, it almost certainly implies that at least 2 Portworx nodes are down. Any volumes with a replica on the downed nodes will see an I/O interruption.
