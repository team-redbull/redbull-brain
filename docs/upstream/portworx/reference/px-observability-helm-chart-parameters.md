# Portworx Observability Helm Chart Parameters

Source: https://docs.portworx.com/portworx-enterprise/reference/px-observability-helm-chart-parameters (Portworx Enterprise latest)

Portworx Observability Helm Chart Parameters | Portworx Enterprise Documentation

EARLY ACCESS

This feature is available as Early Access (EA) and should not be used in production.

This topic provides the configurable parameters of the latest Portworx Observability Helm chart and their default values.

## UI (`ui.*`)​

The `ui` container runs `nginx` and the `authproxy` as sibling processes.

KeyTypeDefaultDescription

`ui.image.repository`string`docker.io/portworx/px-observability-ui`UI image.

`ui.image.tag`string`1.0.0-ea`Image tag.

`ui.image.pullPolicy`string`Always`Container `imagePullPolicy`. Determines how and when the Kubelet attempts to pull a container image from a remote registry to a node; set to `IfNotPresent` for air-gapped clusters with no registry egress.

`ui.replicas`int`1`Deployment replica count. The authproxy caches its minted token per pod, so replicas are independent — no shared state to coordinate.

`ui.resources`object`75m`/`160Mi` requests, `300m`/`320Mi` limitsRendered verbatim into the container's `resources`. Any valid `ResourceRequirements` shape works.

`ui.serviceAccount.create`bool`true`Create the ServiceAccount the UI Deployment runs as. Set `false` to bring your own — then `ui.serviceAccount.name` is required and chart rendering fails without it.

`ui.serviceAccount.name`string`""`ServiceAccount name. When empty and `create: true`, defaults to the chart fullname. The token-minter Role/RoleBinding always bind to whichever name resolves here.

`ui.service.type`string`ClusterIP`Service type. On OpenShift, leave as `ClusterIP` and use `route.enabled` instead; elsewhere use `NodePort`/`LoadBalancer` for external access, or `kubectl port-forward`.

`ui.service.port`int`8080`Service port. `targetPort` is the container's named `http` port (8080) and is not configurable.

The UI's container ports, probes (`/healthz`), and the `UPSTREAM_URL` port (8710) are fixed by the image and PX Cache Agent's REST port; they are deliberately not exposed as values.

### Route (`route.*`)​

KeyTypeDefaultDescription

`route.enabled`bool`false`Create an OpenShift `Route` for the UI Service. Only meaningful on OpenShift - the `route.openshift.io/v1` API does not exist on vanilla Kubernetes, and enabling it there fails the install. TLS is fixed at `edge` termination with `insecureEdgeTerminationPolicy: Redirect`, since nginx serves plain HTTP only. The hostname is left to the OCP router to assign.

## PX Cache Agent (`cacheAgent.*`)​

This chart bundles PX Cache Agent's resources.

note

`cacheAgent.service.name` and `cacheAgent.serviceAccount.name` are read by the UI's templates regardless of `cacheAgent.enabled`. This is because the `authproxy` needs to know which agent `service` to proxy to and whose token to mint. Everything else under `cacheAgent.*` only takes effect when `cacheAgent.enabled` is `true`.

KeyTypeDefaultDescriptionUsed when disabled?

`cacheAgent.enabled`bool`true`Install PX Cache Agent's Deployment, Service, ServiceAccount, RBAC, and CRDs as part of this release. Set `false` when an agent already runs in the cluster.—

`cacheAgent.installCRDs`bool`true`Install the five `agent.multicluster.portworx.com` CRDs (`clusters`, `clusteraccesses`, `disasterrecoverypairs`, `disasterrecoveryactions`, `protectiongroups`). Set `false` if another release or operator already owns them — Helm will not adopt pre-existing CRDs. Ignored unless `cacheAgent.enabled`.No

`cacheAgent.image.repository`string`docker.io/portworx/px-cache-agent`Agent image. A dev artifactory path — px-cache-agent's own repo carries three disagreeing canonical references, so override this for any non-dev install. Templated through `required`: explicitly setting it empty/null fails rendering rather than producing a `:tag`-only image.No

`cacheAgent.image.tag`string`1.1.0-pxo-ui`Agent image tag. Also `required` — see above.No

`cacheAgent.image.pullPolicy`string`Always`Agent container `imagePullPolicy`.No

`cacheAgent.serviceAccount.name`string`px-cache-agent`ServiceAccount the agent runs as, bound to its ClusterRole, leader-election Role, and `cluster-monitoring-view`. Also the SA whose token the UI's authproxy mints (`SERVICE_ACCOUNT_NAME`) and the sole `resourceNames` entry on the UI's token-minter Role — so when `cacheAgent.enabled=false` this must be set to the existing agent's SA name.Yes

`cacheAgent.service.name`string`px-cache-agent-service`Name of the agent Service. Also the host in the UI authproxy's `UPSTREAM_URL` (`http://<name>:8710`) — so when `cacheAgent.enabled=false` this must be set to the existing agent's Service name. Cross-namespace targets need a fully qualified name.Yes

`cacheAgent.prometheusEndpoint`string`http://px-prometheus.portworx.svc.cluster.local:9090`Passed as the agent's `--prometheus-endpoint` arg. Point at the Thanos Querier on OpenShift, or wherever PX metrics are scraped.No

`cacheAgent.resources`object`100m`/`64Mi` requests, `400m`/`2Gi` limitsRendered verbatim into the agent container's `resources`. The 2Gi memory limit is generous because the agent caches query results on disk in an emptyDir (`/tmp`, 1Gi cap) and in memory.No

The agent's replica count (1), ports (8710 REST / 7710 gRPC / 8081 metrics / 8082 health), `DATABASE_PATH`, emptyDir size limit, nodeSelector, tolerations, and securityContext are copied verbatim from px-cache-agent's own manifests and are not exposed as values.

## Reference​

- Install Portworx Observability

- Monitor Portworx Clusters with Portworx Observability

In this topic:
