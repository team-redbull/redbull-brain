# pxctl cloudmigrate

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/cloudmigrate-reference (Portworx Enterprise latest)

pxctl cloudmigrate | Portworx Enterprise Documentation

## pxctl cloudmigrate

```

pxctl cloudmigrate

```

#### Description

Migrate volumes across clusters

## pxctl cloudmigrate start

```

pxctl cloudmigrate start

```

#### Description

Migrate volume(s) to a paired Portworx cluster

#### Flags

FlagDescription

`--volume_id`, `-v`

(`str`)

ID of the volume to be migrated

This flag is required.

`--cluster_id`, `-c`

(`str`)

ID of the cluster where the volume should be migrated

## pxctl cloudmigrate cancel

```

pxctl cloudmigrate cancel

```

#### Description

Cancel migrate tasks

#### Flags

FlagDescription

`--task_id`, `-t`

(`str`)

ID of the task to be canceled

This flag is required.

## pxctl cloudmigrate status

```

pxctl cloudmigrate status

```

#### Description

Status of volume migrations

#### Flags

FlagDescription

`--task_id`, `-t`

(`str`)

ID of the task to be queried

`--cluster_id`, `-c`

(`str`)

ID of the cluster for which to get status

`--active`, `-a`

(`bool`)

Show only active migrations

Default value: `true`

`--volume`, `-v`

(`str`)

Volume Id or name for which to show status
