# storkctl deactivate

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/deactivate (Portworx Enterprise 3.6)

storkctl deactivate | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Deactivate resources

Example: `storkctl deactivate <resource> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl deactivate clusterdomain​

Deactivate a cluster domain

Aliases: `cd`

Example: `storkctl deactivate clusterdomain <name> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--name``string`Name for the deactivate cluster domain action-Optional

`--wait``bool`Wait for clusterdomain update to complete`false`Optional

## storkctl deactivate migrations​

Deactivate apps that were created from a migration

Aliases: `migration`

Example: `storkctl deactivate migration <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--all-namespaces`, `-a``bool`Deactivate applications in all namespaces`false`Optional

In this topic:
