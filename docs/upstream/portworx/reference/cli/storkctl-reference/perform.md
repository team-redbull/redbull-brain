# storkctl perform

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/perform (Portworx Enterprise 3.6)

storkctl perform | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

perform actions

Example: `storkctl perform <action> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl perform failback​

Initiate failback of the given migration schedule

Example: `storkctl perform failback -n <reverse-migration-schedule-namespace> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--exclude-namespaces``stringSlice`Specify the comma-separated list of subset namespaces to be skipped during the failback. By default, all namespaces part of the MigrationSchedule are failed back`[]`Optional

`--exclude-objects``stringSlice`Specific objects to exclude (format: KIND/NAMESPACE/NAME or GROUP/VERSION/KIND/NAMESPACE/NAME). Mutually exclusive with --selectors, --exclude-selectors, --resource-types, and --include-objects.`[]`Optional

`--exclude-selectors``stringToString`Resources with the provided labels will be excluded from activation/deactivation during this failback. Cannot be used together with --selectors.`[]`Optional

`--force``bool`If present, bypasses confirmation prompts and proceeds with the operation`false`Optional

`--include-namespaces``stringSlice`Specify the comma-separated list of subset namespaces to be failed back. By default, all namespaces part of the MigrationSchedule are failed back`[]`Optional

`--include-objects``stringSlice`Specific objects to include (format: KIND/NAMESPACE/NAME or GROUP/VERSION/KIND/NAMESPACE/NAME). Mutually exclusive with --selectors, --exclude-selectors, --resource-types, and --exclude-objects.`[]`Optional

`--migration-reference`, `-m``string`Specify the MigrationSchedule to failback. Also specify the namespace of this MigrationSchedule using the -n flag-Yes

`--resource-types``stringSlice`Filter resources by resource type (KIND or GROUP/VERSION/KIND, e.g. apps/v1/Deployment). May be specified multiple times.`[]`Optional

`--selectors``stringToString`Only resources that have all of the provided labels will be activated/deactivated during this failback (the labels are AND'ed; this is a key=value map, so the same label key cannot be provided with multiple values). Cannot be used together with --exclude-selectors.`[]`Optional

`--skip-last-mile-migration``bool`If present, skip running a last-mile migration before activating workloads during failback`false`Optional

## storkctl perform failover​

Initiate failover of the given migration schedule

Example: `storkctl perform failover -n <migration-schedule-namespace> <flags>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--exclude-namespaces``stringSlice`Specify the comma-separated list of subset namespaces to be skipped during the failover. By default, all namespaces part of the MigrationSchedule are failed over`[]`Optional

`--exclude-objects``stringSlice`Specific objects to exclude (format: KIND/NAMESPACE/NAME or GROUP/VERSION/KIND/NAMESPACE/NAME). Mutually exclusive with --selectors, --exclude-selectors, --resource-types, and --include-objects.`[]`Optional

`--exclude-selectors``stringToString`Resources with the provided labels will be excluded from activation/deactivation during this failover. Cannot be used together with --selectors.`[]`Optional

`--force``bool`If present, bypasses confirmation prompts and proceeds with the operation`false`Optional

`--include-namespaces``stringSlice`Specify the comma-separated list of subset namespaces to be failed over. By default, all namespaces part of the MigrationSchedule are failed over`[]`Optional

`--include-objects``stringSlice`Specific objects to include (format: KIND/NAMESPACE/NAME or GROUP/VERSION/KIND/NAMESPACE/NAME). Mutually exclusive with --selectors, --exclude-selectors, --resource-types, and --exclude-objects.`[]`Optional

`--migration-reference`, `-m``string`Specify the MigrationSchedule to failover. Also specify the namespace of this MigrationSchedule using the -n flag-Yes

`--resource-types``stringSlice`Filter resources by resource type (KIND or GROUP/VERSION/KIND, e.g. apps/v1/Deployment). May be specified multiple times.`[]`Optional

`--selectors``stringToString`Only resources that have all of the provided labels will be activated/deactivated during this failover (the labels are AND'ed; this is a key=value map, so the same label key cannot be provided with multiple values). Cannot be used together with --exclude-selectors.`[]`Optional

`--skip-last-mile-migration``bool`If present, skip running a last-mile migration before activating workloads during failover`false`Optional

`--skip-source-cluster-domain-deactivation``bool`If present, source cluster domain deactivation will be skipped. Note: --skip-source-operations supersedes this flag if both are specified`false`Optional

`--skip-source-operations``bool`If present, operations performed on the source cluster will be skipped, and applications on the current cluster will be scaled up`false`Optional

In this topic:
