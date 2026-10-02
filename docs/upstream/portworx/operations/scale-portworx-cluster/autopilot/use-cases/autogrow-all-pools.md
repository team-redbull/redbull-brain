# Expand every Portworx storage pool in your cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/use-cases/autogrow-all-pools (Portworx Enterprise 3.6)

Expand every Portworx storage pool in your cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can use Autopilot to expand every storage pool in your Portworx cluster until they reach a certain capacity.

Autopilot uses Portworx APIs to expand storage pools, and these APIs currently support the following cloud providers:

- Azure

- AWS

- VMware vSphere

- FlashArray

- Google Cloud Platform

note

The `add-drive` method is not supported with PX-StoreV2.

## Prerequisites​

- Portworx cloud drives: Your Portworx installation must use one of the supported cloud drives where Portworx provisions the backing drives using the cloud provider

- Autopilot version: 1.3.13 or newer

## Example​

The following example Autopilot rules use the different scale types supported to resize all Portworx storage pools in the cluster until each pool exceeds 400 GiB. For more information about scale types, refer to `openstorage.io.action.storagepool/expand`.

- Auto

- Add drive

- Resize drive

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand-till-400

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate.

  conditions:

    expressions:

    # pool size is less than 400 GiB

    - key: "px_pool_stats_total_bytes/(1024*1024*1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when condition is true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # resize pool by scalepercentage of current size. The 100% shown below will double the current pool size.

        scalepercentage: "100"

        # when scaling, add-drive/resize-drive to the pool based on available resources

        scaletype: "auto"

```

### Key Sections in the Spec

- The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains a single formula:

- The key `px_pool_stats_total_bytes/(1024*1024*1024)` calculates the total pool capacity in GiB.

- The `Lt` (less than) operator sets the threshold at 400GiB, meaning the action will trigger if a pool’s size is below this value.

- The `actions` section specifies what action Portworx performs when the conditions are met. Action parameters modify action behavior, and different actions contain different action parameters. In this example, the actions section directs Portworx to do the following:

- The pool size is doubled by increasing it by 100% of its current size (`scalepercentage: "100"`).

- The `auto` scale type is used, allowing Autopilot to either add new drives or resize existing ones automatically, based on available resources and configuration.

note

PX-StoreV2 supports scaling using only the `resize-drive` method. The `add-drive` method is not supported. If you select the `auto` scaling method, Portworx automatically uses `resize-drive` to scale the storage pool.

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand-till-400

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate.

  conditions:

    expressions:

    # pool size is less than 400 GiB

    - key: "px_pool_stats_total_bytes/(1024*1024*1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when condition is true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # resize pool by scalepercentage of current size. The 100% shown below will double the current pool size.

        scalepercentage: "100"

        # explicitly add new drives to the pool

        scaletype: "add-drive"

```

### Key Sections in the Spec

- The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains a single formula:

- The key `px_pool_stats_total_bytes/(1024*1024*1024)` calculates the total pool capacity in GiB.

- The `Lt` (less than) operator sets the threshold at 400GiB, meaning the action will trigger if a pool’s size is below this value.

- The `actions` section specifies what action Portworx performs when the conditions are met. Action parameters modify action behavior, and different actions contain different action parameters. In this example, the actions section directs Portworx to do the following:

- The pool size is doubled by increasing it by 100% of its current size (`scalepercentage: "100"`).

- The `add-drive` scale type is used, explicitly instructing Portworx to expand the pool by attaching new drives rather than resizing existing ones.

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: pool-expand-till-400

spec:

  enforcement: required

  ##### conditions are the symptoms to evaluate.

  conditions:

    expressions:

    # pool size is less than 400 GiB

    - key: "px_pool_stats_total_bytes/(1024*1024*1024)"

      operator: Lt

      values:

        - "400"

  ##### action to perform when condition is true

  actions:

    - name: "openstorage.io.action.storagepool/expand"

      params:

        # resize pool by scalepercentage of current size. The 100% shown below will double the current pool size.

        scalepercentage: "100"

        # explicitly resize existing drives in the pool

        scaletype: "resize-drive"

```

### Key Sections in the Spec

- The `conditions` section establishes threshold criteria dictating when the rule must perform its action. In this example, that criteria contains a single formula:

- The key `px_pool_stats_total_bytes/(1024*1024*1024)` calculates the total pool capacity in GiB.

- The `Lt` (less than) operator sets the threshold at 400GiB, meaning the action will trigger if a pool’s size is below this value.

- The `actions` section specifies what action Portworx performs when the conditions are met. Action parameters modify action behavior, and different actions contain different action parameters. In this example, the actions section directs Portworx to do the following:

- The pool size is doubled by increasing it by 100% of its current size (`scalepercentage: "100"`).

- The `resize-drive` scale type is used, instructing Portworx to expand the pool by resizing the existing drives, ensuring no new drives are added.

note

Autopilot expands the pools such that no volume in the system will go out of quorum. For example, if `volume1` has replicas on `pool1` and `pool2`, Autopilot first expands `pool1`, waits for completion, and then expands `pool2`.

In this topic:
