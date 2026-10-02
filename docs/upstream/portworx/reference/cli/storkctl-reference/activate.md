# storkctl activate

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/activate (Portworx Enterprise latest)

storkctl activate | Portworx Enterprise Documentation

Activate resources

Example: `storkctl activate <resource> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl activate clusterdomain​

Activate a cluster domain

Aliases: `cd`

Example: `storkctl activate clusterdomain <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--all`, `-a``bool`Activate all inactive cluster domains`false`Optional

`--name``string`Name for the activate cluster domain action-Optional

`--wait``bool`Wait for clusterdomain update to complete`false`Optional

## storkctl activate migrations​

Activate apps that were created from a migration

Aliases: `migration`

Example: `storkctl activate migrations <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--all-namespaces`, `-a``bool`Activate applications in all namespaces`false`Optional

In this topic:
