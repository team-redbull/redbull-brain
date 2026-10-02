# Troubleshooting tips for common problem areas

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/get-support (Portworx Enterprise 3.6)

Troubleshooting tips for common problem areas | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Troubleshoot problems​

The following sections provide troubleshooting tips for common problem areas:

### Portworx Node is down​

- Kubernetes

- Openshift

-
`ssh` into your cluster node that has `kubectl` installed with your `kubeconfig` and check the Kubernetes cluster status using `kubectl` to ensure cluster nodes are in the `Ready` status:

```

kubectl get node -o wide

```

-
If a node is not ready, describe that node to see why and take corrective action:

```

kubectl describe node <nodename>

```

-
If the previous command does not help identify the problem, log in as root and consider running the `journalctl` command on the node in question to identify the problem:

```

journalctl -u kubelet

```

-
If the Kubernetes cluster is healthy, check Portworx alerts using `pxctl` from the node, either through `ssh` or using `kubectl exec`. Alerts may help you understand why the Portworx node is down:

```

pxctl alerts show

```

-
You can also enter the `pxctl status` command to check the status on the respective node where portworx is running:

```

pxctl status

```

-
If you find no useful information in the `pxctl status` output, check your Portworx pods to confirm they are up and running:

```

kubectl get pods -n <px-namespace> -l name=portworx

```

-
If necessary, describe the respective Portworx pod to identify the problem:

```

kubectl describe pods <px-podname> -n <px-namespace>

```

-
If necessary, check the `journalctl` logs from the node in question to further help identify the problem:

```

journalctl -lfu portworx*

```

-
Check all Portworx pods running in `<px-namespace>` and confirm they are up and running:

```

kubectl get pods -n <px-namespace>

```

-
Describe the respective pod running in `<px-namespace>` to identify the problem.

```

kubectl describe pod <podname> -n <px-namespace>

```

-
`ssh` into your cluster node that has `oc` installed with your `kubeconfig` and check your cluster status using `oc` to ensure cluster nodes are in the `Ready` status:

```

oc get node -o wide

```

-
If a node is not ready, describe that node to see why and take corrective action:

```

oc describe node <nodename>

```

-
If the previous command does not help identify the problem, log in as root and consider running the `journalctl` command on the node in question to identify the problem:

```

journalctl -u kubelet

```

-
If your cluster is healthy, check Portworx alerts using `pxctl` from the node, either through `ssh` or using `oc exec`. Alerts may help you understand why the Portworx node is down:

```

pxctl alerts show

```

-
You can also enter the `pxctl status` command to check the status on the respective node where portworx is running:

```

pxctl status

```

-
If you find no useful information in the `pxctl status` output, check your Portworx pods to confirm they are up and running:

```

oc get pods -n <px-namespace> -l name=portworx

```

-
If necessary, describe the respective Portworx pod to identify the problem:

```

oc describe pods <px-podname> -n <px-namespace>

```

-
If necessary, check the `journalctl` logs from the node in question to further help identify the problem:

```

journalctl -lfu portworx*

```

-
Check all Portworx pods running in `<px-namespace>` and confirm they are up and running:

```

oc get pods -n <px-namespace>

```

-
Describe the respective pod running in `<px-namespace>` to identify the problem.

```

oc describe pod <podname> -n <px-namespace>

```

### Portworx logs reports "Node is not in quorum", kvdb error: "context deadline exceeded"​

- Kubernetes

- Openshift

- `ssh` into the respective nodes and run `pxctl status` on each node to check the Portworx cluster status:

```

pxctl status

```

- If running internal KVDB check KVDB cluster members and confirm the health status using pxctl:

```

pxctl service kvdb members

```

- If quorum has been lost perform the following before contacting technical support:

- Save px-diags on each affected node (captures all logs)

```

pxctl service diags -a

```

- Make backups of your config map for px-bootstrap and px-cloud-drive

```

kubectl get cm -n kube-system | grep px

```

```

kubectl get cm <px-bootstrap> -n kube-system -o yaml > px-bootstrapbkp.yaml

```

```

kubectl get cm <px-cloud-drive> -n kube-system -o yaml > px-cloud-drivebkp.yaml

```

- Collect KVDB end points using pxctl:

```

pxctl service kvdb endpoints

```

- Contact technical support (see below)

- `ssh` into the respective nodes and run `pxctl status` on each node to check the Portworx cluster status:

```

pxctl status

```

- If running internal KVDB check KVDB cluster members and confirm the health status using pxctl:

```

pxctl service kvdb members

```

- If quorum has been lost perform the following before contacting technical support:

- Save px-diags on each affected node (captures all logs)

```

pxctl service diags -a

```

- Make backups of your config map for px-bootstrap and px-cloud-drive

```

oc get cm -n <px-namespace> | grep px

```

```

oc get cm <px-bootstrap> -n <px-namespace> -o yaml > px-bootstrapbkp.yaml

```

```

oc get cm <px-cloud-drive> -n <px-namespace> -o yaml > px-cloud-drivebkp.yaml

```

- Collect KVDB end points using pxctl:

```

pxctl service kvdb endpoints

```

- Contact technical support (see below)

- If using external etcd, check your external etcd cluster status.

- Portworx container will fail to come up if it cannot reach etcd. For etcd installation instructions, refer this doc.

- The etcd location specified when creating the Portworx cluster needs to be reachable from all nodes.

- For external Etcd run `curl <etcd_location>/version` from each node to ensure reachability. For e.g `curl "http://192.168.33.10:2379/version"`

- If you deployed etcd as a Kubernetes service, use the ClusterIP instead of the kube-dns name. Portworx nodes cannot resolve kube-dns entries since Portworx containers are in the host network.

### Portworx pxctl cluster summary reports Status "Online", StorageStatus "(StorageDown)" "Full or Offline"​

- Identify the node and the storage pool in question by running pxctl (ssh into the respective node) status:

```

pxctl status

```

- From the same node, inspect the pool to identify the disk device that makes up the pool:

```

pxctl service pool show

```

- Logged in as root, identify why the disk is failing by running dmesg

```

dmesg | grep error

```

To correct the problem:

-
Remove or replace the drive following these instructions: Remove or replace

-
If the pool is full follow these instructions: Expand your storage pool size

### Performance related​

- Run Grafana dashboard to identify volumes, pools, nodes, network and other components.

- Grafana.

- Dashboard

- Requires the latest charts from Portworx release 2.10.0 and up.

- Refer to the following performance tuning document: Tune Performance

- There are many performance tuning enhancements in the latest release of Portworx. Please see: Portworx release notes

### PVC Controller pod failed to start​

If you are running Portworx in managed Kubernetes service provider and run into port conflict in the PVC controller, you can overwrite the default PVC Controller ports using the `portworx.io/pvc-controller-port` and `portworx.io/pvc-controller-secure-port` annotations on the `StorageCluster` object:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

  annotations:

    portworx.io/pvc-controller-port: "10261"

    portworx.io/pvc-controller-secure-port: "10262"

...

```

## Collect Portworx logs​

Run the following command on the suspect or affected nodes running Portworx:

```

pxctl service diags -a

```

note

Include these logs when contacting Portworx support, along with generated diags located in `/var/cores/<node-x-x-diags>-<timestamp>.tar.gz`

### Set log level to debug mode​

If you need more information to be logged for debugging, you can change the log level to `debug` by adding the environment variable `PX_LOGLEVEL` to the `StorageCluster`.

note

This change restarts the portworx nodes and becomes effective after the restart.

- Kubernetes

- Openshift

-
Get the `StorageCluster` Spec by running the `kubectl get stc -A` command.

```

kubectl get stc -A

```

```

NAMESPACE     NAME                       CLUSTER UUID                           STATUS    VERSION   AGE

kube-system   tp-aks-temp-setup-px-int   xxxxxxxx-xxxx-xxxx-xxxx-5d69340b972d   Running   3.0.4     3h55m

```

-
Edit the `StorageCluster` to add the environment variable `PX_LOGLEVEL` and set the value to `debug`.

```

kubectl edit stc <stc_name> -n kube-system

```

```

spec:

  env:

  - name: "PX_LOGLEVEL"

    value: "debug"

```

-
Get the `StorageCluster` Spec by running the `oc get stc -A` command.

```

oc get stc -A

```

```

NAMESPACE     NAME                       CLUSTER UUID                           STATUS    VERSION   AGE

kube-system   tp-aks-temp-setup-px-int   xxxxxxxx-xxxx-xxxx-xxxx-5d69340b972d   Running   3.0.4     3h55m

```

-
Edit the `StorageCluster` to add the environment variable `PX_LOGLEVEL` and set the value to `debug`.

```

oc edit stc <stc_name> -n kube-system

```

```

spec:

  env:

  - name: "PX_LOGLEVEL"

    value: "debug"

```

-
After the portworx node restarts, verify if the debug mode is enabled by running the `journalctl -lu portworx* ` command on a worker node.

```

journalctl -lu portworx*

```

```

Jun 24 09:31:06 px-node portworx[8040]: time="2024-06-24T09:31:06Z" level=debug msg="criRuntime.List()  cache hit cid=4d0e7db692a>

Jun 24 09:31:08 px-node portworx[8040]: time="2024-06-24T09:31:08Z" level=debug msg="evalPoolStatus returns map[0:{newStatus:Up c>

Jun 24 09:31:09 px-node portworx[8040]: time="2024-06-24T09:31:09Z" level=debug msg="all members healthy" file="kvlistener.go:508>

```

You can now see `level=debug` in the logs, with more detailed information to troubleshoot.

## Generate stack traces​

Portworx support will occasionally request stack traces to help you troubleshoot. Enter the following command on the troubled node to create a `*.stack` file in the `/var/cores` directory with the latest timestamp:

```

pxctl service diags --profile

```

## Contact support​

View your options for contacting support by visiting the Portworx support page:
 Portworx support

In this topic:
