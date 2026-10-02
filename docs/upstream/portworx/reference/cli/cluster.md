# Cluster operations using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/cluster (Portworx Enterprise 3.6)

Cluster operations using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document outlines how to manage your Portworx cluster operation with `pxctl cluster`. Run the `/opt/pwx/bin/pxctl cluster` with the `--help` flag to list the available subcommands and flags.

## Listing all nodes in a cluster​

To list all nodes in your Portworx cluster, run:

```

pxctl cluster list

```

```

Cluster ID: xxxxxxxx-xxxx-xxxx-xxxx-0242ac110002

Status: OK

Nodes in the cluster:

ID					DATA IP		CPU		MEM TOTAL	MEM FREE	CONTAINERS	VERSION		STATUS

xxxxxxxx-xxxx-xxxx-xxxx-4782959264bc	X.X.X.243	0.125078	34 GB		33 GB		N/A		1.1.4-6b35842	Online

xxxxxxxx-xxxx-xxxx-xxxx-de2699fa39b4	X.X.X.171	0.187617	34 GB		33 GB		N/A		1.1.4-6b35842	Online

xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5	X.X.X.189	0.125078	34 GB		33 GB		N/A		1.1.4-6b35842	Online

```

## Inspecting a node​

Use the following command to get information on a node in the cluster:

```

pxctl cluster inspect xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5

```

```

ID       	:  xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5

Mgmt IP  	:  X.X.X.189

Data IP  	:  X.X.X.189

CPU      	:  0.8755472170106317

Mem Total	:  33697398784

Mem Used 	:  702279680

Status  	:  Online

Containers:	There are no running containers on this node.

```

## Deleting a node in a cluster​

Here is how to delete a node:

```

pxctl cluster delete xxxxxxxx-xxxx-xxxx-xxxx-4782959264bc

```

```

node xxxxxxxx-xxxx-xxxx-xxxx-4782959264bc deleted successfully

```

Run the `pxctl cluster delete` with the `--help` flag to list the available subcommands and flags.

### Related topics​

- For more information about decommissioning a Portworx node through Kubernetes, refer to the Decommission a Node page.

## Showing nodes based on IO Priority​

To list the nodes in your Portworx cluster based on IO Priority (high, medium and low), type:

```

pxctl cluster provision-status --io_priority low

```

```

Node					Node Status	Pool	Pool Status	IO_Priority	Size	Available	Used	Provisioned	ReserveFactor	Zone	Region

xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5	Online		0	Online		LOW		100 GiB	99 GiB		1.0 GiB	0 B		default	default

xxxxxxxx-xxxx-xxxx-xxxx-bc72878d4be5	Online		1	Online		LOW		200 GiB	199 GiB		1.0 GiB	0 B		50		default	default

xxxxxxxx-xxxx-xxxx-xxxx-de2699fa39b4	Online		0	Online		LOW		100 GiB	92 GiB		8.2 GiB	70 GiB		default	default

xxxxxxxx-xxxx-xxxx-xxxx-4782959264bc	Online		0	Online		LOW		150 GiB	149 GiB		1.0 GiB	0 B		default	default

```

Run the `pxctl cluster provision-status` command with the `--help` flag to list the available subcommands and flags.

## Enabling optimized restores​

With Portworx Enterprise 2.1.0, users can choose to do optimized restores. The way this works is that every successful restore creates a snapshot that will be used for the next incremental restore of the same volume. Hence, for an incremental restore, only the last incremental backup will be downloaded instead of downloading all the dependent backups. Optimized restores are especially useful for workflows that involve frequent restores from a different cluster. However, this works only if dependent backups were downloaded previously.

Currently, to enable or disable optimized restores, you must use the `pxctl cluster options` command.

Run the `pxctl cluster options` command with the `--help` flag to list the available subcommands and flags.

Use the following command to list the options:

```

pxctl cluster options list

```

```

Auto decommission timeout (minutes)  :  20

Replica move timeout (minutes)       :  1440

Internal Snapshot Interval (minutes) :  30

Re-add timeout (minutes)             :  1440

Resync repl-add                      :  off

Domain policy                        :  strict

Optimized Restores                   :  off

```

Use the following command to enable optimized restores:

```

pxctl cluster options update --optimized-restores on

```

```

Successfully updated cluster wide options

```

Let's make sure the new settings were applied:

```

pxctl cluster options list

```

```

Auto decommission timeout (minutes)  :  20

Replica move timeout (minutes)       :  1440

Internal Snapshot Interval (minutes) :  30

Re-add timeout (minutes)             :  1440

Resync repl-add                      :  off

Domain policy                        :  strict

Optimized Restores                   :  on

```

## Use a network interface for cloudsnaps​

By default, cloudsnaps do not use a specific network interface to upload/download the cloudsnap data. Instead, the underlying Go libraries determine the network interface. If you need to use a specific network interface, you can set one using the `--cloudsnap-nw-interface` option. Setting this option directs Portworx to use the specified interface for all cloudsnap related operations.

This is a cluster-wide setting, meaning that the chosen network interface must be available on all nodes. If the chosen network interface is not available, Portworx falls-back to the "no interface chosen" default behavior.

To enable this feature, enter the following `pxctl cluster options update` command with the `--cloudsnap-nw-interface` option and specify your desired network interface and confirm at the prompt:

```

pxctl cluster options update --cloudsnap-nw-interface <your-network-interface>

```

```

Currently cloudsnap network interface is set to :data, changing this will affect new cloudsnaps and not the current onesDo you still want to change this now? (Y/N): y

Successfully updated cluster wide options

```

## Configure retry limit on an error​

You can configure the number of retries for an error from the object store. These retries are performed with a 10-second backoff delay, followed by progressively longer delays (incrementing by 10-second intervals) between each attempt. If the object store has multiple IP addresses as the endpoints, then for a given request, the retries are done on each of these endpoints.

Set the limit by running the `pxctl cluster options update` command with the `--cloudsnap-err-retry-limit` option, as shown in the following example:

```

pxctl cluster options update --cloudsnap-err-retry-limit 7

```

```

Successfully updated cluster-wide options

```

Verify if the limit is set.

```

pxctl cluster options list

```

```

Auto decommission timeout (minutes)  :  20

Replica move timeout (minutes)       :  1440

Internal Snapshot Interval (minutes) :  30

Re-add timeout (minutes)             :  1440

Resync repl-add                      :  off

Domain policy                        :  strict

Optimized Restores                   :  on

Cloudsnap Error Retry Limit          :  7

```

### Related topics​

- For more information about creating and managing the snapshots of your Portworx volumes through Kubernetes, refer to the Create and use snapshots page.

## pxctl cluster options update --provisioning-commit-labels reference​

```

--provisioning-commit-labels '[{"OverCommitPercent": <percent_value>, "SnapReservePercent": <percent_value>, "LabelSelector": {"<label_key>": "<label_value>"}},{"OverCommitPercent": <percent_value>, "SnapReservePercent":<percent_value>} ]'

```

KeyDescriptionValue

OverCommitPercentThe maximum storage percentage volumes can provision against backing storageAny integer over 100

SnapReservePercentThe percent of the previously specified maximum storage storage percentage that is reserved for snapshotsAny integer under 100

labelSelectorThe key values for labels or node IDs you wish to apply this rule toEnumerated string: `node` with a comma separated list of node IDs
 Any existing label key and value.

## Configure cache flush operations​

On systems with a large amount of memory and heavy IO activity, system memory and page cache experience a lot of activity, resulting in significant memory pressure. On these systems, the Portworx storage process may slow down or get stuck trying to allocate memory.

To prevent Portworx from slowing or getting stuck, you can preemptively drop system memory pages which are not currently in use, i.e. pages which are inactive and not dirty.

You can configure cache flush operations for all nodes on the cluster using flags with the `pxctl cluster options update` command.

note

- This command is intended for advanced users only.

- This operation drops all cached pages for all devices and may impact read performance; you should only apply the config when necessary.

- Legacy support for cache flush was enabled through an environment variable: `PX_ENABLE_CACHE_FLUSH="true"`. As long as the cache flush feature has not been enabled, Portworx still checks for this env var when a node starts and will enable cache flushing if it's set to `true`. If you disable cache flush using the `pxctl` command, cache flush will be disabled regardless of whether the env var is set to `true` or not.

### Enable cache flush operations​

Enter the `pxctl cluster options update` command with the `--cache-flush` flag set to `enabled`:

```

pxctl cluster options update --cache-flush enabled

```

```

Successfully updated cluster wide options

```

### Disable cache flush operations​

Enter the `pxctl cluster options update` command with the `--cache-flush` flag set to `disabled`:

```

pxctl cluster options update --cache-flush disabled

```

```

Successfully updated cluster wide options

```

### Configure the cache flush interval​

Enter the `pxctl cluster options update` command with the `--cache-flush-seconds` flag followed by your desired cache flush interval in seconds:

```

pxctl cluster options update --cache-flush-seconds 60

```

```

Successfully updated cluster wide options

```

note

You can specify the `--cache-flush-seconds` flag alongside the `--cache-flush` flag in a single command:

```

pxctl cluster options update --cache-flush enabled --cache-flush-seconds 300

```

### Check cache flush configuration​

To see if cache flush is enabled and see what the current interval is, enter the `pxctl cluster options list` command:

```

pxctl cluster options list

```

```

...

Cache flush                                             : enabled

Cache flush interval in seconds                         : 30

```

## Configure sentinel mount cleanup interval and timeout​

Sentinel Mount is a Portworx feature that enhances the efficiency and scalability of Sharedv4 (NFS) volume mounts in Kubernetes environments. When multiple pods on the same node mount the same Sharedv4 volume, Portworx typically performs an NFS mount for each pod. This leads to redundant NFS connections, increased mount table entries, and complex cleanup operations. To address this, Portworx uses a sentinel mount - a single, canonical NFS mount per volume per node. The first pod creates the NFS mount (the sentinel), and subsequent pods use lightweight bind mounts to access the same volume path, avoiding repeated NFS mount operations.

Portworx Enterprise allows you to configure the interval and timeout for cleaning up sentinel mounts. A background thread performs sentinel mount cleanup at regular intervals. During cleanup, the system only removes sentinel mounts that have exceeded their time-to-live (TTL).

Sentinel mounts only apply to Sharedv4 volumes. You can adjust the cleanup interval and TTL to match your environment and workload requirements.

- You can set the cleanup interval between 10 and 3,600 seconds (1 hour). The default value is 300 seconds.

- You can set the cleanup timeout between 0 and 86,400 seconds (1 day). The default value is 0 seconds.

-
Run the following command to list available options:

```

pxctl cluster options list | grep sentinel

```

```

Sharedv4 sentinel cleanup timeout (seconds)             : 0

Sharedv4 sentinel cleanup interval (seconds)            : 300

```

-
To update the timeout value, run the following command:

```

pxctl cluster options update --sharedv4-sentinel-cleanup-timeout-sec 10

```

```

Successfully updated cluster-wide options

```

-
To update the interval value, run the following command:

```

pxctl cluster options update --sharedv4-sentinel-cleanup-interval-sec 100

```

```

Successfully updated cluster-wide options

```

Run the `pxctl cluster options list` command again to verify that the new settings have been applied.

```

pxctl cluster options list | grep sentinel

```

```

Sharedv4 sentinel cleanup timeout (seconds)             : 10

Sharedv4 sentinel cleanup interval (seconds)            : 100

```

## Configure Portworx token timeout​

Use the following command to configure the Portworx token timeout. Configuring this value helps prevent token expiration during high-load or delayed KVDB operations.

```

pxctl cluster options update --runtime-options px_token_timeout_minutes=<value>

```

```

Successfully updated cluster-wide options

```

Replace `<value>` with the desired timeout value in minutes. The minimum value is 3 minutes.

Retain the values previously defined in `--runtime-options` along with the above parameter. For more information, see Set runtime options.

## Configure `StorageClass` validation for clones​

Portworx Enterprise can clone a volume or a snapshot. Before creating a clone, Portworx compares the properties of the source with the parameters in the destination `StorageClass`. Validated properties include backend type, Kube Datastore affinity, replication factor, volume mode, I/O profile, format, shared volume settings, Sharedv4 settings, sticky flag, journal, compression, deduplication, discard behavior, fast path, encryption, near-sync replication, automatic file system trim, copy-on-write on demand, aggregation level, scale, snapshot interval, snapshot schedule, and volume labels.

The default validation behavior depends on the clone source:

- Volume: Portworx enforces `StorageClass` validation. If a source property is incompatible with the destination `StorageClass`, Portworx rejects the clone.

- Snapshot: Portworx skips `StorageClass` validation. It allows cloning across StorageClasses with different parameters and raises a warning if validation detects an infrastructure mismatch.

note

This behavior applies when `disable-clone-sc-validation` is not configured and matches the behavior of releases earlier than Portworx Enterprise 3.7.0.

To change the validation behavior, set the `disable-clone-sc-validation` runtime option:

```

pxctl cluster options update --runtime-options "disable-clone-sc-validation=<value>"

```

```

Successfully updated cluster-wide options

```

Replace `<value>` with one of the following values:

ValueValidation behavior

`snapshot`Skips validation for snapshot-to-volume clones and enforces validation for volume-to-volume clones. Portworx raises a warning if snapshot validation detects an infrastructure mismatch. This is the default behavior when `disable-clone-sc-validation` is not configured.

`volume`Skips validation for volume-to-volume clones.

`none`Enforces validation for both volume-to-volume and snapshot-to-volume clones.

`all`Skips validation for both volume-to-volume and snapshot-to-volume clones.

important

The `--runtime-options` flag replaces the complete set of runtime options. Include all existing runtime options in the command when you set `disable-clone-sc-validation`. Otherwise, Portworx removes the omitted options from the runtime configuration. For more information, see Set runtime options.

Verify the runtime options:

```

pxctl cluster options list

```

In this topic:
