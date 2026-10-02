# Configure PX-Security on your cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/px-security (Portworx Enterprise 3.6)

Configure PX-Security on your cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

While Kubernetes provides a great authentication model for its users, storage systems could be exposed to malicious requests. PX-Security provides a method to protect against such requests, further providing deployers with a more secured system.

The following documents demonstrate how to setup PX-Security to authenticate PVC requests from Kubernetes. This model leverages Kubernetes user authentication, which secures access to Namespaces, Secrets, and PersistentVolumes. With access already provided and secured by Kubernetes, this model provides a way to secure the communication between Kubernetes and Portworx. Securing Portworx also protects the storage system from unwanted access from outside Kubernetes.

Perform the steps in the following sections to set up PX-Security according to this reference architecture:

- Enabling Security in your cluster - Update the StorageCluster spec gen to auto-generate a shared secret, an admin token, and a User token.

- Generate multitenant tokens - For a secure multitenant solution, Portworx can enhance the multitenant model by providing resource access control for application volumes.The following reference architecture provides a model where volume access is authenticated using tokens stored in the secret of the namespace of the tenant.This solution is currently supported in CSI only.

- Setup StorageClass to authenticate requests - Create a StorageClass which will instruct Portworx to authenticate all requests using the user token in the secret.

- Customize security setup - Customizing your Portworx Operator Security configuration further.

## Enabling Security in your cluster​

Portworx Operator includes first-class support for PX-Security in the StorageCluster spec. This means that the operator will auto-generate the following for you if security is enabled:

- Shared Secret stored under the secret px-shared-secret

- Admin token stored under the secret px-admin-token

- User token stored under the secret px-user-token

This document guides you through enabling PX-Security in your cluster by adding a single flag to your StorageCluster object.

- Enable security under spec.security of your StorageCluster:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

  namespace: <px-namespace>

spec:

  image: portworx/oci-monitor:2.6.0.1

  security:

    enabled: true

```

- You can now apply the StorageCluster spec and wait until Portworx is ready.

Once you've enabled security in Portworx, continue to the next section.

note

To use pxctl in this context, see use pxctl with security enabled. Otherwise, all pxctl commands will fail with an access denied error.

## Generate multitenant tokens for secure multitenant solution​

Now that the system is up and running, you can create tokens.

note

If you want to create your own application to generate tokens, you can base it on our open source golang example application openstorage-sdk-auth

SSH to one of your nodes and follow the steps below to use `pxctl` to generate tokens:

### Fetching the shared secret​

Fetch the shared secret, which is stored in a Kubernetes secret. Below, the secret is saved in the environment variable `$PORTWORX_AUTH_SHARED_SECRET`.

Get the shared secret:

- Kubernetes

- OpenShift

```

PORTWORX_AUTH_SHARED_SECRET=$(kubectl -n kube-system get \

        secret px-shared-secret -o json \

    | jq -r '.data."shared-secret"' \

    | base64 -d)

```

```

PORTWORX_AUTH_SHARED_SECRET=$(oc -n kube-system get \

        secret px-shared-secret -o json \

    | jq -r '.data."shared-secret"' \

    | base64 -d)

```

## Generate a storage admin token​

`pxctl` uses YAML configuration files to create tokens.

You must create a token for the storage admin used for `pxctl` to manage Portworx(like root in Linux)

-
Create a file called `admin.yaml` with the following:

```

name: Storage Administrator

email: the email of the storage admin

sub: ${uuid} or email of the storage admin

roles: ["system.admin"]

groups: ["*"]

```

-
Create a token for the storage administrator using `admin.yaml`. In the example below:

- The issuer matches the setting in the Portworx manifest of `portworx.com` as the set value for `-jwt-issuer`.

- The example sets the duration of the token to one year -- You may want to adjust it to a much shorter duration if you plan on refreshing the token often.

```

ADMIN_TOKEN=$(/opt/pwx/bin/pxctl auth token generate \

        --auth-config=admin.yaml \

        --issuer=portworx.com \

        --shared-secret=$PORTWORX_AUTH_SHARED_SECRET \

        --token-duration=1y)

```

-
Save the storage admin token in the `pxctl` context:

```

/opt/pwx/bin/pxctl context create admin --token=$ADMIN_TOKEN

```

## Generate tenant tokens​

This model is based on isolating tenant accounts by namespaces. You will need to create an account for the tenant in Kubernetes and restrict it to one or more namespaces. You will then store the tenant's token in each namespace they own.

The following steps provide instructions for creating and storing the token in a namespace for the tenant:

-
Create a file called `tenant-name.yaml` with the following:

```

name: <Tenant name>

email: <Tenant email>

sub: ${uuid} or email of the tenant

roles: ["system.user"]

groups: ["<groups the tenant participate if any"]

```

note

The `sub` is the unique identifier for this user and must not be shared amongst other tokens according to the JWT standard. This is the value used by Portworx to track ownership of resources. If `email` is also used as the `sub` unique identifier, please make sure it is not used by any other tokens. You can find more information on the rules of each of the value on the openstorage-sdk-auth repo.

-
Create a token for the Kubernetes using `tenant-name.yaml`:

```

TENANT_TOKEN=$(/opt/pwx/bin/pxctl auth token generate \

    --auth-config=tenant-name.yaml \

    --issuer=portworx.com \

    --shared-secret=$PORTWORX_AUTH_SHARED_SECRET \

    --token-duration=1y)

```

-
Save the tenant Kubernetes token in a secret called `<tenant namespace>/px-user-token`:

- Kubernetes

- OpenShift

```

kubectl -n <tenant namespace> create secret \

  generic px-user-token --from-literal=auth-token=$TENANT_TOKEN

```

```

oc -n <tenant namespace> create secret \

  generic px-user-token --from-literal=auth-token=$TENANT_TOKEN

```

-
Annotate the Kubernetes secret so that other components like Stork and PX-Backup do not backup this resource.

- Kubernetes

- OpenShift

```

kubectl -n <tenant namespace> annotate secret px-user-token \

  stork.libopenstorage.org/skipresource=true

```

```

oc -n <tenant namespace> annotate secret px-user-token \

  stork.libopenstorage.org/skipresource=true

```

Kubernetes storage classes can now be set up to use this secret to get access to the token to communicate with Portworx.

Once you have completed the steps in this section, continue to the next section.

## Setup StorageClass to authenticate requests​

In the previous section, you created a `StorageCluster` in the `<px-namespace>` namespace with security enabled.

As a result, the operator has created the secret `px-user-token` in that namespace. Now you can create a StorageClass which will instruct Portworx to authenticate all requests using the token in that secret.

Portworx validates requests to manage volumes using the token saved in the secret referenced by the StorageClass. As you create more StorageClasses, remember to reference the secret with the token to authenticate the requests. The example below demonstrates a StorageClass with token secrets added:

### StorageClass for CSI​

#### Create PVCs​

When you use CSI, the `StorageClass` references the secret for the supported CSI operations: provisioning, node publishing (mount and unmount), and controller expansion.

note

If you enable the FA/FB driver and use PX-Security, StorageClasses that provision FlashArray or FlashBlade Direct Access volumes require additional CSI secret parameters. Configure PX-Security before provisioning Direct Access volumes. For more information, see Prerequisites.

-
Create the following `storageclass.yaml` file:

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: fio-fa-da-sc

provisioner: pxd.portworx.com

parameters:

  backend: "pure_block"

  max_iops: "1000"

  max_bandwidth: "1G"

  csi.storage.k8s.io/fstype: "ext4"

  pure_fa_pod_name: "<fa-pod-name>"

  csi.storage.k8s.io/provisioner-secret-name: px-user-token

  csi.storage.k8s.io/provisioner-secret-namespace: <px-namespace>

  csi.storage.k8s.io/node-publish-secret-name: px-user-token

  csi.storage.k8s.io/node-publish-secret-namespace: <px-namespace>

  csi.storage.k8s.io/controller-expand-secret-name: px-user-token

  csi.storage.k8s.io/controller-expand-secret-namespace: <px-namespace>

  csi.storage.k8s.io/node-stage-secret-name: px-user-token

  csi.storage.k8s.io/node-stage-secret-namespace: <px-namespace>

  csi.storage.k8s.io/controller-publish-secret-name: px-user-token

  csi.storage.k8s.io/controller-publish-secret-namespace: <px-namespace>

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

-
Apply the `storageclass.yaml` file:

- Kubernetes

- OpenShift

```

kubectl apply -f storageclass.yaml

```

```

oc apply -f storageclass.yaml

```

#### Create VolumeSnapshots​

To create a VolumeSnapshot with PX-Security enabled, you can follow a similar approach to the one used for PVCs, ensuring that PX-Security is applied via the correct secret parameters.
 Prerequisites​
Ensure you have:

- Portworx installed and running on your OpenShift Bare Metal cluster.

- A valid `px-user-token` for PX-Security configured in the `kube-system` namespace.

- CSI snapshots enabled and VolumeSnapshot CRDs available.

To create VolumeSnapshots with PX-Security enabled:

-
A VolumeSnapshotClass defines how snapshots will be created using a specific storage driver. In this case, you will be using the Portworx CSI driver (`pxd.portworx.com`), with security tokens passed for PX-Security.

Here is an example YAML manifest for a VolumeSnapshotClass with PX-Security:

```

kind: VolumeSnapshotClass

apiVersion: snapshot.storage.k8s.io/v1

metadata:

  name: <example-snapclass>

driver: pxd.portworx.com

deletionPolicy: Delete

parameters:

  csi.storage.k8s.io/snapshotter-secret-name: px-user-token

  csi.storage.k8s.io/snapshotter-secret-namespace: kube-system

  csi.storage.k8s.io/snapshotter-list-secret-name: px-user-token

  csi.storage.k8s.io/snapshotter-list-secret-namespace: kube-system

  csi.storage.k8s.io/group-snapshotter-secret-name: px-user-token

  csi.storage.k8s.io/group-snapshotter-secret-namespace: kube-system

```

where:

- `secret-name`: Refers to the secret name containing the user token for creating snapshots.

- `secret-namespace`: The namespace where the secret is stored, typically kube-system.

- `deletionPolicy`: This defines the behavior when the snapshot is deleted. You can choose between Delete (the snapshot is also deleted from the storage system) and Retain (the snapshot is kept).

-
Once the VolumeSnapshotClass is created, you can create a snapshot of a PersistentVolumeClaim (PVC). Here's an example of how to create a VolumeSnapshot:

```

apiVersion: snapshot.storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: <example-snapshot>

spec:

  volumeSnapshotClassName: <example-snapclass>

  source:

    persistentVolumeClaimName: <example-pvc>

```

In this example:

- The `volumeSnapshotClassName` must reference the VolumeSnapshotClass you created earlier.

- The `persistentVolumeClaimName` should refer to the PVC you want to snapshot.

-
After applying the above YAMLs, you can verify that the snapshot was created successfully using the following command:

```

kubectl get volumesnapshot

```

-
(Optional) If you wish to restore a PVC from the created snapshot, you can create a new PVC from the snapshot like the following. Note that you will need to use a storage class with PX-Security enabled.

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: <restored-pvc>

spec:

  storageClassName: <storage-class-name>

  dataSource:

    name: <example-snapshot>

    kind: VolumeSnapshot

    apiGroup: snapshot.storage.k8s.io

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 10Gi

```

## Customize security setup​

This document guides you through optionally customizing your Portworx Operator Security configuration further to fit specific needs:

- Disable guest role access

- Managing the guest role yourself

- Changing token lifetime

- Add a custom issuer, shared secret, and tokenLifetime to your StorageCluster

Prerequisites

- PX-Security is enabled

### Disable guest role access​

In Portworx, the system guest role is enabled by default. To turn off this feature, you can disable it in the StorageCluster spec:

note

Once the guest role is disabled, volumes created without a token will only be accessible with a token.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  security:

    enabled: true

    auth:

      guestAccess: 'Disabled'

```

## Managing the guest role yourself​

You can exercise finer control over the `system.guest` role by setting it to `managed` mode. This instructs the Operator to stop updating the system guest role, allowing you to customize it yourself.

To enter `managed` mode, set the value of the `spec.security.auth.guestAccess` field to `managed`:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  security:

    enabled: true

    auth:

      guestAccess: 'Managed'

```

## Changing token lifetime​

By default, the token is valid for 24 hours. You can optionally specify a different JWT token lifetime. The Operator then generates a token with that token lifetime and refreshes it for the user accordingly.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  security:

    enabled: true

    auth:

      selfSigned:

        tokenLifetime: '4h'

```

## Add a custom issuer, shared secret, and tokenLifetime to your StorageCluster​

Add your `issuer`, `tokenLifetime`, and `sharedSecret` Kubernetes secret's name to the `spec.security.auth.selfSigned` object in your StorageCluster:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: px-cluster

  namespace: <px-namespace>

spec:

  security:

    enabled: true

    auth:

      selfSigned:

        issuer: "portworx.com"

        sharedSecret: "px-shared-secret"

        tokenLifetime: "1h"

```

### (Optionally) Generate a new cluster token​

If you use Disaster Recovery functionality or are using data-migrating functionality between Kubernetes or OpenShift clusters, run the following command to generate a new cluster token after these operations, as the token will have changed that is used for pairing and migrating your clusters:

```

pxctl cluster token reset

```

You will then need to update any other clusters' clusterpair objects with the new token.

## Implications on pxctl​

The `pxctl` command will also be secured. As a result, you may need to perform extra steps to run `pxctl` commands.

## Security parameter overview​

The following parameters are utilized and required by PX-Security. In the Operator-based installation, here are the parameters that are automatically created for you, but they can be manually changed if needed.

### Configuration​

For non-sensitive information, you can use command-line parameters with the following arguments:

NameDescription

`-jwt_issuer <issuer>`JSON Web Token issuer (e.g. openstorage.io). This is the token issuer for your self-signed tokens. It must match the `iss` value in token claims

`-jwt_rsa_pubkey_file <file path>`JSON Web Token RSA Public file path

`-jwt_ecds_pubkey_file <file path>`JSON Web Token ECDS Public file path

`-username_claim <claim>`Name of the claim in the token to be used as the unique ID of the user (`<claim>` can be `sub`, `email` or `name`, default: `sub`)

In this topic:
