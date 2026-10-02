# Installation on Air-Gapped Amazon Elastic Kubernetes Service (EKS) Cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/install/aws/aws-eks-airgapped (Portworx Enterprise latest)

Installation on Air-Gapped Amazon Elastic Kubernetes Service (EKS) Cluster | Portworx Enterprise Documentation

This topic provides instructions for installing Portworx on an air-gapped Amazon Elastic Kubernetes Service (Amazon EKS) cluster. You can deploy Portworx and required packages by using a private container registry. Ensure that your cluster meets all the prerequisites before installing Portworx Enterprise.

The following collection of tasks describes how to install Portworx on an air-gapped Amazon Elastic Kubernetes Service (EKS) cluster:

- Create an IAM policy

- Attach the IAM policy

- Get Portworx container images

- Set your container registry

- Create a version manifest ConfigMap for Portworx Operator

- Install NFS packages for SharedV4

- Generate the Portworx specification

- Deploy Portworx Operator

- Deploy StorageCluster

- Verify Portworx pod status

- Verify Portworx cluster status

- Verify pxctl cluster provision status

- What to do next

Complete all tasks to install Portworx.

### Create an IAM policy​

Provide the permissions for all the instances in the Auto Scaling group by creating an IAM role. Perform the following steps in the AWS Management Console:

- For non-encrypted volumes

- For encrypted volumes

-
In the AWS Management Console, open IAM, select Policies under Identity and Access Management (IAM), and then select Create policy.

-
Choose the JSON tab, and then paste the following permissions into the editor. Provide your own value for `Sid` if applicable. You can either use the minimum permissions required or the permissions required for disk encryption.

note

These are the minimum permissions needed for storage operations for a Portworx cluster. For complete permissions required for all of Portworx storage operations, see the credentials reference.

```

{

  "Version": "2012-10-17",

  "Statement": [

    {

      "Sid": "",

      "Effect": "Allow",

      "Action": [

        "ec2:AttachVolume",

        "ec2:ModifyVolume",

        "ec2:DetachVolume",

        "ec2:CreateTags",

        "ec2:CreateVolume",

        "ec2:DeleteTags",

        "ec2:DeleteVolume",

        "ec2:DescribeTags",

        "ec2:DescribeVolumeAttribute",

        "ec2:DescribeVolumesModifications",

        "ec2:DescribeVolumeStatus",

        "ec2:DescribeVolumes",

        "ec2:DescribeInstances",

        "autoscaling:DescribeAutoScalingGroups"

      ],

      "Resource": ["*"]

    }

  ]

}

```

-
Name the policy and create it.

-
In the AWS Management Console, open IAM, select Policies under Identity and Access Management (IAM), and then select Create policy.

-
Choose the JSON tab, and then paste the following permissions into the editor. Provide your own value for `Sid` if applicable. You can either use the minimum permissions required or the permissions required for disk encryption.

note

These are the minimum permissions needed for storage operations for a Portworx cluster. For complete permissions required for all of Portworx storage operations, see the credentials reference.

```

{

  "Version": "2012-10-17",

  "Statement": [

    {

      "Sid": "",

      "Effect": "Allow",

      "Action": [

        "ec2:AttachVolume",

        "ec2:ModifyVolume",

        "ec2:DetachVolume",

        "ec2:CreateTags",

        "ec2:CreateVolume",

        "ec2:DeleteTags",

        "ec2:DeleteVolume",

        "ec2:DescribeTags",

        "ec2:DescribeVolumeAttribute",

        "ec2:DescribeVolumesModifications",

        "ec2:DescribeVolumeStatus",

        "ec2:DescribeVolumes",

        "ec2:DescribeInstances",

        "autoscaling:DescribeAutoScalingGroups"

      ],

      "Resource": ["arn:aws:kms:*:<account-id>:key/<kms-key-id>"]

    }

  ]

}

```

-
Name the policy and create it.

### Attach the IAM policy​

Attach the previously created policy to your node instance role or AWS user account.

- Attach the policy to a node instance role

- Attach the policy to your AWS user account

Follow these instructions to attach the policy to your `NodeInstanceRole`:

-
From the IAM page, click Roles in the left pane.

-
On the Roles page, search for and select your node group `NodeInstanceRole` using your cluster name. The system displays the node group instance role.

note

If there are more than one nodegroup `NodeInstanceRole` for your cluster, attach the policy to those `NodeInstanceRole`s as well.

-
Attach the previously created policy by selecting Attach policies from the Add permissions dropdown on the right side of the screen.

-
Under Other permissions policies, search for your policy name. Select your policy name and select the Attach policies button to attach it.

System should show attached policy on the Permissions policies section of your nodegroup `NodeInstanceRole`.

-
From the IAM page, click Users in the left pane.

-
On the Users page, search for and select your AWS user account.

-
On your user account detail page, click Add permissions in the upper right corner of the Permissions policies section.

-
Select Attach policies directly in the Permissions options section.

-
Use the search bar in the Permissions policies section to search and select your previously created policy, and click Next.

-
Click Add permissions to attach the policy to your AWS user account.

Once the policy is successfully attached to your user account, you will be navigated back to your user account detail page and the policy will be listed in the Permissions policies section.

### Get Portworx container images​

-
Set an environment variable for the Kubernetes version you are using:

```

KBVER=$(kubectl version | awk -F'[v+_-]' '/Server/ {print $3}')

```

-
Set an environment variable to the Portworx version:

```

PXVER=<portworx-version>

```

-
On an internet-connected host with the same architecture and OS version as the Kubernetes cluster nodes intended for Portworx installation, download the air-gapped installation bootstrap script for the specified Kubernetes and Portworx versions:

```

curl -o px-ag-install.sh -L "https://install.portworx.com/$PXVER/air-gapped?kbver=$KBVER"

```

-
Pull the container images required for the specified versions:

```

sh px-ag-install.sh pull

```

### Set your container registry​

To make the Portworx container images available in your air-gapped cluster, configure a container registry that the nodes can access. In AWS, you can use Amazon Elastic Container Registry (ECR). ECR repositories host a single image each, and Portworx consists of multiple images. Create a separate ECR repository for each image.

-
Sign in to Docker:

```

aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com

```

-
Create an ECR repository for each image. The following command creates repositories in the `us-west-2` Region, differentiated by the `pxmirror` prefix. Replace the Region with the one where you are deploying your Portworx cluster:

```

for images in $(curl -fsSL install.portworx.com/$PXVER/air-gapped | awk -F / '/^IMAGES="$IMAGES /{print $NF}' | cut -d: -f1); do aws ecr create-repository --repository-name pxmirror/$images --image-scanning-configuration scanOnPush=true --region us-west-2; done

```

If the output is paged, press q to exit after each repository is created.

-
Create the Kubernetes pull secret in the same Region, replacing `<namespace>` with the namespace in which you will deploy Portworx:

```

kubectl create secret docker-registry ecr-pxmirror --docker-server XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com --docker-username=AWS --docker-password=$(aws ecr get-login-password --region us-west-2) -n <namespace>

```

The registry used in the preceding command is `XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/pxmirror`, where `XXXXXXXXXXXX` is your AWS account ID number.

note

Skip the above steps if you are not using the ECR registry.

-
Push the container images to a private registry that is accessible to your air-gapped nodes. Do not include `http://` in your private registry path:

```

sh px-ag-install.sh push XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com/pxmirror

```

### Create a version manifest ConfigMap for Portworx Operator​

-
Download the Portworx version manifest:

```

curl -o versions.yaml "https://install.portworx.com/$PXVER/version?kbver=$KBVER&opver=<operator-version>"

```

Replace `<operator-version>` with the Operator version you want to use.

-
(Optional) If your installation images are spread across multiple custom registries, update your version manifest with the custom registry location details. You can use DNS hostname+domains or IP addresses (IPv4 or IPv6) to specify the container registry server in the following format:

```

<dns-host.domain or IPv4 or IPv6>[:<port>]/repository/image:tag

```

The following example demonstrates registries using a custom DNS hostname and domain, IPv4, and IPv6:

```

version: 2.13.3

components:

  stork: custom-registry.acme.org/portworx/backup/stork:23.2.1

  autopilot: 192.168.1.2:5433/tools/autopilot:1.3.7

  nodeWiper: [2001:db8:3333:4444:5555:6666:7777:8888]:5443/portworx/px-node-wiper:2.13.2

```

note

-
Ensure that the Custom Container Registry location field is empty for any specs you generate in the spec generator.

-
`kubeScheduler`, `kubeControllerManager`, and `pause` may not appear in the version manifest, but you can include them in the `px-version` configmap:

```

...

kubeScheduler: custom-registry.acme.org/k8s/kube-scheduler-amd64:v1.26.4

kubeControllerManager: custom-registry.acme.org/k8s/kube-controller-manager-amd64:v1.26.4

pause: custom-registry.acme.org/k8s/pause:3.1

```

-
Create a configmap from the downloaded or updated version manifest, replacing `<namespace>` with the namespace in which you will deploy Portworx:

```

kubectl -n <namespace> create configmap px-versions --from-file=versions.yaml

```

## Install NFS packages for SharedV4​

To install the NFS package on your host systems so that Portworx can use the SharedV4 feature, follow these steps:

-
Start the repository container as a standalone service in Docker:

```

docker run -p 8080:8080 docker.io/portworx/px-repo:1.2.0

```

-
Using a browser within your air-gapped environment, navigate to your host IP address where the above docker image is running (For example, `http://<ip-address>:8080`), and follow the instructions for your Linux distribution provided by the container to configure your host to use the package repository service, and install the NFS packages.

## Generate the Portworx specification​

To install Portworx, first generate the Kubernetes manifests that you will deploy in your Amazon EKS cluster.

-
Sign in to the Portworx Central console.
 The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
 The system displays the Generate Spec page.

-
From the Portworx Version dropdown menu, select the Portworx version to install.

-
From the Platform dropdown menu, select AWS.

-
From the Distribution Name dropdown menu, select Elastic Kubernetes Service (EKS).

-
Click Customize.

-
On the Basic tab:

- To use an internal Portworx-managed key-value store (kvdb), Select Built-in etcd. TLS for internal KVDB is enabled, by default. If Cert-Manager is already running in your Kubernetes cluster, deselect the Deploy Cert-Manager for TLS certificates option to avoid installation failures.

- Click Next.

-
On the Storage tab, retain the recommended default values and click Next.

-
On the Network tab:

- Enter the Data Network Interface to be used for data traffic.

- Enter the Management Network Interface to be used for management traffic.

- Enter the Starting port for Portworx services.

- Click Next.

-
On the Deployment tab:

-
In the Kubernetes Distribution section, under Are you running on either of these?, select None.

-
In the Component Settings section:

- Select the Restrict Data Protection RBAC to restrict RBAC permissions for Stork (if enabled) and Operator. You will not be able to use Backup and DR capabilities with this restriction. For more information, see Restrict Data Protection RBAC.

- Select the Enable Monitoring checkbox to enable monitoring of Portworx components and resources.

- To configure the monitoring stack, select one of the following:

- Portworx Managed - To enable Portworx to install and manage Prometheus and Operator automatically.
 Ensure that no other Prometheus Operator instance already running on the cluster.

- User Managed - To configure and manage your own monitoring stack.

- Select the Enable Autopilot checkbox to enable Portworx Autopilot. For User Managed monitoring stack, Portworx supports the following metrics providers that Autopilot will use to fetch metrics for rule evaluation and automated actions.

- Prometheus - Provide a valid Prometheus URL

- Datadog - Provide a valid Datadog URL, Secret Name and Secret Namespace. To create a Secret, refer to enable Datadog.
 For more information on Autopilot, see Expanding your Storage Pool with Autopilot.

- Deselect the Enable Telemetry checkbox to clear the default selection.

-
In the Environment Variables section, enter name-value pairs in the respective fields.

- For restricting Portworx services from listening on all network interfaces, set `PX_DISABLE_WILDCARD_LISTENERS` to `"true"`. By default, Portworx services listen on `0.0.0.0` (all interfaces). When this environment variable is set to true, each service listens only on its management IP, data IP or local loopbacks as required. If you do not set `PX_DISABLE_WILDCARD_LISTENERS` to `"true"` during spec generation, you can add it later to the StorageCluster spec as an environment variable.

note

- When you update `PX_DISABLE_WILDCARD_LISTENERS` in StorageCluster, it triggers a rolling update of the cluster. This causes Portworx to restart on each node and it comes up with the new network configuration. We recommend making this change during a planned maintenance window.

- You cannot switch the IP address family (IPv4 to IPv6 or IPv6 to IPv4) using `PX_PREFER_IPV6_NETWORK_IP` while `PX_DISABLE_WILDCARD_LISTENERS` is set to `"true"`. To switch the IP address family, first disable `PX_DISABLE_WILDCARD_LISTENERS`, switch the IP family, and then re-enable `PX_DISABLE_WILDCARD_LISTENERS`.

-
In the Registry and Image Settings section:

-
If you use a single private registry, enter the internal registry path and the details for how to connect to your private registry in the Custom Container Registry Location field.

-
If you use multiple private registries, leave the Custom Container Registry Location field blank.

-
Select Finish to generate the specs.

## Deploy Portworx Operator​

Deploy the Operator by running the command that Portworx Central provided, which looks similar to the following:

```

kubectl apply -f "https://install.portworx.com/<portworx_version>?comp=pxoperator"

```

```

serviceaccount/portworx-operator created

podsecuritypolicy.policy/px-operator created

clusterrole.rbac.authorization.k8s.io/portworx-operator created

clusterrolebinding.rbac.authorization.k8s.io/portworx-operator created

deployment.apps/portworx-operator created

```

## Deploy StorageCluster​

Deploy the StorageCluster by running the command that Portworx Central provided, which looks similar to the following:

```

kubectl apply -f "https://install.portworx.com/<portworx_version>?operator=true&mc=false&kbver=&b=true&c=px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-8dfd338e915b&stork=true&csi=true&mon=true&tel=false&st=k8s&reg=XXXXXXXXXXXX.dkr.ecr.us-west-2.amazonaws.com&rsec=ecr-pxmirror&promop=true"

```

```

storagecluster.core.libopenstorage.org/px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-8dfd338e915b created

```

## Verify Portworx pod status​

List and filter the results for Portworx pods, and specify the namespace where you deployed Portworx:

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

Note the name of a `px-cluster` pod. You will run `pxctl` commands from these pods in Verify pxctl cluster provision status.

## Verify Portworx cluster status​

You can find the status of the Portworx cluster by running `pxctl status` from a pod. Enter the following `kubectl exec` command, specifying the pod name you retrieved in Verify Portworx pod status:

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

The status displays `PX is operational` when the cluster is running as expected. If the cluster is using the PX-StoreV2 datastore, the `StorageNode` entries for each node display `Yes(PX-StoreV2)`.

## Verify pxctl cluster provision status​

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

-
Verify the Portworx cluster provision status by running the following command.
 Specify the pod name you retrieved in Verify Portworx pod status.

```

kubectl exec <px-pod> -n <px-namespace> -- /opt/pwx/bin/pxctl cluster provision-status

```

```

NODE					        NODE STATUS	 POOL					      POOL STATUS  IO_PRIORITY	SIZE	AVAILABLE	USED   PROVISIONED ZONE REGION	RACK

0c99e1f2-9d49-xxxx-xxxx-xxxxxxxxxxxx	Up	    0 ( 8ec9e6aa-7726-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

1e89102f-0510-xxxx-xxxx-xxxxxxxxxxxx	Up	    0 ( 06fcc73a-7e2f-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

24508311-e2fe-xxxx-xxxx-xxxxxxxxxxxx	Up	    0 ( 58ab2e3f-a22e-xxxx-xxxx-xxxxxxxxxxxx )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

```

## What to do next​

Create a PVC. For more information, see Create your first PVC.

In this topic:
