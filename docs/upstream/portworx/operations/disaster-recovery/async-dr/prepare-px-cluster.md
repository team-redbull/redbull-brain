# Prepare your Portworx cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/async-dr/prepare-px-cluster (Portworx Enterprise 3.6)

Prepare your Portworx cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When running Portworx in the cloud, you must configure an external load balancer for the `portworx-api` service type on your source and destination clusters. The external load balancer assigns a public IP address for accessing Portworx on port 9001 from your worker nodes.

important

-
On bare metal setups, you don't need to set the `portworx-api` service type to `LoadBalancer`. However, ensure that the `portworx-api` and `portworx-service` services are present in your cluster, and the Portworx cluster is in a healthy state.

-
It is recommended that you enable authorization on your Portworx cluster before enabling a load balancer.

- Kubernetes

- OpenShift

Enable load balancing by running the following command:

```

kubectl edit stc <stc-name> -n <namespace>

```

Enable load balancing by running the following command:

```

oc edit stc <stc-name> -n <namespace>

```

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  annotations:

    portworx.io/service-type: "portworx-api:LoadBalancer"

...

```

- Kubernetes

- OpenShift

You can verify the changes using the `kubectl get service` command.

```

kubectl get service -n <namespace>

```

```

NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                        AGE

portworx-api                LoadBalancer   10.233.56.13    192.0.2.20    9001:30278/TCP,9020:30908/TCP,9021:32598/TCP   18h

```

You can verify the changes using the `oc get service` command.

```

oc get service -n <namespace>

```

```

NAME                        TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)                                        AGE

portworx-api                LoadBalancer   10.233.56.13    192.0.2.10    9001:30278/TCP,9020:30908/TCP,9021:32598/TCP   18h

```

## Install storkctl​

Stork is Portworx's storage scheduler that provides seamless integration between Portworx and your orchestrator (Kubernetes or OpenShift). Stork co-locates pods with their data, provides seamless migration of pods in case of storage issues, and enables you to create and restore snapshots of Portworx volumes. `storkctl` is a command-line tool for interacting with Stork. Install `storkctl` on both clusters after installing Portworx.

important

Always use the latest `storkctl` binary tool by downloading it from the currently running Stork container.

Perform the following steps to download `storkctl` from the Stork pod:

- Kubernetes

- OpenShift

-
Linux:

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
OS X:

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
Windows:

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(kubectl get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

-
Linux:

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
OS X:

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
Windows:

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(oc get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

In this topic:
