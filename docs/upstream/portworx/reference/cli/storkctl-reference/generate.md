# storkctl generate

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/generate (Portworx Enterprise latest)

storkctl generate | Portworx Enterprise Documentation

Generate stork specs

note

The following commands support a set of global flags that can be used across all `storkctl` commands. For details, see the Global Flags section.

## storkctl generate clusterpair​

Generate a spec to be used for cluster pairing from a remote cluster

###  Flags

FlagInput typeDescriptionDefaultRequired

`--project-mappings``string`Project mappings between source and destination clusters (currently supported only for Rancher).
Use comma-separated <source-project-id>=<dest-project-id> pairs.
For the project-id, you can also have a cluster-id field added as a prefix to the project-id.
It is recommended to include both one-to-one mappings of the project-id and Rancher cluster-id prefixed project-id as follows:
<source-project-id>=<dest-project-id>,<source-cluster-id>:<source-project-id>=<dest-cluster-id>:<dest-project-id>-Optional

`--storageoptions`, `-s``string`comma separated key-value pair storage options-Optional

In this topic:
