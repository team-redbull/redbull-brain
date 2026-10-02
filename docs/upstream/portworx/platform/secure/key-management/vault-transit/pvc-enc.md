# Encrypt Kubernetes PVCs with Vault Transit

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/vault-transit/pvc-enc (Portworx Enterprise 3.6)

Encrypt Kubernetes PVCs with Vault Transit | Portworx Enterprise Documentation

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

### Encryption using StorageClass​

In this method, each volume will use its own unique passphrase for encryption. Portworx relies on vault transit secrets engine to generate a Data Encryption Key. This key will then be used to encrypt and decrypt your volumes.

#### Step 1: Create a StorageClass​

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

#### Step 2: Create a PVC​

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-mysql-pvc

spec:

  storageClassName: px-secure-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

If you do not want to specify the `secure` flag in the StorageClass, but you want to encrypt the PVC using that StorageClass, then create the PVC as below:

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

### Encryption using PVC annotations with Vault Namespaces​

If you have Vault Namespaces enabled and your secret resides inside a specific namespace, you must provide the name of that namespace and the secret key to Portworx.

#### Step 1: Create a StorageClass​

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

#### Step 2: Create a PVC with annotations​

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-mysql-pvc

  annotations:

    px/vault-namespace: <your-vault-namespace>

spec:

  storageClassName: px-secure-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

The PVC requires an extra annotation `px/vault-namespace` to indicate the Vault namespace where the secret key resides. If your key resides in the global vault namespace set in Portworx using the parameter `VAULT_NAMESPACE`, you don't need to specify this annotation. However, if the key resides in any other namespace, then this annotation is required.

### Encryption using PVC annotations with cluster wide secrets​

#### Step 1: Create cluster wide secret​

A cluster wide secret key is a common key that can be used to encrypt all your volumes. This common key needs to be pre-created in your KMS provider. You can set the cluster secret key using the following command:

```

pxctl secrets set-cluster-key

```

```

Enter cluster wide secret key: *****

Successfully set cluster secret key!

```

In the above prompt you need to enter the secret key that you created in your KMS. This command needs to be run just once for the cluster.

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

#### Step 3: Create a PVC with annotations​

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: secure-mysql-pvc

  annotations:

    px/secret-name: default

spec:

  storageClassName: px-secure-sc

  accessModes:

  - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

important

Portworx only allows default key for `px/secret-name` annotation for cluster wide secrets

In this topic:
