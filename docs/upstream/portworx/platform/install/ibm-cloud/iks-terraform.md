# Installation on IBM Cloud Kubernetes Service (IKS) cluster using Terraform

Source: https://docs.portworx.com/portworx-enterprise/platform/install/ibm-cloud/iks-terraform (Portworx Enterprise latest)

Installation on IBM Cloud Kubernetes Service (IKS) cluster using Terraform | Portworx Enterprise Documentation

This topic provides instructions for installing Portworx on a IBM Cloud Kubernetes Service (IKS) cluster using Terraform. You can use the Terraform module to upgrade an active installation and to automate Portworx deployment across multiple IKS clusters.

Ensure that your cluster meets all the prerequisites before installing Portworx Enterprise.

The following collection of tasks describe how to install Portworx on a IBM Cloud Kubernetes Service (IKS) cluster using Terraform:

- Configure your Terraform on IBM Cloud setup

- Declare the IBM Cloud resources

- Retrieve the kubeconfig file

- Install Portworx

- Verify Portworx Pod Status

- Verify Portworx Cluster Status

- Verify pxctl Cluster Provision Status

Complete all the tasks to install Portworx.

## Configure your Terraform on IBM Cloud setup​

-
Clone the Terraform repository:

```

git clone https://github.com/portworx/terraform-ibm-portworx-enterprise.git

```

-
Depending on your cluster resources, navigate to the appropriate folder:

- IKS cluster using mounted volumes:

```

cd examples/iks-with-attached-drives

```

- IKS cluster using cloud drives:

```

cd examples/iks-with-cloud-drives

```

- IKS cluster where existing worker nodes are converted to Portworx nodes:

```

cd examples/iks-worker-node-replace

```

### Declare the IBM Cloud resources​

Create a variable file and name it `terraform.tfvars`. In this file, declare the IBM Cloud resources required for your Portworx deployment.

-
For an IKS cluster using mounted volumes or cloud drives, declare the following:

```

iks_cluster_name="<your_iks-cluster_name>"

resource_group="<your_resource_group_name>"

ibmcloud_api_key="<secret_ibm_cloud_key>"

```

- `resource_group`: Specify the resource group name where your IKS cluster exists, and the Portworx Enterprise service instance will be created in the same resource group.

- `iks_cluster_name`: Name of your IKS cluster

- `ibmcloud_api_key`: IBM Cloud API key associated with your cluster

-
For an IKS cluster where existing worker nodes are converted to Portworx nodes, declare the following:

```

resource_group   = "<your_resource_group_name>"

region           = "<region_name>"

iks_cluster_name = "<your_iks_cluster_name>"

worker_ids       = ["<worker_id_1>", "<worker_id_2>", "<worker_id_3>"]

replace_all_workers = false

```

- `resource_group`: Specify the resource group name where your IKS cluster exists, and the Portworx Enterprise service instance will be created in the same resource group.

- `region`: Specify the IBM region where your cluster is provisioned

- `worker_ids`: List of all worker nodes IDs to be replaced.

- `iks_cluster_name`: Name of your IKS cluster

For the complete list of variables, refer to the `examples/variables.tf` file in your setup directory.

### Retrieve the kubeconfig file​

To access the IKS cloud services and resources from your client machine, run the following command:

```

export IC_API_KEY="secret_ibm_cloud_key"

ibmcloud ks cluster config --admin --cluster <cluster_name | cluster_id>

```

## Install Portworx​

-
Initialize Terraform:

```

terraform init

```

-
Generate a Terraform execution plan:

```

terraform plan -out tf.plan

```

-
Apply the execution plan:

```

terraform apply tf.plan

```

-
Run the following command to deploy Portworx:

```

terraform output

```

```

associated_iks_cluster_id = "cdkasv9w0oi7m5g5i6qg"

associated_iks_cluster_name = "schakravorty-px-wdc-b3c.4x16"

portworx_enterprise_id = "crn:v1:bluemix:public:portworx:us-east:a/b5c47bfad9f99ace9c94c3986bd1fdc9:xxxxxxxx-xxxx-xxxx-xxxx-5192d195b094::"

portworx_enterprise_service_name = "portworx-enterprise-b0d0b748"

portworx_version_installed = "2.11.4"

```

Wait for a few minutes for the Portworx pods to be created. You will see that the command outputs the details of the Portworx Enterprise service.

## Verify Portworx Pod Status​

Enter the following command to list and filter the results for Portworx pods and specify the namespace where you have deployed Portworx:

```

kubectl get pods -n <px-namespace> -o wide | grep -e portworx -e px

```

```

NAME                                                    READY   STATUS    RESTARTS         AGE     IP                NODE                   NOMINATED NODE   READINESS GATES

portworx-api-774c2                                      1/1     Running   0                2m55s   192.168.121.196   username-k8s1-node0    <none>           <none>

portworx-api-t4lf9                                      1/1     Running   0                2m55s   192.168.121.99    username-k8s1-node1    <none>           <none>

portworx-api-dvw64                                      1/1     Running   0                2m55s   192.168.121.99    username-k8s1-node2    <none>           <none>

portworx-kvdb-94bpk                                     1/1     Running   0                4s      192.168.121.196   username-k8s1-node0    <none>           <none>

portworx-kvdb-8b67l                                     1/1     Running   0                10s     192.168.121.196   username-k8s1-node1    <none>           <none>

portworx-kvdb-fj72p                                     1/1     Running   0                30s     192.168.121.196   username-k8s1-node2    <none>           <none>

portworx-operator-58967ddd6d-kmz6c                      1/1     Running   0                4m1s    10.244.1.99       username-k8s1-node0    <none>           <none>

prometheus-px-prometheus-0                              2/2     Running   0                2m41s   10.244.1.105      username-k8s1-node0    <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-3e9bf3cd834d-9gs79   2/2     Running   0                2m55s   192.168.121.196   username-k8s1-node0    <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-3e9bf3cd834d-vpptx   2/2     Running   0                2m55s   192.168.121.99    username-k8s1-node1    <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-3e9bf3cd834d-bxmpn   2/2     Running   0                2m55s   192.168.121.191   username-k8s1-node2    <none>           <none>

px-csi-ext-868fcb9fc6-54bmc                             4/4     Running   0                3m5s    10.244.1.103      username-k8s1-node0    <none>           <none>

px-csi-ext-868fcb9fc6-8tk79                             4/4     Running   0                3m5s    10.244.1.102      username-k8s1-node2    <none>           <none>

px-csi-ext-868fcb9fc6-vbqzk                             4/4     Running   0                3m5s    10.244.3.107      username-k8s1-node1    <none>           <none>

px-prometheus-operator-59b98b5897-9nwfv                 1/1     Running   0                3m3s    10.244.1.104      username-k8s1-node0    <none>           <none>

```

Note the name of a `px-cluster` pod. You will run `pxctl` commands from these pods in Verify pxctl Cluster Provision Status.

## Verify Portworx Cluster Status​

You can find the status of the Portworx cluster by running `pxctl status` commands from a pod.
Enter the following `kubectl exec` command, specifying the pod name you retrieved in Verify Portworx Pod Status:

```

kubectl exec <pod-name> -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-70c31d0f478e

    IP: 192.168.121.99

    Local Storage Pool: 1 pool

    POOL    IO_PRIORITY     RAID_LEVEL      USABLE  USED    STATUS  ZONE    REGION

    0       HIGH            raid0           3.0 TiB 10 GiB  Online  default default

    Local Storage Devices: 3 devices

    Device  Path            Media Type              Size            Last-Scan

    0:1     /dev/vdb        STORAGE_MEDIUM_MAGNETIC 1.0 TiB         14 Jul 22 22:03 UTC

    0:2     /dev/vdc        STORAGE_MEDIUM_MAGNETIC 1.0 TiB         14 Jul 22 22:03 UTC

    0:3     /dev/vdd        STORAGE_MEDIUM_MAGNETIC 1.0 TiB         14 Jul 22 22:03 UTC

    * Internal kvdb on this node is sharing this storage device /dev/vdc  to store its data.

    total           -       3.0 TiB

    Cache Devices:

        * No cache devices

Cluster Summary

    Cluster ID: px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-3e9bf3cd834d

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-6f3fd5522eae

    Scheduler: kubernetes

    Nodes: 3 node(s) with storage (3 online)

    IP              ID                                      SchedulerNodeName       Auth            StorageNode     Used    Capacity        Status  StorageStatus       Version         Kernel                  OS

    192.168.121.196 xxxxxxxx-xxxx-xxxx-xxxx-fad8c65b8edc    username-k8s1-node0      Disabled        Yes             10 GiB  3.0 TiB         Online  Up 2.11.0-81faacc   3.10.0-1127.el7.x86_64  CentOS Linux 7 (Core)

    192.168.121.99  xxxxxxxx-xxxx-xxxx-xxxx-70c31d0f478e    username-k8s1-node1      Disabled        Yes             10 GiB  3.0 TiB         Online  Up (This node)      2.11.0-81faacc  3.10.0-1127.el7.x86_64  CentOS Linux 7 (Core)

    192.168.121.191 xxxxxxxx-xxxx-xxxx-xxxx-19d45b4c541a    username-k8s1-node2      Disabled        Yes             10 GiB  3.0 TiB         Online  Up  2.11.0-81faacc  3.10.0-1127.el7.x86_64  CentOS Linux 7 (Core)

Global Storage Pool

    Total Used      :  30 GiB

    Total Capacity  :  9.0 TiB

```

Status displays `PX is operational` when the cluster is running as expected.

## Verify pxctl Cluster Provision Status​

-
Access the Portworx CLI.

-
Run the following command to find the storage cluster:

```

kubectl -n <px-namespace> get storagecluster

```

```

NAME                                              CLUSTER UUID                           STATUS   VERSION   AGE

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-3e9bf3cd834d   xxxxxxxx-xxxx-xxxx-xxxx-6f3fd5522eae   Online   2.11.0    10m

```

The status must display the cluster is `Online`.

-
Run the following command to find the storage nodes:

```

kubectl -n <px-namespace> get storagenodes

```

```

NAME                  ID                                     STATUS   VERSION          AGE

username-k8s1-node0   xxxxxxxx-xxxx-xxxx-xxxx-fad8c65b8edc   Online   2.11.0-81faacc   11m

username-k8s1-node1   xxxxxxxx-xxxx-xxxx-xxxx-70c31d0f478e   Online   2.11.0-81faacc   11m

username-k8s1-node2   xxxxxxxx-xxxx-xxxx-xxxx-19d45b4c541a   Online   2.11.0-81faacc   11m

```

The status must display the nodes are `Online`.

-
Verify the Portworx cluster provision status by running the following command.
 Specify the pod name you retrieved in Verify Portworx Pod Status.

```

kubectl exec <px-pod> -n <px-namespace> -- /opt/pwx/bin/pxctl cluster provision-status

```

```

NODE					                NODE STATUS	 POOL						              POOL STATUS  IO_PRIORITY	SIZE	AVAILABLE	USED   PROVISIONED ZONE REGION	RACK

0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxx	Up		    0 ( 8ec9e6aa-7726-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxx	Up		    0 ( 06fcc73a-7e2f-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx	Up		    0 ( 58ab2e3f-a22e-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

```

## What to do next​

Create a PVC. For more information, see Create your first PVC.

In this topic:
