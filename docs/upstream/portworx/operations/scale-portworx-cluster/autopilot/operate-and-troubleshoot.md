# Operating and Troubleshooting Autopilot

Source: https://docs.portworx.com/portworx-enterprise/operations/scale-portworx-cluster/autopilot/operate-and-troubleshoot (Portworx Enterprise 3.6)

Operating and Troubleshooting Autopilot | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This section provides common operational procedures for monitoring and troubleshooting your autopilot installation.

## Troubleshooting objects monitored by Autopilot​

Follow the steps in the sections below to troubleshoot objects monitored by Autopilot

### Get recent statuses using AutopilotRuleObjects​

For each object monitored by Autopilot, it will create a corresponding `autopilotruleobject` instance in the namespace of the object.

- For volumes (PVCs), the `autopilotruleobject` instance will be in the namespace of the PVC.

- For storage pools, the `autopilotruleobject` instance will be in the namespace where Portworx is installed.

The `autopilotruleobject` is created immediately unless there is an issue with the rule. The `autopilotruleobject` will initialize and go to Normal state if the conditions are not met yet.

#### List all autopilotruleobjects​

The following command lists all Autopilot rule objects in all namespaces:

- OpenShift

- Kubernetes

```

oc get autopilotruleobjects --all-namespaces

```

Instead of entering the full `autopilotruleobjects` string, you can use the `aro` alias.

```

oc get aro --all-namespaces

```

```

NAMESPACE   NAME                                       AGE

pg1         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c   1s

```

```

kubectl get autopilotruleobjects --all-namespaces

```

Instead of entering the full `autopilotruleobjects` string, you can use the `aro` alias.

```

kubectl get aro --all-namespaces

```

```

NAMESPACE   NAME                                       AGE

pg1         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c   1s

```

#### Describe a specific object​

The `Status` section contains a list of recent object statuses:

- OpenShift

- Kubernetes

```

oc describe aro -n pg1 pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

```

```

Name:         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

Namespace:    pg1

Labels:       rule=volume-resize

Annotations:  <none>

API Version:  autopilot.libopenstorage.org/v1alpha1

Kind:         AutopilotRuleObject

Metadata:

  Creation Timestamp:  2020-08-26T22:29:45Z

  Generation:          2

  Owner References:

    API Version:           autopilot.libopenstorage.org/v1alpha1

    Block Owner Deletion:  true

    Controller:            true

    Kind:                  AutopilotRule

    Name:                  volume-resize

    UID:                   xxxxxxxx-xxxx-xxxx-xxxx-62fbd2d5dbbc

  Resource Version:        7554069

  Self Link:               /apis/autopilot.libopenstorage.org/v1alpha1/namespaces/pg1/autopilotruleobjects/pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

  UID:                     xxxxxxxx-xxxx-xxxx-xxxx-37fe57310baf

Status:

  Items:

    Last Process Timestamp:  2020-08-26T22:29:45Z

    Message:                 rule: volume-resize:pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c transition from Normal => Triggered

    State:                   Triggered

    Last Process Timestamp:  2020-08-26T22:30:19Z

    Message:                 rule: volume-resize:pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c transition from Triggered => ActionAwaitingApproval

    State:                   ActionAwaitingApproval

Events:                      <none>

```

```

kubectl describe aro -n pg1 pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

```

```

Name:         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

Namespace:    pg1

Labels:       rule=volume-resize

Annotations:  <none>

API Version:  autopilot.libopenstorage.org/v1alpha1

Kind:         AutopilotRuleObject

Metadata:

  Creation Timestamp:  2020-08-26T22:29:45Z

  Generation:          2

  Owner References:

    API Version:           autopilot.libopenstorage.org/v1alpha1

    Block Owner Deletion:  true

    Controller:            true

    Kind:                  AutopilotRule

    Name:                  volume-resize

    UID:                   xxxxxxxx-xxxx-xxxx-xxxx-62fbd2d5dbbc

  Resource Version:        7554069

  Self Link:               /apis/autopilot.libopenstorage.org/v1alpha1/namespaces/pg1/autopilotruleobjects/pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c

  UID:                     xxxxxxxx-xxxx-xxxx-xxxx-37fe57310baf

Status:

  Items:

    Last Process Timestamp:  2020-08-26T22:29:45Z

    Message:                 rule: volume-resize:pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c transition from Normal => Triggered

    State:                   Triggered

    Last Process Timestamp:  2020-08-26T22:30:19Z

    Message:                 rule: volume-resize:pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c transition from Triggered => ActionAwaitingApproval

    State:                   ActionAwaitingApproval

Events:                      <none>

```

#### List autopilotruleobjects for a given autopilotrule​

You can use the label selector `rule=<RULE_NAME>` for list `autopilotruleobjects` only for that autopilotrule.

- OpenShift

- Kubernetes

```

oc get aro --all-namespaces -l rule=volume-resize

```

```

NAMESPACE   NAME                                       AGE

pg1         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c   4m3s

```

```

kubectl get aro --all-namespaces -l rule=volume-resize

```

```

NAMESPACE   NAME                                       AGE

pg1         pvc-xxxxxxxx-xxxx-xxxx-xxxx-03263da7b04c   4m3s

```

## Troubleshooting autopilot​

-
Create a directory (`ap-cores`) in which to store your support bundle files and send the support signal to the autopilot process:

- OpenShift

- Kubernetes

```

mkdir ap-cores

POD=$(oc get pods -n portworx -l name=autopilot | grep -v NAME | awk '{print $1}')

oc exec -n portworx $POD -- killall -SIGUSR1 autopilot

```

```

mkdir ap-cores

POD=$(kubectl get pods -n portworx -l name=autopilot | grep -v NAME | awk '{print $1}')

kubectl exec -n portworx $POD -- killall -SIGUSR1 autopilot

```

-
Copy the support bundle files from your Kubernetes cluster to your directory:

- OpenShift

- Kubernetes

```

oc cp  portworx/$POD:/tmp/aut-diags.zip ap-cores/aut-diags.zip

ls ap-cores

```

```

kubectl cp  portworx/$POD:/tmp/aut-diags.zip ap-cores/aut-diags.zip

ls ap-cores

```

-
Collect and place your autopilot pod logs into an `autopilot-pod.log` file within your temporary directory:

- OpenShift

- Kubernetes

```

oc logs $POD -n portworx --tail=99999 > ap-cores/autopilot-pod.log

```

```

kubectl logs $POD -n portworx --tail=99999 > ap-cores/autopilot-pod.log

```

Once you've created a support bundle and collected your logs, send all of the files in the `ap-cores/` directory to Portworx support.

In this topic:
