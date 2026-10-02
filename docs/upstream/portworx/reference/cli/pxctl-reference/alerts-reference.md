# pxctl alerts

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/alerts-reference (Portworx Enterprise latest)

pxctl alerts | Portworx Enterprise Documentation

## pxctl alerts

```

pxctl alerts

```

#### Description

px alerts

## pxctl alerts show

```

pxctl alerts show

```

#### Description

Start with example and categorically filter alerts using available flags

#### Example

```

pxctl alerts show --type=all

```

#### Flags

FlagDescription

`--type`, `-t`

(`str`)

alert type (used default if not set)
Valid values:

- `volume`

- `node`

- `cluster`

- `drive`

- `pool`

- `all`

Default value: `all`

`--id`, `-i`

(`str`)

alert id

`--resource`, `-r`

(`str`)

resource name

`--severity`, `-s`

(`str`)

min severity value
Valid values:

- `notify`

- `warn`

- `warning`

- `alarm`

Default value: `notify`

`--start-time`

(`str`)

start time (YYYY-MM-DDTHH:mm:ss.sssZ - RFC3339)

`--end-time`

(`str`)

end time (YYYY-MM-DDTHH:mm:ss.sssZ - RFC3339)

`--is-cleared`, `-c`

(`str`)

filter by alert clear flag
Valid values:

- `true`

- `false`

`--out`, `-o`

(`str`)

output alerts to a file in CSV format

## pxctl alerts purge

```

pxctl alerts purge

```

#### Description

Alerts from show command are the alerts that will get purged in purge command

#### Example

```

pxctl alerts purge --type=all

```

#### Flags

FlagDescription

`--confirm-yes`, `-y`

(`bool`)

set to confirm yes and skip y/n question

`--type`, `-t`

(`str`)

alert type (used default if not set)
Valid values:

- `volume`

- `node`

- `cluster`

- `drive`

- `pool`

- `all`

Default value: `all`

`--id`, `-i`

(`str`)

alert id

`--resource`, `-r`

(`str`)

resource name

`--severity`, `-s`

(`str`)

min severity value
Valid values:

- `notify`

- `warn`

- `warning`

- `alarm`

Default value: `notify`

`--start-time`

(`str`)

start time (YYYY-MM-DDTHH:mm:ss.sssZ - RFC3339)

`--end-time`

(`str`)

end time (YYYY-MM-DDTHH:mm:ss.sssZ - RFC3339)

`--is-cleared`, `-c`

(`str`)

filter by alert clear flag
Valid values:

- `true`

- `false`

## pxctl alerts info

```

pxctl alerts info

```

#### Description

show info on alerts
