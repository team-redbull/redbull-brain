# storkctl update

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/update (Portworx Enterprise 3.6)

storkctl update | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Update stork resources

Example: `storkctl update <resource> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl update volumesnapshotschedules​

Update snapshot schedules

Aliases: `volumesnapshotschedule`, `snapshotschedule`, `snapshotschedules`

Example: `storkctl update volumesnapshotschedule <name> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--new-pvc-name``string`Specify the PVC name to be updated in the volumesnapshotschedule-Yes

In this topic:
