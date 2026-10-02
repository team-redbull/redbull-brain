# Manage storage nodes on GCP

Source: https://docs.portworx.com/portworx-enterprise/reference-architectures/auto-disk-provisioning/gcp (Portworx Enterprise 3.6)

Manage storage nodes on GCP | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

note

If you are running on GKE, visit Portworx on GKE.

## Key-value store in Portworx​

Portworx uses a key-value database (KVDB) to store the cluster's state, configuration data, and metadata associated with storage volumes and snapshots. You can configure either an external or an internal KVDB. For more information, see KVDB for Portworx topic.

### Firewall settings for Portworx​

Ensure ports 9001-9022 are open between the nodes that will run Portworx. Your nodes should also be able to reach the port KVDB is running on (for example etcd usually runs on port 2379).

## Disk template​

Portworx takes in a disk spec which gets used to provision GCP persistent disks dynamically.

A GCP disk template defines the Google persistent disk properties that Portworx will use as a reference. There are 2 ways you can provide this template to Portworx.

1. Using a template specification

The spec follows the following format:

```

"type=<GCP disk type>,size=<size of disk>"

```

- type: Following two types are supported

- pd-standard

- pd-ssd

- size: This is the size of the disk in GB

See GCP disk for more details on above parameters.

Examples:

- `"type=pd-ssd,size=200"`

- `"type=pd-standard,size=200", "type=pd-ssd,size=100"`

2. Using existing GCP disks as templates

You can also reference an existing GCP disk as a template. On every node where Portworx is brought up as a storage node, a new GCP disk(s) identical to the template will be created.

For example, if you created a template GCP disk called px-disk-template-1, you can pass this in to Portworx as a parameter as a storage device.

Ensure that these disks are created in the same zone as the GCP node group.

In this topic:
