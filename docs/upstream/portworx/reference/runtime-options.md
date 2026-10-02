# Runtime parameters

Source: https://docs.portworx.com/portworx-enterprise/reference/runtime-options (Portworx Enterprise latest)

Runtime parameters | Portworx Enterprise Documentation

Runtime options are cluster-wide settings that you can change on a running cluster without reinstalling Portworx Enterprise. Set runtime options by using the `pxctl cluster options update --runtime-options` command.

## Set runtime options​

The `--runtime-options` flag replaces the entire set of runtime options with the values that you specify. It does not merge the specified values with the existing configuration. If you omit a previously configured option, the option is removed from the runtime configuration.

To preserve existing values, review the current runtime options before making changes:

```

pxctl cluster options list

```

Include every option that you want to retain in the update command, along with the option that you are changing. For example, to add `max_resync_bandwidth_mbps` to a cluster that already has `device_delete_after_discard` set, run:

```

pxctl cluster options update --runtime-options "device_delete_after_discard=1,max_resync_bandwidth_mbps=850"

```

```

Successfully updated cluster-wide options

```

Run the following command again to verify that all expected runtime options are set:

```

pxctl cluster options list

```

warning

Do not modify runtime options unless necessary. Contact Portworx Support before changing a runtime option.

## KVDB runtime options​

The following table provides the internal KVDB runtime options that can be used to customize the KVDB database during its runtime.

ParameterDescriptionDefault value

kvdb-
heartbeat-
intervalSpecifies the frequency in milliseconds at which each KVDB node will send heartbeats to its peers.250 ms

kvdb-
election-
timeoutSpecifies the timeout for leader election in milliseconds.1000 ms. By default, Portworx will set the election timeout to 5 times the heartbeat interval.

kvdb-
snap-
countSpecifies the number of committed transactions to trigger a snapshot to disk.10000

kvdb-
debug-
modeSpecifies the debug mode for KVDB debug logs.1 (enabled by default)

kvdb-
pre-
voteRuns the pre-vote election algorithm when a node rejoins. If enabled, it avoids cluster disruptions caused by leader elections when a new node joins.1 (enabled by default)

### Related topics​

- Internal KVDB

In this topic:
