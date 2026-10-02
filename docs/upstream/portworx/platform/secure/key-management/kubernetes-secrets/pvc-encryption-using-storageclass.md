# Encrypt PVCs using StorageClass with Kubernetes Secrets

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/kubernetes-secrets/pvc-encryption-using-storageclass (Portworx Enterprise 3.6)

Encrypt PVCs using StorageClass with Kubernetes Secrets | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Portworx Encrypted Volumes​

Portworx has two different kinds of encrypted volumes:

-
Encrypted Volumes

Encrypted volumes are regular volumes which can be accessed from only one node.

-
Encrypted Sharedv4 Volumes

Encrypted sharedv4 volume allows access to the same encrypted volume from multiple nodes.

Using a StorageClass parameter, you can tell Portworx to encrypt all PVCs created using that StorageClass. Portworx uses a cluster wide secret to encrypt all the volumes created using the secure StorageClass.

#### Step 1: Create cluster wide secret key​

A cluster wide secret key is a common key that points to a secret value/passphrase which can be used to encrypt all your volumes.

Create a cluster wide secret in Kubernetes, if not already created:

- Kubernetes

- OpenShift

```

kubectl -n portworx create secret generic px-vol-encryption \

  --from-literal=cluster-wide-secret-key=<value>

```

```

oc -n portworx create secret generic px-vol-encryption \

  --from-literal=cluster-wide-secret-key=<value>

```

The cluster-wide secret must reside in the `px-vol-encryption` secret under the `portworx` namespace.

Now you must provide Portworx with the cluster-wide secret key, which acts as the default encryption key for all volumes.

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl secrets set-cluster-key \

  --secret cluster-wide-secret-key

```

```

PX_POD=$(oc get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

oc exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl secrets set-cluster-key \

  --secret cluster-wide-secret-key

```

#### Step 2: Create a StorageClass​

Create a storage class with the `secure` parameter set to `true`.

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-secure-sc

provisioner: pxd.portworx.com

parameters:

  secure: "true"

  repl: "3"

  #backend: "pure_block"  # Uncomment for FADA volumes.

```

note

When you use `backend: "pure_block"` with encryption, only Filesystem volumes (`volumeMode: Filesystem`) is supported. FADA raw-block volumes (`volumeMode: Block`) cannot be encrypted.

To create a sharedv4 encrypted volume set the `sharedv4` parameter to `true` as well.

#### Step 3: Create Persistent Volume Claim​

Create a PVC that uses the above `px-secure-sc` storage class.

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-pvc

spec:

  storageClassName: px-secure-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

#### Step 4: Verify the volume​

Once the PVC has been created, verify the volume created in Portworx is encrypted:

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl volume list

```

```

PX_POD=$(oc get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

oc exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl volume list

```

```

ID                 NAME                                      ...  ENCRYPTED  ...

10852605918962284  pvc-xxxxxxxx-xxxx-xxxx-xxxx-080027ee1df7  ...  yes        ...

```

In this topic:
