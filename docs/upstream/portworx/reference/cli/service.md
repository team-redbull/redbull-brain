# Service operations using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/service (Portworx Enterprise latest)

Service operations using pxctl | Portworx Enterprise Documentation

The Portworx `pxctl` CLI tool allows you to run the following service operations:

- Perform a node audit

- Manage the call home feature

- Generate diagnostics package

- Get the version of the installed software

- Configure kvdb

- Place Portworx in maintenance mode

- Manage the physical storage drives

These commands are helpful when you want to debug issues related to your Portworx cluster.

You can see an overview of the available service operations by running the following command:

```

/opt/pwx/bin/pxctl service --help

```

## Perform a node audit​

You can audit the node with:

```

pxctl service audit

```

```

AuditID		Error	Message

kvdb-limits	none	KV limits audit not yet available

kvdb-response	none	KV response audit not yet available

```

## Manage the call home feature​

With `pxctl`, you can enable and disable the call home feature:

```

pxctl service call-home enable

```

```

Call home feature successfully enabled

```

If you want to disable this feature, just run:

```

pxctl service call-home disable

```

```

Call home feature successfully disabled

```

## Generate a complete diagnostics package​

When there is an operational failure, you can use the `pxctl service diags` command to generate a complete diagnostics package. Run the `pxctl service diags` command with the `--help` flag to list the available subcommands and flags.

The diagnostics package will be available at `/var/cores`. It will be automatically uploaded to Pure1 if telemetry is enabled.

See Enable Pure1 integration for details on enabling Pure1 telemetry.

To collect diagnostics at the cluster level using the Portworx Operator, see On-demand diagnostics using `PortworxDiag` custom resource.

As an example, here's how to generate the diagnostics package for a container called `px-enterprise`:

```

pxctl service diags -a

```

```

Connected to Docker daemon.  unix:///var/run/docker.sock

Running PX diagnostics on local node....

Using PX OCI container: <PX_VERSION>-<BUILD_HASH>

Archived cores to: /var/cores/test-k8s1-node0-px-cores.20210514230349.tgz, cleaning up archived cores...

Removing /var/cores/core-px-storage-sig6-user0-group0-pid312-time1620773250...

Getting diags file....

Creating a diags tar ball...

Executing core cleanup...

Finished core cleanup.

Removing /var/cores/test-k8s1-node0-px-cores.20210514230349.tgz...

Generated diags:  /var/cores/test-k8s1-node0-diags-20210514230401.tar.gz

Done generating PX diagnostics.

```

Note: <PX_VERSION> and <BUILD_HASH> reflect the Portworx version and the respective hash.

## Get the version of the installed software​

The following command displays the version of the installed software:

```

pxctl service info

```

```

PX (OCI) Version:  <PX_VERSION>

PX (OCI) Build Version:  <BUILD_HASH>

PX Kernel Module Version:  <KERNEL_MODULE_VERSION>

```

Note:

- <PX_VERSION> and <BUILD_HASH> reflect the Portworx version and the respective hash.

- <KERNEL_MODULE_VERSION> reflects the kernel module version used by Portworx.

## Configure KVDB​

You can configure the KVDB with the `pxctl service kvdb` command. Run the `pxctl service kvdb` command with the `--help` flag to list the available subcommands and flags.

## Place Portworx in maintenance mode​

Use the `pxctl service maintenance` command to enter or exit maintenance mode. Once the node is in maintenance mode, you can add or replace drives, add memory, and so on.

Run the `pxctl service maintenance` command with the `--help` flag to list the available subcommands and flags.

Enter maintenance mode with:

```

pxctl service maintenance --enter

```

```

This is a disruptive operation, PX will restart in maintenance mode.

Are you sure you want to proceed ? (Y/N): y

```

Once you're done adding or replacing drives, or adding memory, you can exit maintenance mode by running:

```

pxctl service maintenance --exit

```

## Manage the physical storage drives​

You can manage the physical storage drives on a node using the `pxctl service drive` command. Run the `pxctl service drive` command with the `--help` flag to list the available subcommands and flags.

### Add a physical drive to a server​

Use the `pxctl service drive add` command to add a physical drive to a server. Run the `pxctl service drive add` command with the `--help` flag to list the available subcommands and flags.

The following example shows how to add a physical drive:

```

pxctl service drive add --drive /dev/mapper/volume-3bfa72dd -o start

```

```

Adding drives may make storage offline for the duration of the operation.

Are you sure you want to proceed ? (Y/N): y

Adding device  /dev/mapper/volume-3bfa72dd ...

Drive add  successful. Requires restart.

```

note

To add physical drives, you must place the server in maintenance mode first.

## Rebalance storage across drives​

Over time, your cluster's storage may become unbalanced, with some pools and drives filled to capacity and others utilized less. This can occur for a number of reasons, such as:

- Adding new nodes or pools

- Increasing the size of pools by increasing the size of underlying drives or adding new drives

- Volumes being removed from only a subset of nodes

If your cluster's storage is unbalanced, you can use the `pxctl service pool rebalance` command to redistribute the volume replicas. This command determines which pools are over-loaded and under-loaded, and moves volume replicas from the former to the latter. This ensures that all pools on the nodes are evenly loaded.

note

You can run this cluster-wide command from any of your Portworx nodes.

### Start a rebalance operation​

Use the `submit` subcommand to start the rebalance operation, which returns a job ID:

```

pxctl service pool rebalance submit

```

```

This command will start rebalance for:

 - all storage pools for checking if they are over-loaded

 - all storage pools for checking if they are under-loaded

which meet either of following conditions:

1. Pool's provision space is over 20% or under 20% of mean value across pools

2. Pool's used space is over 20% or under 20% of mean value across pools

*Note: --remove-repl-1-snapshots is off, space from such snapshots will not be reclaimed

Do you wish to proceed ?  (Y/N): Y

Pool rebalance request: 859941020356581382 submitted successfully.

For latest status: pxctl service pool rebalance status --job-id 859941020356581382

```

note

The rebalance operation runs as a background service.

### List running rebalance jobs​

Enter the `list` subcommand to see all currently running jobs:

```

pxctl service pool rebalance list

```

```

JOB			STATE	CREATE TIME			STATUS

859941020356581382	RUNNING	2020-08-11T11:16:12.928785518Z

```

### Monitor a rebalance operation​

Monitor the status of a rebalance operation, as well as all the steps it has taken so far, by entering the `status` subcommand with the `--job-id` flag and the ID of a running rebalance job:

```

pxctl service pool rebalance status --job-id 859941020356581382

```

```

Rebalance summary:

Job ID             : 859941020356581382

Job State          : DONE

Last updated       : Sun, 23 Aug 2020 22:08:31 UTC

Total running time : 4 minutes and 25 seconds

Job summary

    - Provisioned space balanced : 827 GiB done, 0 B pending

    - Used space balanced        : 17 GiB done, 0 B pending

    - Volume replicas balanced   : 42 done, 0 pending

Rebalance actions:

Replica add action:

        Volume             : 956462089713112944

        Pool               : xxxxxxxx-xxxx-xxxx-xxxx-eaca75365214

        Node               : xxxxxxxx-xxxx-xxxx-xxxx-489393d6636b

        Replication set ID : 0

        Start              : Sun, 23 Aug 2020 22:04:06 UTC

        End                : Sun, 23 Aug 2020 22:04:27 UTC

        Work summary

            - Provisioned space balanced : 20 GiB done, 0 B pending

Replica remove action:

        Volume             : 956462089713112944

        Pool               : xxxxxxxx-xxxx-xxxx-xxxx-5e34a2b712e3

        Node               : xxxxxxxx-xxxx-xxxx-xxxx-81b36fef6177

        Replication set ID : 0

        Start              : Sun, 23 Aug 2020 22:04:06 UTC

        End                : Sun, 23 Aug 2020 22:04:29 UTC

        Work summary

            - Provisioned space balanced : 20 GiB done, 0 B pending

```

### Pause or terminate a running rebalance operation​

If you need to temporarily suspend a running rebalance operation, you can pause it. Otherwise, you can cancel it entirely:

-
Use the `cancel` subcommand with the `--job-id` flag and the ID of a running rebalance job to terminate a running rebalance operation:

```

pxctl service pool rebalance cancel --job-id 859941020356581382

```

-
Use `pause` subcommand with the `--job-id` flag and the ID of a running rebalance job to terminate a running rebalance operation:

```

pxctl service pool rebalance pause --job-id 859941020356581382

```

### pxctl service pool rebalance reference​

Rebalance storage pools

```

pxctl service pool rebalance [command] [flags]

```

#### Commands​

CommandDescription

cancelCancels a rebalance job specified with the `--job-ID` flag and a valid job ID

listLists rebalance jobs in the system

pausePauses a rebalance job specified with the `--job-ID` flag and a valid job ID

resumeResumes a rebalance job specified with the `--job-ID` flag and a valid job ID

statusShows the status of a rebalance job specified with the `--job-ID` flag and a valid job ID

submitStart a new rebalance job

## Display drive information​

You can use the `pxctl service drive show` command to display drive information on the server:

```

pxctl service drive show

```

```

PX drive configuration:

Pool ID: 0

	Type:  Default

	UUID:  xxxxxxxx-xxxx-xxxx-xxxx-2b69eeebb81b

	IO Priority:  HIGH

	Labels:  medium=STORAGE_MEDIUM_MAGNETIC,beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,iopriority=HIGH,kubernetes.io/arch=amd64,kubernetes.io/hostname=myhostname-k8s1-node0,kubernetes.io/os=linux

	Size: 3.0 TiB

	Status: Online

	Has metadata:  Yes

	Balanced:  Yes

	Drives:

	3: /dev/vdd, Total size 1.0 TiB, Online

	1: /dev/vdb, Total size 1.0 TiB, Online

	2: /dev/vdc, Total size 1.0 TiB, Online

	Cache Drives:

	No Cache drives found in this pool

```

## Configure the email settings for alerts​

You can use the `pxctl service email` command to list the available subcommands:

```

pxctl service email

```

```

Usage:

  pxctl service email [flags]

  pxctl service email [command]

Available Commands:

  clear       Clear email settings for alerts.

  get         Get email settings for alerts.

  set         Configure email settings for alerts.

Flags:

  -h, --help   help for email

Global Flags:

      --ca string            path to root certificate for ssl usage

      --cert string          path to client certificate for ssl usage

      --color                output with color coding

      --config string        config file (default is $HOME/.pxctl.yaml)

      --context string       context name that overrides the current auth context

  -j, --json                 output in json

      --key string           path to client key for ssl usage

      --output-type string   use "wide" to show more details

      --raw                  raw CLI output for instrumentation

      --ssl                  ssl enabled for portworx

```

#### pxctl service email set​

Run the `pxctl service email set` command with the `--help` flag to list the available subcommands and flags.

Receive Warning and Critical alerts:

```

/opt/pwx/bin/pxctl service email set --server=smtp.gmail.com --smtp-port=587 --username=username@company.com --password='IncrediblySecretPassword' --recipient=username@company.com --severity warning

```

Receive Only Critical alerts:

```

/opt/pwx/bin/pxctl service email set --server=smtp.gmail.com --smtp-port=587 --username=username@company.com --password='IncrediblySecretPassword' --recipient=username@company.com

```

note

You must add single quotes around the password.

## Scan for bad blocks​

You can use `pxctl service scan` to scan for bad blocks on a drive. Run the `pxctl service scan` command with the `--help` flag to list the available subcommands and flags.

## Delete all Portworx related data​

With `pxctl service node-wipe`, you can delete all data related to Portworx from the node. It will also wipe the storage device that was provided to Portworx. This command can be run only when Portworx is stopped on the node. Run this command if a node needs to be re-initialized.

Run the `pxctl service node-wipe` command with the `--help` flag to list the available subcommands and flags.

note

This is a disruptive command and could lead to data loss. Please use caution.

Here is an example:

```

pxctl service node-wipe

```

```

This is a disruptive operation.

It will delete all PX configuration files from this node. Data on the storage disks attached on this node will be irrevocably deleted.

Executing manual log rotation logs...

Failed to set pxd timeout. Wipe command might take more time to finish.

Removed PX footprint from device /dev/sdc.

Wiped node successfully.

```

## Perform pool maintenance tasks​

The `pxctl service pool` command allows you to run the following pool maintenance related tasks:

- list the available pools

- update the properties of a pool

You can list the available subcommands with:

```

pxctl service pool

```

```

Usage:

  pxctl service pool [flags]

  pxctl service pool [command]

Available Commands:

  cache       Update cache properties on a given pool

  expand      Expand pool

  maintenance Pool maintenance

  rebalance   Rebalance storage pools

  show        Show pools

  update      Update pool properties

Flags:

  -h, --help   help for pool

Global Flags:

      --ca string            path to root certificate for ssl usage

      --cert string          path to client certificate for ssl usage

      --color                output with color coding

      --config string        config file (default is $HOME/.pxctl.yaml)

      --context string       context name that overrides the current auth context

  -j, --json                 output in json

      --key string           path to client key for ssl usage

      --output-type string   use "wide" to show more details

      --raw                  raw CLI output for instrumentation

      --ssl                  ssl enabled for portworx

```

## Update pool properties​

You can use the `pxctl service pool update` command to perform the following operations:

- Set the IO priority

- Add labels

Run the `pxctl service pool update` command with the `--help` flag to list the available subcommands and flags.

#### Understand the --labels flag behavior​

The `--labels` flag allows you to add, remove, and update labels for your storage pools.
 Add a new label​
Enter the `pxctl service pool update` command with the pool ID and the `--labels` flag with a comma separated list of labels you wish to add:

```

pxctl service pool update 0 --labels  ioprofile=HIGH,media_type=SSD

```

 Replace a label's value​
Enter the `pxctl service pool update` command with the pool ID and the `--labels` flag with a comma separated list of the labels you wish to replace:

```

pxctl service pool update 0 --labels  media_type=NVME

```

Updating a single label does not affect the other labels' stored values.
 Delete a label's value​
Enter the `pxctl service pool update` command with the pool ID and the `--labels` flag with a comma separated list of the labels you wish to delete containing no value:

```

pxctl service pool update 0 --labels  ioprofile=,media_type=

```

## Delete a pool from a node​

If you have a node with multiple pools and you can’t decommission the entire node, you can delete a pool instead. You may need to do this in one of the following scenarios:

- If there's a problem with the drives on one of your pools, you can delete the pool and reinitialize it either without the problematic drive, or with a new drive.

- If you've added more capacity to a pool than you need, you can delete your pool and reinitialize it with fewer drives.

note

- If you want to increase the size of a storage pool, use the `pxctl service drive add` command.

- Portworx won’t delete a pool until you have manually drained the pool of any volumes.

caution

`pxctl service pool delete` is a destructive operation, and all deleted data is not recoverable. Ensure you've taken proper precautions and understand the impact of this operation before running it.

Perform the following steps to delete a pool from a node, and optionally, reinitialize it:

-
Once you have identified which pool you want to delete, list all volumes on that pool:

```

pxctl volume list --pool-uid <pool-uuid>

```

-
For each volume on the node, sequentially reduce its replication factor to `1` to isolate the volumes located in your pool. The following example command reduces the replication factor from `3` to `2`:

```

pxctl volume ha-update --repl=2 --node <node-id> <volume-name>

```

-
Verify that your pool is empty by listing all volumes on the pool again:

```

pxctl volume list --pool-uid <pool-uuid>

```

-
Once your pool is empty, delete your pool:

```

pxctl service pool delete <pool-id>

```

-
(Optional) Reinitialize your pool by entering the `pxctl drive add` command, specifying whatever new and existing drives you want to add:

```

pxctl service drive add --drive /path/to/drive -o start

```

### pxctl service pool show​

Show storage pool information

```

pxctl service pool show

```

```

PX drive configuration:

Pool ID: 0

        IO Priority:  LOW

        Labels:

        Size: 5.5 TiB

        Status: Online

        Has metadata:  No

        Drives:

        0: /dev/sdb, 2.7 TiB allocated of 2.7 TiB, Online

        1: /dev/sdc, 2.7 TiB allocated of 2.7 TiB, Online

        Cache Drives:

        0:0: /dev/nvme0n1, capacity of 745 GiB, Online

                Status:  Active

                TotalBlocks:  762536

                UsedBlocks:  12

                DirtyBlocks:  0

                ReadHits:  487

                ReadMisses:  42

                WriteHits:  1134

                WriteMisses:  7

                BlockSize:  1048576

                Mode:  writethrough

Journal Device:

        1: /dev/sdg1, STORAGE_MEDIUM_MAGNETIC

Metadata  Device:

        1: /dev/sdg2, STORAGE_MEDIUM_MAGNETIC

```

### pxctl service pool cache​

You can use the `pxctl service pool cache command` command to:

- Disable caching on a pool

- Enable caching on a pool

- Force the cache to be flushed

- Check if pool caching is enabled for a pool

Refer to the Pool caching section for more details.

### pxctl service pool delete​

You can use the `pxctl service pool delete` command to delete storage pools which may be misconfigured or otherwise not functioning properly.

```

pxctl service pool delete --help

```

```

Delete pool

Note:

  This operation is supported only on on-prem local disks and AWS cloud-drive

Usage:

  pxctl service pool delete [flags]

Examples:

pxctl service pool delete [flags] poolID

Flags:

  -h, --help   help for delete

Global Flags:

      --ca string            path to root certificate for ssl usage

      --cert string          path to client certificate for ssl usage

      --color                output with color coding

      --config string        config file (default is $HOME/.pxctl.yaml)

      --context string       context name that overrides the current auth context

  -j, --json                 output in json

      --key string           path to client key for ssl usage

      --output-type string   use "wide" to show more details

      --raw                  raw CLI output for instrumentation

      --ssl                  ssl enabled for portworx

```

Before you remove a pool, consider the following requirements:

- Your target pool for deletion must be empty and contain no replicas

- If your target pool for deletion is a metadata pool, it must be readable

- You must have more pools on the node than just your target pool for deletion

- You must place your node in maintenance mode to use this command

The following example deletes a storage pool from a node containing 2 storage pools:

```

pxctl service pool delete 0

```

```

This will permanently remove storage pool and cannot be undone.

Are you sure you want to proceed ? (Y/N): y

Pool 0 DELETED.

```

note

New pools created after a pool deletion increment from the last pool ID. A new pool created after this example would have a pool ID of 2

## Control volume attachments for a node​

Portworx allows you to control volume attachments on a node. You can disable new volume attachments on a node by running the `pxctl service node cordon-attachments`. This operation is called as "cordoning attachments" for a node.

You can re-enable volume attachments by running `pxctl service node uncordon-attachments`. This operation is called as "uncordoning attachments" from a node.

### Cordon attachments on a node​

-
Identify which node you want to cordon attachments from by entering the `pxctl cluster list` command:

```

pxctl cluster list

```

Find the ID of your node in the first column:

```

Cluster ID: local-ddryeu-20-11-17-01-27-43-px-int

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-091e20d68ad1

Status: OK

Nodes in the cluster:

ID					SCHEDULER_NODE_NAME		DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION			Kernel				OS			STATUS

xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0	nathan-docs-root-lasher-3	xx.x.55.225	3.193277	6.1 GB		4.5 GB		N/A		2.6.2.0-b5b1d0c		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

xxxxxxxx-xxxx-xxxx-xxxx-28b223b256a0	nathan-docs-root-lasher-0	xx.x.31.114	12.827004	6.1 GB		4.5 GB		N/A		2.6.2.0-562f049		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

xxxxxxxx-xxxx-xxxx-xxxx-a2a1f157f6be	nathan-docs-root-lasher-2	xx.xx.59.32	3.109244	6.1 GB		4.5 GB		N/A		2.6.2.0-562f049		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

```

-
Enter the `pxctl service node cordon-attachments` command with the `--node string` flag followed by the ID of the node you want to cordon:

```

pxctl service node cordon-attachments --node <node-ID>

```

```

Volume attachments cordoned on node xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0.

Note: Volumes which are already attached on this node will stay attached.

To drain existing attachments use: pxctl service node cordon-attachments submit --node xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0

```

### Uncordon attachments from a node​

To re-enable volume attachments on a node, enter the `pxctl service node uncordon-attachments` command with the `--node string` flag followed by the ID of the node you want to remove the cordon for:

```

pxctl service node uncordon-attachments --node <node-ID>

```

```

Volume attachments re-enabled on node xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0.

```

## Drain volume attachments​

If you have a node with volumes attached to it, you can remove them using the `pxctl service node drain-attachments` command. This command executes volume drain operations as a background job, and will delete all the pods that are using the volumes which are attached on this node.

### Start volume attachment drain operations​

-
Identify which node you want to drain of sharedv4 volumes by entering the `pxctl cluster list` command:

```

pxctl cluster list

```

Find the ID of your desired node in the first column:

```

Cluster ID: local-ddryeu-20-11-17-01-27-43-px-int

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-091e20d68ad1

Status: OK

Nodes in the cluster:

ID					SCHEDULER_NODE_NAME		DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION			Kernel				OS			STATUS

xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0	nathan-docs-root-lasher-3	xx.x.55.225	3.193277	6.1 GB		4.5 GB		N/A		2.6.2.0-b5b1d0c		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

xxxxxxxx-xxxx-xxxx-xxxx-28b223b256a0	nathan-docs-root-lasher-0	xx.x.31.114	12.827004	6.1 GB		4.5 GB		N/A		2.6.2.0-562f049		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

xxxxxxxx-xxxx-xxxx-xxxx-a2a1f157f6be	nathan-docs-root-lasher-2	xx.xx.59.32	3.109244	6.1 GB		4.5 GB		N/A		2.6.2.0-562f049		3.10.0-862.3.2.el7.x86_64	CentOS Linux 7 (Core)	Online

```

-
enter the submit command:

```

pxctl service node drain-attachments submit --node <node-id>

```

```

Drain volume attachments request: 624258766140697912 submitted successfully for node xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0

For latest status: pxctl service node drain-attachments status --job-id 624258766140697912

```

note

The drain command will disable new volume attachments on the node. To re-enable attachments on this node, run the `pxctl service node uncordon-attachments` command.

### List volume attachment drain operations​

If you want to a list of drain operations Portworx has performed, enter the `pxctl service node drain-attachments list` command:

```

pxctl service node drain-attachments list

```

```

JOB			TYPE			STATE	CREATE TIME

624258766140697912	DRAIN_ATTACHMENTS	DONE	2020-11-23T22:49:45.769448246Z

```

### Monitor volume attachment drain operations​

To monitor specific jobs, enter the `pxctl service node drain-attachments status` command with `--job-id` flag, followed by the ID of the specific job you want to see the status for:

```

pxctl service node drain-attachments status --job-id 624258766140697912

```

```

Drain Volume Attachments Summary:

NodeID                   : xxxxxxxx-xxxx-xxxx-xxxx-7fa9e52c59e0

Job ID                   : 624258766140697912

Job State                : DONE

Last updated             : Mon, 23 Nov 2020 22:50:17 UTC

Status                   : all volume attachments removed from this node

Job summary

Total number of volumes attached on this node                   : 0

Total number of volume attachments removed from this node       : 0

Total number of pending volume attachments                      : 0

```

In this topic:
