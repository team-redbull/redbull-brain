# Installation on IBM Cloud using IBM Catalog

Source: https://docs.portworx.com/portworx-enterprise/platform/install/ibm-cloud/ibm-cloud-install (Portworx Enterprise 3.6)

Installation on IBM Cloud using IBM Catalog | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This topic provides instructions for installing Portworx on an IBM Cloud Kubernetes Service (IKS) cluster and a Red Hat OpenShift on IBM Cloud cluster using IBM Catalog on a typical cluster that has the following properties:

- The cluster is located in a single availability zone

- Portworx is installed using an internal KVDB

- Kubernetes or OpenShift has access to the public network and gateway

Ensure that your cluster meets all the prerequisites before installing Portworx Enterprise.

The following collection of tasks describe how to install Portworx on a IBM Cloud Kubernetes Service (IKS) cluster and Red Hat OpenShift on IBM Cloud cluster using IBM Catalog:

- (Optional) Create a StorageClass for encrypting cloud drives

- Install Portworx

- Verify Portworx Pod Status

- Verify Portworx Cluster Status

- Verify pxctl Cluster Provision Status

Complete all the tasks to install Portworx.

## (Optional) Create a StorageClass for encrypting cloud drives​

To set up encryption for cloud drives, create a custom StorageClass in your cluster (where you plan to deploy Portworx). This may impact the performance of your environment. Follow the steps outlined in the IBM documentation.

## Install Portworx​

-
Log in to IBM Cloud.

-
From the top navigation bar, select Catalog.
 The system displays the Catalog page.

-
Search for Portworx Enterprise in the Search the catalog field and select the Portworx Enterprise tile.
 The system displays the configuration page.

-
From the Select a location dropdown menu, select the location of your Kubernetes or OpenShift cluster.

-
In the Select a pricing plan section, choose one of the following plans:

- px-dr-enterprise

- px-enterprise

-
In the Configure your resource section, configure the following fields:

- Service name: Enter a name for your Portworx installation or keep the default name.

- Select a resource group: Specify the resource group associated with your Kubernetes or OpenShift cluster.

- Tags: Enter one or more tags to help identify your service instance.

- IBM Cloud API key: Enter your IBM Cloud API key.

note

The API key is required to populate the Kubernetes or OpenShift cluster name.

- Kubernetes or OpenShift Cluster name: Select the cluster from the dropdown menu.
 This list is populated based on the API key provided in the previous step. If you are installing on Red Hat OpenShift on IBM Cloud, ensure that you select the OpenShift cluster name.

- Portworx cluster name: Enter a name for the Portworx storage layer.
 The cluster name must be a unique name for the storage layer that Portworx creates within your Kubernetes or OpenShift cluster.

- Namespace: Enter the namespace to install Portworx.

- From the Cloud drives dropdown menu, select Use Cloud Drives, and configure the following:

- Number of drives: Select the number of drives to provision.
 The maximum number of drives you can provision is 3.

- Initial Storage Nodes (Optional): Enter the number of storage nodes that need to be created across zones and node pools.
 Set this to the maximum number of worker nodes in your cluster.

- Storage Class name: Enter a name for each drive to provision or retain the default storage class name.
All cloud drives must show the same Storage Class name. For encrypting cloud drives, select your custom StorageClass from the dropdown.

- Size: Enter the size of the disk to provision in gigabytes.

- From the Portworx metadata key-value store dropdown menu, choose one of the following:

- Portworx KVDB: To deploy Portworx with an internal KVDB cluster.

- Databases for etcd: To deploy Portworx on an existing etcd cluster.

- If you selected Databases for etcd in the previous step, provide the Etcd API endpoints and the Etcd secret name.

- From the secret_type dropdown menu, choose one of the following:

- Kubernetes secret

- IBM Key Protect | HPCS

- (Optional) In Advance Options, provide any additional configuration settings.

- From the Portworx versions dropdown menu, select the version of Portworx to install.

- Leave the Helm Parameters blank.

- To enable the CSI driver support, from the CSI dropdown menu, select Enable.

-
From the right sidebar, select the checkbox to agree to the terms and conditions.

-
Click Create to launch the Portworx cluster.
 This process may take 20 minutes or longer.

For upgrading Portworx installed using IBM Catalog, see Upgrade Portworx deployment via Helm.

## Verify Portworx Pod Status​

Run the following command to list and filter the results for Portworx pods:

- Kubernetes

- OpenShift

```

kubectl get pods -n <px-namespace> -o wide | grep -e portworx -e px

```

```

NAME                                                    READY   STATUS    RESTARTS         AGE     IP              NODE                         NOMINATED NODE   READINESS GATES

portworx-api-8scq2                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-0               <none>           <none>

portworx-api-f24b9                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-3               <none>           <none>

portworx-api-f95z5                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-2               <none>           <none>

portworx-kvdb-558g5                                     1/1     Running   0                3m46s   xx.xx.xxx.xxx   worker-node-2               <none>           <none>

portworx-kvdb-9tfjd                                     1/1     Running   0                2m57s   xx.xx.xxx.xxx   worker-node-0               <none>           <none>

portworx-kvdb-cjcxg                                     1/1     Running   0                3m7s    xx.xx.xxx.xxx   worker-node-3               <none>           <none>

portworx-operator-548b8d4ccc-qgnkc                      1/1     Running   0                5h2m    xx.xx.xxx.xxx   worker-node-0               <none>           <none>

portworx-pvc-controller-ff669698-62ngd                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-3               <none>           <none>

portworx-pvc-controller-ff669698-6b4zj                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-2               <none>           <none>

portworx-pvc-controller-ff669698-pffvl                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-0               <none>           <none>

prometheus-px-prometheus-0                              2/2     Running   0                5h      xx.xx.xxx.xxx   worker-node-0               <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-2qsp4   2/2     Running   0                3h20m   xx.xx.xxx.xxx   worker-node-3               <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-5vnzv   2/2     Running   0                3h20m   xx.xx.xxx.xxx   worker-node-0               <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-lxzd5   2/2     Running   0                3h20m   xx.xx.xxx.xxx   worker-node-2               <none>           <none>

px-csi-ext-77fbdcdcc9-7hkpm                             4/4     Running   0                3h19m   xx.xx.xxx.xxx   worker-node-3               <none>           <none>

px-csi-ext-77fbdcdcc9-9ck26                             4/4     Running   0                3h18m   xx.xx.xxx.xxx   worker-node-0               <none>           <none>

px-csi-ext-77fbdcdcc9-ddmjr                             4/4     Running   0                3h20m   xx.xx.xxx.xxx   worker-node-2               <none>           <none>

px-prometheus-operator-7d884bc8bc-5sv9r                 1/1     Running   0                5h1m    xx.xx.xxx.xxx   worker-node-0               <none>           <none>

```

```

oc get pods -n <px-namespace> -o wide | grep -e portworx -e px

```

```

NAME                                                    READY   STATUS    RESTARTS         AGE     IP              NODE                         NOMINATED NODE   READINESS GATES

portworx-api-8scq2                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-api-f24b9                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-api-f95z5                                      1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-kvdb-558g5                                     1/1     Running   0                3m46s   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-kvdb-9tfjd                                     1/1     Running   0                2m57s   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-kvdb-cjcxg                                     1/1     Running   0                3m7s    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-operator-548b8d4ccc-qgnkc                      1/1     Running   0                5h2m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-pvc-controller-ff669698-62ngd                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-pvc-controller-ff669698-6b4zj                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-pvc-controller-ff669698-pffvl                  1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

prometheus-px-prometheus-0                              2/2     Running   0                5h      xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-2qsp4   2/2     Running   0                3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-5vnzv   2/2     Running   0                3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx-lxzd5   2/2     Running   0                3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

px-csi-ext-77fbdcdcc9-7hkpm                             4/4     Running   0                3h19m   xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

px-csi-ext-77fbdcdcc9-9ck26                             4/4     Running   0                3h18m   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-csi-ext-77fbdcdcc9-ddmjr                             4/4     Running   0                3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

px-prometheus-operator-7d884bc8bc-5sv9r                 1/1     Running   0                5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

```

Note the name of a `px-cluster` pod. You will run `pxctl` commands from these pods in Verify Portworx Cluster Status.

## Verify Portworx Cluster Status​

You can find the status of the Portworx cluster by running `pxctl status` commands from a pod:

- Kubernetes

- OpenShift

```

kubectl exec <px-pod-name> -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: 24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx

    IP: xx.xx.xxx.xxx

    Local Storage Pool: 1 pool

    POOLIO_PRIORITYRAID_LEVELUSABLEUSEDSTATUSZONEREGION

    0HIGHraid025 GiB33 MiBOnlinedefaultdefault

    Local Storage Devices: 1 device

    DevicePathMedia TypeSizeLast-Scan

    0:0/dev/sdaSTORAGE_MEDIUM_SSD32 GiB10 Oct 22 23:45 UTC

    total-32 GiB

    Cache Devices:

     * No cache devices

    Kvdb Device:

    Device PathSize

    /dev/sdc1024 GiB

     * Internal kvdb on this node is using this dedicated kvdb device to store its data.

    Metadata Device:

    1/dev/sddSTORAGE_MEDIUM_SSD64 GiB

Cluster Summary

    Cluster ID: px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx

    Cluster UUID: 482b18b1-2a8b-xxxx-xxxx-xxxxxxxxxxxx

    Scheduler: kubernetes

    Nodes: 3 node(s) with storage (3 online)

    IPIDSchedulerNodeNameAuthStorageNodeUsedCapacityStatusStorageStatusVersionKernelOS

    xx.xx.xxx.xxx24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxxworker-node-3DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp (This node)3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

    xx.xx.xxx.xxx1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxxworker-node-0DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

    xx.xx.xxx.xxx0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxxworker-node-2DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

Global Storage Pool

    Total Used    :  99 MiB

    Total Capacity:  74 GiB

```

Status displays `PX is operational` when the cluster is running as expected.

```

oc exec <px-pod-name> -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: 24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx

    IP: xx.xx.xxx.xxx

    Local Storage Pool: 1 pool

    POOLIO_PRIORITYRAID_LEVELUSABLEUSEDSTATUSZONEREGION

    0HIGHraid025 GiB33 MiBOnlinedefaultdefault

    Local Storage Devices: 1 device

    DevicePathMedia TypeSizeLast-Scan

    0:0/dev/sdaSTORAGE_MEDIUM_SSD32 GiB10 Oct 22 23:45 UTC

    total-32 GiB

    Cache Devices:

     * No cache devices

    Kvdb Device:

    Device PathSize

    /dev/sdc1024 GiB

     * Internal kvdb on this node is using this dedicated kvdb device to store its data.

    Metadata Device:

    1/dev/sddSTORAGE_MEDIUM_SSD64 GiB

Cluster Summary

    Cluster ID: px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx

    Cluster UUID: 482b18b1-2a8b-xxxx-xxxx-xxxxxxxxxxxx

    Scheduler: kubernetes

    Nodes: 3 node(s) with storage (3 online)

    IPIDSchedulerNodeNameAuthStorageNodeUsedCapacityStatusStorageStatusVersionKernelOS

    xx.xx.xxx.xxx24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxxworker-node-3DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp (This node)3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

    xx.xx.xxx.xxx1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxxworker-node-0DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

    xx.xx.xxx.xxx0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxxworker-node-2DisabledYes(PX-StoreV2)33 MiB25 GiBOnlineUp3.2.0-28944c85.4.217-1.el7.elrepo.x86_64CentOS Linux 7 (Core)

Global Storage Pool

    Total Used    :  99 MiB

    Total Capacity:  74 GiB

```

Status displays `PX is operational` when the cluster is running as expected.

## Verify pxctl Cluster Provision Status​

- Kubernetes

- OpenShift

-
Find the storage cluster:

```

kubectl -n <px-namespace> get storagecluster

```

```

NAME                                              CLUSTER UUID                           STATUS   VERSION          AGE

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx   482b18b1-2a8b-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-dev-rc1   5h6m

```

The status must display the cluster is `Online`.

-
Find the storage nodes:

```

kubectl -n <px-namespace> get storagenodes

```

```

NAME            ID                                     STATUS   VERSION          AGE

worker-node-0   1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

worker-node-2   0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

worker-node-3   24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

```

The status must display the nodes are `Online`.

-
Verify the Portworx cluster provision status:

```

kubectl exec <px-pod> -n <px-namespace> -- /opt/pwx/bin/pxctl cluster provision-status

```

```

NODE                NODE STATUS POOL              POOL STATUS  IO_PRIORITYSIZEAVAILABLEUSED   PROVISIONED ZONE REGIONRACK

0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 8ec9e6aa-7726-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 06fcc73a-7e2f-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 58ab2e3f-a22e-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

```

-
Find the storage cluster:

```

oc -n <px-namespace> get storagecluster

```

```

NAME                                              CLUSTER UUID                           STATUS   VERSION          AGE

px-cluster-378d7ae1-f4ca-xxxx-xxxx-xxxxxxxxxxxx   482b18b1-2a8b-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-dev-rc1   5h6m

```

The status must display the cluster is `Online`.

-
Find the storage nodes:

```

oc -n <px-namespace> get storagenodes

```

```

NAME                          ID                                     STATUS   VERSION          AGE

username-vms-silver-sight-0   1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

username-vms-silver-sight-2   0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

username-vms-silver-sight-3   24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx   Online   3.2.0-28944c8   3h25m

```

The status must display the nodes are `Online`.

-
Verify the Portworx cluster provision status:

```

oc exec <px-pod> -n <px-namespace> -- /opt/pwx/bin/pxctl cluster provision-status

```

```

NODE                NODE STATUS POOL              POOL STATUS  IO_PRIORITYSIZEAVAILABLEUSED   PROVISIONED ZONE REGIONRACK

0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 8ec9e6aa-7726-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 06fcc73a-7e2f-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxxUp    0 ( 58ab2e3f-a22e-xxxx-xxxx-xxxxxxxxxxxx )OnlineHIGH32 GiB32 GiB33 MiB0 Bdefaultdefaultdefault

```

## What to do next​

Create a PVC. For more information, see Create your first PVC.

In this topic:
