# pxctl service

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/service-reference (Portworx Enterprise 3.6)

pxctl service | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl service

```

pxctl service

```

#### Description

Service mode utilities

## pxctl service exit

```

pxctl service exit

```

#### Description

Stop the PX daemon

## pxctl service audit

```

pxctl service audit

```

#### Description

Audit the PX node

## pxctl service node-usage

```

pxctl service node-usage <required-argument>

```

#### Description

Volume usage by PX node

#### Example

```

pxctl service node-usage <node-id> "Node-ID" is mandatory

```

## pxctl service info

```

pxctl service info

```

#### Description

Show PX module version information

## pxctl service call-home

```

pxctl service call-home <required-argument>

```

#### Description

Enable or disable the call home feature

#### Example

```

pxctl service call-home <enable|disable>    * Required argument is "enable" or "disable"

```

## pxctl service call-home status

```

pxctl service call-home status

```

#### Description

Check call-home status

## pxctl service node-wipe

```

pxctl service node-wipe

```

#### Description

Wipes PX configuration data on this node

#### Flags

FlagDescription

`--storage_devices`, `-s`

(`str`)

comma-separated list of storage devices to be wiped.

## pxctl service diags

```

pxctl service diags

```

#### Description

creates a new tgz package with essential diagnostic information.

#### Flags

FlagDescription

`--output`, `-o`

(`str`)

output file name

`--dockerhost`

(`str`)

docker host daemon

Default value: `unix:///var/run/docker.sock`

`--container`

(`str`)

PX container ID

`--live`, `-l`

(`bool`)

gets diags from running px

`--upload`, `-u`

(`bool`)

upload diags to cloud

`--profile`, `-p`

(`bool`)

only dump profile

`--all`, `-a`

(`bool`)

creates a new tgz package with all the available diagnostic information.

`--cluster`, `-c`

(`bool`)

generate diags for all the nodes in the cluster.

`--node`, `-n`

(`str`)

generate diags for a specific remote node with the provided NodeIp or NodeID.

`--force`, `-f`

(`bool`)

force overwrite existing diags.

`--collect-cloudsnap-status`

(`bool`)

Collect cloudsnap status for all volumes. Warning - this is a costly operation and may take significant time if there are many volumes.

## pxctl service perf

```

pxctl service perf

```

#### Description

Analyze node performance statistics captured via 'pxctl service dump --nodestats'.

Sections (top-level keys in nodestats JSON):
 coordstats, vol_stats, net_stats, log_stats, targetstats,
 target_vol_stats, target_vol_io_stats, nodepoolstats, pool_stats,
 thread_pool_stats, rm_stats, discard_stats, device_delete_stats,
 relaxed_reclaim_stats, devices_rsets_repl_status.

Groups:
 coordinator: vol_stats, coordstats
 target: targetstats, target_vol_io_stats, target_vol_stats, log_stats
 pool: nodepoolstats, pool_stats, discard_stats
 network: net_stats
 system: thread_pool_stats, rm_stats
 tasks: device_delete_stats, relaxed_reclaim_stats
 health: devices_rsets_repl_status

Unknown top-level keys are also reported as raw JSON for visibility; no smart
diff or correlation is attempted for such sections. If nid is missing it is
treated as nid=0. Correlation across layers is always attempted when possible for
known sections.

## pxctl service perf report

```

pxctl service perf report

```

#### Description

Print a human-readable performance report from nodestats, optionally
filtered by section/group.

By default, fetches stats via gRPC and writes a new snapshot to the
default cache directory (/var/lib/osd/log/px_node_stats/) before
reporting.

When --cache-dir is set, writes the snapshot to that directory instead.

Alternatively, provide a file path as an argument to report from an
existing snapshot file.

#### Example

```

pxctl service perf report --group coordinator,target

```

#### Flags

FlagDescription

`--section`

(`str`)

Comma-separated sections: coordstats, vol_stats, net_stats, log_stats, targetstats, target_vol_stats, target_vol_io_stats, nodepoolstats, pool_stats, thread_pool_stats, rm_stats, discard_stats, device_delete_stats, relaxed_reclaim_stats, devices_rsets_repl_status

`--group`

(`str`)

Comma-separated groups: coordinator, target, pool, network, system, tasks, health

`--cache-dir`

(`str`)

Directory for nodestats files; defaults to /var/lib/osd/log/px_node_stats/

Default value: `/var/lib/osd/log/px_node_stats/`

`--detail`

(`bool`)

Show additional per-message/per-node detail where available (more verbose)

`--latency`

(`bool`)

Show only max latency info (device, max time, reported at) for each IO type (read/write/discard/flush)

`--volumes`

(`str`)

Comma-separated list of volume IDs to include when showing vol_stats

`--sort`

(`str`)

Sort vol_stats by field: reads, writes, iops, bytes (descending order)
Valid values:

- ``

- `reads`

- `writes`

- `iops`

- `bytes`

`--top`

(`int`)

Show only top N volumes after sorting (requires --sort)
Valid range:
0 1000

## pxctl service perf diff

```

pxctl service perf diff <required-argument>

```

#### Description

Compare two nodestats JSON files and show per-section deltas plus a
correlation summary. Files must be produced by 'pxctl service dump
--nodestats' or 'pxctl service perf report'.

#### Example

```

pxctl service perf diff stats.1700000000.json stats.1700000030.json

```

#### Flags

FlagDescription

`--section`

(`str`)

Comma-separated sections: coordstats, vol_stats, net_stats, log_stats, targetstats, target_vol_stats, target_vol_io_stats, nodepoolstats, pool_stats, thread_pool_stats, rm_stats, discard_stats, device_delete_stats, relaxed_reclaim_stats, devices_rsets_repl_status

`--group`

(`str`)

Comma-separated groups: coordinator, target, pool, network, system, tasks, health

`--cache-dir`

(`str`)

Directory with nodestats JSON snapshots; if set without args, diff oldest vs newest

Default value: `/var/lib/osd/log/px_node_stats/`

`--detail`

(`bool`)

Show additional per-message/per-node detail where available (more verbose)

`--metrics`

(`bool`)

Show only Disk and network metrics (KIOPS/MiBps/%) and skip full per-section output and correlation

`--volumes`

(`str`)

Comma-separated list of volume IDs to include when showing vol_stats

## pxctl service perf watch

```

pxctl service perf watch

```

#### Description

Show rolling deltas and correlation across layers from nodestats.

By default, watches the default cache directory (/var/lib/osd/log/px_node_stats/)
for new snapshots written by the PX daemon every 30 seconds. This avoids
race conditions with the daemon's collection.

When --cache-dir is set to a different directory, actively fetches stats
via gRPC and writes new snapshots to that directory.

The --interval value is in seconds, must be >= 30, and is rounded up to
the next multiple of 30 if needed. This aligns with the underlying
nodestats collection window.

#### Example

```

pxctl service perf watch --interval 60 --group coordinator,target

```

#### Flags

FlagDescription

`--interval`

(`int`)

Polling interval in seconds (>= 30; rounded up to multiple of 30)

Default value: `30`

`--section`

(`str`)

Comma-separated sections: coordstats, vol_stats, net_stats, log_stats, targetstats, target_vol_stats, target_vol_io_stats, nodepoolstats, pool_stats, thread_pool_stats, rm_stats, discard_stats, device_delete_stats, relaxed_reclaim_stats, devices_rsets_repl_status

`--group`

(`str`)

Comma-separated groups: coordinator, target, pool, network, system, tasks, health

`--cache-dir`

(`str`)

Directory for nodestats files; defaults to /var/lib/osd/log/px_node_stats/

Default value: `/var/lib/osd/log/px_node_stats/`

`--detail`

(`bool`)

Show additional per-message/per-node detail in each interval (more verbose)

`--samples`

(`int`)

Number of recent samples to use when summarizing trends (default 10)

Default value: `10`

`--metrics`

(`bool`)

Show only Disk and network metrics (KIOPS/MiBps/%) and skip full per-section output and correlation

`--volumes`

(`str`)

Comma-separated list of volume IDs to include when showing vol_stats

## pxctl service perf analyze

```

pxctl service perf analyze

```

#### Description

Analyze nodestats JSON files from a directory over a time range and display
delta metrics (KIOPS/MiBps) for each interval in tabular format.

Use --group or --section to show other sections like net_stats, rm_stats, etc.

Each DiskStat-based section is shown as a table with 5 IO types:
read, write, discard, flush, total.

If more samples exist than --samples allows, the time range is divided
into equal windows and the first sample from each window is used.

#### Example

```

pxctl service perf analyze --start 2025-12-17T10:00:00Z --end 2025-12-17T11:00:00Z

```

#### Flags

FlagDescription

`--cache-dir`

(`str`)

Directory containing nodestats JSON files

Default value: `/var/lib/osd/log/px_node_stats/`

`--start`

(`str`)

Start time filter (RFC3339 or epoch seconds)

`--end`

(`str`)

End time filter (RFC3339 or epoch seconds)

`--samples`

(`int`)

Maximum number of intervals to display (default 10)

Default value: `10`

`--section`

(`str`)

Comma-separated sections: coordstats, vol_stats, net_stats, log_stats, targetstats, target_vol_stats, target_vol_io_stats, nodepoolstats, pool_stats, thread_pool_stats, rm_stats, discard_stats, device_delete_stats, relaxed_reclaim_stats, devices_rsets_repl_status

`--group`

(`str`)

Comma-separated groups: coordinator, target, pool, network, system, tasks, health

`--detail`

(`bool`)

Show additional per-message/per-node detail where available (more verbose)

`--volumes`

(`str`)

Comma-separated list of volume IDs to include when showing vol_stats

`--latency`

(`bool`)

Show only max latency info (device, max time, reported at) for each IO type (read/write/discard/flush)

## pxctl service maintenance

```

pxctl service maintenance

```

#### Description

Maintenance mode operations

#### Flags

FlagDescription

`--exit`, `-x`

(`bool`)

exit maintenance mode

`--enter`, `-e`

(`bool`)

enter maintenance mode

`--cycle`, `-c`

(`bool`)

cycle maintenance mode

## pxctl service email

```

pxctl service email

```

#### Description

Email setting commands

## pxctl service email set

```

pxctl service email set

```

#### Description

Configure email settings for alerts.

#### Flags

FlagDescription

`--server`, `-s`

(`str`)

IP or DNS name for smtp server

`--smtp-port`, `-p`

(`str`)

IP or DNS name for smtp server

`--username`, `-u`

(`str`)

Username to authenticate with smtp-server (if required)

`--password`

(`str`)

Password to authenticate with smtp-server (if required)

`--sender`

(`str`)

Sender of alert emails (defaults to noreply@portworx.com)

Default value: `noreply@portworx.com`

`--recipient`, `-r`

(`str`)

Recipient of alert emails.

`--severity`

(`str`)

Minimum severity for email trigger, (warning|critical)

Default value: `critical`

## pxctl service email get

```

pxctl service email get

```

#### Description

Get email settings for alerts.

## pxctl service email clear

```

pxctl service email clear

```

#### Description

Clear email settings for alerts.

## pxctl service slack

```

pxctl service slack

```

#### Description

Slack setting commands

## pxctl service slack set

```

pxctl service slack set

```

#### Description

Configure slack settings for alerts.

#### Flags

FlagDescription

`--webhookurl`, `-w`

(`str`)

url of the slack webhook

This flag is required.

`--severity`, `-s`

(`str`)

Minimum severity for slack trigger, (warning|critical)

Default value: `critical`

## pxctl service slack get

```

pxctl service slack get

```

#### Description

Get slack settings for alerts.

## pxctl service slack delete

```

pxctl service slack delete

```

#### Description

Delete slack settings for alerts.

## pxctl service drive

```

pxctl service drive

```

#### Description

Storage drive maintenance

## pxctl service drive show

```

pxctl service drive show

```

#### Description

Show drives

#### Flags

FlagDescription

## pxctl service drive add

```

pxctl service drive add

```

#### Description

Add storage

#### Flags

FlagDescription

`--drive`, `-d`

(`str`)

Comma-separated source drives

`--spec`, `-s`

(`str`)

Cloud drive spec in type=<>,size=<> format

`--newpool`

(`bool`)

Use this drive to create a new pool.

`--journal`

(`bool`)

Use this drive as a journal device

`--metadata`

(`bool`)

Use this drive as a system metadata device.

`--use-as-cache`

(`bool`)

Use this drive as a cache device for the given pool (must also specify --pool-id).

`--max-pool-size-tb`

(`int`)

(PX-StoreV2) Hint to construct the pool to allow max size to reach atleast this limit, value in tebibytes. Only applicable during new pool creation.
Valid range:
0 480

`--drives-count`

(`int`)

Specify number of drives to be created. Only applicable during new pool creation using cloud drives.

Default value: `4`
Valid range:
1 32

`--pool-id`, `-p`

(`int`)

Add this drive to the specified existing pool ID. If a pod is specified in the spec, it must be on the same backend as the specified pool.

Default value: `-1`

`--operation`, `-o`

(`str`)

start|status
Valid values:

- `start`

- `status`

Default value: `start`

## pxctl service drive replace

```

pxctl service drive replace

```

#### Description

Replace source drive with target drive

#### Flags

FlagDescription

`--source`, `-s`

(`str`)

Source drive

`--target`, `-t`

(`str`)

Target drive

`--operation`, `-o`

(`str`)

start|cancel|status
Valid values:

- `start`

- `cancel`

- `status`

Default value: `start`

## pxctl service drive rebalance

```

pxctl service drive rebalance

```

#### Description

Rebalance storage

#### Flags

FlagDescription

`--pool-id`, `-p`

(`str`)

Storage pool

`--operation`, `-o`

(`str`)

start|cancel|status
Valid values:

- `start`

- `cancel`

- `status`

Default value: `status`

## pxctl service drive check

```

pxctl service drive check

```

#### Description

Check drives

#### Flags

FlagDescription

`--full`

(`bool`)

Detailed report

## pxctl service node

```

pxctl service node

```

#### Description

Node maintenance operations

## pxctl service node drain-attachments

```

pxctl service node drain-attachments

```

#### Description

Drain/Remove volume attachments from a node

## pxctl service node drain-attachments submit

```

pxctl service node drain-attachments submit

```

#### Description

Submit a new job to drain attachments.

#### Flags

FlagDescription

`--node`, `-n`

(`str`)

NodeID of the node from which the volume attachments will be removed

This flag is required.

`--issuer`, `-i`

(`str`)

Name of the issuer who is submitting this job

`--wait`, `-w`

(`bool`)

Wait until the drain job is complete. The command will be unblocked when the job completes or a it hits a 5 min timeout.

`--wait-timeout-sec`, `-t`

(`int`)

Wait timeout in seconds. Default is 5 mins.

Default value: `300`

`--quiet`, `-q`

(`bool`)

Do not print summary when running the command in wait mode.

## pxctl service node drain-attachments list

```

pxctl service node drain-attachments list

```

#### Description

Lists drain attachment jobs in the system

## pxctl service node drain-attachments status

```

pxctl service node drain-attachments status

```

#### Description

Status of a drain attachments job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service node drain-attachments cancel

```

pxctl service node drain-attachments cancel

```

#### Description

Cancels a drain attachments job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service node cordon-attachments

```

pxctl service node cordon-attachments

```

#### Description

Cordons/Disables any new volume attachments from a node. Existing volumes will stay attached

#### Flags

FlagDescription

`--node`

(`str`)

ID of the node for which any new volume attachments will be disabled

This flag is required.

## pxctl service node uncordon-attachments

```

pxctl service node uncordon-attachments

```

#### Description

Re-enables volume attachments for a node.

#### Flags

FlagDescription

`--node`

(`str`)

ID of the node for which volume attachments will be re-enabled

This flag is required.

## pxctl service pool

```

pxctl service pool

```

#### Description

Storage pool maintenance

## pxctl service pool show

```

pxctl service pool show

```

#### Description

Show pools

#### Flags

FlagDescription

## pxctl service pool rebalance

```

pxctl service pool rebalance

```

#### Description

Rebalance storage pools

## pxctl service pool rebalance submit

```

pxctl service pool rebalance submit

```

#### Description

Submit a new rebalance job

#### Flags

FlagDescription

`--dry-run`, `-d`

(`bool`)

Produces steps that would be taken without making any changes to the system

`--source-pool-selector`

(`str`)

Comma-separated label selector of the form label1=value1,label2=value2 etc., that allows selecting pools to which over-load trigger thresholds will apply.

`--target-pool-selector`

(`str`)

Comma-separated label selector of the form label1=value1,label2=value2 etc., that allows selecting pools to which under-load trigger thresholds will apply.

`--max-duration-minutes`, `-m`

(`uint`)

Defines how long operation should run when started. 0 values means no limit on duration

`--remove-repl-1-snapshots`

(`str`)

delete snapshots which don't have parent on same pool after rebalance
Valid values:

- `on`

- `off`

Default value: `off`

## pxctl service pool rebalance list

```

pxctl service pool rebalance list

```

#### Description

Lists rebalance jobs in the system

## pxctl service pool rebalance status

```

pxctl service pool rebalance status

```

#### Description

Status of a rebalance job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool rebalance cancel

```

pxctl service pool rebalance cancel

```

#### Description

Cancels a rebalance job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool rebalance resume

```

pxctl service pool rebalance resume

```

#### Description

Resumes a rebalance job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool rebalance pause

```

pxctl service pool rebalance pause

```

#### Description

Pauses a rebalance job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool drain

```

pxctl service pool drain

```

#### Description

Drain storage pools

## pxctl service pool drain submit

```

pxctl service pool drain submit

```

#### Description

Submit a new drain request

#### Flags

FlagDescription

`--dry-run`, `-d`

(`bool`)

Print all the ha-update operations that will be executed if this drain request is submitted

`--source-uuids`

(`str`)

List of comma-separated sources that will be drained. Can specify either pool or node UUIDs

`--target-uuids`

(`str`)

List of comma-separated targets to which the volume replicas will be relocated. Can specify either pool or node UUIDs

`--source-pool-selector`

(`str`)

Comma-separated label selector of the form label1=value1,label2=value2 that matches the pools which will be drained.

`--target-pool-selector`

(`str`)

Comma-separated label selector of the form label1=value1,label2=value2 that allows selecting pools to which replicas will be moved.

`--max-duration-minutes`, `-m`

(`uint`)

Maximum duration for which long operation can run after start

## pxctl service pool drain list

```

pxctl service pool drain list

```

#### Description

Lists all pool drain jobs

## pxctl service pool drain status

```

pxctl service pool drain status

```

#### Description

Status of a pool drain job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool drain cancel

```

pxctl service pool drain cancel

```

#### Description

Cancels a pool drain job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool drain resume

```

pxctl service pool drain resume

```

#### Description

Resumes a pool drain job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool drain pause

```

pxctl service pool drain pause

```

#### Description

Pauses a pool drain job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl service pool drain clear

```

pxctl service pool drain clear

```

#### Description

Clears the pool drain status of a pool and restores to normal operation

#### Flags

FlagDescription

`--uuid`, `-u`

(`str`)

pool uuid

This flag is required.

## pxctl service pool expand

```

pxctl service pool expand

```

#### Description

Expand pool

#### Flags

FlagDescription

`--size`, `-s`

(`int`)

Minimum new required size of the storage pool in GiB. The eventual size of the pool can be greater than this as PX needs to add/resize disks such that all disks in the pool are of the same size

This flag is required.

`--uid`, `-u`

(`str`)

Pool's UID

This flag is required.

`--operation`, `-o`

(`str`)

Operation to perform to expand the pool (add-drive, resize-drive, auto)

This flag is required.

Default value: `auto`

`--dont-wait-for-clean-volumes`, `-f`

(`bool`)

Don't wait for volumes on the pool to be clean before starting expansion

## pxctl service pool update

```

pxctl service pool update

```

#### Description

Update pool properties

#### Example

```

pxctl sv pool update [flags] <pool-id> *pool-id or --uid <pool-uid> flag is mandatory, if both are specified, pool-uid is ignored

```

#### Flags

FlagDescription

`--io_priority`

(`str`)

IO Priority
Valid values:

- `high`

- `medium`

- `low`

Default value: `low`

`--labels`

(`str`)

comma separated name=value pairs (empty value to remove label)

Default value: `NoLabel`

`--resize`

(`bool`)

extend pool to maximum available physical storage

`--uid`, `-u`

(`str`)

Pool's UID

`--reset-last-op`

(`bool`)

Admin command to reset pool's last operation. Pool resources won't be cleaned up. Use with caution!

## pxctl service pool cache

```

pxctl service pool cache

```

#### Description

Update cache properties on a given pool

## pxctl service pool cache configure

```

pxctl service pool cache configure <required-argument>

```

#### Description

configure cache parameters for a pool

#### Example

```

pxctl sv pool cache configure [flags] <pool-id> *pool-id is mandatory

```

#### Flags

FlagDescription

`--mode`

(`str`)

cache operating mode
Valid values:

- ``

- `writethrough`

- `writeback`

`--blocksize`

(`str`)

cache blocksize hint, software can optimize this value

Default value: `auto`

`--policy`

(`str`)

cache policy
Valid values:

- ``

- `smq`

- `mq`

`--tunables`

(`str`)

cache settings

## pxctl service pool cache status

```

pxctl service pool cache status <required-argument>

```

#### Description

cache status on given pool

#### Example

```

pxctl sv pool cache status <pool-id> *pool-id is mandatory

```

## pxctl service pool cache enable

```

pxctl service pool cache enable <required-argument>

```

#### Description

enable cache on a pool

#### Example

```

pxctl sv pool cache enable <pool-id> *pool-id is mandatory

```

## pxctl service pool cache disable

```

pxctl service pool cache disable <required-argument>

```

#### Description

disable cache on a pool

#### Example

```

pxctl sv pool cache disable <pool-id> *pool-id is mandatory

```

## pxctl service pool cache flush

```

pxctl service pool cache flush <required-argument>

```

#### Description

force cache flush on a pool

#### Example

```

pxctl sv pool cache flush <pool-id> *pool-id is mandatory

```

#### Flags

FlagDescription

`--operation`, `-o`

(`str`)

start|status
Valid values:

- `start`

- `status`

Default value: `start`

## pxctl service pool migrate

```

pxctl service pool migrate

```

#### Description

Migrate pools from a node

#### Example

```

pxctl sv pool migrate --node <node-id> [--pools <pool-uuid1,pool-uuid2>]

```

#### Flags

FlagDescription

`--node`

(`str`)

ID of the node from which to migrate pools

`--pools`

(`str`)

Comma-separated list of pool UUIDs to migrate. All pools must belong to the same node. If not specified, all pools from the node will be migrated

## pxctl service pool migrate status

```

pxctl service pool migrate status

```

#### Description

Show status of pool migration operations

#### Example

```

pxctl sv pool migrate status [--source-node-id <node-id>] [--pool <pool-uuid>] [--plan-id <plan-id>] [--intent-id <intent-id>]

```

#### Flags

FlagDescription

`--source-node-id`, `-n`

(`str`)

Filter by source node ID

`--pool`, `-p`

(`str`)

Filter by pool UUID

`--plan-id`

(`str`)

Filter by plan ID

`--intent-id`

(`str`)

Filter by intent ID

## pxctl service pool migrate list

```

pxctl service pool migrate list

```

#### Description

List all pool migration plans and intents

#### Example

```

pxctl sv pool migrate list [--active-only] [--intents] [--plans]

```

#### Flags

FlagDescription

`--active-only`, `-a`

(`bool`)

Show only active plans (not in final states)

`--intents`, `-i`

(`bool`)

Include intents in the output

`--plans`

(`bool`)

Include plans in the output

## pxctl service pool trim

```

pxctl service pool trim

```

#### Description

Trim pools

## pxctl service pool trim start

```

pxctl service pool trim start

```

#### Description

Start pool trim operation

#### Example

```

pxctl service pool trim start <pool-id>

```

#### Flags

FlagDescription

`--all`, `-a`

(`bool`)

Trim all pools

`--yes`, `-y`

(`bool`)

Assume 'yes' to confirmation prompt

## pxctl service pool trim status

```

pxctl service pool trim status

```

#### Description

Get pool trim status

#### Example

```

pxctl service pool trim status

```

## pxctl service pool trim stop

```

pxctl service pool trim stop

```

#### Description

Stop all pool trim operations

#### Example

```

pxctl service pool trim stop

```

#### Flags

FlagDescription

`--yes`, `-y`

(`bool`)

Assume 'yes' to confirmation prompt

## pxctl service pool maintenance

```

pxctl service pool maintenance

```

#### Description

Pool maintenance

#### Flags

FlagDescription

`--exit`, `-x`

(`bool`)

exit maintenance mode

`--enter`, `-e`

(`bool`)

enter maintenance mode

`--yes`, `-y`

(`bool`)

Assume 'yes' to confirmation prompt

## pxctl service kvdb

```

pxctl service kvdb

```

#### Description

PX Kvdb operations

## pxctl service kvdb restore

```

pxctl service kvdb restore

```

#### Description

Restore keys and values into kvdb from a kvdb.dump file

#### Example

```

/opt/pwx/bin/pxctl service kvdb restore --kvdb_dump_file <file_path>

```

#### Flags

FlagDescription

`--kvdb_dump_file`, `-k`

(`str`)

Kvdb dump file location

This flag is required.

`--force`, `-f`

(`bool`)

Force will delete any existing keys from kvdb and perform the restore

## pxctl service kvdb endpoints

```

pxctl service kvdb endpoints

```

#### Description

List the kvdb client endpoints

## pxctl service kvdb members

```

pxctl service kvdb members

```

#### Description

List the kvdb cluster members

## pxctl service relaxedreclaim

```

pxctl service relaxedreclaim <required-argument>

```

#### Description

Manage the RelaxedReclaim queue for the node

## pxctl service relaxedreclaim purge

```

pxctl service relaxedreclaim purge

```

#### Description

Purge the RelaxedReclaim queue for the node

#### Example

```

/opt/pwx/bin/pxctl service relaxedreclaim purge <node-id>

```

## pxctl service relaxedreclaim list

```

pxctl service relaxedreclaim list

```

#### Description

List the RelaxedReclaim queue for the node

#### Example

```

/opt/pwx/bin/pxctl service relaxedreclaim list

```

## pxctl service relaxedreclaim delete

```

pxctl service relaxedreclaim delete

```

#### Description

Delete a volume from the RelaxedReclaim queue for the node

#### Example

```

/opt/pwx/bin/pxctl service relaxedreclaim delete <vol-id>

```

## pxctl service usage-report

```

pxctl service usage-report

```

#### Description

creates & download tgz package for px consumption reports

#### Flags

FlagDescription

`--download`

(`bool`)

generate reports for px consumption
