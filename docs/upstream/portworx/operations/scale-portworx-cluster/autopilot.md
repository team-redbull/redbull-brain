# Automate storage operations with Autopilot

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot (Portworx Enterprise latest)

Automate storage operations with Autopilot | Portworx Enterprise Documentation

Autopilot is a Portworx component that continuously monitors storage resources and performs actions based on real-time metrics. It can be configured with metrics providers such as Prometheus or Datadog to collect metrics about cluster objects (for example, volumes, pools, or PVCs). These metrics are responsible for all Autopilot decisions.

Autopilot behavior is defined using the AutopilotRule Custom Resource. This rule specifies:

- What to monitor (via selectors and namespace selectors)

- Which metrics to evaluate (conditions)

- What to do when conditions are met (actions)

Autopilot continuously evaluates incoming metrics against rule conditions. When all conditions defined in a rule are met, the rule transitions to a triggered state and the corresponding action is scheduled and executed. For more information, refer to Working with Autopilot Rules.

By default, actions are executed automatically when conditions are met. You can configure Autopilot to require explicit approval before executing actions. For more information, refer to Action approvals with AutopilotRule

You can apply Autopilot rules across a wide range of storage automation scenarios, including expanding and automatically rebalancing Portworx storage pools. For more information, refer to Autopilot Use cases

The format of conditions in Autopilot rules differs between Prometheus and Datadog. The examples use Prometheus as the provider. For Datadog, refer to Conditions for information about writing conditions in Autopilot rules.
