# pxctl role

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/pxctl-reference/role-reference (Portworx Enterprise 3.6)

pxctl role | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## pxctl role

```

pxctl role

```

#### Description

Portworx pxctl authorization role commands. Roles define permission rules for users capabilities.

## pxctl role list

```

pxctl role list

```

#### Description

Display the role names available for use by a user.

#### Example

```

pxctl role list

```

## pxctl role create

```

pxctl role create

```

#### Description

Create a role using a json file which specifies the role and its rules. A role consist of a set of rules defining services
and api's which are allowable.
e.g. Rule file which allows inspection of any object and listings of only volumes:
 {
 "name": "test.view",
 "rules": [
 {
 "services": [
 "volumes"
 ],
 "apis": [
 "*enumerate*"
 ]
 },
 {
 "services": [
 "*"
 ],
 "apis": [
 "inspect*"
 ]
 }
 ]
 }

#### Example

```

pxctl role create --role-config <path to json file>

```

#### Flags

FlagDescription

`--role-config`

(`str`)

create role using role json file

This flag is required.

## pxctl role delete

```

pxctl role delete

```

#### Description

Remove a role and its permission rules by name.

#### Example

```

pxctl role delete --name <role name>

```

#### Flags

FlagDescription

`--name`

(`str`)

role to delete

This flag is required.

## pxctl role update

```

pxctl role update

```

#### Description

Update a role applies changes to an existing role. Changes to the role and its rules are specified in a json file.
Json file format is the same as the "role create" json file. Which defines the role and the rules. The entire role
be updated.

#### Example

```

pxctl role update --role-config <path to json file>

```

#### Flags

FlagDescription

`--role-config`

(`str`)

update role using role json file

This flag is required.

## pxctl role inspect

```

pxctl role inspect

```

#### Description

Display permission rules for a specific role or for all the roles.

#### Example

```

pxctl role inspect --name <role name> | --all

```

#### Flags

FlagDescription

`--name`

(`str`)

show permission rules of a specified role name

`--all`

(`bool`)

list roles and permission rules of all the roles
