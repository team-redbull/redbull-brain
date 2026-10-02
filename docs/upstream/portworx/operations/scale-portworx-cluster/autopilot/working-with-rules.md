# Working with Autopilot Rules

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/working-with-rules (Portworx Enterprise 3.6)

Working with Autopilot Rules | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Users use an AutopilotRule CRD to tell Autopilot which objects to monitor, the conditions to monitor, and the corresponding actions to perform when conditions occur.

An AutopilotRule has 4 main parts:

- Selector Matches labels on the objects that the rule should monitor.

- Namespace Selector Matches labels on the Kubernetes namespaces the rule should monitor. This is optional, and the default is all namespaces.

- Conditions The metrics for the objects to monitor.

- Actions to perform once the metric `conditions` are met.

Autopilot also provides the following optional fields:

-
Action Window controls the action trigger time by defining the timestamps during which the `action` can be triggered once the `conditions` are met. Use this parameter with caution to avoid downtime as it waits for `conditions` to be met while the window is active to trigger the `actions`. This feature is available with Autopilot version 1.4 and above.

-
Actions Cool Down Period defines the duration for which autopilot will not re-trigger any actions once they have been executed.

The subsequent sections describe common operations for managing Autopilot rules.

## Creating an AutopilotRule​

-
Create an `AutopilotRule` spec file.

- The Use cases page provides end-to-end examples on specific Autopilot use cases. Refer to these to help you create your spec.

- The AutopilotRule Reference page page defines the specification of the rule spec.

-
Apply the spec in your cluster.

- OpenShift

- Kubernetes

```

kubectl apply -f volume-resize-autopilotrule.yaml

```

```

autopilotrule.autopilot.libopenstorage.org/volume-resize created

```

```

kubectl apply -f volume-resize-autopilotrule.yaml

```

```

autopilotrule.autopilot.libopenstorage.org/volume-resize created

```

## Updating an AutopilotRule​

You can update an autopilot rule in-place with the `kubectl edit` command:

- OpenShift

- Kubernetes

```

oc edit autopilotrule volume-resize

```

```

autopilotrule.autopilot.libopenstorage.org/volume-resize created

```

```

kubectl edit autopilotrule volume-resize

```

## Deleting an AutopilotRule​

Delete an Autopilot rule by using `kubectl delete autopilotrule` and specifying the rule you want to delete. When you do this, Autopilot stops monitoring all objects that match this rule.

- OpenShift

- Kubernetes

```

oc delete autopilotrule volume-resize

```

```

autopilotrule.autopilot.libopenstorage.org "volume-resize" deleted

```

```

kubectl delete autopilotrule volume-resize

```

```

autopilotrule.autopilot.libopenstorage.org "volume-resize" deleted

```

## Monitoring AutopilotRules​

Autopilot generates events, which you can monitor with the `kubectl get events` command:

- OpenShift

- Kubernetes

-
To see events for all `AutopilotRule` objects:

```

oc get events --field-selector involvedObject.kind=AutopilotRule --all-namespaces

```

-
To see events for a specific `AutopilotRule` object, you must add `involvedObject.name` and the name of your Autopilot rule.

In below example, we are listing all events for the `volume-resize` rule.

```

oc get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=volume-resize --all-namespaces

```

```

 NAMESPACE   LAST SEEN   TYPE     REASON       KIND            MESSAGE

 default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     9m52s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     9m48s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

```

-
To see events for all `AutopilotRule` objects:

```

kubectl get events --field-selector involvedObject.kind=AutopilotRule --all-namespaces

```

-
To see events for a specific `AutopilotRule` object, you must add `involvedObject.name` and the name of your Autopilot rule.

In below example, we are listing all events for the `volume-resize` rule.

```

kubectl get events --field-selector involvedObject.kind=AutopilotRule,involvedObject.name=volume-resize --all-namespaces

```

```

 NAMESPACE   LAST SEEN   TYPE     REASON       KIND            MESSAGE

 default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     21m         Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     9m52s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

 default     9m48s       Normal   Transition   AutopilotRule   rule: pvc-xxxxxxxx-xxxx-xxxx-xxxx-aa931955114b transition from Initializing => Normal

```

In this topic:
