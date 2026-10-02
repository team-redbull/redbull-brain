# Manage storage nodes on AWS

Source: https://docs.portworx.com/portworx-enterprise/reference-architectures/auto-disk-provisioning/aws (Portworx Enterprise latest)

Manage storage nodes on AWS | Portworx Enterprise Documentation

note

If you are running on Kubernetes, visit Portworx on Kubernetes on Amazon Elastic Kubernetes Service (EKS)

Below guide explains how Portworx dynamic disk provisioning works on AWS and the requirements for it. This is typically useful when an autoscaling group (ASG) is managing your AWS instances.

## EBS volume template​

An EBS volume template defines the EBS volume properties that Portworx will use as a reference. These templates are given to Portworx during installation.

### Use a template specification​

You can specify a template spec which will be used by Portworx to create new EBS volumes.

The spec follows the following format:

```

"type=<EBS volume type>,size=<size of EBS volume>,iops=<IOPS value>,enc=<true/false>,kms=<CMK>,tags=<key:value;key:value>,throughput=<throughput of the disk>"

```

-
type: The following types are supported:

- gp2

- gp3

- io1 (For io1 volumes specifying the iops value is mandatory.)

-
size: This is the size of the EBS volume in GB

-
iops: This is the required IOs per second from the EBS volume.

-
enc: This needs to be set to true if EBS volumes need to be encrypted. Default: false

-
kms: This is the AWS KMS key to encrypt the EBS volume. i.e.`<key>` in `arn:aws:kms:us-east-1:<account-id>:key/<key>`

-
tags: This adds custom labels to EBS volumes created on EKS drives. The key-value pairs are added as labels to the newly created volumes.

-
throughput: This is used to specify the throughput of the disk. Valid only for gp3 disk type. The ratio between the accompanying `iops` parameter and the `throughput` value must not exceed .25. For example, if the value of `iops` is 4000, the value of `throughput` must not exceed 1000.

See EBS details for more details on above parameters.

#### Examples​

- `"type=gp2,size=200"`

- `"type=gp2,size=100","type=io1,size=200,iops=1000"`

- `"type=gp2,size=100,enc=true,kms=AKXXXXXXXX123","type=io1,size=200,iops=1000,enc=true,kms=AKXXXXXXXXX123"`

- `"type=gp2,size=100,tags=key:value;key:value"`

- `"type=gp3,size=199,iops=4000,throughput=1000"`

## EC2 Instance types​

A Portworx cluster can be deployed with a heterogeneous makeup of EC2 instance types. Some of your nodes can be used for converged compute and storage, some for compute only and some for storage only.

Follow this guide to select your appropriate instance type. Once you create an AMI template for an instance type, you will create multiple instances from that AMI. Make sure your AMIs are available in each region that you want to run the Portworx cluster in.

note

Since Portworx is a replicated block device, you can also use instance local store volumes for maximum performance. However you must have Portworx replication turned on.

## Multi Zone Availability​

Since Portworx is a replicated storage solution, Portworx by Everpure recommends using multiple availability zones when creating your EC2 based cluster. Follow this site for more information on geographical availability of your instances: here.

In this topic:
