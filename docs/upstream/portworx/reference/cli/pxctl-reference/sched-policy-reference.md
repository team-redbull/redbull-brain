# pxctl sched-policy

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/sched-policy-reference (Portworx Enterprise 3.6)

pxctl sched-policy | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl sched-policy

```

pxctl sched-policy

```

#### Description

Manage schedule policies

#### Example

```

pxctl sched-policy create --periodic 15 myPolicyName

```

## pxctl sched-policy create

```

pxctl sched-policy create <required-argument>

```

#### Description

Create a schedule policy

#### Example

```

pxctl sched-policy create [flags] policy-name

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

## pxctl sched-policy delete

```

pxctl sched-policy delete <required-argument>

```

#### Description

Delete a schedule policy

#### Example

```

pxctl sched-policy delete [flags] policy-name

```

## pxctl sched-policy update

```

pxctl sched-policy update <required-argument>

```

#### Description

Update a schedule policy

#### Example

```

pxctl sched-policy update [flags] policy-name

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

## pxctl sched-policy list

```

pxctl sched-policy list

```

#### Description

List all schedule policies
