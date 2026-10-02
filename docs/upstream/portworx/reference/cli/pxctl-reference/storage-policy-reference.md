# pxctl storage-policy

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/storage-policy-reference (Portworx Enterprise latest)

pxctl storage-policy | Portworx Enterprise Documentation

## pxctl storage-policy

```

pxctl storage-policy

```

#### Description

Manage storage policies for creating volumes

#### Example

```

pxctl storage-policy create --replication 2,min --periodic 60,10 devpolicy

```

## pxctl storage-policy create

```

pxctl storage-policy create <required-argument>

```

#### Description

Create a storage policy

#### Example

```

pxctl storage-policy create [flags] policy-name

```

#### Flags

FlagDescription

`--sticky`

(`bool`)

sticky volumes cannot be deleted until the flag is disabled

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

`--replication`, `-r`

(`str`)

replication factor `repl,max/min` (replication is equal by default)

`--journal`

(`bool`)

Journal data for volume

`--aggregation_level`, `-a`

(`str`)

aggregation level
Valid values:

- `1`

- `2`

- `3`

- `auto`

Default value: `1`

`--policy`

(`str`)

policy names separated by comma

`--secure`

(`bool`)

encrypt volumes using AES-256

`--shared`

(`bool`)

make a globally shared namespace volumes

`--io_profile`

(`str`)

IO Profile
Valid values:

- `sequential`

- `cms`

- `db`

Default value: `sequential`

`--force`

(`bool`)

Force volume creation to fail if storage policy rules not followed by volume

`--update`

(`bool`)

Allow volume to update without storage policy restriction

## pxctl storage-policy delete

```

pxctl storage-policy delete <required-argument>

```

#### Description

Delete a storage policy

#### Example

```

pxctl storage-policy delete policy-name

```

#### Flags

FlagDescription

## pxctl storage-policy update

```

pxctl storage-policy update <required-argument>

```

#### Description

Update a storage policy

#### Example

```

pxctl storage-policy update [flags] policy-name

```

#### Flags

FlagDescription

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

`--replication`, `-r`

(`str`)

replication factor `repl,max/min` (replication is equal by default)

`--sticky`

(`bool`)

set sticky setting

`--journal`

(`bool`)

Journal data for volumes

`--aggregation_level`, `-a`

(`str`)

aggregation level
Valid values:

- `1`

- `2`

- `3`

- `auto`

Default value: `1`

`--policy`

(`str`)

policy names separated by comma

`--secure`

(`bool`)

encrypt volumes using AES-256

`--shared`

(`bool`)

make a globally shared namespace volumes

`--io_profile`

(`str`)

IO Profile
Valid values:

- `sequential`

- `cms`

- `db`

Default value: `sequential`

`--force`

(`bool`)

Force volume creation to fail if storage policy rules not followed by volume

`--update`

(`bool`)

Allow volume to update without storage policy restriction

## pxctl storage-policy list

```

pxctl storage-policy list

```

#### Description

List all storage policies

## pxctl storage-policy inspect

```

pxctl storage-policy inspect <required-argument>

```

#### Description

Inspect a storage policy.

#### Example

```

pxctl storage-policy inspect policyName

```

## pxctl storage-policy set-default

```

pxctl storage-policy set-default

```

#### Description

Set storage policy as default policy

#### Example

```

pxctl storage-policy set-default policyName

```

## pxctl storage-policy unset-default

```

pxctl storage-policy unset-default

```

#### Description

Remove default storage policy restriction

#### Example

```

pxctl storage-policy unset-default

```

## pxctl storage-policy access

```

pxctl storage-policy access

```

#### Description

This command manages access permissions to a storage policy. There are two ways
to provide access, one is by adding a group and the other is by adding
a specific user as a collaborator. When adding a collaborator, you
must use the unique id of the user. Please consult with your admin
on how to obtain the unique id of the user.
ACCESS TYPES
When adding a group or collaborator, an access type must also be
given, which can be either Read, Write, or Admin.
A Read access type allows access to the storage policy without modifying
it. With a Read access type, one can list or inspect the storage policy.
A Write access type allows modification of the storage policy and its volume specs,
for example allowing to create, update stirage policy in adition to all Read access.
An Admin access type allows full access to the storage policy, like deleting
the storage in addition to all Write access.
Note only system admin can set/release default storage policy restriction on cluster
SETTING ACCESS TYPES
To set access types, add the following suffix to the group or collaborator
separated by a colon ':'
 r - For Read access type
 w - For Write access type
 a - For Admin access type

#### Example

```

Add group1 for read access

  pxctl stp access add --group group1:r

Add group2 for write access

  pxctl stp access add --group group2:w

Add user1 for admin access using the id of user1

  pxctl stp access add --collaborator user1Id:a

Remove user1 access using the id of user1

  pxctl stp access remove --collaborator user1Id

Set the access using one command. This clears any previous settings and updates it with

the following

  pxctl stp access update --groups group1:r,group2:w --collaborators user1Id:a

```

## pxctl storage-policy access show

```

pxctl storage-policy access show

```

#### Description

List the owner and storage policy ACLS

#### Example

```

pxctl storage-policy access show [flags] policyName

```

## pxctl storage-policy access add

```

pxctl storage-policy access add

```

#### Description

Adds a single group or collaborator

#### Example

```

pxctl storage-policy access add [flags] policyName

```

#### Flags

FlagDescription

`--group`, `-g`

(`str`)

group to add with access type. See storage-policy access help for more information

`--collaborator`, `-c`

(`str`)

collaborator to add with access type. Must be the unique id of the user. See storage-policy access for more information

## pxctl storage-policy access remove

```

pxctl storage-policy access remove

```

#### Description

Removes a single group or collaborator

#### Example

```

pxctl storage-policy access remove [flags] policyName

```

#### Flags

FlagDescription

`--group`, `-g`

(`str`)

group to remove

`--collaborator`, `-c`

(`str`)

collaborator to remove

## pxctl storage-policy access update

```

pxctl storage-policy access update

```

#### Description

Update the owner and/or complete set of storage policy ACLS

#### Example

```

pxctl storage policy access update [flags] policyName

```

#### Flags

FlagDescription

`--owner`, `-o`

(`str`)

username of the desired owner. Only an administrator can change this value.

`--groups`, `-g`

(`str`)

list of comma-separated group names with access type. See storage-policy access for more information

`--collaborators`, `-c`

(`str`)

list of comma-separated collaborator names with access type. See storage policy access for more information
