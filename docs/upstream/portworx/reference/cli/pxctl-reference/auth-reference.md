# pxctl auth

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/auth-reference (Portworx Enterprise latest)

pxctl auth | Portworx Enterprise Documentation

## pxctl auth

```

pxctl auth

```

#### Description

Portworx pxctl token based authentication and authorization commands

## pxctl auth token

```

pxctl auth token

```

#### Description

Manage tokens for use by pxctl

#### Example

```

pxctl auth token <command> <command flags>

```

## pxctl auth token generate

```

pxctl auth token generate

```

#### Description

Generate a self signed token based on a specified configuration yaml. The configuration defines your identity, roles, and groups to be used when generating a token.
e.g.
 name: Jim Stevens
 sub: jstevens@portworx.com/jstevens
 email: jstevens@portworx.com
 roles: ["system.user"]
 groups: ["px-engineering", "kubernetes-csi"]

#### Example

```

pxctl auth token generate --auth-config=<authconfig.yaml> --issuer <issuer> --ecdsa-private-keyfile <ecdsa key file> OR --rsa-private-keyfile <rsa key file> OR --shared-secret <secret>

```

#### Flags

FlagDescription

`--auth-config`

(`str`)

Auth account information file providing email, name, etc.

This flag is required.

`--ecdsa-private-keyfile`

(`str`)

ECDSA Private file to sign token

`--issuer`

(`str`)

Issuer name of token. Do not use https:// in the issuer since it could indicate that this is an OpenID Connect issuer.

This flag is required.

`--output`

(`str`)

Output token to file instead of standard out

`--rsa-private-keyfile`

(`str`)

RSA Private file to sign token

`--shared-secret`

(`str`)

Shared secret to sign token

`--token-duration`

(`str`)

Duration of time where the token will be valid. Postfix the duration by using s for seconds, m for minutes, h for hours, d for days, and y for years.

Default value: `1d`
