# Optimize Cache Performance with Auto-Tune Cache Migration Threshold

Source: https://docs.portworx.com/portworx-enterprise/operations/tune-performance/auto-tune-cache (Portworx Enterprise 3.6)

Optimize Cache Performance with Auto-Tune Cache Migration Threshold | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Enable auto-tune and optimize your cache performance by auto-tuning cache tunables like migration threshold.

## Enable auto-tune​

Use the `pxctl cluster options update` command with the `--poolcache` flag to enable auto-tune.

```

pxctl cluster options update --poolcache on

```

This enables auto-tuning with default thresholds.

- Minimum dirty threshold: 33%

- Maximum dirty threshold: 67%

## Custom thresholds​

You can specify custom thresholds using `poolcache` option.

```

pxctl cluster options update --poolcache on,<min_dirty>,<max_dirty>

```

For example, to set thresholds to `40%` minimum and `75%` maximum:

```

pxctl cluster options update --poolcache on,40,75

```

## Threshold limits​

ParameterDefaultMinimumMaximum

`min_dirty`33%10%(must be < max_dirty)

`max_dirty`67%(must be > min_dirty)90%

info

If you specify invalid thresholds (min >= max, or out of limits), Portworx will override them with default values.

## Disable auto-tune​

To disable auto-tuning, use `poolcache` option.

```

pxctl cluster options update --poolcache off

```

You can manually tune `migration_threshold` by configuring storage pool cache.

## Check auto-tune status​

View the current auto-tune configuration and state:

```

pxctl service pool cache status <pool_id>

```

Look for these fields:

- `AutoTune`: Whether auto-tuning is enabled

- `DirtyState`: Current state (`low`, `optimal`, or `high`)

- `MinDirtyPercent`: Configured minimum threshold

- `MaxDirtyPercent`: Configured maximum threshold

Example output:

```

PX Cache Configuration and Status:

Pool ID:  0

        Enabled:  true

        ...

        DirtyBlocks: 2500

        TotalBlocks: 8564

        ...

        DirtyState: optimal

        AutoTune: true

        MinDirtyPercent: 33

        MaxDirtyPercent: 67

```

In this example, dirty blocks are 2500/8564 = ~29%, which would be below the 33% threshold (DirtyState: low).

## View current cluster options​

Check the current auto-tune configuration for the cluster:

```

pxctl cluster options list

```

Look for the `PoolCacheConfig` section in the output.

## Best practices for auto-tune pool cache​

- Start with defaults. The default thresholds (33%, 67%) work well for most workloads.

- Monitor before tuning. Use `pxctl service pool cache status` to understand your workload patterns before adjusting thresholds.

- Workload considerations:

- For bursty write workloads, consider lowering the max threshold to trigger earlier cleanup

- For steady-state workloads, default thresholds are usually optimal

- Don't over-tune. Frequently changing thresholds can cause unstable behavior

## Troubleshooting storage pool cache configuration​

### Cache is always in "high" state​

This indicates your workload consistently generates more writes than the backing storage can absorb. Consider:

- Adding more cache capacity

- Using faster backing storage

- Reducing write load

### Cache is always in "low" state​

This indicates your cache is larger than needed for your workload. This is not a problem - it just means you have headroom for burst activity.

### Auto-tune not taking effect​

Verify auto-tune is enabled:

- Check cluster options: `pxctl cluster options list`

- Verify pool status shows `AutoTune: true`

- Ensure caching is enabled on the pool

## Related Topics​

- Storage pool caching

- Configure storage pool cache

- pxctl cluster options reference

In this topic:
