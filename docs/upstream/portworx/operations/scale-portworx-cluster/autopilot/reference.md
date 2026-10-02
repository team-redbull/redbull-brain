# AutopilotRule Reference

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/reference (Portworx Enterprise 3.6)

AutopilotRule Reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This topic describes the `AutopilotRule` Custom Resource Definition (CRD) specifications and actions supported by Autopilot. It provides examples of the `events` option available to view the actions that Autopilot is taking or has taken in the past.

## AutopilotRule CRD specification​

FieldDescriptionOptional?Default

selectorSelects the objects affected by this rule using either `matchLabels`, `matchExpressions`, or both selectors. Syntax.Yesempty

namespaceSelectorSelects the namespaces affected by this rule using either `matchLabels`, `matchExpressions`, or both namespace selectors. Syntax.Yesall

conditionsDefines the metrics that need to be for the rule's actions to trigger. All conditions are AND'ed. Syntax.No

actionsDefines what action to take when the conditions are met. Syntax. See Supported Autopilot actions for all actions that you can specify here.No

pollIntervalDefines the interval in seconds at which the conditions for the rule are queried from the metrics provider.
Note: You can reduce the poll interval to speed up Autopilot operations, but this will increase the load on Prometheus and lead to an increase in CPU consumption.Yes

- Autopilot version 1.3.15 or earlier: 10 seconds

- Autopilot version 1.3.16 or later: 60 seconds

actionsCoolDownPeriodDefines the duration in seconds for which autopilot will not re-trigger any actions once they have been executed.Yes5 minutes

actionWindowDefines the timestamps during which the action can be triggered. SyntaxYesNone

### selector​

Selects the objects affected by this rule using either `matchLabels`, `matchExpressions`, or both selectors.

note

You can refer to Labels and Selectors for more information on how to use `matchLabels` and `matchExpressions`.

#### `matchLabels`​

```

selector:

  matchLabels:

    <selector-key>: <selector-value>

```

#### `matchExpressions`​

```

selector:

  matchExpressions:

    - key: <selector-key>

      operator: <logical-operator>

      values:

        - <selector-value>

```

#### Example​

Below is an example spec snippet for using `matchLabels`:

```

selector:

  matchLabels:

    app: postgres

```

Below is an example spec snippet for using `matchExpressions`:

```

selector:

  matchExpressions:

    - key: app

      operator: In

      values:

        - data-writer

        - writer

```

### namespaceSelector​

Selects the namespaces affected by this rule using a either `matchLabels`, `matchExpressions`, or both selectors.

note

You can refer to Labels and Selectors for more information on how to use `matchLabels` and `matchExpressions`.

#### `matchLabels`​

```

namespaceSelector:

  matchLabels:

    <selector-key>: <selector-value>

```

#### `matchExpressions`​

```

namespaceSelector:

  matchExpressions:

    - key: <selector-key>

      operator: <logical-operator>

      values:

        - <selector-value>

```

#### Example​

Below is an example spec snippet for using `matchLabels`:

```

namespaceSelector:

  matchLabels:

    app: postgres

```

Below is an example spec snippet for using `matchExpressions`:

```

namespaceSelector:

  matchExpressions:

    - key: app

      operator: In

      values:

        - data-writer

        - writer

```

### conditions​

Defines the metrics that need to be for the rule's actions to trigger. Conditions schema differs for Prometheus and Datadog. For Prometheus, a condition is evaluated using key, operator, and values while Datadog evaluates using a single expression.

note

Multiple conditions are combined using a logical AND.

#### conditions for Prometheus​

Conditions compare the `key` field with the `values` field using the `operator` field. Condition keys can contain logic and use monitoring values.

```

conditions:

  - key: "<condition-formula>"

    operator: <logical-operator>

    values:

    - "<comparator>"

  for: <5>

```

It follows the below schema.

FieldDescriptionOptional?Default

keyThis is the metrics query that would be sent to the monitoring provider (e.g prometheus).noempty

operatorThis is the logical operator to use to compare the results of the query in key above to the values. Supported operators are:

- `In`

- `NotIn`

- `Lt`

- `Gt`

- `LtEq`

- `GtEq`

- `InRange`

- `NotInRange`

noempty

valuesThis is the value or list of values against which the key and operator are compared.

- `In`, `NotIn` need a list of values

-  `Gt`, `Lt`, `GtEq`, `LtEq` need a single numerical value.

- `InRange`, `NotInRange` need exactly 2 numerical values

noempty

forSpecifies the duration (in seconds) for which the condition must be true before triggering the defined action.yes30

#### conditions for Datadog​

Datadog’s query syntax differs from PromQL in a few key ways:

- Aggregations are prefixes, e.g. `avg:metric` and not `avg(metric)`.

- Label filters use colon syntax and no quotes, e.g. `{pool:pool-1}`.

- You can group by tags inline using by `{pool}` or `{volumename}`.

FieldDescriptionOptional?Default

providerMetrics provider to be used by AutopilotRule. Use `datadog` to use Datadog as provider.No`prometheus`

expressionsContains `expression` that will be evaluated based on the Datadog metrics.Noempty

Example of the Datadog query for expression:

```

100 * (avg:portworx.px_pool_stats_available_bytes{cluster_name:<your_cluster_name>} by {pool} / avg:portworx.px_pool_stats_total_bytes{cluster_name:<your_cluster_name>} by {pool})

```

The parameter `cluster_name` requires you to provide value for `<your_cluster_name>`. Provide a complete Datadog expression that already evaluates to a boolean using native helper functions such as `is_less` or `is_greater` in the query.

Example AutopilotRule to expand a pool when available capacity is less than 10%:

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand-datadog

spec:

  conditions:

    provider: datadog

    expressions:

      - expression: is_less(

          100 * (avg:portworx.px_pool_stats_available_bytes{cluster_name:<your_cluster_name>} by {pool} / avg:portworx.px_pool_stats_total_bytes{cluster_name:<your_cluster_name>} by {pool}),

          10

        )

  actions:

    - name: openstorage.io.action.storagepool/expand

      params:

        scalepercentage: "50"

```

This AutopilotRule uses `datadog` as `provider` and in `expressions` contains 1 expression. The expression will return 1 if the capacity is less than 10%. The `actions` to expand storage pool will execute and expand storage pool by 50% of the current value.

### actions​

Defines what action to take when the conditions are met. See the Supported Actions section for the list of actions that you can specify.

```

action:

  name: <operation>

  params:

    <operation-specific-paramater>: <value>

    maxsize: "<value>Gi"

```

### actionWindow​

Defines time-based execution windows during which actions may be triggered. If not specified, actions may trigger immediately when conditions are met. This feature is available with Autopilot version 1.4 and above.

note

Action windows are applicable only for `openstorage.io.action.storagepool/expand` and `openstorage.io.action.storagepool/rebalance` actions. Volume resize actions `openstorage.io.action.volume/resize` are not affected by action windows and will execute immediately when conditions are met.

The following table describes the 3 parameters that are needed to define and enable action window:

FieldDescriptionOptional?Default

`enabled`Controls whether window enforcement is active.Yes`true`

`timezone`Specifies the timezone for evaluating the time windows. Must be a valid IANA timezone (for example, `America/New_York`, `UTC`, `Europe/London`, `Asia/Tokyo`).Yes`UTC`

`windows`Defines one or more time windows during which actions may be triggered. If multiple windows are defined, actions may trigger when the current time matches any window. At least one window must be defined. SyntaxNoempty

#### `windows`​

Defines one or more timestamps during which the action will be triggered using the following fields.

FieldDescriptionOptional?Default

`name`Name for this window.Yesempty

`startTime`Start time in `HH:MM` (24-hour) or `hh:mmAM/am/PM/pm` (12-hour) format.Noempty

`endTime`End time in `HH:MM` (24-hour) or `hh:mmAM/am/PM/pm` (12-hour) format.Noempty

`daysOfWeek`Specifies which days this window is active. Valid values: `Sunday`, `Sun`, `Monday`, `Mon`, `Tuesday`, `Tue`, `Wednesday`, `Wed`, `Thursday`, `Thu`, `Friday`, `Fri`, `Saturday`, `Sat`. If empty, the window applies to all days.Yesempty (all days)

#### Example​

Here is an example of the Autopilot rule with an action window that is defined only to trigger storage pool expansion at a specific time on weekdays and weekends.

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand-with-action-window

spec:

  # Action Window Configuration

  actionWindow:

    enabled: true #optional, disables when set to false

    timezone: "America/New_York"

    windows:

      # Weekday trigger window

      - name: "trigger-window-1"

        startTime: "02:00"      # 2:00 AM (24-hour format)

        endTime: "04:00"        # 4:00 AM

        daysOfWeek: ["Mon", "Tue", "Wed", "Thu", "Fri"]

      # Weekend trigger window

      - name: "trigger-window-2"

        startTime: "12:00AM"    # 12:00 AM (12-hour format)

        endTime: "6:00AM"       # 6:00 AM

        daysOfWeek: ["Saturday", "Sunday"]

  # conditions are the symptoms to evaluate

  conditions:

    expressions:

    # Pool available capacity less than 40%

    - key: "100 * (px_pool_stats_available_bytes / px_pool_stats_total_bytes)"

      operator: Lt

      values:

        - "40"

  # action to perform when conditions are true and action window is met

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        scalepercentage: "10"

        scaletype: "add-disk"

```

Note the following about this configuration:

- Action window enforcement is enabled, and all time evaluations are performed using the `America/New_York` timezone.

- Two action windows are defined, and an action to expand storage pool will be triggered if the current time falls within any of the configured windows and the conditions are met.

- The `trigger-window-1` window allows storage pool expansion between 02:00 and 04:00 from Monday through Friday using the 24-hour time format.

- The `trigger-window-2` window allows storage pool expansion between 12:00 AM and 6:00 AM on Saturday and Sunday using the 12-hour time format.

## Supported Autopilot actions​

### openstorage.io.action.volume/resize​

This action is to perform resize on Kubernetes PersistentVolumeClaims (PVCs).
 Parameters​

- scalepercentage: Specifies the percentage of current PVC size by which Autopilot should resize the PVC. If not specified, the default is 50%.

- maxsize: Specifies the maximum PVC size in bytes after which Autopilot should stop resizing the PVCs. Note that you can specify the unit of measurement as part of the value. For example, if you want to use GiB, you can specify the unit of measurement like this: `maxsize: "400Gi"`. If not specified, the default value is unlimited.

 Examples​
Resize the PVC by 100% of current size

```

  actions:

  - name: openstorage.io.action.volume/resize

    params:

      scalepercentage: "100"

      maxsize: "12Gi"

```

### openstorage.io.action.storagepool/expand​

This action performs expansion on Portworx storage pools.
 Parameters​

- scalepercentage: Specifies the percentage of current pool size by which Autopilot should resize it. If not specified, the default is 50%.

- scaletype: Specifies the type of operation to be performed to expand the pool. Supported values are:

- auto: Portworx scales the pool automatically by either adding new disks or resizing the existing disks. Autopilot chooses the best method to expand the pool based on the current configuration and available resources.

- add-drive: Portworx adds new disks to the existing storage pool.

important

You cannot use the `add-drive` operation if you are using PX-StoreV2 as your backend for expanding your pools.

- resize-drive: Portworx resizes the existing disks in the storage pool.

- scalesize: Specifies the new minimum required size of the storage pool in Gi or Ti. The eventual size of the pool can be greater than this as Portworx needs to add/resize disks such that all disks in the pool are of the same size.

- dontWaitForCleanVolumes (Optional): When set to `"true"`, Autopilot forces pool expansion even if some volumes have a single replica (`repl1`) on the pool. This bypasses single-replica (`repl1`) volume checks that would normally block pool expansion operations.

note

You cannot combine the scalepercentage and scalesize parameters; use only one of them in an Autopilot rule.

 Examples​
Expand the pool by 50% of current size automatically:

```

actions:

  - name: openstorage.io.action.storagepool/expand

    params:

      scalepercentage: "50"

      scaletype: "auto"

```

Expand the pool by 50% of current size by adding disks:

```

actions:

  - name: openstorage.io.action.storagepool/expand

    params:

      scalepercentage: "50"

      scaletype: "add-drive"

```

Expand the pool by 100Gi by resizing disks:

```

actions:

  - name: openstorage.io.action.storagepool/expand

    params:

      scalesize: "100Gi"

      scaletype: "resize-drive"

```

Force expand the pool by 50% of the current size by resizing disks, skipping single-replica (`repl1`) volume checks:

```

actions:

  - name: openstorage.io.action.storagepool/expand

    params:

      scalepercentage: "50"

      scaletype: "resize-drive"

      dontWaitForCleanVolumes: "true"

```

#### Use cases​

- Automatically expand storage pools by usage

- Expand all storage pools

### openstorage.io.action.storagepool/rebalance​

This action performs a rebalance operation on Portworx Storage Pools.

#### Use cases​

- Automatically rebalance storage pools based on provisioned and used space

## Autopilot Events​

You can view the actions Autopilot takes by querying Autopilot events. These events provide insight into how your Autopilot rules are functioning, what actions they may be taking, and what actions they have taken in the past.

Autopilot rule eventDescription

InitializingThe rule's initial startup state where monitoring has not yet begun.

NormalAutopilot is monitoring the rule as expected.

TriggeredThe rule has its activation conditions met.

ActiveActionsPendingThe rule's activation conditions have been met, but the actions are not yet being performed.

ActiveActionsTakenAutopilot has performed the rule's actions, but still hasn't moved out of the active status.

ActionsDeclinedAutopilot has intentionally declined to perform a rule's action, for example when a PVC reaches a maximum user-defined size.

ActiveActionsInProgressThe rule is active and had its conditions met and there is an ongoing action on the object.

ActionNotLicensedThe action Autopilot is trying to perform is not permitted due to license restrictions

ActionAwaitingWindowThe rule's conditions are met, but the action is waiting for the configured action window to become active. This state only applies to storage pool expand and rebalance actions.

You can query events from Kubernetes by entering the following `kubectl get events` command:

- OpenShift

- Kubernetes

```

kubectl get events --field-selector involvedObject.kind=AutopilotRule

```

```

LAST SEEN   FIRST SEEN   COUNT   NAME                                   KIND            SUBOBJECT   TYPE      REASON           SOURCE      MESSAGE

41m         41m          1       pvc-total-size-15gi.15f13fcf9664716d   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Initializing => Normal

41m         41m          1       pvc-total-size-15gi.15f13fcf96a75e4f   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Initializing => Normal

36m         38m          2       pvc-total-size-15gi.15f14003ff20f5ec   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsInProgress => ActiveActionsTaken

35m         37m          2       pvc-total-size-15gi.15f140126cc4021c   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsTaken => Normal

35m         38m          3       pvc-total-size-15gi.15f13ff9ae4cc963   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Normal => Triggered

34m         34m          2       pvc-total-size-15gi.15f14032de7660a7   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsInProgress => ActionsDeclined

```

```

oc get events --field-selector involvedObject.kind=AutopilotRule

```

```

LAST SEEN   FIRST SEEN   COUNT   NAME                                   KIND            SUBOBJECT   TYPE      REASON           SOURCE      MESSAGE

41m         41m          1       pvc-total-size-15gi.15f13fcf9664716d   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Initializing => Normal

41m         41m          1       pvc-total-size-15gi.15f13fcf96a75e4f   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Initializing => Normal

36m         38m          2       pvc-total-size-15gi.15f14003ff20f5ec   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsInProgress => ActiveActionsTaken

35m         37m          2       pvc-total-size-15gi.15f140126cc4021c   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsTaken => Normal

35m         38m          3       pvc-total-size-15gi.15f13ff9ae4cc963   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from Normal => Triggered

34m         34m          2       pvc-total-size-15gi.15f14032de7660a7   AutopilotRule               Normal    Transition       autopilot   rule: pvc-total-size-15gi:pvc-xxxxxxxx-xxxx-xxxx-xxxx-000c29fda8e7 transition from ActiveActionsInProgress => ActionsDeclined

```

In this topic:
