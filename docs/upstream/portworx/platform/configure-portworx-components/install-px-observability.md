# Portworx Observability

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/install-px-observability (Portworx Enterprise 3.6)

Portworx Observability | Portworx Enterprise Documentation

Skip to main content

EARLY ACCESS

This feature is available as Early Access (EA) and should not be used in production.

Version: 3.7

Portworx Observability is an in-cluster observability dashboard for Portworx clusters, which you can deploy along with Portworx Enterprise. It uses the PX Cache agent to read cluster state and Prometheus metrics.

Instead of gathering information manually from `kubectl` output, Prometheus queries, Grafana dashboards, or separate diagnostic commands, Portworx Observability gives cluster administrators and support engineers a single cluster-level view of Portworx health, topology, resources, alerts, metrics, and support actions through an user interface.

Portworx Observability runs entirely inside your cluster, it does not require an external cloud service or outbound network access. This makes it suitable for air-gapped, regulated, and other restricted environments.

important

Portworx Observability is an Early Access feature. It supports a single cluster per installation and is platform-agnostic. Auditing of UI actions is not currently available.

## Deployment and access model​

- Portworx Observability UI should be deployed as a standalone service alongside Portworx Enterprise.

- By default, the UI service is a Kubernetes `ClusterIP` service, and the default UI service port is `8080`. It also supports `NodePort` and `LoadBalancer`.

- The UI is accessible through a Kubernetes port-forward if `ClusterIP` is chosen.

- PX Cache Agent APIs are cluster-internal.

- Requests are authenticated using Kubernetes token review.

- Requests are authorized using Kubernetes subject access review.

- User has `cluster-admin` access.

caution

`pods/portforward` is a highly privileged Kubernetes permission because it allows direct network access to pods in a namespace. Grant it only to the administrators who need to launch the UI.

## Prerequisites​

Ensure that your cluster meets the following prerequisites before you install Portworx Observability:

- Portworx Enterprise version 3.5.2 or later is installed and running

- Helm version 3.8.0 or later is installed.

- Permission to create and update resources in the Portworx namespace.

- The `pods/portforward` permission in the Portworx namespace, required to launch the UI.

- Prometheus reachable by PX Cache Agent. For the endpoint appropriate to your deployment, see Monitor Portworx Clusters on Kubernetes or Configure Portworx Monitoring on OpenShift.

## Install Portworx Observability​

Perform the following steps, depending on whether Portworx Enterpise is installed on an OpenShift cluster or on a non-OpenShift Kubernetes cluster. For OpenShift, Portworx Observability uses the PX Cache Agent that Portworx Operator provides through the OpenShift Dynamic Plugin integration. For non-OpenShift, it uses the Cache Agent bundled with the Helm chart.

note

Install Portworx Observability in the same namespace as Portworx.

- Kubernetes

- OpenShift

-
Add Portworx Helm Repository:

```

helm repo add portworx http://charts.portworx.io

helm repo update

```

-
Install the Portworx Observability Helm chart:

```

helm install px-observability-ui portworx/px-observability-ui \

  --version <observability-ui-version> \

  --namespace <px-namespace>

```

Note:

- Update `<observability-ui-version>` with the Portworx Observability chart version you want to install.

- Replace `<px-namespace>` with the namespace where Portworx is installed, for example, `portworx`.

- Default UI service type is `ClusterIP` service. Set `ui.service.type` to `NodePort` or `LoadBalancer` using `--set` option with the above installation command.

-
Verify that the UI and PX Cache Agent pods are running:

```

kubectl -n <px-namespace> get pods

```

-
Verify that the UI service is created:

```

kubectl -n <px-namespace> get service px-observability-ui

```

-
Enable the OpenShift Dynamic Plugin for the Portworx Operator.
For more information, see Enable Portworx OpenShift Dynamic Plugin.

-
Override the Cache Agent image in the `StorageCluster` specification:

```

kind: StorageCluster

spec:

  ocpDynamicPlugin:

    cacheAgentImage: "<registry-path>/px-cache-agent:<cache-agent-version>"

```

Replace:

- `<registry-path>` with the registry and repository that host the Cache Agent image.

- `<cache-agent-version>` with the Cache Agent version required by the Portworx Observability release you are installing.

-
Add Portworx Helm Repository:

```

helm repo add portworx http://charts.portworx.io

helm repo update

```

-
Install the Portworx Observability UI chart with the bundled Cache Agent disabled, so that the UI uses the Cache Agent service managed by the Operator:

```

helm install px-observability-ui portworx/px-observability-ui \

  --version <observability-ui-version> \

  --namespace <px-namespace> \

  --set cacheAgent.enabled=false

```

Note:

- Update `<observability-ui-version>` with the Portworx Observability chart version you want to install.

- Replace `<px-namespace>` with the namespace where Portworx is installed, for example, `portworx`.

- Default UI service type is `ClusterIP` service. Set `ui.service.type` to `NodePort` or `LoadBalancer` using `--set` option with the above installation command.

note

The `cacheAgent.prometheusEndpoint` value in this example points to the Thanos Querier service of the OpenShift monitoring stack. If your cluster uses a different monitoring endpoint, set the value accordingly.

-
Verify that the UI pod is running:

```

oc -n <px-namespace> get pods

```

-
Verify that both the UI service and the Cache Agent service exist:

```

oc -n <px-namespace> get service px-observability-ui

oc -n <px-namespace> get service px-cache-agent-service

```

## Launch Portworx Observability​

- ClusterIP

- NodePort

- LoadBalancer

-
Forward the UI service port to your local machine:

```

kubectl -n <px-namespace> port-forward service/px-observability-ui 8080:8080

```

-
Open the following URL in a browser:

```

http://localhost:8080/cluster

```

The system displays the Portworx Observability overview dashboard.

Keep the port-forward process running while you use the UI. To end the session, press `Ctrl+C` in the terminal where the port-forward command is running.

-
For NodePort, use Node IP and Node Port to access Portworx Observability Dashboard.

```

kubectl get svc px-observability-ui -n <px-namespace> -o jsonpath='{.spec.ports[0].nodePort}'

```

-
Open the following URL in a browser:

```

http://<node-ip>:<node-port>

```

The system displays the Portworx Observability overview dashboard.

-
For LoadBalancer, use Load Balancer IP and port to access Portworx Observability Dashboard.

```

kubectl get svc px-observability-ui -n {{ .Release.Namespace }} -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'

```

-
Open the following URL in a browser:

```

http://<loadbalancer-endpoint>

```

The system displays the Portworx Observability overview dashboard.

On OpenShift, use `oc` instead of `kubectl`.

## Troubleshoot Portworx Observability Installation​

If the Portworx Observability does not launch, perform the following checks:

-
Verify that the UI pod is running:

```

kubectl -n <px-namespace> get pods

```

-
Verify that the UI service exists:

```

kubectl -n <px-namespace> get service px-observability-ui

```

-
Verify that you have access to the Portworx namespace and the `pods/portforward` permission in it.

-
Verify that the UI and PX Cache Agent are installed in the same namespace as Portworx.

-
Verify that the Prometheus or Thanos endpoint configured for PX Cache Agent is reachable from the PX Cache Agent pod.

-
On OpenShift, confirm that the OpenShift Dynamic Plugin is enabled and that the `StorageCluster` specification references the expected Cache Agent image:

```

oc -n <px-namespace> get storagecluster -o yaml | grep -A2 ocpDynamicPlugin

```

## Reference​

- Monitor Portworx Clusters with Portworx Observability

- Portworx Observability Helm Chart Parameters

In this topic:
