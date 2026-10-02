# pxctl context

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/context-reference (Portworx Enterprise latest)

pxctl context | Portworx Enterprise Documentation

## pxctl context

```

pxctl context

```

#### Description

Portworx pxctl context commands for setting authentication and connection info

## pxctl context list

```

pxctl context list

```

#### Description

Display yaml representation of all registered contexts

#### Example

```

pxctl context list

```

## pxctl context create

```

pxctl context create <required-argument>

```

#### Description

Create a context with authentication and connection info

#### Example

```

pxctl context create <context> [--endpoint <endpoint>] [--token <token>]

```

#### Flags

FlagDescription

`--token`, `-t`

(`str`)

Token to use for this context

`--endpoint`, `-e`

(`str`)

Endpoint to use for this context

## pxctl context delete

```

pxctl context delete

```

#### Description

Remove a context from the list by context name or token

#### Example

```

pxctl context delete <context> [--token <token>]

```

#### Flags

FlagDescription

`--token`, `-t`

(`str`)

Token associated with context you would like to delete

## pxctl context set

```

pxctl context set <required-argument>

```

#### Description

set the current context

#### Example

```

pxctl context set <context>

```

## pxctl context unset

```

pxctl context unset

```

#### Description

unset the current context

#### Example

```

pxctl context context unset

```
