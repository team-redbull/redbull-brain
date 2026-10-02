# Set up a witness node

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/witness-node-setup (Portworx Enterprise latest)

Set up a witness node | Portworx Enterprise Documentation

In a Portworx cluster, quorum refers to the minimum number of active storage nodes necessary to maintain cluster operation. If at least half of the nodes are offline, the cluster loses quorum, causing all operations to stop, and Portworx does not process any IOs.

In a Synchronous DR setup, a single Portworx cluster spans two Kubernetes or OpenShift clusters, each within a Metro Area Network. The same quorum principles apply here, with all storage nodes from both source and destination data centers contributing to quorum. Portworx quorum can be lost in the event of a disaster.

To solve the quorum issue, you can deploy a witness site that is used as the quorum tie-breaker when there is a network partition or when a data center goes offline. The witness node is a single virtual machine and a special Portworx storageless node that participates in quorum but does not store any data. Typically situated in a third data center, the witness node ensures quorum integrity.

## Prerequisites​

-
Portworx Enterprise DR license is activated.

-
The witness node needs to be a storageless node.

-
Docker engine is installed.

-
The witness node must also meet the following CPU and memory requirements based on the datastore that you install on it:

DatastoreCPURAM

PX-StoreV14 cores minimum, 8 cores recommended4 GB minimum, 8 GB recommended

PX-StoreV24 cores minimum*8 GB minimum

note

* PX-StoreV2 storage nodes require a minimum of 8 CPU cores. Because a witness node does not store application data, the `witness-install.sh` script sets the `small_conf=1` runtime option for PX-StoreV2 installations to reduce the minimum CPU requirement to 4 cores.

The witness node uses PX-StoreV2 by default unless you select PX-StoreV1 during installation.

## Set up a witness node​

Perform the following to set up a witness node:

-
Check your Portworx Enterprise version by running the following command on your source and destination clusters (both should have the same version):

- Kubernetes

- OpenShift

```

kubectl get pods -A -o jsonpath="{.items[*].spec.containers[*].image}" | xargs -n1 | sort -u | grep oci-monitor | cut -d ":" -f2

```

```

oc get pods -A -o jsonpath="{.items[*].spec.containers[*].image}" | xargs -n1 | sort -u | grep oci-monitor | cut -d ":" -f2

```

-
Download the witness-install.sh script file on a designated VM.

-
Find the `cluster-name` by running the following command from a Portworx pod.

```

pxctl status | grep "Cluster ID"

```

-
Create the required directories on the designated VM:

```

sudo mkdir -p /opt/pwx /etc/pwx

```

-
Install Portworx as a storageless witness node on the designated VM.

important

- Before running the script, identify the datastore version used by the source and destination Portworx clusters. The witness node must use the same datastore version on both clusters. Specify `--store-version=px-storev1` for PX-StoreV1 clusters or `--store-version=px-storev2` for PX-StoreV2 clusters. If you omit the `--store-version` flag, the script uses PX-StoreV2.

- Specify the Portworx Enterprise version from step 1, the external `etcd` endpoints, and the cluster name from step 3.

- A PX-StoreV1 witness node requires the `btrfs` kernel module on the designated VM. If the module is not available, such as in an air-gapped environment, use PX-StoreV2.

-
To install the witness node with PX-StoreV2, run the following command:

```

bash witness-install.sh --cluster-id="<cluster-name>" \

  --etcd="etcd:http://<your-etcd-endpoint1>:2379,etcd:http://<your-etcd-endpoint2>:2379,etcd:http://<your-etcd-endpoint3>:2379" \

  --docker-image=portworx/px-enterprise:"<your-px-version>"

```

-
To install the witness node with PX-StoreV1, specify `--store-version=px-storev1`:

```

bash witness-install.sh --cluster-id="<cluster-name>" \

  --etcd="etcd:http://<your-etcd-endpoint1>:2379,etcd:http://<your-etcd-endpoint2>:2379,etcd:http://<your-etcd-endpoint3>:2379" \

  --docker-image=portworx/px-enterprise:"<your-px-version>" \

  --store-version=px-storev1

```

-
Verify Portworx status on the witness node:

```

pxctl status

```

The `witness-install.sh` script can take a couple of minutes to complete, as shown in the following example output:

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 30 days)

..

....

```

You will see `PX is operational`, and once the script is successfully completed, you can quit the script by entering `ctrl + c`. Note that the witness node requires a valid Portworx license. To check the status of your license, use the `pxctl license list` command.

## Related topics​

-
To upgrade the witness node, see Upgrade the Portworx OCI bundle.

-
To uninstall the witness node, see Uninstall the Portworx OCI bundle.

In this topic:
