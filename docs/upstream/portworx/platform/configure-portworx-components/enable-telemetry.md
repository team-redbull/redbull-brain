# Portworx Telemetry

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/enable-telemetry (Portworx Enterprise 3.6)

Portworx Telemetry | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx telemetry provides insights into cluster health, resource utilization, and configuration patterns. Pure 1 uses this data to recommend best practices and improvements tailored to your environment, enabling better resource planning and performance tuning.

This topic describes how to enable Portworx telemetry for Pure1 integration and how to configure the metrics collector. It also explains how to disable telemetry on your cluster.

## Enable Telemetry for Pure1 Integration​

Telemetry to Pure1 is enabled by default when you generate the StorageCluster spec from Portworx Central, unless you disable it by setting `spec.monitoring.telemetry.enabled` to `false`.

With telemetry enabled, Portworx automatically enable telemetry for stork which include Stork logs to be collected and uploaded to Pure1 telemetry. These logs will assist in troubleshooting and observability of Stork operations. For more information, see Stork telemetry.

If telemetry is enabled and the `PX_HTTPS_PROXY` environment variable is set, Portworx disables telemetry and creates a Kubernetes event of type `Warning` to notify you.

If you disabled telemetry during installation, you can enable it by setting `spec.monitoring.telemetry.enabled` to `true` in your StorageCluster spec:

StorageCluster

```

spec:

  monitoring:

    telemetry:

      enabled: true

```

important

Enabling telemetry restarts the Portworx pods running on your Kubernetes cluster. Enabling or disabling telemetry on an existing cluster triggers a rolling restart of the Portworx cluster for the change to take effect. It is recommended to perform this update during a planned maintenance window to avoid any service disruption.

After you enable Pure1 integration:

- Portworx automatically uploads the diagnostics bundle and real-time Prometheus metrics from your Portworx cluster to Pure1. If you are running Portworx Operator version 25.5.2 or later, you can disable uploading real-time Prometheus metrics to Pure1 by disabling the metrics collector while keeping telemetry enabled. For more information, see Metrics collector configuration.

- You can use Pure1 AI Copilot to interact with your Portworx storage clusters using natural language. For more information, see Portworx on Pure1 AI Copilot.

note

If you are running Operator version 25.5.2 and later with telemetry enabled and you use GitOps to manage your `StorageCluster`, set `metricsCollector.enabled` to `true` in your Git manifest to keep the repository in sync with the cluster state. This is because applying a StorageCluster spec with only `telemetry.enabled: true` automatically sets `metricsCollector.enabled` to `true`.

StorageCluster

```

...

spec:

  monitoring:

    telemetry:

      enabled: true

      metricsCollector:

        enabled: true

```

...

### Additional configuration for air-gapped clusters​

In air-gapped clusters, telemetry is supported via a simple or traditional proxy that serves in HTTP mode. Along with the configuration in the above section, you need to make additional configuration to enable telemetry for air-gapped clusters. If you have a next generation firewall acting as a proxy, or if you have problems with the telemetry configuration, contact Portworx Support for assistance.

To enable telemetry, configure a proxy and add it to the `PX_HTTP_PROXY` or `PX_HTTPS_PROXY` environment variable in your `StorageCluster` specification. Telemetry communicates through the specified proxy.

StorageCluster

```

...

spec:

  env:

    - name: PX_HTTP_PROXY

      value: "http://<IP:port>"

    - name: PX_HTTPS_PROXY

      value: "http://<IP:port>"

...

```

## Metrics collector configuration​

Starting with Portworx Operator 25.5.2, you can configure the metrics collector separately from other telemetry components.

The metrics collector requires telemetry to be enabled. When telemetry is enabled, the metrics collector is enabled by default. You can disable the metrics collector while keeping telemetry enabled, but you cannot enable the metrics collector without telemetry.

When telemetry is enabled, the Operator automatically adds `metricsCollector.enabled: true` to your StorageCluster spec. If you use GitOps to manage your StorageCluster, ensure your Git manifest includes this field so that your Git repository matches the actual cluster state.

The telemetry metrics collector scrapes Prometheus metrics from Portworx pods, forwards these real-time metrics to Pure1 for monitoring and analytics, and provides data for Pure1 dashboards showing capacity, utilization, and performance trends.

When you disable the metrics collector, real-time metrics forwarding to Pure1 stops, which means Pure1 dashboards no longer display current metrics. However, diagnostics upload to Pure1 continues to work, and support functionality remains intact. Pure1 AI Copilot continues to function because it uses diagnostics data. Your own Prometheus monitoring solutions continue to work normally because Portworx continues exporting metrics locally.

Disable metrics collector while keeping telemetry enabled:

```

spec:

  monitoring:

    telemetry:

      enabled: true

      metricsCollector:

        enabled: false

```

This configuration disables real-time metrics forwarding to Pure1 but maintains diagnostics uploads for support purposes.

Use a custom image for the metrics collector:

```

spec:

  monitoring:

    telemetry:

      enabled: true

      metricsCollector:

        enabled: true

        image: "portworx/realtime-metrics:<version>"

```

This configuration allows you to deploy a specific version or hotfix image for the metrics collector.

## Disable Telemetry​

To disable the metrics collector and telemetry integration, add the following section in your StorageCluster spec:

StorageCluster CRD

```

...

spec:

  monitoring:

    telemetry:

      enabled: false

...

```

This removes the `telemetry` container from the Portworx pod.

important

If you want to disable only the metrics collector while keeping telemetry active for diagnostics upload, refer to the Metrics collector configuration section for more information.

In this topic:
