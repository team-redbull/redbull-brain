# KVDB for Portworx

Source: https://docs.portworx.com/portworx-enterprise/concepts/kvdb-for-portworx (Portworx Enterprise 3.6)

KVDB for Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx uses a key-value database (KVDB) to store the cluster state, configuration data, and metadata associated with storage volumes and snapshots.

For most deployments, Portworx by Everpure recommends using the built-in internal KVDB, which Portworx installs and manages automatically.

However, you must use an external KVDB in the following scenarios:

- When you are configuring a synchronous DR setup.

- When your Portworx cluster includes a combination of Kubernetes and non-Kubernetes nodes.

Choose one of the following topics based on the KVDB type you plan to use when installing Portworx Enterprise:

- Internal KVDB

- External KVDB
