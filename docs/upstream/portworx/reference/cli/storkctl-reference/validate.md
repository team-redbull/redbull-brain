# storkctl validate

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/validate (Portworx Enterprise latest)

storkctl validate | Portworx Enterprise Documentation

Validate stork resources

Example: `storkctl validate <resource> <flags>`

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl validate backuplocation​

Validate BackupLocation credentials and connectivity

Aliases: `bl`

Example: `storkctl validate backuplocation <backuplocation-name> -n <namespace>`

###  Flags

FlagInput typeDescriptionDefaultRequired

`--all-namespaces`, `-A``bool`If present, list the requested object(s) across all namespaces.
Namespace in current context is ignored even if specified with --namespace.`false`Optional

In this topic:
