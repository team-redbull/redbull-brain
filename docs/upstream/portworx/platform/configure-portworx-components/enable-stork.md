# Portworx Stork

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/enable-stork (Portworx Enterprise 3.6)

Portworx Stork | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Stork is a storage scheduler for Kubernetes that helps achieve tighter integration of Portworx with Kubernetes. It allows users to co-locate pods with their data, provides seamless migration of pods in case of storage errors, and makes it easier to create and restore snapshots of Portworx volumes.

Stork consists of two components: the Stork scheduler and an extender. Both run in HA mode with three replicas by default.

When you install Portworx using the Portworx Enterprise Cluster Spec from Portworx Central, Stork is installed by default.

This topic describes how to verify Portworx Stork installation, upgrade Stork, and enable Stork telemetry.

## Verify Stork Installation​

Run the following command:

```

kubectl get pods -n portworx

...

stork-56f7c6d4cb-6b4tf                      1/1     Running    0              21h

stork-56f7c6d4cb-qs25p                      1/1     Running    0              21h

stork-56f7c6d4cb-v7q6b                      1/1     Running    0              21h

stork-scheduler-78c6dc7c6-bkglp             1/1     Running    0              21h

stork-scheduler-78c6dc7c6-lt8ql             1/1     Running    0              21h

stork-scheduler-78c6dc7c6-vwbmn             1/1     Running    0              21h

...

```

## Upgrade Stork​

Perform the following steps to upgrade Stork:

-
Edit the storage cluster specification (Kubernetes resource):

```

kubectl edit stc <stc-name> -n <portworx-namespace>

```

-
Change the Stork image and version details in `stork` section:

```

stork:

   args:

     webhook-controller: "true"

   enabled: true

   image: openstorage/stork:<stork_version>

```

-
Save and exit.

## Configure Stork scheduler performance settings​

The Stork scheduler is a `kube-scheduler` binary the Portworx Operator deploys and configures through the `stork-config` ConfigMap. The scheduler throttles Kubernetes API calls with a default QPS of `50` and Burst of `100`. In clusters that create many pods simultaneously, these defaults can cause pods to remain in `Pending` state while the scheduler queues API calls.

Starting with Portworx Operator 26.4.0, you can configure scheduler performance settings directly in the StorageCluster spec. The operator persists these values across reconciles and upgrades, and restarts the `stork-scheduler` pods automatically when you change them.

To configure Stork scheduler performance settings:

-
Edit the StorageCluster spec:

```

kubectl edit storagecluster <cluster-name> -n <portworx-namespace>

```

-
Add or update the scheduler fields under `spec.stork.scheduler`:

```

spec:

  stork:

    scheduler:

      verboseLogLevel: 5       # Optional: sets --v=5 on stork-scheduler

      kubeSchedulerClientQPS: 1000

      kubeSchedulerClientBurst: 500

      kubeSchedulerExtenderWeight: 5

      kubeSchedulerNodeCacheEnabled: true   # Optional: requires Stork 26.4.2 or later

```

-
Save and exit. The operator updates the `stork-config` ConfigMap and restarts the `stork-scheduler` pods automatically.

note

If you previously modified the `stork-config` ConfigMap directly to work around this limitation, those changes are reverted on every operator upgrade. To make your values persistent, set them once in the StorageCluster spec using the fields above.

note

When `kubeSchedulerNodeCacheEnabled` is not set, the operator automatically enables it for Stork 26.4.2 or later and leaves it disabled for older Stork versions. Setting it to `true` explicitly against a Stork version older than 26.4.2 is ignored, with a warning logged by the operator.

For the full list of available fields and their valid ranges, see Stork configuration.

## Enable Stork telemetry​

When you enable Portworx Enterprise telemetry, the system collects and uploads Stork logs to Pure1 telemetry. These logs help with troubleshooting and observability of Stork operations.

For Stork log telemetry, the following requirements must be met:

- Portworx Operator version is 26.2.0 or later

- Stork version is 26.3.0 or later

- Telemetry is enabled

There is no flag to disable only Stork log telemetry. If any requirement is not met, Stork telemetry is not enabled. You can configure the `log-file-buffer-size-mib`, `log-file-max-backups`, and `log-file-max-age` parameters in the Stork section of the StorageCluster CR. For more information, see Stork configuration.

### Limitations​

- Stork-scheduler pod logs are not collected to `/var/cores/portworx-bundle/stork/`. For collecting stork-scheduler logs, you need to use the `PortworxDiag` CRD. For more information, see On-demand diagnostics using `PortworxDiag` custom resource.

For more information about Portworx telemetry, see Portworx Telemetry. For available Stork configuration options, see Stork configuration.

In this topic:
