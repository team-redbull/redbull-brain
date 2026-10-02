# Encrypt PVCs using CSI and Kubernetes Secrets

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/kubernetes-secrets/pvc-encryption-using-csi (Portworx Enterprise 3.6)

Encrypt PVCs using CSI and Kubernetes Secrets | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This topic explains the PVC encryption methods used with the Kubernetes Container Storage Interface. For information about using Portworx with CSI, see the Portworx with CSI topic.

## Prerequisites​

In order to perform the steps in this document, you must have Portworx with CSI enabled.

## Encrypt your volumes​

You can encrypt your volumes in one of two ways:

- Per StorageClass

- Per PVC

### Encrypt your volumes per StorageClass​

You can encrypt your volumes by specifying the encryption key in a Kubernetes secret. This secret can be same as the one created to host the authentication token. Using this method, you can handle both authentication and encryption together, and multiple PVCs referring to this storage class can use the same secret for encryption.

#### Step 1: Create a Kubernetes secret that contains the passphrase used for encrypting the Portworx volume​

Enter the following command, specifying your own passphrase in `mysecret-passcode-for-encryption`, which encrypts the PVC:

- Kubernetes

- OpenShift

```

kubectl create secret generic volume-secrets -n kube-system --from-literal=mysql-pvc-secret-key=<mysecret-passcode-for-encryption>

```

```

oc create secret generic volume-secrets -n kube-system --from-literal=mysql-pvc-secret-key=<mysecret-passcode-for-encryption>

```

#### Step 2: Create a CSI Kubernetes secret that points to the Kubernetes encryption secret​

The CSI implementation reads the Kubernetes secret `px-secret` and passes its contents to Portworx. The `px-secret` must contain values for the following fields, which tell Portworx which Kubernetes secret to fetch the encryption passphrase from:

- `SECRET_NAME`: The name you have given your secret (in this case, `volume-secrets`).

- `SECRET_KEY`: The key for accessing the encryption key in the referenced `SECRET_CONTEXT`/`SECRET_NAME`.

- `SECRET_CONTEXT`: The namespace in which you created the secret (in this case, `kube-system`).

Enter the following command:

- Kubernetes

- OpenShift

```

kubectl create secret generic px-secret -n kube-system --from-literal=SECRET_NAME=volume-secrets --from-literal=SECRET_KEY=mysql-pvc-secret-key --from-literal=SECRET_CONTEXT=kube-system

```

```

oc create secret generic px-secret -n kube-system --from-literal=SECRET_NAME=volume-secrets --from-literal=SECRET_KEY=mysql-pvc-secret-key --from-literal=SECRET_CONTEXT=kube-system

```

#### Step 3: Create a CSI storage class for encrypted PVC​

Create the storage class which refers to the CSI secret you created in step 2 above. Specify the following:

- `csi.storage.k8s.io/provisioner-secret-name`: the name of your CSI secret

- `csi.storage.k8s.io/provisioner-secret-namespace`: the namespace in which your CSI secret is located

- `csi.storage.k8s.io/node-publish-secret-name`: the name of your CSI secret

- `csi.storage.k8s.io/node-publish-secret-namespace`: the namespace in which your CSI secret is located

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: px-csi-db-encrypted-k8s

provisioner: pxd.portworx.com

parameters:

  repl: "3"

  secure: "true"

  io_profile: auto

  io_priority: "high"

  csi.storage.k8s.io/provisioner-secret-name: px-secret

  csi.storage.k8s.io/provisioner-secret-namespace: kube-system

  csi.storage.k8s.io/node-publish-secret-name: px-secret

  csi.storage.k8s.io/node-publish-secret-namespace: kube-system

reclaimPolicy: Delete

volumeBindingMode: Immediate

allowVolumeExpansion: true

```

### Encrypt your volumes per PVC​

You can encrypt volumes by allowing your users to specify encryption keys in their PVCs. Using this method, each PVC will use its own key for encryption. Follow the steps below to create two PVCs which use different passphrases for encryption:

#### Step 1: Create two Kubernetes secrets to house the encryption keys for your two PVCs​

Kubernetes secrets can be in the Portworx namespace or in a user namespace. In this example we will be creating Kubernetes secrets in the user namespace `default`.

Enter the following command to create the secret for your first PVC, specifying your own passphrase for `mysecret-passcode-for-encryption`, which encrypts the PVC:

- Kubernetes

- OpenShift

```

kubectl create secret generic volume-secrets-1 --from-literal=mysql-pvc-secret-key-1=mysecret-passcode-for-encryption-1

kubectl create secret generic volume-secrets-2 --from-literal=mysql-pvc-secret-key-2=mysecret-passcode-for-encryption-2

```

```

oc create secret generic volume-secrets-1 --from-literal=mysql-pvc-secret-key-1=mysecret-passcode-for-encryption-1

oc create secret generic volume-secrets-2 --from-literal=mysql-pvc-secret-key-2=mysecret-passcode-for-encryption-2

```

#### Step 2: Create two additional Kubernetes secrets that refer to the encryption key secrets​

Enter the following command to create another secret associated with your first PVC, specifying the following options:

- This secret's name (`mysql-pvc-1` in this example)

- The `-n` option with the same namespace as the first encryption key secret you created (`csi-test-demo` in this example)

- The `--from-literal=SECRET_NAME=` option and the name of the encryption key secret you created

- The `--from-literal=SECRET_KEY=` option and the key from inside the PVC's encryption key secret

- The `--from-literal=SECRET_CONTEXT=` option and the encryption key secret's namespace as described in step 1

- Kubernetes

- OpenShift

```

kubectl create secret generic mysql-pvc-1 -n csi-test-demo --from-literal=SECRET_NAME=volume-secrets-1 --from-literal=SECRET_KEY=mysql-pvc-secret-key-1 --from-literal=SECRET_CONTEXT=csi-test-demo

```

Enter the same command for your second PVC, but specify a different secret name and optionally, a different namespace:

```

kubectl create secret generic mysql-pvc-2 -n csi-test-demo --from-literal=SECRET_NAME=volume-secrets-2 --from-literal=SECRET_KEY=mysql-pvc-secret-key-2 --from-literal=SECRET_CONTEXT=csi-test-demo

```

```

oc create secret generic mysql-pvc-1 -n csi-test-demo --from-literal=SECRET_NAME=volume-secrets-1 --from-literal=SECRET_KEY=mysql-pvc-secret-key-1 --from-literal=SECRET_CONTEXT=csi-test-demo

```

Enter the same command for your second PVC, but specify a different secret name and optionally, a different namespace:

```

oc create secret generic mysql-pvc-2 -n csi-test-demo --from-literal=SECRET_NAME=volume-secrets-2 --from-literal=SECRET_KEY=mysql-pvc-secret-key-2 --from-literal=SECRET_CONTEXT=csi-test-demo

```

#### Step 3: Create a CSI storage class for encrypted PVCs​

Create a StorageClass CRD, specifying the `${pvc.name}` and `${pvc.namespace}` template variables:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-csi-db-encrypted-pvc-k8s

provisioner: pxd.portworx.com

parameters:

  repl: "3"

  secure: "true"

  io_profile: auto

  io_priority: "high"

  csi.storage.k8s.io/provisioner-secret-name: ${pvc.name}

  csi.storage.k8s.io/provisioner-secret-namespace: ${pvc.namespace}

  csi.storage.k8s.io/node-publish-secret-name: ${pvc.name}

  csi.storage.k8s.io/node-publish-secret-namespace: ${pvc.namespace}

    #backend: "pure_block"  # Uncomment for FADA volumes.

reclaimPolicy: Delete

volumeBindingMode: Immediate

allowVolumeExpansion: true

```

note

When you use `backend: "pure_block"` with encryption, only Filesystem volumes (`volumeMode: Filesystem`) is supported. FADA raw-block volumes (`volumeMode: Block`) cannot be encrypted.

#### Step 4: Create encrypted PVCs​

Create two encrypted PVCs, one for each of the secrets you created in the preceding steps:

-
Create the `mysql-pvc-1` PVC that uses the passcode you created previously. In the example, that passcode is `mysecret-passcode-for-encryption-1`:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-pvc-1

  namespace: csi-test-demo

spec:

  storageClassName: px-csi-db-encrypted-pvc-k8s

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

-
Create the `mysql-pvc-2` PVC that uses the passcode you created previously. In the example, that passcode is `mysecret-passcode-for-encryption-2`:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: mysql-pvc-2

  namespace: csi-test-demo

spec:

  storageClassName: px-csi-db-encrypted-pvc-k8s

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

The templatized parameters in the CSI storage class point to the name and namespace of the PVC itself. This ensures that each PVC requires a separate Kubernetes secret of the same name in the same namespace. In this way, each PVC gets encrypted with its own passphrase.

## Manually attach encrypted volumes​

When you need to manually attach a CSI-encrypted volume to a host using the `pxctl host attach` command, you must provide the encryption secret information. This information can be obtained from the volume's labels in the `pxctl volume inspect` output.

### Get secret information from volume inspect​

To find the secret information for an encrypted volume, inspect the volume and look for the labels containing `SECRET_CONTEXT`, `SECRET_KEY`, and `SECRET_NAME`:

```

pxctl volume inspect <volume-id>

```

The output will include labels similar to:

```

Labels : SECRET_CONTEXT=csi-test-demo,SECRET_KEY=mysql-pvc-secret-key-1,SECRET_NAME=volume-secrets-1,...

```

### Attach the encrypted volume​

Use the `pxctl host attach` command with the `--secret_options` and `--secret_key` flags to attach the encrypted volume:

```

pxctl host attach <volume-id> --secret_options="SECRET_CONTEXT=<k8s_namespace_of_secret>,SECRET_KEY=<key_name_of_passcode>" --secret_key="<k8s_secret_holds_the_passcode>"

```

Where:

- `volume-id`: The ID of the encrypted volume

- `k8s_namespace_of_secret`: The Kubernetes namespace containing the secret (obtained from volume labels)

- `key_name_of_passcode`: The key name within the secret that holds the passphrase (obtained from volume labels)

- `k8s_secret_holds_the_passcode`: The name of the Kubernetes secret that contains the encryption passphrase (obtained from volume labels)

For example, using the labels from the inspect output above:

```

pxctl host attach 949983077935010586 --secret_options="SECRET_CONTEXT=csi-test-demo,SECRET_KEY=mysql-pvc-secret-key-1" --secret_key="volume-secrets-1"

```

In this topic:
