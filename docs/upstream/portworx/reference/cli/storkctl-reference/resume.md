# storkctl resume

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/resume (Portworx Enterprise latest)

storkctl resume | Portworx Enterprise Documentation

Resume schedules

Example: `storkctl resume <resource> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl resume applicationbackupschedules​

Resume applicationBackup schedules

Aliases: `applicationbackupschedule`

Example: `storkctl resume applicationbackupschedule <name> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--backupLocation`, `-b``string`Name of the BackupLocation for which to resume ALL applicationBackup schedules-Optional

## storkctl resume migrationschedules​

Resume migration schedules

Aliases: `migrationschedule`

Example: `storkctl resume migrationschedule <name> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--admin-cluster-pair``string`Referenced admin clusterpair name to resume related migration schedules-Optional

`--clusterPair`, `-c``string`Referenced clusterpair name to resume related migration schedules-Optional

## storkctl resume volumesnapshotschedules​

Resume snapshot schedules

Aliases: `volumesnapshotschedule`, `snapshotschedule`, `snapshotschedules`

Example: `storkctl resume volumesnapshotschedule <name> <flags>`

In this topic:
