# pxctl clouddrive

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/clouddrive-reference (Portworx Enterprise 3.6)

pxctl clouddrive | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl clouddrive

```

pxctl clouddrive

```

#### Description

Manage cloud drives

## pxctl clouddrive list

```

pxctl clouddrive list

```

#### Description

List all the cloud drives currently being used

## pxctl clouddrive list-drives

```

pxctl clouddrive list-drives

```

#### Description

List all the cloud drives currently being used

#### Flags

FlagDescription

`--selector`, `-l`

(`str`)

Selector (label query) to filter on. Supports '='.(e.g. -l key1=value1)

## pxctl clouddrive inspect

```

pxctl clouddrive inspect

```

#### Description

Inspect and view all the drives of a DriveSet

#### Flags

FlagDescription

`--node`

(`str`)

Node ID of the DriveSet to inspect.

This flag is required.

`--pool-uid`

(`str`)

Pool UUID of the drives to inspect.

## pxctl clouddrive update-labels

```

pxctl clouddrive update-labels

```

#### Description

Updates the labels on the drive set for the provided node.

#### Flags

FlagDescription

`--node`, `-n`

(`str`)

ID of the node who owns the drive set.

This flag is required.

`--labels`, `-l`

(`str`)

Comma separated list of key value pairs in the <key1>=<value1>,<key2>=<value2> format. If not provided sets empty labels.

## pxctl clouddrive transfer

```

pxctl clouddrive transfer

```

#### Description

Transfers the cloud drive set from given source node to a destination node

## pxctl clouddrive transfer submit

```

pxctl clouddrive transfer submit

```

#### Description

Submit a new job to transfer a cloud drive set

#### Flags

FlagDescription

`--src`, `-s`

(`str`)

ID of the PX node who currently owns the drive set. This is the 'NodeID' displayed in the output of the 'pxctl clouddrive list' command.

This flag is required.

`--dest`, `-d`

(`str`)

ID of the instance who should own the drive set. This is the 'InstanceID' displayed in the output of the 'pxctl clouddrive list' command. The destination instance needs to be a storage less node (with no Drive IDs) and in the same zone (if your cluster has zones). This is optional and if not provided, an online storageless node will be used.

## pxctl clouddrive transfer list

```

pxctl clouddrive transfer list

```

#### Description

Lists cloud drive transfer jobs in the system

## pxctl clouddrive transfer status

```

pxctl clouddrive transfer status

```

#### Description

Status of a cloud drive transfer job

#### Flags

FlagDescription

`--job-id`, `-i`

(`str`)

This flag is required.

## pxctl clouddrive credentials-validate

```

pxctl clouddrive credentials-validate

```

#### Description

Validate credentials for cloud providers and verify that the account has all the permissions that portworx requires.

Use one of the following methods to validate credentials:
1. --secret: Use credentials from the secret provider
2. --username: Provide username directly (password will be prompted)

#### Example

```

pxctl clouddrive credentials-validate --secret

pxctl clouddrive credentials-validate --username <username>

```

#### Flags

FlagDescription

`--secret`, `-s`

(`bool`)

Use credentials from the secret provider

`--username`, `-u`

(`str`)

Username for cloud provider authentication (password will be prompted)
