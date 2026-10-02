# pxctl cloudsnap

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/cloudsnap-reference (Portworx Enterprise 3.6)

pxctl cloudsnap | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl cloudsnap

```

pxctl cloudsnap

```

#### Description

Backup and restore snapshots to/from cloud

## pxctl cloudsnap backup

```

pxctl cloudsnap backup <required-argument>

```

#### Description

Backup a snapshot to cloud

#### Example

```

/opt/pwx/bin/pxctl cloudsnap backup [flags] volName

```

#### Flags

FlagDescription

`--label`

(`str`)

list of comma-separated name=value `pairs`

`--full`, `-f`

(`bool`)

Force a full backup

`--delete-local`, `-d`

(`bool`)

Deletes local snap created for backup after backup is done, also forces next backup to be full

`--cred-id`

(`str`)

Cloud credentials ID to be used for the backup

`--frequency`, `-i`

(`uint`)

Maximum number of incremental cloudsnaps after which full is forced, default 7

## pxctl cloudsnap backup-group

```

pxctl cloudsnap backup-group

```

#### Description

Backup a group of snapshot for a given list of volumes, group id, or labels to cloud

#### Flags

FlagDescription

`--group`

(`str`)

group id

`--full`

(`bool`)

Force a full backup

Default value: `false`

`--delete-local`, `-d`

(`bool`)

Deletes local snap created for backup after backup is done, also forces next backup to be full

`--cred-id`

(`str`)

Cloud credentials ID to be used for the backup

`--label`

(`str`)

list of comma-separated name=value `pairs`

`--volume_ids`, `-v`

(`str`)

list of comma-separated volume IDs

## pxctl cloudsnap restore

```

pxctl cloudsnap restore

```

#### Description

Restore volume to a cloud snapshot

#### Flags

FlagDescription

`--volume`, `-v`

(`str`)

Volume name to be created for restore

`--snap`, `-s`

(`str`)

Cloud-snap id to restore

`--cred-id`

(`str`)

Cloud credentials ID to be used for the restore

`--repl`, `-r`

(`uint`)

replication factor(If not specified, inherits cloudsnaps repl factor)

Default value: `1`
Valid range:
1 3

`--io_priority`

(`str`)

IO Priority(If not specified, inherits cloudsnap's IO Priority)
Valid values:

- `high`

- `medium`

- `low`

Default value: `low`

`--label`, `-l`

(`str`)

list of comma-separated name=value `pairs`

`--queue_depth`, `-q`

(`uint`)

block device queue depth(If not specified, inherits cloudsnap's queuedepth)

Default value: `128`
Valid range:
1 256

`--aggregation_level`, `-a`

(`str`)

aggregation level(If not specified, inherits cloudsnap's aggregation level)
Valid values:

- `1`

- `2`

- `3`

- `auto`

Default value: `1`

`--nodes`

(`str`)

comma-separated Node Ids or Pool Ids

`--zones`

(`str`)

comma-separated Zone names

`--racks`

(`str`)

comma-separated Rack names

`--match_src_vol_provisioning`

(`bool`)

provision the restore volume on same pools as the source volume(src volume must exist)

`--best_effort_location_provisioning`

(`bool`)

requested nodes, zones, racks are optional

`--storagepolicy`

(`str`)

storage policy name(If not specified, inherits cloudsnap's storage policy)

`--journal`

(`bool`)

Journal data for this volume(If not specified, inherits cloudsnap's journal option)

`--nodiscard`

(`bool`)

Disable discard support for this volume(If not specified, inherits cloudsnap's discard option)

`--io_profile`

(`str`)

IO Profile((defaults to cloudsnap's IO Profile)
Valid values:

- `sequential`

- `db`

- `db_remote`

Default value: `sequential`

`--sticky`

(`bool`)

sticky volumes cannot be deleted until the flag is disabled(if not specified, inherits cloudsnap's sticky option)

`--group`, `-g`

(`str`)

group

`--enforce_cg`

(`bool`)

enforce group during provision

`--shared`

(`bool`)

make this a globally shared namespace volume(If not specified, inherits cloudsnap's shared option)

`--sharedv4`

(`bool`)

set sharedv4 setting(if not specified, inherits cloudsnap's sharedv4 option)

`--periodic`, `-p`

(`str`)

periodic snapshot interval in `mins,k` (keeps 5 by default), 0 disables all schedule snapshots

`--daily`, `-d`

(`str-slice`)

daily snapshot at specified `hh:mm,k` (keeps 7 by default)

`--weekly`, `-w`

(`str-slice`)

weekly snapshot at specified `weekday@hh:mm,k` (keeps 5 by default)

`--monthly`, `-m`

(`str-slice`)

monthly snapshot at specified `day@hh:mm,k` (keeps 12 by default)

`--fastpath`

(`bool`)

Enable fastpath IO support for this volume(If not specified, inherits cloudsnap's fastpath option)

`--secret_key`

(`str`)

secret_key used to decrypt an encrypted volume

`--secret_options`

(`str`)

Secret options is used to pass specific secret parameters. Usage: --secret_options=k1=v1,k2=v2

## pxctl cloudsnap list

```

pxctl cloudsnap list

```

#### Description

List snapshot in cloud

#### Flags

FlagDescription

`--src`, `-s`

(`str`)

Optional source volume to list cloud backups

`--cred-id`

(`str`)

Cloud credentials ID to be used for the backup

`--deleted-source-vol`, `-d`

(`bool`)

List cloudsnaps of volumes no longer in cluster(deleted source volumes)

`--cluster`, `-c`

(`str`)

Optional Cluster ID or Bucket name to list cloud backups. Current cluster-id is default

`--migration`, `-m`

(`bool`)

Optional, lists migration related cloudbackups

`--status`, `-t`

(`str`)

Optional backup status(failed. aborted, stopped) to list cloud backups; Defaults to Done

`--label`

(`str`)

Optional list of comma-separated name=value `pairs` to match with cloudsnap metadata

`--max`, `-x`

(`uint`)

Optional number to limit display of backups in each page

`--all`, `-a`

(`bool`)

List cloud backups of all clusters in cloud

`--paginate`, `-p`

(`bool`)

Paginate list with user input to continue

`--cloudsnap-id`, `-i`

(`str`)

Optional cloudsnap id to list(lists a single entry)

## pxctl cloudsnap status

```

pxctl cloudsnap status

```

#### Description

Report status of active backups/restores

#### Flags

FlagDescription

`--name`, `-n`

(`str`)

Optional task name to list status

`--src`, `-s`

(`str`)

Optional source volume to list backup/restore task status

`--local`, `-l`

(`bool`)

Node's local cloud-snaps(not cluster-wide) status

## pxctl cloudsnap history

```

pxctl cloudsnap history

```

#### Description

Show history of cloudsnap operations

#### Flags

FlagDescription

`--src`, `-s`

(`str`)

Optional source volume to list history

## pxctl cloudsnap stop

```

pxctl cloudsnap stop

```

#### Description

stop an active backup/restore

#### Flags

FlagDescription

`--name`, `-n`

(`str`)

Name of active backup/restore

This flag is required.

## pxctl cloudsnap schedules

```

pxctl cloudsnap schedules

```

#### Description

Manage schedules for cloud-snaps

## pxctl cloudsnap schedules create

```

pxctl cloudsnap schedules create

```

#### Description

Create a cloud-snap schedule for a volume

#### Example

```

/opt/pwx/bin/pxctl cloudsnap schedules create [flags] volName

```

#### Flags

FlagDescription

`--max`, `-x`

(`uint`)

Maximum number of cloud snaps to maintain. This flag also dictates the frequency with which Portworx uploads full backups for CloudSnaps.

Default value: `7`

`--retention`, `-r`

(`uint`)

Retention period for cloud snaps in number of days

`--full`, `-f`

(`bool`)

Force scheduled backups to be full always

`--periodic`, `-p`

(`str`)

Cloudsnap interval in minutes

`--daily`, `-d`

(`str-slice`)

Daily snapshot at specified hh:mm (UTC)

`--weekly`, `-w`

(`str-slice`)

Weekly snapshot at specified weekday@hh:mm (UTC)

`--monthly`, `-m`

(`str-slice`)

Monthly snapshot at specified day@hh:mm (UTC)

`--cred-id`

(`str`)

Cloud credentials ID to be used for the backup

## pxctl cloudsnap schedules delete

```

pxctl cloudsnap schedules delete

```

#### Description

Delete a cloud-snap schedule

#### Flags

FlagDescription

`--uuid`

(`str`)

UUID of schedule to be deleted

## pxctl cloudsnap schedules list

```

pxctl cloudsnap schedules list

```

#### Description

List the configured cloud-snap schedules

## pxctl cloudsnap schedules update

```

pxctl cloudsnap schedules update

```

#### Description

update cloud-snap schedule for a volume

#### Example

```

/opt/pwx/bin/pxctl cloudsnap schedules update -i <uuid> [flags]

```

#### Flags

FlagDescription

`--uuid`, `-i`

(`str`)

uuid of the schedule being updated

This flag is required.

`--max`, `-x`

(`uint`)

Maximum number of cloud snaps to maintain, default 7

Default value: `7`

`--retention`, `-r`

(`uint`)

Retention period for cloud snaps in number of days

`--full`, `-f`

(`bool`)

Force scheduled backups to be full always

`--periodic`, `-p`

(`str`)

Cloudsnap interval in minutes

`--daily`, `-d`

(`str-slice`)

Daily snapshot at specified hh:mm (UTC)

`--weekly`, `-w`

(`str-slice`)

Weekly snapshot at specified weekday@hh:mm (UTC)

`--monthly`, `-m`

(`str-slice`)

Monthly snapshot at specified day@hh:mm (UTC)

`--cred-id`

(`str`)

Cloud credentials ID to be used for the backup

## pxctl cloudsnap catalog

```

pxctl cloudsnap catalog

```

#### Description

Display catalog for the backup in cloud

#### Flags

FlagDescription

`--snap`, `-s`

(`str`)

Cloud Backup ID to display the catalog

`--cred-id`

(`str`)

Cloud credentials ID to be used for the operation

## pxctl cloudsnap delete

```

pxctl cloudsnap delete

```

#### Description

Delete a cloudsnap from the objectstore. This is not reversible.

#### Flags

FlagDescription

`--snap`, `-s`

(`str`)

ID of cloudsnap

`--cred-id`

(`str`)

Cloud credentials ID to be used for the operation
