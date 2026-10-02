# Prepare your Environment for Portworx Installation with FlashArray

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage/flasharray/prepare (Portworx Enterprise 3.6)

Prepare your Environment for Portworx Installation with FlashArray | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page includes detailed system requirements that are specific to FlashArray to ensure a seamless deployment and optimal performance of Portworx Enterprise in your Kubernetes environment.

Before you begin preparing your environment, ensure that all system requirements for installing Portworx are met.

The following collection of tasks describes how to prepare your environment for Portworx installation.

Complete all the tasks to prepare your environment for installation.

## Supported FlashArray models​

Portworx supports Pure FlashArray//C and FlashArray//X. For information about minimum and maximum supported versions, see Supported Pure Storage FlashArray and FlashBlade Models and Versions.

## Software requirements​

Install the following system packages on all nodes, including the control plane node, to support storage provisioning and data path operations when using FlashArray.

CategoryRequirement

PackagesEnsure that the latest versions of the following packages are installed on nodes where you plan to run Portworx Enterprise:

- RHEL

- `iscsi-initiator-utils`

- `device-mapper-multipath`

- `kpartx` (installed as part of `device-mapper-multipath`)

- Ubuntu

- `open-iscsi`

- `multipath-tools`

- `kpartx` (installed as part of `multipath-tools`)

- Debian

- `open-iscsi`

- `multipath-tools`

- `kpartx` (installed as part of `multipath-tools`)

- SUSE Linux Enterprise Server

- `open-iscsi`

- `multipath-tools`

- `kpartx` (installed as part of `multipath-tools`)

Note: For NVMe-oF/TCP protocol, you need multipath version 0.8.7 or later.

Red Hat SystemsEnsure that the second action, `CAPACITY_DATA_HAS_CHANGED`, is uncommented in the 90-scsi-ua.rules file, and restart the udev service.

CSI Snapshot FeatureTo use the CSI snapshot feature, install the Snapshot controller and deploy the CRDs available here in your Kubernetes cluster.

FC Protocol (Optional)If you are using the FC protocol, ensure that the latest FC initiator software is installed.

NVMe CLI (Optional)If you are using the NVMe protocol, ensure that the following NVMe CLI version is installed:

- RHEL version earlier than 9.4/Ubuntu version earlier than 22.04: NVMe CLI version 1.16

- RHEL version 9.4 to 9.5/Ubuntu version 22.04 or later: NVMe CLI version 2.6

- RHEL version 9.6 or later: NVMe CLI version 2.11

## Physical network requirements​

This section outlines the physical network prerequisites for Portworx to communicate with FlashArray.

Ensure proper connectivity and protocol configuration for optimal performance and compatibility.

- Ensure the FlashArray management IP address is accessible by all nodes.

- Verify that your cluster has an operational FlashArray with a configured dataplane connectivity layout.

- Use one of the following storage networking protocols supported by Portworx Enterprise:

- iSCSI: For block storage over IP networks.

- NVMe-oF RoCE or NVMe-oF TCP: For high-performance and low-latency storage access.

- Fibre Channel (FC): For dedicated storage area networks.

- If using iSCSI:

- Ensure that the storage node iSCSI initiators are on the same VLAN as the FlashArray iSCSI target ports.

- If using multiple NICs to connect to an iSCSI host, ensure all NICs are accessible from the FlashArray management IP address.

- If using Fibre Channel:

- Verify that the storage node Fibre Channel WWNs are correctly zoned to the FlashArray Fibre Channel WWN ports.

## Multipath configuration​

- FlashArray and Portworx Enterprise do not support user-friendly names. Set `user_friendly_names` to `no` before installing Portworx Enterprise on your cluster. This ensures consistent device naming conventions between Portworx and FlashArray.

- Add `polling_interval 10` as recommended by RHEL Linux settings. This defines how often the system checks for path status updates.

- To avoid interference from the multipathd service during Portworx volume operations, set the pxd device denylist rule.

Your `/etc/multipath.conf` file should follow this structure:

- RHEL/CentOS

- Ubuntu

```

defaults {

    user_friendly_names no

    enable_foreign "^$"

    polling_interval    10

    find_multipaths yes

}

devices {

    device {

        vendor                      "NVME"

        product                     "Pure Storage FlashArray"

        path_selector               "queue-length 0"

        path_grouping_policy        group_by_prio

        prio                        ana

        failback                    immediate

        fast_io_fail_tmo            10

        user_friendly_names         no

        no_path_retry               0

        features                    0

        dev_loss_tmo                60

    }

    device {

        vendor                   "PURE"

        product                  "FlashArray"

        path_selector            "service-time 0"

        hardware_handler         "1 alua"

        path_grouping_policy     group_by_prio

        prio                     alua

        failback                 immediate

        path_checker             tur

        fast_io_fail_tmo         10

        user_friendly_names      no

        no_path_retry            0

        features                 0

        dev_loss_tmo             600

    }

}

blacklist_exceptions {

        property "(SCSI_IDENT_|ID_WWN)"

}

blacklist {

      devnode "^pxd[0-9]*"

      devnode "^pxd*"

      device {

        vendor "VMware"

        product "Virtual disk"

      }

}

```

```

defaults {

    user_friendly_names no

    find_multipaths yes

}

devices {

    device {

        vendor                      "NVME"

        product                     "Pure Storage FlashArray"

        path_selector               "queue-length 0"

        path_grouping_policy        group_by_prio

        prio                        ana

        failback                    immediate

        fast_io_fail_tmo            10

        user_friendly_names         no

        no_path_retry               0

        features                    0

        dev_loss_tmo                60

    }

    device {

        vendor                   "PURE"

        product                  "FlashArray"

        path_selector            "service-time 0"

        hardware_handler         "1 alua"

        path_grouping_policy     group_by_prio

        prio                     alua

        failback                 immediate

        path_checker             tur

        fast_io_fail_tmo         10

        user_friendly_names      no

        no_path_retry            0

        features                 0

        dev_loss_tmo             600

    }

}

blacklist {

      devnode "^pxd[0-9]*"

      devnode "^pxd*"

      device {

        vendor "VMware"

        product "Virtual disk"

      }

}

```

## Configure udev rules​

Configure queue settings with udev rules on all nodes. For recommended settings for FlashArray, refer to Applying Queue Settings with Udev.

## Apply Multipath and Udev configurations​

Apply the Multipath and Udev configurations created in the previous sections for the changes to take effect.

- OpenShift Container Platform

- Other Kubernetes platforms

Use a MachineConfig in OpenShift to apply multipath and Udev configuration files consistently across all nodes.

-
Encode the configuration files in base64 format and add them to the MachineConfig, as shown in the following example:

```

apiVersion: machineconfiguration.openshift.io/v1

kind: MachineConfig

metadata:

  creationTimestamp:

  labels:

    machineconfiguration.openshift.io/role: worker

  name: <your-machine-config-name>

spec:

  config:

    ignition:

      version: 3.2.0

    storage:

      files:

      - contents:

          source: data:text/plain;charset=utf-8;base64,<base64-encoded-multipath-conf>

        filesystem: root

        mode: 0644

        overwrite: true

        path: /etc/multipath.conf

      - contents:

          source: data:text/plain;charset=utf-8;base64,<base64-encoded-udev_conf>

        filesystem: root

        mode: 0644

        overwrite: true

        path: /etc/udev/rules.d/99-pure-storage.rules

    systemd:

      units:

      - enabled: true

        name: iscsid.service

      - enabled: true

        name: multipathd.service

```

-
Apply the MachineConfig to your cluster:

```

oc apply -f <your-machine-config-name>.yaml

```

- Update the `multipath.conf` file as described in the Configure `multipath.conf` file section and restart the `multipathd` service on all nodes:

```

systemctl restart multipathd.service

```

- Create the Udev rules as described in the Configure Udev rules section and apply them on all nodes:

```

udevadm control --reload-rules && udevadm trigger

```

## Set up user access in FlashArray​

To establish secure communication between Portworx and FlashArray, you should create a user account and generate an API token. This token acts as an authentication key, allowing Portworx to interact with FlashArray and perform storage operations on behalf of the authorized user. This section provides the steps to generate an API token, which serves as your authorization within the FlashArray environment.

Secure multi-tenancy

If multiple users share a single FlashArray, you can enable secure multi-tenancy using FlashArray realms and pods. A realm isolates tenant-specific storage, and a pod groups volumes within that realm.

important

FlashArray host sharing with realms is not supported when using Secure Multi-Tenancy (SMT). You cannot mix hosts within a realm with hosts outside a realm on the same node. For example, using Boot from SAN with a host outside the realm is not supported.

To enable this feature:

- Create a realm and pod on the FlashArray.

- Add the realm to the `pure.json` file.

- Reference the pod name in the `StorageCluster` specification.

Note that a FlashArray pod is a logical grouping on the storage array and is not related to Kubernetes pods.

This configuration ensures that each tenant can access only their assigned storage volumes.

- FlashArray without secure multi-tenancy

- FlashArray with secure multi-tenancy

-
Create a user:

- In your FlashArray dashboard, select Settings in the left pane.

- On the Settings page, select Users and Policies.

- In the Users section, click the vertical ellipsis in the top-right corner and select Create User:

- In the Create User window, enter your details and set the role to Storage Admin.

- Select Create to add the new user.

-
Generate an API token:

- To create a token for the user you created, select the user from the Users list, click the vertical ellipsis in the right-hand corner of the username, and select Create API Token:

- In the API Token window, leave the Expires in field blank if you want to create a token that never expires, and click Create.

- Save this information to avoid the need to recreate the token.

info

The following steps must be performed on the FlashArray CLI.

-
Create a realm for each customer: All volumes from the Portworx Enterprise installation will be placed within this realm, ensuring customer-specific data isolation.

```

purerealm create <customer1-realm>

```

```

Name                Quota Limit

<customer1-realm>   -

```

-
Create a pod inside the realm: A pod in FlashArray defines a boundary where specific volumes are placed.

```

purepod create <customer1-realm>::<fa-pod-name>

```

note

Stretched FlashArray pods (pods spanning multiple FlashArrays) are not supported.

By assigning realms and pods in FlashArray, you ensure that different users interact only with the specific storage resources allocated to them.

-
Create a policy for a realm: Ensure that you have administrative privileges on FlashArray before proceeding. This policy grants users access to their respective realms with defined capabilities.

```

purepolicy management-access create --realm <customer1-realm> --role storage --aggregation-strategy all-permissions <realm-policy>

```

For basic privileges, use the following command:

```

purepolicy management-access create --realm <customer1-realm> --role storage --aggregation-strategy least-common-permissions <realm-policy>

```

-
Verify the created policy: This step ensures that the policy has been set up correctly with the right permissions.

```

purepolicy management-access list

```

```

Name             Type         Enabled  Capability  Aggregation Strategy      Resource Name    Resource Type

<realm-policy>  admin-access  True     all         all-permissions           <customer1-realm>  realms

```

This policy ensures that users linked to the specified realm can perform storage operations within their allocated realm.

-
Create a user linked to a policy: This command creates a user with the access rights defined by the policy. You must create a password that the user can use to log in to FlashArray, as shown in the output:

```

pureadmin create --access-policy <realm-policy> <flasharray-user>

```

```

Enter password:

Retype password:

Name               Type   Access Policy

<flasharray-user>  local  <realm-policy>

```

This step ensures that users are securely connected to their designated realms with appropriate access.

-
Sign in as the newly created user in the FlashArray CLI.

-
Run `pureadmin create --api-token` and copy the created token.

## Create `pure.json` file​

To integrate Portworx Enterprise with FlashArray, create a JSON configuration file (named pure.json) containing essential information about the FlashArray environment. This file should include the management endpoints and the API token you generated.

note

You can provision Portworx Enterprise to automatically create and maintain the `pure.json` configuration file by enabling Portworx Fusion Controller in your Portworx cluster. After you enable Portworx Fusion Controller, you do not need to manually generate or manage individual FlashArray or FlashBlade tokens or update the configuration file when arrays are added or removed from the fleet. Portworx Fusion Controller handles discovery and token management through Fusion Coordinator, reducing operational overhead and simplifying integration with Portworx Enterprise.
For more information on how to enable Portworx Fusion Controller, see Enable Portworx Fusion Controller.

- Management endpoints: These are URLs or IP addresses that Portworx uses to communicate with FlashArray through API calls. To locate these, go to Settings > Connectors in your FlashArray dashboard. Note the IP addresses or hostnames of your management interfaces, prefixed with vir, indicating virtual interfaces.

important

- For an IPv6 address, ensure that the IP address is enclosed in square brackets. For example: `"MgmtEndPoint": "[XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX]"`.

- API token: Generated in the previous section.

- Realm (secure multi-tenancy only): Realms define tenant boundaries within a secure multi-tenancy setup. When multiple FlashArrays are attached to a cluster, the admin can specify a realm to ensure that storage volumes are isolated for each tenant. FlashArray volumes created through Portworx will be placed within the specified realm.

note

Each cluster can only support one realm per array, meaning a single Portworx deployment cannot use multiple realms on the same FlashArray.

Use the information above to create a JSON file. Below is a template for the configuration content, which you should populate with your specific information:

note

-
If you are configuring both FlashArray and FlashBlade, you can add FlashBlade configuration information in the same file. Refer to the JSON file for more information.

-
Portworx Enterprise refreshes your Everpure credentials every 5 minutes. During each cycle, Portworx Enterprise reads the `pure.json` configuration from the secret store (Kubernetes or Vault) and updates the internal device registry. If you add new FlashArray or FlashBlade entries to `pure.json`, Portworx Enterprise automatically discovers and registers them within approximately 5 minutes. No restart or manual intervention is required.

-
By default, Portworx Enterprise encrypts management traffic to FlashArray systems but does not verify their certificates. To verify the identity of each FlashArray, configure SSL certificate verification in `pure.json`. For more information, see Enable SSL Certificate Verification for FlashArray and FlashBlade.

- FlashArray without secure multi-tenancy

- FlashArray with secure multi-tenancy

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<fa-management-endpoint>",

      "APIToken": "<fa-api-token>"

    }

  ]

}

```

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<fa-management-endpoint1>",

      "APIToken": "<fa-api-token>",

      "Realm": "<fa-realm>"

    }

  ]

}

```

## Add FlashArray configuration to a secret store provider​

- Kubernetes

- Vault

To enable Portworx Enterprise to access the FlashArray configuration, add the `pure.json` file to a Kubernetes secret by running the following command to create a secret named `px-pure-secret`:

```

kubectl create secret generic px-pure-secret --namespace <stc-namespace> --from-file=pure.json=<file path>

```

```

secret/px-pure-secret created

```

important

- The specific name `px-pure-secret` is required so that Portworx Enterprise can correctly identify and access the Kubernetes secret upon startup. This secret securely stores the FlashArray configuration details and allows Portworx Enterprise to access this information within the Kubernetes environment.

- Ensure that the `px-pure-secret` is in the same namespace where you plan to install Portworx Enterprise.

When using Portworx with Pure Storage FlashArray, you can supply the FlashArray credentials by creating a secret in Vault. Follow the steps below to properly create and verify the secret.

#### Step 1: Create the Secret​

Store FlashArray credentials (that include management endpoint and API token) as key-value pairs at the path `secret/pureJson`. If you are not using a custom backend path, use `secret` as shown. If you are using a custom secret path, replace secret with your custom path.

Run the following command, substituting the placeholder values with your actual credentials:

```

vault kv put secret/pureJson pure.json=<contents of the pure.json configuration file>

```

If your custom secret path is, for example, customPath:

```

vault kv put customPath/pureJson pure.json=<contents of the pure.json configuration file>

```

#### Step 2: Retrieve and Verify the Secret​

To ensure that the secret was created correctly, use this command:

```

vault kv get secret/pureJson

```

The command should return an output similar to the following:

```

========== Data ==========

Key                 Value

---                 -----

pure.json         {

                      "FlashArrays": [

                        {

                          "MgmtEndPoint": "<fa-management-endpoint>",

                          "APIToken": "<fa-api-token>"

                        }

                      ]

                    }

```

## Configure FlashArray connectivity​

- iSCSI

- NVMe-oF/TCP

- NVMe-oF RDMA

If you are using the iSCSI protocol, follow the instructions below to verify the iSCSI setup:

-
Run the following command from the node to discover your iSCSI targets:

```

iscsiadm -m discovery -t st -p <flash-array-interface-endpoint>

```

```

10.13.xx.xx0:3260,207 iqn.2010-06.com.purestorage:flasharray.xxxxxxx

10.13.xx.xx1:3260,207 iqn.2010-06.com.purestorage:flasharray.xxxxxxx

```

-
Run the following command on each node to verify if each node has a unique initiator:

```

cat /etc/iscsi/initiatorname.iscsi

```

```

InitiatorName=iqn.1994-05.com.redhat:xxxxx

```

-
If the initiator names are not unique, assign a new unique initiator name using the following command:

```

echo "InitiatorName=`/sbin/iscsi-iname`" > /etc/iscsi/initiatorname.iscsi

```

important

Replace the initiator names on any nodes that have duplicates with the newly generated unique names.

-
After making changes to the initiator names, restart the iSCSI service to apply the changes:

```

systemctl restart iscsid

```

If you are using the NVMe-oF/TCP protocol, complete the following steps to ensure that the prerequisites are met and optimize performance for FlashArray.

#### Prerequisites​

-
Supported Operating System: RHEL 9.4 and Ubuntu 22.04

-
Supported Multipath version: `multipath-tools` (0.8.7 or later)

-
Supported NVMe CLI version

Operating SystemNVMe CLI version

- RHEL version earlier than 9.4

- Ubuntu version earlier than 22.04

Version 1.16

- RHEL version 9.4 to 9.5

- Ubuntu version 22.04 or later

Version 2.6

RHEL version 9.6 or laterVersion 2.11

-
Ensure that device mapper multipath is used by default. To verify, check if the multipath parameter exists under `/sys/module/nvme_core/parameters/`. If it exists, it should be set to `N`, which indicates that native NVMe multipath is supported but disabled. If there is no multipath parameter, the kernel doesn’t support native NVMe multipath, and device mapper multipath is used by default, which is expected.

```

modprobe nvme_core

cat /sys/module/nvme_core/parameters/multipath  # Should return `N`

```

Disabling native NVMe multipath on OpenShift Container Platform

If the command returns Y, indicating that native NVMe multipath is enabled, apply the following MachineConfig to disable it:

```

  apiVersion: machineconfiguration.openshift.io/v1

kind: MachineConfig

metadata:

  name: set-kernel-args

  labels:

    machineconfiguration.openshift.io/role: worker

spec:

  kernelArguments:

    - nvme_core.multipath=N

```

-
Make sure that NVMe-oF/TCP interface is enabled in FlashArray.

#### Optimize NVMe Performance Settings​

The following settings are recommended to optimize performance and ensure that NVMe storage devices function efficiently within a multipath environment:

-
Disable I/O Scheduler: NVMe devices manage their own queuing and prioritize requests, making kernel-level I/O scheduling unnecessary.

```

cat /sys/block/nvme0n1/queue/scheduler  # Should return '[none] mq-deadline'

```

-
Enable blk-mq: Enabling block multi-queue (blk-mq) for multipath devices allows the system to use multiple I/O queues, improving parallel request handling.

```

cat /sys/module/dm_mod/parameters/use_blk_mq  # Should return 'Y'

```

After modifying the configuration, restart the multipathd service:

```

systemctl restart multipathd.service

```

#### Verify NVMe Qualified Name (NQN)​

After installing the NVMe CLI, verify the NVMe Qualified Name (NQN) on all nodes:

-
Run the following command on each node to verify whether each node has a unique NVMe Qualified Name (NQN):

```

cat /etc/nvme/hostnqn

```

```

nqn.2014-08.org.nvmexpress:uuid:xxxxxxx-xxxx-xxxx-xxxx-c6412d6e0e77

```

-
If the NQNs are not unique, assign a new name using the following command to prevent potential conflicts in networked environments:

```

nvme gen-hostnqn > /etc/nvme/hostnqn

```

By ensuring that these settings are properly configured, you can optimize NVMe performance and maintain stable connectivity with FlashArray in an NVMe-oF/TCP environment.

tip

On OpenShift Container Platform, to automatically generate a unique host NQN when a new node boots, you can apply a `MachineConfig` that creates a systemd service. The following `MachineConfig` generates the NQN once and then disables the service:

```

apiVersion: machineconfiguration.openshift.io/v1

kind: MachineConfig

metadata:

  name: 99-generate-hostnqn-once

  labels:

    machineconfiguration.openshift.io/role: worker

spec:

  config:

    ignition:

      version: 3.2.0

    systemd:

      units:

        - name: generate-hostnqn.service

          enabled: true

          contents: |

            [Unit]

            Description=Generate NVMe Host NQN at first boot only

            After=network-online.target

            Wants=network-online.target

            [Service]

            Type=oneshot

            ExecStart=/bin/sh -c '/usr/sbin/nvme gen-hostnqn > /etc/nvme/hostnqn'

            ExecStartPost=/bin/systemctl disable generate-hostnqn.service

            RemainAfterExit=yes

            [Install]

            WantedBy=multi-user.target

```

This service ensures the NQN is generated only once at first boot and won't persist across reboots.

NVMe-oF RDMA can be used with FlashArray Direct Access (FADA) volumes. When you select NVME-oF RDMA during StorageCluster spec generation or specify the protocol in the spec manually, Portworx recognizes that you want to use the NVMe-oF RDMA protocol and uses it to communicate with the FlashArray.

note

- QoS (IOPS and bandwidth) limits are not supported with NVMe volumes.

- In-place upgrades from iSCSI or Fibre Channel to NVMe are not supported. Changing the SAN type might result in unpredictable attachment behavior.

#### Prerequisites​

- Check that your setup meets the requirements in the NVMe-oF RDMA Support Matrix.

- Make sure that your Linux kernel supports NVMe. You need to load the `nvme-fabrics` and `nvme-rdma` modules on boot or include them when you compile the kernel.

- Install the `nvme-cli` package.

- Ensure that all nodes have unique NQN (`/etc/nvme/hostnqn`) and host ID (`/etc/nvme/hostid`) entries.

#### Configure hardware​

Configure your Cisco, Juniper, or Arista switch for use with Pure FlashArray NVMe-oF RDMA.

#### Configure the adapter as a PCI device​

Configure the NVMe-oF RDMA adapter installed in ESXi as a PCI device. For example, on vSphere, follow the steps in Enable Passthrough for a Network Device on a host from the VMware documentation.

Once the NVMe-oF RDMA adapter is set up as a PCI device, the VM can mount as a PCI device and access external storage directly.

#### Use NVMe-oF RDMA in a VM​

If you are using a VM, you also need to perform additional steps to enable and configure PCI passthrough.

The following examples illustrate how to perform these steps for vSphere. Your environment might require different steps.

#### Enable RoCE as PCI passthrough​

After you install a physical adapter, the NVMe-oF RDMA adapter should be listed in PCI Devices.

-
Navigate to a host in the vSphere Client navigator.

-
Select the Configure tab, then under Hardware, select PCI devices.

-
Select all of the NVMe adapters that you have added, then select Toggle passthrough.

When passthrough configurations complete successfully, the device is listed in the Passthrough-enabled devices tab.

#### Configure PCI passthrough in a VM​

-
In the vSphere client, select the VM you want to add the PCI passthrough card to from the list of VMs. Right click the VM, then select Edit settings.

-
Click Add new device, then select PCI device.

-
Select DirectPathIO, then select any of the RoCE adapter interfaces.

Add as many PCI devices for RoCE adapters as you need for the VM. Multiple ports on the FlashArray will provide redundant connections, but for extra redundancy you should add two or more PCI devices in case one device fails.

## Volume attachment limits​

Portworx Enterprise supports up to 1024 volume attachments per node (LUNs for SCSI transports; namespaces for NVMe-oF). The effective limit also depends on the Linux storage stack, the HBA, and driver parameters. Before you deploy Portworx Enterprise, ensure that the operating system (OS) and host bus adapters (HBAs) are configured to support the number of attachments required for your use case.

For Fibre Channel (FC), use the following commands to inspect LUN limits:

-
Identify the adapter type:

```

lspci -nn | grep -i fibre

```

(Look for QLogic or Emulex in the output)

-
Inspect the LUN limits:

-
For QLogic adapters:

```

cat /sys/module/qla2xxx/parameters/ql2xmaxlun

```

-
For Emulex adapters:

```

cat /sys/module/lpfc/parameters/lpfc_max_luns

```

tip

If the LUN limit is lower than the number of volume attachments you plan to use, you can update the LUN limits.

- OpenShift Container Platform

- Other Kubernetes platforms

Use the following MachineConfig to update the kernel arguments on all nodes:

- QLogic

- Emulex

```

apiVersion: machineconfiguration.openshift.io/v1

kind: MachineConfig

metadata:

  name: fc-lun-update

  labels:

    machineconfiguration.openshift.io/role: worker

spec:

  kernelArguments:

    - scsi_mod.max_luns=65535

    - qla2xxx.ql2xmaxlun=65535

```

```

apiVersion: machineconfiguration.openshift.io/v1

kind: MachineConfig

metadata:

  name: fc-lun-update

  labels:

    machineconfiguration.openshift.io/role: worker

spec:

  kernelArguments:

    - scsi_mod.max_luns=65535

    - lpfc.lpfc_max_luns=65535

  config:

    ignition:

      version: 3.2.0

    storage:

      files:

        - path: /etc/modprobe.d/lpfc.conf

          mode: 0644

          contents:

            source: data:text/plain;base64,b3B0aW9ucyBscGZjIGxwZmNfbWF4X2x1bnM9NjU1MzU=

```

Manually run the following commands on all nodes:

- QLogic

- Emulex

```

echo "options qla2xxx ql2xmaxlun=65535" > /etc/modprobe.d/qla2xxx.conf

dracut -f

reboot

```

```

echo "options lpfc lpfc_max_luns=65535" > /etc/modprobe.d/lpfc.conf

dracut -f

reboot

```

In this topic:
