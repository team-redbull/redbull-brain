# pxctl volume

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/volume-reference (Portworx Enterprise 3.6)

pxctl volume | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl volume

```

pxctl volume

```

#### Description

Manage volumes

#### Example

```

pxctl volume create -s 100 myVolName

```

## pxctl volume create

```

pxctl volume create <required-argument>

```

#### Description

Create a volume

#### Example

```

pxctl volume create [flags] volume-name

```

#### Flags

FlagDescription

`--shared`

(`bool`)

make this a globally shared namespace volume

`--secure`

(`bool`)

encrypt this volume using AES-256

`--secret_key`

(`str`)

secret_key to use to fetch secret_data for the PBKDF2 function

`--secret_options`

(`str`)

Secret options is used to pass specific secret parameters. Usage: --secret_options=k1=v1,k2=v2

`--use_cluster_secret`

(`bool`)

Use cluster wide secret key to fetch secret_data

`--label`, `-l`

(`str`)

list of comma-separated name=value `pairs`

`--size`, `-s`

(`uint`)

volume size in GB

Default value: `1`

`--block_size`, `-b`

(`uint`)

block size in Bytes

Default value: `4096`

`--queue_depth`, `-q`

(`uint`)

block device queue depth

Default value: `128`
Valid range:
1 256

`--repl`, `-r`

(`uint`)

replication factor

Default value: `1`
Valid range:
1 3

`--scale`

(`uint`)

auto scale to max number

Default value: `1`
Valid range:
1 1024

`--io_priority`

(`str`)

IO Priority
Valid values:

- `high`

- `medium`

- `low`

Default value: `low`

`--journal`

(`bool`)

Journal data for this volume

`--early_ack`

(`bool`)

Reply to async write requests after it is copied to shared memory

`--async_io`

(`bool`)

Enable async IO to backing storage

`--nodiscard`

(`bool`)

Disable discard support for this volume

`--writezero`

(`bool`)

Enable WriteZero for this volume

`--fastpath`

(`bool`)

Enable fastpath IO support for this volume

`--io_profile`

(`str`)

IO Profile
Valid values:

- `db_remote`

- `auto`

- `none`

- `journal`

- `use_cluster_default`

Default value: `use_cluster_default`

`--sticky`

(`bool`)

sticky volumes cannot be deleted until the flag is disabled

`--sharedv4`

(`bool`)

export this volume via Sharedv4

`--sharedv4_service_type`

(`str`)

creates a sharedv4 service volume when used with the sharedv4 option
Valid values:

- `ClusterIP`

- `NodePort`

- `LoadBalancer`

- ``

`--sharedv4_failover_strategy`

(`str`)

specifies how aggressively to fail over to a new server for a sharedv4 or sharedv4 service volume
Valid values:

- `aggressive`

- `normal`

- ``

`--aggregation_level`, `-a`

(`str`)

aggregation level
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

`--group`, `-g`

(`str`)

group

`--enforce_cg`

(`bool`)

enforce group during provision

`--best_effort_location_provisioning`

(`bool`)

requested nodes, zones, racks are optional

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

`--policy`

(`str`)

policy names separated by comma

`--storagepolicy`

(`str`)

storage policy name

`--mount_options`

(`str`)

comma separated list of mount options provided as key=value pairs

`--sharedv4_mount_options`

(`str`)

comma separated list of sharedv4 client mount options provided as key=value pairs

`--proxy_endpoint`

(`str`)

proxy endpoint provided in the following format '<protocol>://<endpoint>' Ex 'nfs://<nfs-server-ip>'

`--proxy_nfs_exportpath`

(`str`)

export path for nfs proxy volume

`--proxy_nfs_subpath`

(`str`)

sub path from the nfs share to which this proxy volume has access to

`--cow_ondemand`

(`bool`)

Enable On-demand COW on volume

Default value: `true`

`--direct_io`

(`bool`)

Enable Direct IO on volume

`--max_iops`

(`str`)

maximum iops this volume is restricted to. syntax --max_iops <ReadIOPS>,<WriteIOPS>. provide off for no throttling. e.g. --max_iops off,1000. For FADA volumes, syntax --max_iops <IOPSLimit>.

`--max_bandwidth`

(`str`)

maximum io bandwidth (MB/s) this volume is restricted to. syntax --max_bandwidth <ReadBW>,<WriteBW>. provide off for no throttling. e.g. --max_bandwidth 200,off. For FADA volumes, syntax --max_bandwidth <BandwidthLimit> in MB/s.

`--readahead`

(`bool`)

Enable or disable readahead functionality for this volume

## pxctl volume list

```

pxctl volume list

```

#### Description

List volumes in the cluster

#### Flags

FlagDescription

`--all`, `-a`

(`bool`)

show all volumes, including snapshots

`--node`

(`str`)

show all volumes whose replica is present on the given node

`--pool-uid`

(`str`)

show all volumes whose replica is present on the given pool

`--cloud-drive-id`

(`str`)

show all volumes whose replica is present on the given cloud drive

`--name`

(`str`)

volume name used during creation if any

`--label`, `-l`

(`str`)

list of comma-separated name=value pairs

`--snapshot`, `-s`

(`bool`)

show all snapshots (read-only volumes)

`--snapshot-schedule`

(`bool`)

show all schedule created snapshots

`--sched-policy`

(`str`)

filter volumes by sched policy

`--parent`, `-p`

(`str`)

show all snapshots created for given volume

`--volumes`, `-v`

(`bool`)

show only volumes

`--group`, `-g`

(`str`)

show all volumes for given group

`--time`, `-t`

(`bool`)

show all volumes sorted by creation time

`--trashcan`

(`bool`)

list volume snapshots in the trashcan in the cluster

`--kube-datastore`

(`str`)

show volumes associated with the specified Kube Datastore (affinity or replica on KDS)

## pxctl volume update

```

pxctl volume update <required-argument>

```

#### Description

Update volume settings

#### Example

```

pxctl volume update [flags] volName

```

#### Flags

FlagDescription

`--label`, `-l`

(`str`)

list of comma-separated name=value pairs to update (use empty label value to remove label)

`--shared`

(`str`)

set shared setting
Valid values:

- `on`

- `off`

Default value: `off`

`--export_options`

(`str`)

set export options

`--mount_options`

(`str`)

Set mount options for a volume. Provide the mount options as a comma-separated key=value pairs. (Use empty value to reset mount options)

`--sharedv4_mount_options`

(`str`)

Set sharedv4 client mount options for a volume. Provide the mount options as a comma-separated key=value pairs. (Use empty value to reset mount options)

`--sticky`

(`str`)

set sticky setting
Valid values:

- `on`

- `off`

Default value: `off`

`--queue_depth`

(`uint`)

block device queue depth

Default value: `128`
Valid range:
1 256

`--scale`

(`uint`)

New scale factor

Default value: `1`
Valid range:
1 1024

`--journal`

(`str`)

Journal data for this volume
Valid values:

- `on`

- `off`

Default value: `off`

`--early_ack`

(`str`)

Reply to async write requests after it is copied to shared memory
Valid values:

- `on`

- `off`

Default value: `off`

`--pure_nfs_endpoint`

(`str`)

Set Pure FB NFS endpoint for a FB DirectAccess volume. Provide the Pure FB NFS endpoint as a string.

`--add_pure_tags`

(`str`)

Add tags to a FlashArray DirectAccess volume. Provide tags to add in the format `key:value` or `namespace:key:value` separated by semicolons. Tag values may be empty.

`--del_pure_tags`

(`str`)

Remove tags from a FlashArray DirectAccess volume. Provide tags to remove in the format `key` or `namespace:key` separated by semicolons.

`--async_io`

(`str`)

Enable async IO to backing storage
Valid values:

- `on`

- `off`

Default value: `off`

`--nodiscard`

(`str`)

Disable discard support for this volume
Valid values:

- `on`

- `off`

Default value: `off`

`--writezero`

(`str`)

Enable WriteZero for this volume
Valid values:

- `on`

- `off`

Default value: `off`

`--io_profile`

(`str`)

IO Profile
Valid values:

- `db_remote`

- `auto`

- `none`

- `journal`

- `use_cluster_default`

Default value: `use_cluster_default`

`--io_priority`

(`str`)

IO Priority
Valid values:

- `high`

- `medium`

- `low`

Default value: `low`

`--group`, `-g`

(`str`)

Set/Reset the Group field on a Volume

`--size`, `-s`

(`uint`)

New size for the volume (GiB)

Default value: `1`

`--sharedv4`

(`str`)

set sharedv4 setting
Valid values:

- `on`

- `off`

Default value: `off`

`--sharedv4_service_type`

(`str`)

set sharedv4 service type. (Use empty value to clear this setting)
Valid values:

- `ClusterIP`

- `NodePort`

- `LoadBalancer`

- ``

`--sharedv4_failover_strategy`

(`str`)

set sharedv4 failover strategy. (Use empty value to clear this setting)
Valid values:

- `aggressive`

- `normal`

- ``

`--fastpath`

(`bool`)

Enable fastpath IO support for this volume

`--cow_ondemand`

(`str`)

Enable On-demand COW on volume
Valid values:

- `on`

- `off`

Default value: `on`

`--max_iops`

(`str`)

maximum iops this volume is restricted to. syntax --max_iops <ReadIOPS>,<WriteIOPS>. provide off for no throttling. e.g. --max_iops off,1000. For FADA volumes, syntax --max_iops <IOPSLimit>.

`--max_bandwidth`

(`str`)

maximum io bandwidth (MB/s) this volume is restricted to. syntax --max_bandwidth <ReadBW>,<WriteBW>. provide off for no throttling. e.g. --max_bandwidth 200,off. For FADA volumes, syntax --max_bandwidth <BandwidthLimit> in MB/s.

`--readahead`

(`str`)

Enable or disable readahead functionality for this volume
Valid values:

- `on`

- `off`

Default value: `off`

## pxctl volume ha-update

```

pxctl volume ha-update <required-argument>

```

#### Description

Update volume HA level

#### Example

```

pxctl volume ha-update --repl 3 myVol

```

#### Flags

FlagDescription

`--repl`, `-r`

(`uint`)

New replication factor

Default value: `1`
Valid range:
1 3

`--node`, `-n`

(`str`)

comma-separated Node ID(s) or Pool UUID(s)

`--zones`

(`str`)

comma-separated Zone names (only for ha-increase)

`--racks`

(`str`)

comma-separated Rack names (only for ha-increase)

`--cancel`, `-c`

(`bool`)

Cancel ha-increase operation

`--best_effort_location_provisioning`

(`bool`)

requested nodes, zones, racks are optional

`--sources`

(`str`)

comma-separated Node Id(s) to be used as source for ha-increase operation

## pxctl volume snap-interval-update

```

pxctl volume snap-interval-update <required-argument>

```

#### Description

Update volume configuration

#### Example

```

pxctl volume snap-interval-update [flags] volName

```

#### Flags

FlagDescription

`--periodic`, `-p`

(`str`)

periodic snapshot interval in mins,k (keeps 5 by default), 0 disables all schedule snapshots

`--daily`, `-d`

(`str-slice`)

daily snapshot at specified hh:mm,k (keeps 7 by default)

`--weekly`, `-w`

(`str-slice`)

weekly snapshot at specified weekday@hh:mm,k (keeps 5 by default)

`--monthly`, `-m`

(`str-slice`)

monthly snapshot at specified day@hh:mm,k (keeps 12 by default)

`--policy`

(`str`)

policy names separated by comma

## pxctl volume inspect

```

pxctl volume inspect <required-argument>

```

#### Description

Inspect a volume

#### Example

```

pxctl volume inspect [flags] volName

```

#### Flags

FlagDescription

`--extended`, `-e`

(`bool`)

extended report on volume state

## pxctl volume requests

```

pxctl volume requests

```

#### Description

Show all pending requests

## pxctl volume usage

```

pxctl volume usage <required-argument>

```

#### Description

Show volume usage information

#### Example

```

/opt/pwx/bin/pxctl volume usage myVol

```

## pxctl volume delete

```

pxctl volume delete <required-argument>

```

#### Description

Delete a volume

#### Example

```

pxctl volume delete [flags] myVol

```

#### Flags

FlagDescription

## pxctl volume stats

```

pxctl volume stats <required-argument>

```

#### Description

Volume Statistics

#### Example

```

pxctl volume stats [flags] volName

```

## pxctl volume import

```

pxctl volume import <required-argument>

```

#### Description

Import data into a volume

#### Example

```

pxctl volume import [flags] volName

```

#### Flags

FlagDescription

`--src`

(`str`)

Local source `path` for the data

`--secret_options`

(`str`)

Secret options is used to pass specific secret parameters. Usage: --secret_options=k1=v1,k2=v2

`--secret_key`

(`str`)

the encryption passphrase for this volume can be fetched from the secret provider

## pxctl volume clone

```

pxctl volume clone <required-argument>

```

#### Description

Create a clone volume

#### Example

```

pxctl volume clone [flags] volName

```

#### Flags

FlagDescription

`--name`

(`str`)

clone name

`--label`, `-l`

(`str`)

list of comma-separated name=value pairs

## pxctl volume restore

```

pxctl volume restore <required-argument>

```

#### Description

Restore volume from snapshot

#### Example

```

pxctl volume restore [flags] volName

```

#### Flags

FlagDescription

`--snapshot`, `-s`

(`str`)

snapshot-name-or-ID

`--trashcan`, `-t`

(`str`)

volume name or id in trashcan

## pxctl volume snapshot

```

pxctl volume snapshot

```

#### Description

Manage volume snapshots

## pxctl volume snapshot create

```

pxctl volume snapshot create <required-argument>

```

#### Description

Create a volume snapshot

#### Example

```

pxctl volume snapshot create [flags] volName

```

#### Flags

FlagDescription

`--name`

(`str`)

snapshot name

`--label`, `-l`

(`str`)

list of comma-separated name=value pairs

## pxctl volume snapshot group

```

pxctl volume snapshot group

```

#### Description

Create group snapshots for given group id or labels

#### Flags

FlagDescription

`--group`, `-g`

(`str`)

group id

`--label`, `-l`

(`str`)

list of comma-separated name=value pairs

`--volume_ids`, `-v`

(`str`)

list of comma-separated volume IDs

`--delete-on-failure`, `-d`

(`bool`)

delete created snaps if not all volumes succeeded in the group

## pxctl volume access

```

pxctl volume access

```

#### Description

This command manages access permissions to a volume. There are two ways
to provide access, one is by adding a group and the other is by adding
a specific user as a collaborator. When adding a collaborator, you
must use the unique id of the user. Please consult with your admin
on how to obtain the unique id of the user.

ACCESS TYPES
When adding a group or collaborator, an access type must also be
given, which can be either Read, Write, or Admin.

A Read access type allows access to the volume without modifying
it. With a Read access type, one can clone or inspect the volume.
A Write access type allows modification of the volume and its metadata,
for example allowing to mount, unmount, and restoring the volume from
snapshot in addition to all Read access.
An Admin access type allows full access to the volume, like deleting
the volume in addition to all Write access.

SETTING ACCESS TYPES
To set access types, add the following suffix to the group or collaborator
separated by a colon ':'
 r - For Read access type
 w - For Write access type
 a - For Admin access type

SETTING PUBLIC ACCESS
To set public access, add either w, write, r, or read with the public flag.

#### Example

```

Add read access for group1

  pxctl v access add <volume> --group group1:r

Add write access for group2

  pxctl v access add <volume> --group group2:w

Add admin access for user1

  pxctl v access add <volume> --collaborator user1Id:a

Add public access for user2

  pxctl v access add <volume> --public w

Remove user1's access

  pxctl v access remove <volume> --collaborator user1Id

Remove user2's public access

  pxctl v access remove <volume> --public

Set the entire volume access spec with one command. This clears any previous settings.

  pxctl v access update <volume> --groups group1:r,group2:w --collaborators user1Id:a

Show the volume access spec for a given volume

  pxctl v access show <volume>

```

## pxctl volume access show

```

pxctl volume access show

```

#### Description

List the owner and volume ACLS

#### Example

```

pxctl volume access show [flags] volName

```

## pxctl volume access add

```

pxctl volume access add

```

#### Description

Adds a single group or collaborator

#### Example

```

pxctl volume access add [flags] volName

```

#### Flags

FlagDescription

`--group`, `-g`

(`str`)

group to add with access type. See volume access help for more information

`--collaborator`, `-c`

(`str`)

collaborator to add with access type. Must be the unique id of the user. See volume access for more information

`--public`, `-p`

(`str`)

update the ownership as public

## pxctl volume access remove

```

pxctl volume access remove

```

#### Description

Removes a single group or collaborator

#### Example

```

pxctl volume access remove [flags] volName

```

#### Flags

FlagDescription

`--group`, `-g`

(`str`)

group to remove

`--collaborator`, `-c`

(`str`)

collaborator to remove

`--public`, `-p`

(`bool`)

update the ownership as public

## pxctl volume access update

```

pxctl volume access update

```

#### Description

Update the owner and/or complete set of volume ACLS

#### Example

```

pxctl volume access update [flags] volName

```

#### Flags

FlagDescription

`--owner`, `-o`

(`str`)

username of the desired owner. Only an administrator can change this value.

`--groups`, `-g`

(`str`)

list of comma-separated group names with access type. See volume access for more information

`--collaborators`, `-c`

(`str`)

list of comma-separated collaborator names with access type. See volume access for more information

## pxctl volume locate

```

pxctl volume locate

```

#### Description

Locate volume

#### Example

```

pxctl volume locate volume_id

```

## pxctl volume check

```

pxctl volume check

```

#### Description

Perform Background filesystem consistency check operation on the volume

#### Example

```

pxctl volume check <sub_cmd> [flags] volume-name

```

## pxctl volume check start

```

pxctl volume check start <required-argument>

```

#### Description

Start filesystem consistency check on the volume

#### Example

```

pxctl volume check start --mode fix_safe volume-name

```

#### Flags

FlagDescription

`--mode`

(`str`)

select what mode to run filesystem consistency check

This flag is required.
Valid values:

- `fix_safe`

- `check_health`

- `fix_all`

## pxctl volume check stop

```

pxctl volume check stop <required-argument>

```

#### Description

Stop filesystem consistency check on the volume, if any

#### Example

```

pxctl volume check stop volume-name

```

## pxctl volume check status

```

pxctl volume check status <required-argument>

```

#### Description

Get the Status of filesystem consistency check on the volume

#### Example

```

pxctl volume check status volume-name

```

## pxctl volume autofstrim

```

pxctl volume autofstrim

```

#### Description

Periodically frees unused blocks in the volume to the portworx pool

#### Example

```

pxctl volume autofstrim

```

## pxctl volume autofstrim status

```

pxctl volume autofstrim status

```

#### Description

Status of auto filesystem trim

#### Example

```

pxctl volume autofstrim status volume-name

```

## pxctl volume autofstrim usage

```

pxctl volume autofstrim usage

```

#### Description

Report volume usage and trimmable space in locally attached volumes

#### Example

```

pxctl volume autofstrim usage

```

## pxctl volume autofstrim push

```

pxctl volume autofstrim push

```

#### Description

Push front to autofstrim job queue

#### Example

```

pxctl volume autofstrim push volume-name

```

## pxctl volume autofstrim pop

```

pxctl volume autofstrim pop

```

#### Description

Pop auto fstrim job in queue or stop job if active

#### Example

```

pxctl volume autofstrim pop volume-name

```

## pxctl volume trim

```

pxctl volume trim

```

#### Description

Frees unused blocks in the volume to the portworx pool

#### Example

```

pxctl volume trim <sub_cmd> [flags] volume-name

```

## pxctl volume trim start

```

pxctl volume trim start <required-argument>

```

#### Description

Start filesystem trim on the volume

#### Example

```

pxctl volume trim start volume-name

```

## pxctl volume trim status

```

pxctl volume trim status

```

#### Description

Status of filesystem trim on the volume

#### Example

```

pxctl volume trim status

```

## pxctl volume trim stop

```

pxctl volume trim stop <required-argument>

```

#### Description

Stop filesystem trim on the volume

#### Example

```

pxctl volume trim stop volume-name

```

## pxctl volume trim usage

```

pxctl volume trim usage

```

#### Description

Report volume usage and trimmable space in locally attached volumes

#### Example

```

pxctl volume trim usage

```

## pxctl volume verify-checksum

```

pxctl volume verify-checksum <required-argument>

```

#### Description

Verify checksums on all replicas for a given volume

#### Example

```

/opt/pwx/bin/pxctl volume verify-checksum <sub_cmd> [flags] volume-name

```

## pxctl volume verify-checksum start

```

pxctl volume verify-checksum start <required-argument>

```

#### Description

Start checksum validation on the volume

#### Example

```

pxctl volume verify-checksum start volume-name

```

#### Flags

FlagDescription

`--resume`

(`bool`)

Resume checksum verification from saved offset

Default value: `true`

## pxctl volume verify-checksum stop

```

pxctl volume verify-checksum stop <required-argument>

```

#### Description

Stop checksum validation on the volume

#### Example

```

pxctl volume verify-checksum stop volume-name

```

## pxctl volume verify-checksum status

```

pxctl volume verify-checksum status <required-argument>

```

#### Description

Get the Status of checksum validation on the volume

#### Example

```

pxctl volume verify-checksum status volume-name

```
