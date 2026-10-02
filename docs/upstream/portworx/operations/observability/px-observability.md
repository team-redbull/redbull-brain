# Monitor Portworx Clusters with Portworx Observability

Source: https://docs.portworx.com/portworx-enterprise/operations/observability/px-observability (Portworx Enterprise latest)

Monitor Portworx Clusters with Portworx Observability | Portworx Enterprise Documentation

EARLY ACCESS

This feature is available as Early Access (EA) and should not be used in production.

Portworx Observability, an in-cluster user interface, enables Portworx cluster administrators to observe the health of Portworx clusters and components, analyse alerts and issues reported, and also generate diag bundles that can be shared for debugging.

Portworx Observability provides visibility, context, and insight into three aspects of a Portworx cluster:

- Health: critical alerts, events, configuration issues, and degraded cluster objects.

- Performance: storage latency, I/O throughput bottlenecks, and similar performance signals.

- Availability: failures of nodes, storage pools, volumes, and other cluster components.

Portworx Observability shows only the critical alerts and groups related alerts into issues. Each issue links to a topology of the objects it affects and to detail pages that provide vitals, insights, trends, probable root causes, and recommended paths out of the critical state.

Portworx Observability reads cluster state and Prometheus metrics through PX Cache Agent running inside your cluster. It does not depend on an external cloud service or outbound network access. This makes it suitable for air-gapped, regulated, and other restricted environments.

important

Portworx Observability is an Early Access feature. It supports a single cluster per installation and is platform-agnostic. Auditing of UI actions is not currently available.

## Prerequisites​

- Portworx Observability is installed in the same namespace as Portworx.
For more information, see Portworx Observability .

- Prometheus is configured and reachable by PX Cache Agent. For the endpoint appropriate to your deployment, see Monitor Portworx Clusters on Kubernetes or Configure Portworx Monitoring on OpenShift.

- `cluster-admin` level access to the cluster.

- `pods/portforward` permission in the Portworx namespace, if the UI service is exposed as a `ClusterIP` service.

## Launch Portworx Observability​

By default, Portworx Observability creates a `ClusterIP` service on port `8080`, which you access through a Kubernetes port-forward. Perform the following to launch the UI:

-
Forward the UI service port to your local machine:

```

kubectl -n <px-namespace> port-forward service/px-observability-ui 8080:8080

```

Replace `<px-namespace>` with the namespace where Portworx is installed, for example, `portworx`. On OpenShift, use `oc` instead of `kubectl`.

-
Open the following URL in a browser:

```

http://localhost:8080/cluster

```

The system displays the Portworx Observability overview dashboard.

Keep the port-forward process running while you use the UI. To end the session, press `Ctrl+C` in the terminal where the port-forward command is running.

note

If the UI service is exposed as a `LoadBalancer` or `NodePort` service, see Launch Portworx Observability to configure access to it.

## Dashboard View​

The Dashboard view summarizes the health of your Portworx cluster by providing the following information:

- Cluster identity and status: The name and UUID of the Portworx cluster, along with its high-level status.

- Version information: The deployed Portworx Enterprise and Portworx Operator versions.

- Component status: The status of components like telemetry, monitoring and Autopilot to confirm whether they are enabled for the cluster.

- Unified health score: A single score that summarizes the state of the cluster, so that you can judge overall health at a glance.

- Issue triage: A snapshot of the live issues in the cluster, with the issues that need urgent attention surfaced first.

- Impact visualization: The severity of each issue and its blast radius, that is, the set of objects the issue affects.

- Inventory needing attention: The workloads and volumes that currently require action.

Every summary card links to the object or issue behind it, so you can move from the dashboard directly into the details of whatever needs your attention.

### Issue Triage​

Portworx Observability groups related alerts and events into issues, and surfaces only the issues that are critical. For each issue, you can:

- Review its severity and the objects it affects.

- Open the issue-based topology to view its blast radius.

- Open the detail page of any affected object to continue the investigation.

## Topology​

The full topology view provides an interactive view of all Portworx and Kubernetes objects in the cluster and the relationships between them. Use this view when you want to understand how the cluster is put together rather than investigate a specific issue.

In the full topology view, you can:

- Filter the graph by infrastructure or by workload, so that you can narrow a broad view down to a probable root cause.

- Select an object to inspect its additional information.

- See the objects related to the selected object.

- Open the metrics associated with the selected object.

### Issue Based topology​

When you select an issue, Portworx Observability displays a topology that contains only the objects that the issue affects along with the following:

- Probable root causes: The likely reasons for the object's current state.

- Node details and metrics: A link to view the node details and metrics dedicated to the issue.

- Impacted Resources: Displays the Portworx and Kubernetes objects impacted by the issue.

This helps identify the blast radius to show the relationships between the impacted objects and assess the impact of the problem.

As the view is scoped to a single issue and supports drill-through into each impacted object, it shortens the time taken for impact analysis.

## Cluster objects​

Portworx Observability provides detailed views for the following Portworx cluster objects, in the form of a list:

- StorageNodes: The Portworx storage nodes in the cluster and their status.

- Storage pools: The storage pools backing the cluster, along with their capacity and status. For more information about storage pools, see Storage Pools.

- Volumes: The Portworx volumes in the cluster, along with their configuration and status.

- Virtual machines: The KubeVirt virtual machines in the cluster, including the Portworx volumes attached to each virtual machine.

A detailed view goes beyond the current state of the object and provides:

- Vitals: The key attributes and current status of the object.

- Insights and trends: How the object is behaving over time, so that you can distinguish a transient spike from a developing problem.

## Metrics​

Portworx Observability embeds the Portworx Grafana dashboard charts directly in the UI and populates them from your cluster's Prometheus data through PX Cache Agent. You do not need to open Grafana separately or write Prometheus queries to see the standard views.

The following metrics views are available:

- Portworx dashboards: Cluster, node, volume, performance, and etcd-oriented views, depending on which dashboards are available in your deployment. For a description of the panels in each of these dashboards, see Grafana dashboards for Portworx.

- Object-scoped metrics: The same charts, already filtered to a single object, when you open metrics from a detail page or from the topology view.

- Metrics browser: A query interface for the raw metrics, for when the pre-built views are not enough. Use it to write your own queries and visualize the results without leaving the UI. For the complete list of metrics that Portworx exposes, see Portworx metrics.

## Alerts​

The alerts page lists both Prometheus alerts and Portworx alerts. You can search and filter the alert list to narrow it to the alerts you want, and select an alert to open its details.

Use the overview dashboard and the issue list to decide what to prioritize, and the alerts page when you need the complete, ungrouped set of alerts.

## Generate a diagnostic bundle​

When you work with Portworx support, you can generate a diagnostic bundle on demand from the Support page of the UI, instead of running separate CLI commands.

- From the navigation pane, click Support.

- Select Generate diag bundle to start the diagnostic bundle generation.

- Wait for the collection to complete, then download or share the bundle with Portworx support.

## Troubleshooting​

If the Portworx Observability UI does not open or does not display data, see the troubleshooting steps in Portworx Observability.

In this topic:
