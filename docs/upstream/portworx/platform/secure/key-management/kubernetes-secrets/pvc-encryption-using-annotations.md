# Encrypt PVCs using annotations with Kubernetes Secrets

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/kubernetes-secrets/pvc-encryption-using-annotations (Portworx Enterprise latest)

Encrypt PVCs using annotations with Kubernetes Secrets | Portworx Enterprise Documentation

## Portworx Encrypted Volumes​

Portworx has two different kinds of encrypted volumes:

-
Encrypted Volumes

Encrypted volumes are regular volumes which can be accessed from only one node.

-
Encrypted Sharedv4 Volumes

Encrypted sharedv4 volume allows access to the same encrypted volume from multiple nodes.

Encryption at Storage Class level does not allow using different secret keys for different PVCs. PVC-level annotations let you specify a different secret key per PVC or add encryption to a PVC whose Storage Class does not have the `secure` parameter set. However, if a Storage Class has the `secure` parameter set, PVC-level annotations cannot disable that encryption.

PVC level encryption is achieved using the following PVC annotations:

- `px/secure` - Boolean which tells whether to secure the PVC

- `px/secret-name` - Name of the secret used to encrypt

- `px/secret-namespace` - Namespace of the secret (Kubernetes Secrets only)

- `px/secret-key` - Key to be used in the secret (Kubernetes Secrets only)

### Encryption using cluster wide secret​

#### Step 1: Create cluster wide secret key​

A cluster wide secret key is a shared key that points to a secret value or passphrase used to encrypt all volumes.

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

Note that the cluster wide secret must reside in the `px-vol-encryption` secret under the `portworx` namespace.

Now you must provide Portworx with the cluster wide secret key, which serves as the default encryption key for all volumes.

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

note

The cluster wide key is the secret name where the encryption key exists. It does not contain the value to encrypt.

#### Step 2: Create the secure PVC​

If your Storage Class does not have the `secure` flag set, but you want to encrypt the PVC using the same Storage Class, then create the PVC as below:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-pvc

  annotations:

    px/secure: "true"

spec:

  storageClassName: portworx-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

As there is no `px/secret-name` annotation specified, Portworx will default to the cluster wide secret to encrypt this PVC. If the cluster wide secret is not set, the volume creation will fail until the key is set.

If a Storage Class has the `secure` parameter set, setting the `px/secure` annotation to `false` on a PVC will not disable encryption — the volume will still be encrypted. To provision unencrypted PVCs, use a Storage Class that does not have the `secure` parameter set.

note

If you are running Kubernetes version older than 1.9.4 (or < 1.8.9 in Kubernetes 1.8), then the PVC name must be in `ns.<namespace_of_pvc>-name.<identifier_for_pvc>` format to use the PVC-level encryption feature.

### Encryption using custom secret key​

#### Kubernetes secrets​

You can encrypt your PVC using a custom secret as follows:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-mysql-pvc

  annotations:

    px/secret-name: volume-secrets

    px/secret-namespace: portworx

    px/secret-key: mysql-pvc

spec:

  storageClassName: portworx-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

The encrypted PVC will use the key `mysql-pvc` under the Kubernetes secret `volume-secrets` in `portworx` namespace. If the secret key is not present, then the volume creation will fail until the key is created.

From the annotations in the above PVC, only `px/secret-name` is mandatory.

- If you do not specify the `px/secret-namespace`, Portworx will look for the secret in the PVC's namespace.

- If you do not specify the `px/secret-key`, Portworx will look for a key with the PVC name.

By default, Portworx has `get` and `list` permissions for Kubernetes secrets from all the namespaces. In the above example, you can replace the `px/secret-namespace` annotation with a namespace of your choice where you have created the Kubernetes secret.

In this topic:
