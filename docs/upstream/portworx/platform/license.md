# Set up Portworx Licenses

Source: https://docs.portworx.com/portworx-enterprise/platform/license (Portworx Enterprise 3.6)

Set up Portworx Licenses | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The Portworx Enterprise license is a flexible license, which comes with numerous options. Contact the Everpure support team (support@purestorage.com) to determine which type of Portworx Enterprise license works best for your requirements.

Portworx Enterprise supports the following license types:

License typeDescription

TrialSame as the Portworx Enterprise license. It is a default license installed with 30 days trial period for full Portworx Enterprise functionality

Portworx Enterprise VMEnterprise license, suitable for Virtual Machine (VM) installs on-prem and in cloud

Portworx Enterprise MetalEnterprise license, suitable for installs on any bare metal hardware

Portworx for Modern VirtualizationPortworx license limited running VMs on Kubernetes with Kubevirt. Suitable for installs on bare metal hardware. Does not include storage for containers

Portworx CSI for FA/FBIncluded at no additional cost with every FlashArray & FlashBlade. This license provides essential container storage capabilities for Portworx on FlashArray and FlashBlade. This license allows only Direct Access volumes up to the cluster limit. No license activation required when using FlashArray or FlashBlade.

The license that you select for Portworx Enterprise determines what features you have access to and how long you can use them. For more information about features and configurations supported with different license types, see Portworx Enterprise license types and features.

By default, Portworx Enterprise automatically activates the Trial license (limited to 30 days), which you can upgrade to a Portworx Enterprise license at any time. If you already have a Portworx enterprise license, you should activate it before your trial period expires. Seven days before your Portworx license is set to expire, Portworx sends an alert notifying your license is about to expire and how long you have to renew your license. The alert will keep triggering even after the license has expired. After the trial period expires, you cannot create new volumes, volume snapshots, new volume attachments, or new node addition to the cluster.

You can restore normal functionality by purchasing and installing a Portworx Enterprise license.

To complete setting up the Portworx Enterprise licensing and billing in your environment, you need to:

-
Activate the Enterprise license on your cluster - You can apply an enterprise license on your cluster using an activation ID or a license file. You need to contact the Everpure support team to obtain this ID or file.
 Once applied, the Portworx Enterprise license is locked to a single Portworx cluster via the unique UUID identifier of the cluster. Such a license (or license-file) will not work on other clusters. If needed, you can also transfer a valid enterprise license between two Portworx clusters.

-
Enable pay-as-you-go (PAYG) billing model on your cluster - You need the pay-as-you-go SaaS key to set up your billing. Contact the Everpure support team to obtain these keys.
 When you convert a cluster with a pay-as-you-go billing model to an air-gapped cluster, you need to transfer your Portworx license as well.
 Once you enable a pay-as-you-go license for an air-gapped cluster with no outbound connectivity, you currently can't switch to any other license.

## Check your license status​​

Use the following commands to check about your license​:

-
pxctl status - This provides a brief license summary.

```

pxctl status

```

```

Status: PX is operational

License: Trial license (expires in 30 days)

[...]

```

-
pxctl license list - The command gives details on the features allowed under the current licenses, and it lists the SKU.

```

pxctl license list

```

```

DESCRIPTION				ENABLEMENT	ADDITIONAL INFO

Number of nodes maximum			1000

Number of volumes maximum		100000

Volume capacity [TB] maximum		  40

Storage aggregation			 yes

Shared volumes				 yes

Volume sets				 yes

BYOK data encryption			 yes

Resize volumes on demand		 yes

Snapshot to object store [CloudSnap]	 yes

Cluster-level migration [Kubemotion]	 yes

Bare-metal hosts			 yes

Virtual machine hosts			 yes

Product SKU				Trial		expires in 6 days, 12:13

LICENSE EXPIRES: 2019-04-07 23:59:59 +0000 UTC

For information on purchase, upgrades and support, see

https://docs.portworx.com/knowledgebase/support.html

```

note

7 days before your Portworx license is set to expire, Portworx sends an alert notifying your license is about to expire and how long you have to renew your license. The alert will keep triggering after the license has expired. For more details, see this page.

In this topic:
