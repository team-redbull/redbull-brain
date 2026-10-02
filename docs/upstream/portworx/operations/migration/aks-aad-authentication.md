# Automate authentication for AAD enabled AKS cluster

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/aks-aad-authentication (Portworx Enterprise latest)

Automate authentication for AAD enabled AKS cluster | Portworx Enterprise Documentation

For running disaster recovery (DR) scenarios with Stork, you need to create a unidirectional or bidirectional ClusterPair with the ability to automatically authenticate Stork. When using an Azure Active Directory (AAD) enabled Azure Kubernetes Service (AKS) cluster, the `kubelogin` tool enables automatic login using a service principal.

This page provides instructions on creating a Kubernetes secret using the service principal ID and secret, and then passing it to the Stork spec. This process will automatically authenticate Stork when creating a ClusterPair object during DR setup.

## Prerequisites​

- AAD enabled AKS cluster

- Stork 23.7.0 or newer

- kube API access is enabled for an AKS cluster using Azure Service Principal

## Create a non-interactive authentication​

Once you have configured your `kubeconfig` to use a service principal for authentication instead of the default device code flow, follow the below steps to pass the service principal ID and secret as Stork environment variables to your source and destination clusters.

-
Create a secret using your service principal ID and secret

- Kubernetes

- OpenShift

```

kubectl create secret generic \

-n <px-namespace> px-azure-kube-access \

--from-literal=AAD_SERVICE_PRINCIPAL_CLIENT_ID=<spn-client-id> \

--from-literal=AAD_SERVICE_PRINCIPAL_CLIENT_SECRET=<spn-secret>

```

```

oc create secret generic \

-n <px-namespace> px-azure-kube-access \

--from-literal=AAD_SERVICE_PRINCIPAL_CLIENT_ID=<spn-client-id> \

--from-literal=AAD_SERVICE_PRINCIPAL_CLIENT_SECRET=<spn-secret>

```

-
Edit your source and destination StorageCluster

Pass your service principal ID and secret as Stork environment variables. This will be used by Stork to authenticate with the AKS cluster:

```

stork:

env:

- name: AAD_SERVICE_PRINCIPAL_CLIENT_ID

    valueFrom:

    secretKeyRef:

        key: AAD_SERVICE_PRINCIPAL_CLIENT_ID

        name: px-azure-kube-access

- name: AAD_SERVICE_PRINCIPAL_CLIENT_SECRET

    valueFrom:

    secretKeyRef:

        key: AAD_SERVICE_PRINCIPAL_CLIENT_SECRET

        name: px-azure-kube-access

```

-
Wait for a few minutes, and verify that all Stork pods are in the `running` state:

- Kubernetes

- OpenShift

```

kubectl get pods -n <px-namespace> -l name=stork

```

```

oc get pods -n <px-namespace> -l name=stork

```

Example output:

```

NAME                        READY   STATUS    RESTARTS   AGE

stork-78b8bbf7d8-4nd58      1/1     Running   0          3m25s

stork-78b8bbf7d8-9m6qw      1/1     Running   0          3m25s

stork-78b8bbf7d8-rldkf      1/1     Running   0          3m25s

```

After all Stork pods have started, proceed to the DR section to complete your DR setup.

In this topic:
