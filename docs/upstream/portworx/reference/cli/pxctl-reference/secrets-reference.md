# pxctl secrets

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/secrets-reference (Portworx Enterprise 3.6)

pxctl secrets | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl secrets

```

pxctl secrets

```

#### Description

Manage Secrets. Supported secret stores AWS KMS | Vault | IBM Key Protect | Kubernetes Secrets | Google Cloud KMS

## pxctl secrets set-cluster-key

```

pxctl secrets set-cluster-key

```

#### Description

Sets an existing secret as a cluster-wide (default) secret to be used for volume encryption

#### Flags

FlagDescription

`--secret`

(`str`)

Secret id of an existing secret

`--secret_options`

(`str`)

Secret options is used to pass specific secret parameters. Usage: --secret_options=k1=v1,k2=v2

`--overwrite`

(`bool`)

Overwrite an existing cluster wide secret key

## pxctl secrets upload-cluster-wide-secret

```

pxctl secrets upload-cluster-wide-secret

```

#### Description

Uploads the provided key and secret as a cluster-wide (default) secret. Should be used only when migrating cluster-wide secrets between Portworx clusters.

#### Flags

FlagDescription

`--secret_id`

(`str`)

An ID to identify the secret

This flag is required.

`--secret_value`

(`str`)

The actual secret to be used for encrypting volumes

This flag is required.

`--overwrite`

(`bool`)

If set then the command will overwrite the existing cluster-wide secret (Any existing volumes with the older secret will be unusable)

## pxctl secrets dump-cluster-wide-secret

```

pxctl secrets dump-cluster-wide-secret

```

#### Description

Dumps the cluster-wide secret and the associated key for this cluster. Should be used only when migrating cluster-wide secrets between Portworx clusters.

## pxctl secrets aws

```

pxctl secrets aws

```

#### Description

AWS secret-endpoint commands

## pxctl secrets aws generate-kms-data-key

```

pxctl secrets aws generate-kms-data-key

```

#### Description

Generates a KMS Data Key and associates the given secret_id to it

#### Flags

FlagDescription

`--secret_id`

(`str`)

Secret Id to associate with the KMS Data Key

## pxctl secrets aws list-secrets

```

pxctl secrets aws list-secrets

```

#### Description

Lists all the available secret ids

## pxctl secrets kvdb

```

pxctl secrets kvdb

```

#### Description

kvdb secret-endpoint commands

## pxctl secrets kvdb put-secret

```

pxctl secrets kvdb put-secret

```

#### Description

Put Secret into kvdb

#### Flags

FlagDescription

`--secret_id`

(`str`)

Id of the secret to write in kvdb

`--secret_value`

(`str`)

Value of the secret

## pxctl secrets kvdb get-secret

```

pxctl secrets kvdb get-secret

```

#### Description

Get Secret from kvdb

#### Flags

FlagDescription

`--secret_id`

(`str`)

Id of the secret to fetch from kvdb

## pxctl secrets kvdb list-secrets

```

pxctl secrets kvdb list-secrets

```

#### Description

Lists all the available secret ids

## pxctl secrets gcloud

```

pxctl secrets gcloud

```

#### Description

Google Cloud KMS commands

## pxctl secrets gcloud create-secret

```

pxctl secrets gcloud create-secret

```

#### Description

Creates a new secret

#### Flags

FlagDescription

`--secret_id`, `-i`

(`str`)

Id of the secret to be created

This flag is required.

`--passphrase`, `-p`

(`str`)

The secret passphrase to be associated with the secret id. If passphrase is empty portworx will generate one.

This flag is required.

## pxctl secrets gcloud list-secrets

```

pxctl secrets gcloud list-secrets

```

#### Description

Lists all the available secret ids

## pxctl secrets gcloud delete-secret

```

pxctl secrets gcloud delete-secret

```

#### Description

Deletes a secret with the provided ID. Any volumes encrypted with that secret will not be usable

#### Flags

FlagDescription

`--secret_id`, `-i`

(`str`)

Id of the secret to be deleted

This flag is required.

`--force`, `-f`

(`bool`)

Force delete a secret. Any volumes encrypted with that secret will not be usable.

Default value: `false`

## pxctl secrets ibm

```

pxctl secrets ibm

```

#### Description

IBM Key Protect commands

## pxctl secrets ibm list-secrets

```

pxctl secrets ibm list-secrets

```

#### Description

Lists all the available secret ids
