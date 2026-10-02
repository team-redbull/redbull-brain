# Evacuating a Portworx node

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/evacuate (Portworx Enterprise latest)

Evacuating a Portworx node | Portworx Enterprise Documentation

Sometimes it is necessary to evacuate a node of both workloads and storage. You may want to do this before an upgrade or other maintenance, or you might be trying to rebalance your workloads across the cluster. Note that if you are decommissioning a node, then the steps to do this should be followed here. Also note that upgrades can be done with minimal downtime as documented, so this process is not a prerequisite.

- Kubernetes

- OpenShift

-
Disable Kubernetes provisioning - cordon the node to prevent any further pods from being scheduled

```

kubectl cordon <oldNode>

```

-
Obtain a list of volumes on the node

```

pxctl volume list --node-id <oldNodeID>

```

-
For each volume, reduce the number of replicas (in this example, from 3 to 2) - since there can be at most 3 replicas of a Portworx volume, the replication factor has to be reduced before it can be increased

```

pxctl volume ha-update --repl 2 <volume> --node <oldNodeID>

```

-
For each volume, recreate the replicas elsewhere - increase the replication factor and specify the node on which to place it

```

pxctl volume ha-update --repl 3 <volume> --node <newNodeID>

```

-
Delete the pods - Kubernetes will ensure the pods are reprovisioned on another node, and Stork will try to ensure they land on the node with the new replicas

```

kubectl get pods -o wide | grep <node>

kubectl delete pod <pod>

```

-
Disable OpenShift cluster provisioning - cordon the node to prevent any further pods from being scheduled

```

oc adm cordon <oldNode>

```

-
Obtain a list of volumes on the node

```

pxctl volume list --node-id <oldNodeID>

```

-
For each volume, reduce the number of replicas (in this example, from 3 to 2) - since there can be at most 3 replicas of a Portworx volume, the replication factor has to be reduced before it can be increased

```

pxctl volume ha-update --repl 2 <volume> --node <oldNodeID>

```

-
For each volume, recreate the replicas elsewhere - increase the replication factor and specify the node on which to place it

```

pxctl volume ha-update --repl 3 <volume> --node <newNodeID>

```

-
Delete the pods - OpenShift will ensure the pods are reprovisioned on another node, and Stork will try to ensure they land on the node with the new replicas

```

oc get pods -o wide | grep <node>

oc delete pod <pod>

```
