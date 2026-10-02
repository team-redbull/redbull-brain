# Use pxctl with security enabled

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/px-security/use-pxctl-security-enabled (Portworx Enterprise latest)

Use pxctl with security enabled | Portworx Enterprise Documentation

Once a storage cluster with PX-Security enabled is running, a cluster admin must set up a `pxctl` context on each node in order to interact with the system.

The following steps will guide a storage admin to setup `pxctl` contexts on each node.

-
Retrieve the admin token from the namespace in which Portworx was installed and store it in the `ADMIN_TOKEN` variable:

- Kubernetes

- OpenShift

```

ADMIN_TOKEN=$(kubectl -n <px-namespace> get secret px-admin-token --template='{{index .data "auth-token" | base64decode}}')

```

```

ADMIN_TOKEN=$(oc -n <px-namespace> get secret px-admin-token --template='{{index .data "auth-token" | base64decode}}')

```

-
Find the Portworx pod that is running on the node in which the admin wants to interact with:

Find the node name

- Kubernetes

- OpenShift

```

kubectl get nodes

```

```

oc get nodes

```

Now, save the node name in the variable.

```

K8_NODE_NAME=kubernetes-worker-3.mylab.lan

```

Once the node name is known, run the command below. Ensure that Portworx is installed in the correct namespace. In the below command, it is assumed to be installed in `portworx`.

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl -n <px-namespace> get pods -l name=portworx -o jsonpath="{.items[?(@.spec.nodeName == '$K8_NODE_NAME')].metadata.name}")

```

```

PX_POD=$(oc -n <px-namespace> get pods -l name=portworx -o jsonpath="{.items[?(@.spec.nodeName == '$K8_NODE_NAME')].metadata.name}")

```

-
Save the admin token in the `pxctl` context for that pod:

- Kubernetes

- OpenShift

```

kubectl -n <px-namespace> exec -ti $PX_POD -- /opt/pwx/bin/pxctl context create admin --token=$ADMIN_TOKEN

```

```

oc -n <px-namespace> exec -ti $PX_POD -- /opt/pwx/bin/pxctl context create admin --token=$ADMIN_TOKEN

```

-
Use `kubectl exec` to access the Portworx container and perform any `pxctl` operations:

- Kubernetes

- OpenShift

```

kubectl -n <px-namespace> exec -ti $PX_POD -- /opt/pwx/bin/pxctl status

```

```

 oc -n <px-namespace> exec -ti $PX_POD -- /opt/pwx/bin/pxctl status

```

note

The `pxctl` context will need to be refreshed every time the token expires. This is 24 hours by default, but this default can be changed. See customizing security for more information.
