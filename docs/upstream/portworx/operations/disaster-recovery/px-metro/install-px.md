# Prepare your Portworx cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/install-px (Portworx Enterprise 3.6)

Prepare your Portworx cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In a Synchronous DR deployment setup, install a single Portworx cluster that spans across your source and destination clusters using the instructions on this page.

## Install Portworx​

To enable a single Portworx cluster to span across both your source and destination clusters, you should ensure that the Portworx clusters on both sides are configured with identical KVDB endpoints and cluster names. This setup allows both clusters to share the same Portworx storage fabric.

### Generate a Portworx spec​

Follow these steps to generate the Portworx specifications and then apply them to both your source and destination clusters:

-
Navigate to Portworx Central to log in or create an account.

-
Select Portworx Enterprise from the product catalog and click Continue.

-
On the Product Line page, choose the appropriate license option, then click Continue.

-
For Platform, choose your cloud provider, then click Customize at the bottom of the Summary section.

-
On the Basic page, select the Your etcd details option and enter your external KVDB endpoints, one at a time using the + symbol, then click Next. Here's an example for a three-node etcd cluster:

- `http://<your-etcd-endpoint1>:2379`

- `http://<your-etcd-endpoint2>:2379`

- `http://<your-etcd-endpoint3>:2379`

note

Portworx does not support internal KVDB with Synchronous DR. You need to set up an external three-node cluster for Portworx. Each data center should host one active etcd node, and one node should be operational on the witness node.

-
On the Storage page, select cloud as your environment and choose your cloud provider and click Next.

-
Choose your network and click Next.

-
From the Customize page, specify your cluster name prefix in Advanced Settings. Click Finish to generate the spec.

-
After generating the spec file, copy it to the source and destination clusters.

### Specify domain names and apply the specs​

Cluster domain is a logical or virtual region name that represents the cluster as a whole. Each cluster, along with its associated nodes, constitutes its own distinct cluster domain. You can define the cluster domain for Portworx cluster in the `StorageCluster` spec. It defines a subset of nodes within the extended Portworx cluster that belong to a cluster domain.

A cluster domain and its corresponding set of nodes are linked to one of the following statuses:

- Active State: Nodes from an active cluster domain participate in the cluster activities. Applications can be scheduled on the nodes which are a part of an active cluster domain.

- Inactive State: Nodes from an inactive cluster domain do not participate in the cluster activities. Applications cannot be scheduled on such nodes.

You need to provide a distinct domain names for each cluster. You can use several methods to specify a domain name for your clusters, such as your cloud providers' zone names (for example, `us-east-1a` and `us-east-1b`) or the datacenter names (for example, `datacenter1` and `datacenter2`) that your clusters are using.

Before applying the Portworx specs to your clusters, ensure that both the spec files have the same `metadata.name` and KVDB endpoints, but different domain names.

note

Deploying a Synchronous DR setup with cloud drive on VMware vSphere Kubernetes Service (VKS) clusters requires labeling your drives. For instructions, see the vSphere Kubernetes Service Cluster Installation page.

#### Apply the spec on your source cluster​

Edit the spec to add the source cluster domain name.

-
Specify a domain name using the `portworx.io/misc-args` annotation with the `-cluster_domain` argument. The following example shows how you can specify your source cluster domain name using your cloud providers' zone name (for example, `us-east-1a`):

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  annotations:

    portworx.io/misc-args: "-cluster_domain us-east-1a"

```

-
Apply the edited spec:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-px-source-spec>.yaml

```

```

oc apply -f <your-px-source-spec>.yaml

```

#### Apply the spec on your destination cluster​

Similarly, edit the spec to reflect the destination cluster domain name.

-
Specify the domains using the `-cluster_domain` argument with the `portworx.io/misc-args` annotation. You should use the same method as your source cluster for specifying the domain name of your destination cluster. The following example shows how you can specify the domain name using `us-east-1b`:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  annotations:

    portworx.io/misc-args: "-cluster_domain us-east-1b"

```

-
Apply the edited spec:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-px-destination-spec>.yaml

```

```

oc apply -f <your-px-destination-spec>.yaml

```

A single Portworx cluster will be spanning across both clusters since the `metadata.name` and KVDB endpoints are the same.

## (Optional) Synchronize secrets for PX-Security​

If you set up Metro DR and enable PX-Security, you need to synchronize the system secrets between the two Kubernetes or OpenShift clusters. The system secrets are stored under the `px-system-secret` secret in the namespace where Portworx is installed. This secret is used by Portworx nodes for generating system tokens, and these tokens are used for node to node communication.

When deployed with Operator, each operator instance creates its own unique system secret. To synchronize this secret between the two clusters, use the following steps:

-
Create a copy of the `px-system-secret` from the source cluster by running the following command:

- Kubernetes

- OpenShift

```

kubectl -n <px-namespace> get secret px-system-secrets -oyaml > px-system-secret.source

```

```

oc -n <px-namespace> get secret px-system-secrets -oyaml > px-system-secret.source

```

-
On the destination cluster, delete the existing `px-system-secret` with the following command:

- Kubernetes

- OpenShift

```

kubectl -n <px-namespace> delete secret px-system-secrets

```

```

oc -n <px-namespace> delete secret px-system-secrets

```

-
On the destination cluster, run the following command:

- Kubernetes

- OpenShift

```

kubectl -n <px-namespace> apply -f px-system-secret.source

```

```

oc -n <px-namespace> apply -f px-system-secret.source

```

-
Bounce Portworx pods one node at a time in a rolling update fashion on the DR cluster. This can be done by adding a placeholder env variable to the StorageCluster spec. That will trigger a rolling bounce of all the Portworx pods in the DR cluster.

## Install storkctl​

Stork is Portworx's storage scheduler for Kubernetes, offering seamless integration between Portworx and Kubernetes. It allows you to co-locate pods with their data, provides seamless migration of pods in case of storage issues and makes it easier to create and restore snapshots of Portworx volumes. `storkctl` is a command-line tool for interacting with Stork. Install `storkctl` on both clusters after installing Portworx.

important

Always use the latest `storkctl` binary tool by downloading it from the current running Stork container.

Perform the following steps to download `storkctl` from the Stork pod:

-
Linux:

- Kubernetes

- OpenShift

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/linux/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
OS X:

- Kubernetes

- OpenShift

```

STORK_POD=$(kubectl get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

```

STORK_POD=$(oc get pods -n <namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/darwin/storkctl ./storkctl

sudo mv storkctl /usr/local/bin &&

sudo chmod +x /usr/local/bin/storkctl

```

-
Windows:

- Kubernetes

- OpenShift

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(kubectl get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

kubectl cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

-
Copy `storkctl.exe` from the stork pod:

```

STORK_POD=$(oc get pods -n <px-namespace> -l name=stork -o jsonpath='{.items[0].metadata.name}') &&

oc cp -n <px-namespace> $STORK_POD:/storkctl/windows/storkctl.exe ./storkctl.exe

```

-
Move `storkctl.exe` to a directory in your PATH.

## Check the cluster domain status​

When Stork is deployed, it automatically creates a ClusterDomainStatus object on your source and destination clusters.

-
Run the following commands on each of your clusters to get the current status of the `ClusterDomainStatus` object:

```

storkctl get clusterdomainsstatus

```

```

NAME                            LOCAL-DOMAIN   ACTIVE                                     INACTIVE   CREATED

px-dr-cluster                   us-east-1a     us-east-1a (InSync), us-east-1b (InSync)              29 Nov 22 22:09 UTC

```

-
Run the following command to get details of the `ClusterDomainStatus` object:

- Kubernetes

- OpenShift

```

kubectl describe clusterdomainsstatus

```

```

oc describe clusterdomainsstatus

```

```

Name:         px-dr-cluster

Namespace:

Labels:       <none>

Annotations:  <none>

API Version:  stork.libopenstorage.org/v1alpha1

Kind:         ClusterDomainsStatus

Metadata:

  Creation Timestamp:  2022-11-28T23:13:32Z

  Generation:          3

  Managed Fields:

    API Version:  stork.libopenstorage.org/v1alpha1

    Fields Type:  FieldsV1

    fieldsV1:

      f:status:

        .:

        f:clusterDomainInfos:

        f:localDomain:

    Manager:         stork

    Operation:       Update

    Time:            2022-11-28T23:13:32Z

  Resource Version:  3383

  UID:               xxxxxxxx-2e81-4cbf-b4da-4b9c261793fd

 Status:

  Cluster Domain Infos:

    Name:         us-east-1b

    State:        Active

    Sync Status:  InSync

    Name:         us-east-1a

    State:        Active

    Sync Status:  InSync

  Local Domain:   us-east-1a

Events:           <none>

```

You can see that the `Status` field shows that your Portworx stretched cluster is installed and active.

important

By default, Portworx places volumes and their replicas across two cluster domains. This behavior is controlled by the `Metro DR domain protection` flag, which is enabled by default.

- When upgrading Portworx from version 2.13 or earlier, where domain protection was unavailable, the `Metro DR domain protection` flag can only be applied to new volumes. As a result, the domain protection will not be honored for older volumes during pool rebalancing operations.

- Volume creation might fail if an existing VPS rule in your Portworx cluster places replicas of the repl 2 volumes on the same cluster domain due to the `Metro DR domain protection` flag. This flag takes precedence and places replicas across domains, overriding VPS and causing volume creation failures. For replica volumes to be placed on different cluster domains and to prevent volume creation failures, Portworx by Everpure recommends deleting such conflicting VPS rules.

For placing replicas of a particular volume within the same cluster domain, see how to place replicas on the same cluster domain.

In this topic:
