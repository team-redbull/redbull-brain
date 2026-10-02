# Installing on a vSphere Kubernetes Service Cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/tanzu (Portworx Enterprise 3.6)

Installing on a vSphere Kubernetes Service Cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

note

If you are not using a VKS cluster, skip to next section.

## Label your drives​

The existing Synchronous DR implementation assumes the availability of cloud drives for each of the two clusters. In VKS, cloud drive is a PVC, which is a cluster-scoped resource and in order to help clusters distinguish between their drives, they should be labeled accordingly.

-
Label your worker nodes on both clusters with the `px-dr` label. Set your cluster domain as a value:

```

kubectl label nodes <list-of-nodes or --all> px-dr=<cluster-domain-name>

```

-
Add the `--node_pool_label` parameter to the spec with a key `px-dr`:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  annotations:

    portworx.io/misc-args: '--node_pool_label=px-dr'

```

note

Only deploy Portworx in this mode when your Kubernetes clusters are separated by a metropolitan area network with a maximum latency of 10 ms. Everpure does not recommend you to run in this mode if your Kubernetes clusters are distributed across regions, such as AWS regions `us-east` and `us-west`.

-
Apply the modified Portworx spec on both the clusters, and Portworx will form the stretch cluster.

## Verify Portworx installation​

You can run the following commands to ensure Portworx is successfully installed in a stretch fashion.

-
Run the following command on your source cluster to see if the Portworx cluster is up and running:

```

kubectl get pods

```

```

NAME             READY   STATUS        RESTARTS   AGE

portworx-d6rk7   1/1     Running       0          4m

portworx-d6rk8   1/1     Running       0          5m

portworx-d6rk9   1/1     Running       0          7m

```

-
Run the following command to verify that stretch cluster is installed:

```

kubectl exec portworx-d6rk7 -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

```

Status: PX is operational

License: Trial (expires in 31 days)

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-f0835b788738

      IP: X.X.X.230

      Local Storage Pool: 1 pool

      POOL    IO_PRIORITY     RAID_LEVEL      USABLE  USED    STATUS  ZONE            REGION

      0       LOW             raid0           150 GiB 9.0 GiB Online  us-east-1b      us-east-1

      Local Storage Devices: 1 device

      Device  Path            Media Type              Size            Last-Scan

      0:1     /dev/xvdf       STORAGE_MEDIUM_SSD      150 GiB         09 Apr 19 22:57 UTC

      total                   -                       150 GiB

      Cache Devices:

      No cache devices

Cluster Summary

      Cluster ID: px-dr-cluster

      Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-5dfe2af572e0

      Scheduler: kubernetes

      Nodes: 6 node(s) with storage (6 online)

      IP              ID                                      SchedulerNodeName               StorageNode     Used    Capacity        Status  StorageStatus   Version         Kernel          OS

      172.20.33.100   xxxxxxxx-xxxx-xxxx-xxxx-a978f17cd020    ip-172-20-33-100.ec2.internal   Yes             0 B     150 GiB         Online  Up              2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

      xx.xx.50.47    xxxxxxxx-xxxx-xxxx-xxxx-530f313869f3    ip-172-40-50-47.ec2.internal    Yes             0 B     150 GiB         Online  Up              2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

      xx.xx.34.140   xxxxxxxx-xxxx-xxxx-xxxx-6faf19e8724c    ip-172-40-34-140.ec2.internal   Yes             0 B     150 GiB         Online  Up              2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

      172.20.36.212   xxxxxxxx-xxxx-xxxx-xxxx-82b0da1d2580    ip-172-20-36-212.ec2.internal   Yes             0 B     150 GiB         Online  Up              2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

      172.20.59.248   xxxxxxxx-xxxx-xxxx-xxxx-51e130959644    ip-172-20-59-248.ec2.internal   Yes             0 B     150 GiB         Online  Up              2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

      X.X.X.230   xxxxxxxx-xxxx-xxxx-xxxx-f0835b788738    ip-172-40-40-230.ec2.internal   Yes             0 B     150 GiB         Online  Up (This node)  2.1.0.0-cb23fd1 4.9.0-7-amd64   Debian GNU/Linux 9 (stretch)

Global Storage Pool

      Total Used      :  0 B

      Total Capacity  :  900 GiB

```

```

  You can see that the cluster summary shows `stretch` against each node IP.

```

In this topic:
