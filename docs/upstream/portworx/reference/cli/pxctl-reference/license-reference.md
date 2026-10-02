# pxctl license

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/license-reference (Portworx Enterprise latest)

pxctl license | Portworx Enterprise Documentation

## pxctl license

```

pxctl license

```

#### Description

Manage licenses

## pxctl license list

```

pxctl license list

```

#### Description

List available licenses

#### Flags

FlagDescription

`--all`, `-a`

(`bool`)

show all

## pxctl license add

```

pxctl license add <required-argument>

```

#### Description

Add a license from a file

#### Example

```

  pxctl license add [flags] license-file.bin

```

## pxctl license activate

```

pxctl license activate <required-argument>

```

#### Description

Activate license from a license server

#### Example

```

  pxctl license activate [flags] 9035-1a42-9af0-ccd9-dab6

```

#### Flags

FlagDescription

`--count`, `-n`

(`int`)

define number of activations to consume

Default value: `1`

`--tmout`

(`int`)

define timeout for activation

`--key`

(`str`)

saas key for activating usage based license

## pxctl license setls

```

pxctl license setls <required-argument>

```

#### Description

Set license server

#### Example

```

  pxctl license setls http://hostname:7070/fne/bin/capability

```

#### Flags

FlagDescription

`--interval`, `-i`

(`str`)

license borrow interval (`.M.w.d.h.m.s` [e.g. 1w15m] or number)

`--add`

(`str`)

add license features (`feat1[,feat2,...]` format)

`--ca-path`

(`str`)

extra root CA `files` (/usr/share/ca-certificates/extra/root-corp.crt[,/path2/lvl2-corp.crt] format)

`--import-unknown-ca`

(`bool`)

auto-import self-signed root CA certificate

## pxctl license transfer

```

pxctl license transfer <required-argument>

```

#### Description

Command swaps licenses between the two Portworx clusters. Note that both Portworx clusters need to be operational at the time this command is ran. The source cluster must have a valid PX-Enterprise license, while the destination cluster can have either a valid or expired Trial license, or expired PX-Enterprise license.

#### Example

```

  pxctl license transfer f91531d9-bf65-46f5-9619-eb99128e3270 10.0.15.201

```

## pxctl license expand

```

pxctl license expand

```

#### Description

Expand cluster node count for Blue-green deployments

#### Flags

FlagDescription

`--start`

(`bool`)

Start license expansion

`--end`

(`bool`)

End license expansion
