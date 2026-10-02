# Installation on Amazon Elastic Kubernetes Service (EKS) using AWS Marketplace

Source: https://docs.portworx.com/portworx-enterprise/platform/install/aws/eks/aws-marketplace (Portworx Enterprise latest)

Installation on Amazon Elastic Kubernetes Service (EKS) using AWS Marketplace | Portworx Enterprise Documentation

This topic provides instructions for installing Portworx on an Amazon Elastic Kubernetes Service (Amazon EKS) cluster from AWS Marketplace.

Ensure that your cluster meets all the prerequisites before installing Portworx Enterprise.

The following tasks describe how to install Portworx from AWS Marketplace on an Amazon EKS cluster:

- Grant Portworx the required AWS permissions

- Configure IAM permissions

- Configure with eksctl

- Configure with AWS CLI or AWS Management Console

- Install Portworx from AWS Marketplace

- Add the Helm repository

- Install the Helm chart from the repository

- Helm chart configuration reference

- Monitor Portworx nodes

- Verify Portworx pod status

- Verify Portworx cluster status

- Verify Portworx pool status

- Verify `pxctl` cluster provision status

Complete all tasks to install Portworx from AWS Marketplace.

### Grant Portworx the required AWS permissions​

Portworx requires specific AWS permissions to operate correctly on an Amazon EKS cluster. It uses these permissions to create and attach Amazon EBS volumes to the nodes in your cluster. The following example policy describes these permissions:

- For non-encrypted volumes

- For encrypted volumes

```

{

    "Version": "2012-10-17",

    "Statement": [

        {

            "Sid": "ec2",

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

            "Resource": [

                "*"

            ]

        },

        {

            "Sid": "VisualEditor0",

            "Effect": "Allow",

            "Action": "ec2:DeleteInternetGateway",

            "Resource": [

                "arn:aws:iam::*:role/eksctl-*",

                "arn:aws:ec2:*:*:internet-gateway/*"

            ]

        },

        {

            "Sid": "VisualEditor1",

            "Effect": "Allow",

            "Action": "ec2:DeleteInternetGateway",

            "Resource": "arn:aws:iam::*:instance-profile/eksctl-*"

        },

        {

            "Sid": "VisualEditor2",

            "Effect": "Allow",

            "Action": [

                "iam:CreateInstanceProfile",

                "iam:DeleteInstanceProfile",

                "iam:GetRole",

                "iam:GetInstanceProfile",

                "iam:RemoveRoleFromInstanceProfile",

                "iam:CreateRole",

                "iam:DeleteRole",

                "iam:AttachRolePolicy",

                "iam:PutRolePolicy",

                "iam:AddRoleToInstanceProfile",

                "iam:ListInstanceProfilesForRole",

                "iam:PassRole",

                "iam:CreateServiceLinkedRole",

                "iam:DetachRolePolicy",

                "iam:DeleteRolePolicy",

                "iam:DeleteServiceLinkedRole",

                "iam:GetRolePolicy"

            ],

            "Resource": [

                "arn:aws:iam::*:instance-profile/eksctl-*",

                "arn:aws:iam::*:role/eksctl-*"

            ]

        },

        {

            "Sid": "VisualEditor3",

            "Effect": "Allow",

            "Action": [

                "ec2:AuthorizeSecurityGroupIngress",

                "ec2:DeleteSubnet",

                "ec2:AttachInternetGateway",

                "ec2:DescribeSnapshots",

                "ec2:DeleteSnapshot",

                "ec2:DeleteRouteTable",

                "ec2:AssociateRouteTable",

                "ec2:DescribeInternetGateways",

                "ec2:CreateRoute",

                "ec2:CreateInternetGateway",

                "ec2:RevokeSecurityGroupEgress",

                "autoscaling:DescribeAutoScalingGroups",

                "autoscaling:UpdateAutoScalingGroup",

                "ec2:DeleteInternetGateway",

                "ec2:DescribeKeyPairs",

                "ec2:DescribeRouteTables",

                "ecr:BatchCheckLayerAvailability",

                "ecr:GetLifecyclePolicy",

                "ecr:DescribeImageScanFindings",

                "ec2:ImportKeyPair",

                "ec2:DescribeLaunchTemplates",

                "ec2:CreateTags",

                "ecr:GetDownloadUrlForLayer",

                "ec2:CreateRouteTable",

                "cloudformation:*",

                "ec2:RunInstances",

                "ecr:GetAuthorizationToken",

                "ec2:DetachInternetGateway",

                "ec2:DisassociateRouteTable",

                "ec2:RevokeSecurityGroupIngress",

                "ec2:DescribeImageAttribute",

                "ecr:BatchGetImage",

                "ecr:DescribeImages",

                "ec2:DeleteNatGateway",

                "ec2:DeleteVpc",

                "autoscaling:DeleteAutoScalingGroup",

                "eks:*",

                "ec2:CreateSubnet",

                "ec2:DescribeSubnets",

                "autoscaling:CreateAutoScalingGroup",

                "ec2:DescribeAddresses",

                "ec2:DeleteTags",

                "elasticfilesystem:*",

                "ec2:CreateNatGateway",

                "autoscaling:DescribeLaunchConfigurations",

                "ec2:CreateVpc",

                "ecr:ListTagsForResource",

                "ecr:ListImages",

                "ec2:DescribeVpcAttribute",

                "ec2:DescribeAvailabilityZones",

                "autoscaling:DescribeScalingActivities",

                "ec2:CreateSecurityGroup",

                "sts:DecodeAuthorizationMessage",

                "ec2:CreateSnapshot",

                "ec2:ModifyVpcAttribute",

                "ecr:DescribeRepositories",

                "ec2:ReleaseAddress",

                "ec2:AuthorizeSecurityGroupEgress",

                "ec2:DeleteLaunchTemplate",

                "ec2:DescribeTags",

                "ecr:GetLifecyclePolicyPreview",

                "ec2:DeleteRoute",

                "ec2:DescribeLaunchTemplateVersions",

                "ec2:DescribeNatGateways",

                "ec2:AllocateAddress",

                "ec2:DescribeSecurityGroups",

                "ec2:DescribeImages",

                "autoscaling:CreateLaunchConfiguration",

                "ec2:CreateLaunchTemplate",

                "autoscaling:DeleteLaunchConfiguration",

                "sts:Get*",

                "ec2:DescribeVpcs",

                "ec2:DeleteSecurityGroup",

                "ecr:GetRepositoryPolicy"

            ],

            "Resource": "*"

        },

        {

            "Sid": "VisualEditor4",

            "Effect": "Allow",

            "Action": "iam:ListInstanceProfiles",

            "Resource": [

                "arn:aws:iam::*:instance-profile/eksctl-*",

                "arn:aws:iam::*:role/eksctl-*"

            ]

        }

    ]

}

```

```

{

    "Version": "2012-10-17",

    "Statement": [

        {

            "Sid": "kms",

            "Effect": "Allow",

            "Action": [

                "kms:Encrypt",

                "kms:Decrypt",

                "kms:ReEncrypt*",

                "kms:GenerateDataKey*",

                "kms:DescribeKey"

            ],

            "Resource": [

                "arn:aws:kms:us-west-2:383347425723:key/c1f576b7-6369-xxxx-xxxx-xxxxxxxxxxxxxx"

            ]

        },

        {

            "Sid": "ec2",

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

            "Resource": [

                "*"

            ]

        },

        {

            "Sid": "VisualEditor0",

            "Effect": "Allow",

            "Action": "ec2:DeleteInternetGateway",

            "Resource": [

                "arn:aws:iam::*:role/eksctl-*",

                "arn:aws:ec2:*:*:internet-gateway/*"

            ]

        },

        {

            "Sid": "VisualEditor1",

            "Effect": "Allow",

            "Action": "ec2:DeleteInternetGateway",

            "Resource": "arn:aws:iam::*:instance-profile/eksctl-*"

        },

        {

            "Sid": "VisualEditor2",

            "Effect": "Allow",

            "Action": [

                "iam:CreateInstanceProfile",

                "iam:DeleteInstanceProfile",

                "iam:GetRole",

                "iam:GetInstanceProfile",

                "iam:RemoveRoleFromInstanceProfile",

                "iam:CreateRole",

                "iam:DeleteRole",

                "iam:AttachRolePolicy",

                "iam:PutRolePolicy",

                "iam:AddRoleToInstanceProfile",

                "iam:ListInstanceProfilesForRole",

                "iam:PassRole",

                "iam:CreateServiceLinkedRole",

                "iam:DetachRolePolicy",

                "iam:DeleteRolePolicy",

                "iam:DeleteServiceLinkedRole",

                "iam:GetRolePolicy"

            ],

            "Resource": [

                "arn:aws:iam::*:instance-profile/eksctl-*",

                "arn:aws:iam::*:role/eksctl-*"

            ]

        },

        {

            "Sid": "VisualEditor3",

            "Effect": "Allow",

            "Action": [

                "ec2:AuthorizeSecurityGroupIngress",

                "ec2:DeleteSubnet",

                "ec2:AttachInternetGateway",

                "ec2:DescribeSnapshots",

                "ec2:DeleteSnapshot",

                "ec2:DeleteRouteTable",

                "ec2:AssociateRouteTable",

                "ec2:DescribeInternetGateways",

                "ec2:CreateRoute",

                "ec2:CreateInternetGateway",

                "ec2:RevokeSecurityGroupEgress",

                "autoscaling:DescribeAutoScalingGroups",

                "autoscaling:UpdateAutoScalingGroup",

                "ec2:DeleteInternetGateway",

                "ec2:DescribeKeyPairs",

                "ec2:DescribeRouteTables",

                "ecr:BatchCheckLayerAvailability",

                "ecr:GetLifecyclePolicy",

                "ecr:DescribeImageScanFindings",

                "ec2:ImportKeyPair",

                "ec2:DescribeLaunchTemplates",

                "ec2:CreateTags",

                "ecr:GetDownloadUrlForLayer",

                "ec2:CreateRouteTable",

                "cloudformation:*",

                "ec2:RunInstances",

                "ecr:GetAuthorizationToken",

                "ec2:DetachInternetGateway",

                "ec2:DisassociateRouteTable",

                "ec2:RevokeSecurityGroupIngress",

                "ec2:DescribeImageAttribute",

                "ecr:BatchGetImage",

                "ecr:DescribeImages",

                "ec2:DeleteNatGateway",

                "ec2:DeleteVpc",

                "autoscaling:DeleteAutoScalingGroup",

                "eks:*",

                "ec2:CreateSubnet",

                "ec2:DescribeSubnets",

                "autoscaling:CreateAutoScalingGroup",

                "ec2:DescribeAddresses",

                "ec2:DeleteTags",

                "elasticfilesystem:*",

                "ec2:CreateNatGateway",

                "autoscaling:DescribeLaunchConfigurations",

                "ec2:CreateVpc",

                "ecr:ListTagsForResource",

                "ecr:ListImages",

                "ec2:DescribeVpcAttribute",

                "ec2:DescribeAvailabilityZones",

                "autoscaling:DescribeScalingActivities",

                "ec2:CreateSecurityGroup",

                "sts:DecodeAuthorizationMessage",

                "ec2:CreateSnapshot",

                "ec2:ModifyVpcAttribute",

                "ecr:DescribeRepositories",

                "ec2:ReleaseAddress",

                "ec2:AuthorizeSecurityGroupEgress",

                "ec2:DeleteLaunchTemplate",

                "ec2:DescribeTags",

                "ecr:GetLifecyclePolicyPreview",

                "ec2:DeleteRoute",

                "ec2:DescribeLaunchTemplateVersions",

                "ec2:DescribeNatGateways",

                "ec2:AllocateAddress",

                "ec2:DescribeSecurityGroups",

                "ec2:DescribeImages",

                "autoscaling:CreateLaunchConfiguration",

                "ec2:CreateLaunchTemplate",

                "autoscaling:DeleteLaunchConfiguration",

                "sts:Get*",

                "ec2:DescribeVpcs",

                "ec2:DeleteSecurityGroup",

                "ecr:GetRepositoryPolicy"

            ],

            "Resource": "*"

        },

        {

            "Sid": "VisualEditor4",

            "Effect": "Allow",

            "Action": "iam:ListInstanceProfiles",

            "Resource": [

                "arn:aws:iam::*:instance-profile/eksctl-*",

                "arn:aws:iam::*:role/eksctl-*"

            ]

        }

    ]

}

```

### Configure IAM permissions​

You can configure IAM permissions in multiple ways. The recommended way is to use an `IAMServiceAccount` if your cluster supports it. If not, you can use instance privileges or environment variables.

#### Configure with eksctl​

If you use `eksctl` to manage your Amazon EKS cluster, you can create an `IAMServiceAccount` for Portworx by running the following commands.

-
Enable the IAM OIDC provider for your Amazon EKS cluster. Replace `<clustername>` with your cluster name, and change the region if you aren’t running in `us-east-1`.

```

eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=<clustername> --approve

```

-
Create the `IAMServiceAccount` with the appropriate permissions (required to send metering data to AWS). If you aren’t deploying in `kube-system`, change the namespace. Replace `<clustername>` with your cluster name.

```

eksctl create iamserviceaccount --name portworx-aws --namespace <px-namespace> --cluster <clustername> --attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringFullAccess \

--attach-policy-arn arn:aws:iam::aws:policy/AWSMarketplaceMeteringRegisterUsage --approve --override-existing-serviceaccounts

```

This command creates an `IAMServiceAccount` in the AWS Management Console and a `ServiceAccount` in the specified namespace. You’ll reference it during the Helm chart installation.

#### Configure with AWS CLI or AWS Management Console​

You can configure IAM permissions through the AWS Command Line Interface (AWS CLI) or the AWS Management Console.

For detailed instructions, see Assign IAM roles to Kubernetes service accounts and Create an IAM OIDC provider for your cluster in the official AWS documentation.

Remember the namespace and service account you created, as you’ll specify them during the Helm chart installation.

## Install Portworx from AWS Marketplace​

### Add the Helm repository​

Add the Portworx AWS Helm repository by running the following command:

```

helm repo add portworx https://raw.githubusercontent.com/portworx/aws-helm/master/stable

```

### Install the Helm chart from the repository​

To install the chart with the release name `my-release`, run the following command and substitute relevant values for your setup. See the Helm chart configuration reference for information about configurable parameters.

```

helm install my-release portworx/portworx --set storage.drives="type=gp2\,size=1000" --set serviceAccount="portworx-aws"

```

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

For information related to Upgrade and Uninstall from AWS Marketplace, see Upgrade Portworx Marketplace Deployment and Uninstall Portworx installed using AWS Marketplace.

## Helm chart configuration reference​

The following table lists the configurable parameters of the Portworx chart and their default values.

ParameterDescription

`awsProduct`Portworx product name: `PX-ENTERPRISE` or `PX-ENTERPRISE-DR`. Defaults to `PX-ENTERPRISE`.

`clusterName`Portworx cluster name.

`namespace`Namespace in which to deploy Portworx.

`storage.usefileSystemDrive`Whether Portworx should use an unmounted drive that already has a file system.

`storage.usedrivesAndPartitions`Whether Portworx should use drives and partitions on the disk.

`storage.drives`Semicolon-separated list of drives to use for storage (example: `"/dev/sda;/dev/sdb"`). To automatically generate Amazon EBS disks, use a list of drive specs (example: `"type=gp2\,size=150";type=io1\,size=100\,iops=2000"`). Escape commas.

`storage.journalDevice`Journal device for Portworx metadata.

`storage.maxStorageNodesPerZone`Maximum number of storage nodes per zone. If this number is reached and a new node is added to the zone, Portworx doesn’t provision drives for the new node and starts it as a compute-only node.

`network.dataInterface`Data interface name, such as `<ethX>`.

`network.managementInterface`Management interface name, such as `<ethX>`.

`secretType`Secrets store to use: `aws-kms`, `k8s`, or `none`. Defaults to `k8s`.

`envVars`Semicolon-separated list of environment variables to export to Portworx (example: `MYENV1=val1;MYENV2=val2`).

`serviceAccount`Name of the created service account with the required IAM permissions.

Specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

## Monitor Portworx nodes​

-
Enter the following `kubectl get` command and wait until all Portworx nodes show as `Ready` or `Online` in the output:

```

kubectl -n <px-namespace> get storagenodes -l name=portworx

```

```

NAME                 ID                                     STATUS   VERSION          AGE

username-k8s1-node0   xxxxxxxx-xxxx-xxxx-xxxx-43cf085e764e   Online   2.11.1-3a5f406   4m52s

username-k8s1-node1   xxxxxxxx-xxxx-xxxx-xxxx-4597de6fdd32   Online   2.11.1-3a5f406   4m52s

username-k8s1-node2   xxxxxxxx-xxxx-xxxx-xxxx-e2169ffa111c   Online   2.11.1-3a5f406   4m52s

```

-
Enter the following `kubectl describe` command with the `NAME` of one of the Portworx nodes you retrieved above to show the current installation status for individual nodes:

```

kubectl -n <px-namespace> describe storagenode <portworx-node-name>

```

```

...

Events:

    Type     Reason                             Age                     From                  Message

    ----     ------                             ----                    ----                  -------

    Normal   PortworxMonitorImagePullInPrgress  7m48s                   portworx, k8s-node-2  Portworx image portworx/px-enterprise:2.10.1.1 pull and extraction in progress

    Warning  NodeStateChange                    5m26s                   portworx, k8s-node-2  Node is not in quorum. Waiting to connect to peer nodes on port 9002.

    Normal   NodeStartSuccess                   5m7s                    portworx, k8s-node-2  PX is ready on this node

```

note

- The image pulled in the output differs based on the Portworx license type and version.

- For Portworx Enterprise, the default license activated on the cluster is a 30 day trial, that you can convert to a SaaS-based model or a generic fixed license.

## Verify Portworx pod status​

Run the following command to list and filter the results for Portworx pods, and specify the namespace where you deployed Portworx:

```

kubectl get pods -n <px-namespace> -o wide | grep -e portworx -e px

```

```

NAME                                                    READY   STATUS    RESTARTS         AGE     IP              NODE                         NOMINATED NODE   READINESS GATES

portworx-api-8scq2                                      1/1     Running   1 (90m ago)      5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-api-f24b9                                      1/1     Running   1 (108m ago)     5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-api-f95z5                                      1/1     Running   1 (90m ago)      5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-kvdb-558g5                                     1/1     Running   0                3m46s   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-kvdb-9tfjd                                     1/1     Running   0                2m57s   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-kvdb-cjcxg                                     1/1     Running   0                3m7s    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-operator-548b8d4ccc-qgnkc                      1/1     Running   13 (4m26s ago)   5h2m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

portworx-pvc-controller-ff669698-62ngd                  1/1     Running   1 (108m ago)     5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

portworx-pvc-controller-ff669698-6b4zj                  1/1     Running   1 (90m ago)      5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

portworx-pvc-controller-ff669698-pffvl                  1/1     Running   1 (90m ago)      5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

prometheus-px-prometheus-0                              2/2     Running   2 (90m ago)      5h      xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-fab038f0bbe6-2qsp4   2/2     Running   13 (108m ago)    3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-fab038f0bbe6-5vnzv   2/2     Running   16 (90m ago)     3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-fab038f0bbe6-lxzd5   2/2     Running   16 (90m ago)     3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

px-csi-ext-77fbdcdcc9-7hkpm                             4/4     Running   4 (108m ago)     3h19m   xx.xx.xxx.xxx   username-vms-silver-sight-3   <none>           <none>

px-csi-ext-77fbdcdcc9-9ck26                             4/4     Running   4 (90m ago)      3h18m   xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

px-csi-ext-77fbdcdcc9-ddmjr                             4/4     Running   14 (90m ago)     3h20m   xx.xx.xxx.xxx   username-vms-silver-sight-2   <none>           <none>

px-prometheus-operator-7d884bc8bc-5sv9r                 1/1     Running   1 (90m ago)      5h1m    xx.xx.xxx.xxx   username-vms-silver-sight-0   <none>           <none>

```

Note the name of one of the `px-cluster` pods. You’ll run `pxctl` commands from that pod in the following steps.

## Verify Portworx cluster status​

You can check cluster status by running `pxctl status` from a pod.

Run the following `kubectl exec` command, specifying the pod name you retrieved in Verify Portworx pod status:

```

kubectl exec <px-pod>  -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Disabled or Unhealthy

License: Trial (expires in 31 days)

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-bf578f9addc1

    IP: xx.xx.xxx.xxx

    Local Storage Pool: 1 pool

    POOL	IO_PRIORITY	RAID_LEVEL	USABLE	USED	STATUS	ZONE	REGION

    0	HIGH		raid0		25 GiB	33 MiB	Online	default	default

    Local Storage Devices: 1 device

    Device	Path		Media Type		Size		Last-Scan

    0:0	/dev/sda	STORAGE_MEDIUM_SSD	32 GiB		10 Oct 22 23:45 UTC

    total			-			32 GiB

    Cache Devices:

     * No cache devices

    Kvdb Device:

    Device Path	Size

    /dev/sdc	1024 GiB

     * Internal kvdb on this node is using this dedicated kvdb device to store its data.

    Metadata Device:

    1	/dev/sdd	STORAGE_MEDIUM_SSD	64 GiB

Cluster Summary

    Cluster ID: px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-fab038f0bbe6

    Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-5d610fa334bd

    Scheduler: kubernetes

    Nodes: 3 node(s) with storage (3 online)

    IP		ID					SchedulerNodeName		Auth		StorageNode		Used	Capacity	Status	StorageStatus	Version		Kernel				OS

    xx.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-bf578f9addc1	username-vms-silver-sight-3	Disabled	Yes(PX-StoreV2)	33 MiB	25 GiB		Online	Up (This node)	2.12.0-28944c8	5.4.217-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    xx.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-4a1bafeff5bc	username-vms-silver-sight-0	Disabled	Yes(PX-StoreV2)	33 MiB	25 GiB		Online	Up		2.12.0-28944c8	5.4.217-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

    xx.xx.xxx.xxx	xxxxxxxx-xxxx-xxxx-xxxx-502e658bc307	username-vms-silver-sight-2	Disabled	Yes(PX-StoreV2)	33 MiB	25 GiB		Online	Up		2.12.0-28944c8	5.4.217-1.el7.elrepo.x86_64	CentOS Linux 7 (Core)

Global Storage Pool

    Total Used    	:  99 MiB

    Total Capacity	:  74 GiB

```

The status shows `PX is operational` when the cluster is running as expected. For each node, the `StorageNode` column reads `Yes(PX-StoreV2)`.

## Verify Portworx pool status​

Run the following command to view the Portworx drive configuration for your pod:

```

kubectl exec <px-pod>  -n <px-namespace> -- /opt/pwx/bin/pxctl service pool show

```

```

Defaulted container "portworx" out of: portworx, csi-node-driver-registrar

PX drive configuration:

Pool ID: 0

    Type:  PX-StoreV2

    UUID:  xxxxxxxx-xxxx-xxxx-xxxx-db8abe01d4f0

    IO Priority:  HIGH

    Labels:  kubernetes.io/arch=amd64,kubernetes.io/hostname=username-vms-silver-sight-3,kubernetes.io/os=linux,medium=STORAGE_MEDIUM_SSD,beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,iopriority=HIGH

    Size: 25 GiB

    Status: Online

    Has metadata:  No

    Balanced:  Yes

    Drives:

    0: /dev/sda, Total size 32 GiB, Online

    Cache Drives:

    No Cache drives found in this pool

Metadata  Device:

    1: /dev/sdd, STORAGE_MEDIUM_SSD

```

The `Type: PX-StoreV2` line indicates that the pod uses the PX-StoreV2 datastore.

## Verify `pxctl` cluster provision status​

-
Access the Portworx CLI.

-
Run the following command to find the storage cluster:

```

kubectl -n <px-namespace> get storagecluster

```

```

NAME                                              CLUSTER UUID                           STATUS   VERSION          AGE

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-fab038f0bbe6   xxxxxxxx-xxxx-xxxx-xxxx-5d610fa334bd   Online   2.12.0-dev-rc1   5h6m

```

The status should display `Online`.

-
Run the following command to find the storage nodes:

```

kubectl -n <px-namespace> get storagenodes

```

```

NAME                          ID                                     STATUS   VERSION          AGE

username-vms-silver-sight-0   xxxxxxxx-xxxx-xxxx-xxxx-4a1bafeff5bc   Online   2.12.0-28944c8   3h25m

username-vms-silver-sight-2   xxxxxxxx-xxxx-xxxx-xxxx-502e658bc307   Online   2.12.0-28944c8   3h25m

username-vms-silver-sight-3   xxxxxxxx-xxxx-xxxx-xxxx-bf578f9addc1   Online   2.12.0-28944c8   3h25m

```

The nodes should display `Online`.

-
Verify the Portworx cluster provision status by running the following command. Specify the pod name you retrieved in Verify Portworx pod status.

```

kubectl exec <px-pod> -n <px-namespace> -- /opt/pwx/bin/pxctl cluster provision-status

```

```

NODE					        NODE STATUS	 POOL					      POOL STATUS  IO_PRIORITY	SIZE	AVAILABLE	USED   PROVISIONED ZONE REGION	RACK

xxxxxxxx-xxxx-xxxx-xxxx-502e658bc307	Up	    0 ( xxxxxxxx-xxxx-xxxx-xxxx-f9131bf7ef9d )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

xxxxxxxx-xxxx-xxxx-xxxx-4a1bafeff5bc	Up	    0 ( xxxxxxxx-xxxx-xxxx-xxxx-434152789beb )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

xxxxxxxx-xxxx-xxxx-xxxx-bf578f9addc1	Up	    0 ( xxxxxxxx-xxxx-xxxx-xxxx-db8abe01d4f0 )	Online		HIGH		32 GiB	32 GiB		33 MiB	0 B		default	default	default

```

## What to do next​

Create a PVC. For more information, see Create your first PVC.

In this topic:
