# Scale or Restrict Portworx on Nodes

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/scale-or-restrict (Portworx Enterprise 3.6)

Scale or Restrict Portworx on Nodes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx installation is controlled by Portworx Operator. It automatically scales as you grow your Kubernetes cluster. There are no additional requirements to install Portworx on the new nodes in your Kubernetes cluster.

#### Restricting Portworx to certain nodes​

Choose either of the below options based on current state of Portworx in the cluster.

-
Portworx is not yet deployed in your cluster

To restrict Portworx to run on only a subset of nodes in the Kubernetes cluster, use the `px/enabled` Kubernetes label on the nodes you do not wish to install Portworx on.

Below are examples to prevent Portworx from installing and starting on minion2 and minion5 nodes.

```

kubectl label nodes minion2 minion5 px/enabled=false --overwrite

```

-
Portworx has already been deployed in your cluster

If Portworx is already deployed in your cluster, follow Decommission a node to decommission a Portworx node in your cluster.

In this topic:
