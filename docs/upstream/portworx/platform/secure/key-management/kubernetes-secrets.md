# Kubernetes Secrets

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/kubernetes-secrets (Portworx Enterprise latest)

Kubernetes Secrets | Portworx Enterprise Documentation

Portworx integrates with Kubernetes Secrets to store encryption keys and credentials. These secrets support encrypting data at rest and can also store credentials and encryption keys for cloud provider services used by Portworx.

This topic explains how to configure Portworx to use Kubernetes Secrets.

## Set Kubernetes Secrets as the secrets store​

To set Kubernetes Secrets as the secrets store, follow these steps:

-
Sign in to the Portworx Central console.
The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
The system displays the Generate Portworx Enterprise Spec page.

-
From the Portworx Version dropdown menu, select the Portworx version to install.

-
From the Platform dropdown menu, select the platform.

-
From the Distribution Name dropdown menu, select the distribution.

-
Click Customize.

-
Complete the required configuration in the Basic, Storage, Network, and Deployment tabs.

-
From the Default Secret Store Type dropdown menu, select Kubernetes.

## Create secrets with Kubernetes​

The following section describes the key generation process with Portworx and Kubernetes which can be used for encrypting volumes.

### Set cluster wide secret key​

A cluster wide secret key is a common key that can be used to encrypt all your volumes.
 Create a cluster wide secret in Kubernetes using the appropriate command for your platform.
 Use the same `<px-namespace>` namespace on which you've installed Portworx.

- Kubernetes

- OpenShift

```

NAMESPACE=<px-namespace>

kubectl -n ${NAMESPACE} create secret generic px-vol-encryption \

  --from-literal=<cluster-wide-secret-key>=<value>

```

```

NAMESPACE=<px-namespace>

oc -n ${NAMESPACE} create secret generic px-vol-encryption \

  --from-literal=<cluster-wide-secret-key>=<value>

```

This command creates a secret named `px-vol-encryption` within the namespace you specify as `<px-namespace>`. This secret stores your cluster-wide encryption key. Replace `<value>` with the value of your encryption key.

Provide the cluster wide secret key to Portworx, which acts as the default encryption key for all volumes.

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n ${NAMESPACE} -- /opt/pwx/bin/pxctl secrets set-cluster-key \

  --secret <cluster-wide-secret-key>

```

```

PX_POD=$(oc get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

oc exec $PX_POD -n ${NAMESPACE} -- /opt/pwx/bin/pxctl secrets set-cluster-key \

  --secret <cluster-wide-secret-key>

```

note

The cluster wide key is the secret name where the encrypt key exists. It does not contain the value to encrypt.

## Use Kubernetes Secrets with Portworx​

- Encrypt PVCs using annotations with Kubernetes Secrets

- Encrypt PVCs using CSI and Kubernetes Secrets

- Encrypt PVCs using StorageClass with Kubernetes Secrets

In this topic:
