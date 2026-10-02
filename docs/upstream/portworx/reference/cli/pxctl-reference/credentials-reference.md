# pxctl credentials

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/credentials-reference (Portworx Enterprise latest)

pxctl credentials | Portworx Enterprise Documentation

## pxctl credentials

```

pxctl credentials

```

#### Description

Manage credentials for cloud providers

## pxctl credentials create

```

pxctl credentials create <required-argument>

```

#### Description

Create a credential for cloud providers

#### Example

```

/opt/pwx/bin/pxctl cred create [flags] <name>

```

#### Flags

FlagDescription

`--provider`

(`str`)

Cloud provider type [s3, azure, google, nfs]

`--s3-access-key`

(`str`)

`--s3-secret-key`

(`str`)

`--s3-region`

(`str`)

`--s3-endpoint`

(`str-slice`)

Endpoint of the S3 servers, in comma separated host:port format

`--s3-disable-ssl`

(`bool`)

`--s3-storage-class`

(`str`)

Storage class type [STANDARD, STANDARD_IA]

`--s3-sse`

(`str`)

Server-side-encryption[AES256,aws:kms]

`--use-iam`

(`bool`)

Optional, use instance IAM for credentials, current support only for s3(ec2 IAM) and azure

`--use-workload-identity`

(`bool`)

Optional, use workload identity for AWS S3, Azure and Google credentials

`--bucket`

(`str`)

Optional pre-created bucket name

`--disable-path-style`

(`bool`)

optional, required for virtual-host-style access

`--use-proxy`

(`bool`)

optional, currently supported for s3 only, requires cluster wide proxy(under cluster options)

`--azure-account-name`

(`str`)

`--azure-account-key`

(`str`)

`--google-project-id`

(`str`)

`--google-json-key-file`

(`str`)

`--encryption-passphrase`

(`str`)

Passphrase to be used for encrypting data in the cloudsnaps

`--nfs-server`

(`str`)

`--nfs-sub-path`

(`str`)

sub-path to use in mount

`--nfs-mount-opts`

(`str`)

optional mount options for mounting the mount

`--nfs-timeout-seconds`, `-t`

(`uint`)

optional nfs IO timeout in seconds

Default value: `5`
Valid range:
1 30

## pxctl credentials update

```

pxctl credentials update <required-argument>

```

#### Description

Provide the arguments that need to be updated in the existing credentials

#### Example

```

/opt/pwx/bin/pxctl cred update [flags] <name>

```

#### Flags

FlagDescription

`--provider`

(`str`)

Cloud provider type [s3, azure, google]

`--name`

(`str`)

New name for the credential

`--s3-access-key`

(`str`)

`--s3-secret-key`

(`str`)

`--s3-region`

(`str`)

`--s3-endpoint`

(`str-slice`)

Endpoint of the S3 servers, in comma separated host:port format

`--s3-disable-ssl`

(`bool`)

`--s3-storage-class`

(`str`)

Storage class type [STANDARD, STANDARD_IA]

`--s3-sse`

(`str`)

Server-side-encryption[AES256,aws:kms]

`--use-iam`

(`bool`)

Optional, use instance IAM for credentials, current support only for s3(ec2 IAM) and azure

`--bucket`

(`str`)

Optional pre-created bucket name

`--disable-path-style`

(`bool`)

optional, required for virtual-host-style access

`--use-proxy`

(`bool`)

optional, currently supported for s3 only, requires cluster wide proxy(under cluster options)

`--azure-account-name`

(`str`)

`--azure-account-key`

(`str`)

`--google-project-id`

(`str`)

`--google-json-key-file`

(`str`)

## pxctl credentials list

```

pxctl credentials list

```

#### Description

List all credentials for cloud

## pxctl credentials delete

```

pxctl credentials delete <required-argument>

```

#### Description

Delete a credential for cloud

#### Example

```

/opt/pwx/bin/pxctl cred delete <name or uuid>

```

## pxctl credentials validate

```

pxctl credentials validate <required-argument>

```

#### Description

Validate a credential for cloud

#### Example

```

/opt/pwx/bin/pxctl cred validate <name or uuid>

```

## pxctl credentials delete-refs

```

pxctl credentials delete-refs <required-argument>

```

#### Description

Delete references to a credential

#### Example

```

/opt/pwx/bin/pxctl cred delete-refs <name or uuid>

```
