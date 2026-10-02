# Hyperconvergence

Source: https://docs.portworx.com/portworx-enterprise/concepts/kubernetes-storage-101/hyperconvergence (Portworx Enterprise 3.6)

Hyperconvergence | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

When a pod runs on the same host as its volume, it is known as convergence or hyperconvergence. This configuration reduces the network overhead of an application, resulting in improved performance.

Natively, Kubernetes does not support this. Portworx uses Stork to ensure that the nodes with data for a volume get prioritized when pods are being scheduled. Stork works as a scheduler extender here.

Below is the high-level workflow when a new pod needs to get scheduled:

-
The default Kubernetes scheduler assigns scores to all nodes in the cluster that are candidates for scheduling the pod. It takes into consideration the usual scheduling parameters like CPU, Memory, Taints, Tolerations, Affinities etc.

-
The default scheduler then makes a request to Stork to filter nodes based on storage characteristics of the volume being used by the Pod. Stork will give higher scores to nodes that have the volume's data bits.

Starting with Stork 26.4.2, Portworx Operator 26.4.0, and Portworx Enterprise 3.6.2.2 or later, you can normalize the hyperconvergence scoring by enabling the `spec.stork.args.normalize-stork-scores` parameter, and tune other scoring parameters. Without Stork normalization scoring enabled, pods are always strongly hyperconverged because no other scheduling factor, such as CPU utilization, memory usage, taints, node affinity, or topology spread, could fairly compete for pod placement. For more information, see Enable Stork normalization and tune hyperconvergence scoring.

-
The default scheduler then picks the node with the higher score and assigns that to the pod.

This page has more details on hyperconvergence with Portworx.
