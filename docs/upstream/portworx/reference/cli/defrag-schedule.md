# Set de-fragmentation schedules

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/defrag-schedule (Portworx Enterprise latest)

Set de-fragmentation schedules | Portworx Enterprise Documentation

De-fragmentation is a required process as fragmented data can lead to performance issues. Users can schedule to run this process during periods of low workloads, avoiding any interference and improving performance.

Limitations:

- Not supported with the PX-StoreV2 backend

### Set a defragmentation schedule​

Users can use CLI commands to set up periodic defragmentation schedules during periods of low workloads. Multiple defragmentation schedules can be configured within a cluster; however, only one schedule is allowed per node. The `--include-nodes` option allows you to specify a list of nodes that the defrag schedule will run on.

Use the following command to set up a defragmentation schedule on a node:

```

pxctl cluster defrag schedule create \

--start-time <start-time> \

--max-duration-minutes <duration-of-defrag> \

--include-nodes <nodes-to-be-included-in-the-defrag-run>

--node-selector <label1=value1,label2=value2>

```

important

Portworx interprets the `start-time` in UTC, not in the system's local time zone. Therefore, when configuring a defragmentation schedule, ensure that you convert your intended time to UTC when defining the schedule.

The following flags can be used to set up the schedule:

- `--start-time`: Specifies the start time of the run and can be set in the following formats:

- `daily=19:15` (starts at 19:15 UTC every day)

- `weekly=Sunday@19:15` (starts at 19:15 UTC every Sunday)

- `monthly=22@19:15` (starts at 19:15 UTC on the 22nd day of every month)

- `--max-duration-minutes`: Specifies the duration of each run (end time = start time + max duration).

- `--include-nodes` and `--exclude-nodes`: Specify the comma-separated UUIDs of the nodes to be included or excluded from the run (optional).

- `--max-nodes-in-parallel`: Specifies how many nodes will run the schedule concurrently. The default value is 1. For example, if set to 3, the schedule will run on 3 nodes in parallel (optional).

- `--node-selector` : Specifies the nodes with listed labels on which schedule will run on.

### Configure your defrag schedules cluster-wide​

You can configure all your defragmentation schedule in your cluster with two options:

- Chunk size: The step size of each defragmentation command. The default value is 32 MB.

- Pool full threshold: A percentage threshold for pool space usage. If any pool exceeds this threshold, defragmentation will be disabled for that pool. The default value is 70%.

To configure these options, use the following commands:

```

pxctl cluster options update --defrag-schedule-chunk-size <chunk-size>

```

```

Successfully updated cluster-wide options

```

```

pxctl cluster options update --defrag-schedule-pool-full-threshold <threshold-percentage>

```

```

Successfully updated cluster-wide options

```

To view the current configurations, run the following command:

```

pxctl cluster options list | grep Defrag

```

```

Defrag schedule chunk size (MB)             : 64

Defrag schedule pool full threshold (%)     : 75

```

### Check the status of a defragmentation schedule​

Once the schedule is set, you can use the following command to list your defragmentation schedules:

```

pxctl cluster defrag schedule show

```

```

Defragmentation Schedules:

Schedule ID         : 611122756865623299

Create Time         : 2024-03-08 23:49:12

Frequency           : daily

Start Time          : 23:50

End Time            : 23:51

Nodes Included      : dbca66e4-xxx-xxx, dea00c74-xxx-xxxx

One Iteration Only  : False

Max Number of Nodes Running in Parallel: 2

```

To check the status of the defragmentation operation for each pool, run:

```

pxctl cluster defrag status

```

```

Running Schedule : 611122756865623299 (daily=23:50, 1 minute)

NODE ID          NODE IP         SCHEDULER NODE NAME POOL ID           ITERATIONS POOL USED SPACE LAST START TIME     LAST COMPLETE TIME   RUNNING  PROGRESS

dbca66e4-xxx-xxx 10.13.185.207   N/A                 ce2cec09-5873-xxx 5           4%             2024-03-08 23:50:13  2024-03-08 05:12:54  Yes       0%

```

### Delete a defragmentation schedule​

You can delete schedules using the following methods:

-
Use the `--one-iteration-only` flag while creating a schedule to automatically delete it after one full iteration:

```

pxctl cluster defrag schedule create \

--start-time <start-time> \

--max-duration-minutes <max-duration-of-the-run> \

--max-nodes-in-parallel <number-of-nodes> \

--include-nodes <uuid-1>,<uuid-2> \

--one-iteration-only

```

-
Delete a single schedule:

```

pxctl cluster defrag schedule delete <schedule-id>

```

-
Delete all schedules:

```

pxctl cluster defrag schedule clean-up

```

In this topic:
