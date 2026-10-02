# Enable authorization in Portworx

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/px-security/authorization (Portworx Enterprise latest)

Enable authorization in Portworx | Portworx Enterprise Documentation

Portworx provides Role-Based Access Control (RBAC) to secure access to storage resources in your cluster. This page guides you through enabling authorization in your Portworx deployment.

When upgrading from `auth disabled` to `auth enabled`, there will be no issues for Kubernetes or OpenShift end users. This is because the system guest role will allow users to create and use public volumes. However, users are encouraged to make their volumes private by adding authorization to their PVCs.

note

Enabling authorization will cause a cluster-level interruption event while all nodes in the system come back online with security enabled.

## Enabling authorization with the Portworx Operator​

You can easily set up security in your `StorageCluster` spec with a single flag:

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

### Migrating from Portworx Manifest to StorageCluster Security spec​

In order for Portworx to start with security enabled, it requires a few different environment variables. If you wish to start using the `StorageCluster` security spec, here is how you can migrate your environment variables to spec fields.

-
Familiarize yourself with the Security spec in the StorageCluster article.

-
Create a Kubernetes secret for your shared-secret:

- Kubernetes

- OpenShift

```

kubectl create secret generic -n <px-namespace> px-shared-secret \

  --from-literal=shared-secret=$EXISTING_SHARED_SECRET_VALUE

```

```

oc create secret generic -n <px-namespace> px-shared-secret \

  --from-literal=shared-secret=$EXISTING_SHARED_SECRET_VALUE

```

-
Add the following `spec.security` section in your `StorageCluster`:

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

        issuer: '<value from your PORTWORX_AUTH_JWT_ISSUER environment variable>'

        sharedSecret: 'px-shared-secret'

```

-
Remove the `PORTWORX_AUTH_JWT_ISSUER` and `PORTWORX_AUTH_JWT_SHAREDSECRET` env variables from your StorageCluster env spec.

-
You can now apply the StorageCluster spec and wait until Portworx is ready.

### Migrating to auto-generated PX-Security system secrets​

Another feature of Portworx Operator Security is that you can allow the Operator to auto-generate all required system secrets. This can greatly decrease the complexity of your PX-Security deployment. The auto-generated secrets are random 64 character strings and are base64 encoded. This is a zero downtime migration and can be achieved with the following `StorageCluster` changes:

-
Add the following to your `StorageCluster` security spec:

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

        issuer: '<value from your PORTWORX_AUTH_JWT_ISSUER environment variable>'

        sharedSecret: 'px-shared-secret'

```

-
Remove the `PORTWORX_AUTH_SYSTEM_KEY` and `PORTWORX_AUTH_SYSTEM_APPS_KEY` environment variables in your `StorageCluster` spec.env.

-
Remove the `PX_SHARED_SECRET` environment variable in your `StorageCluster` spec.stork.env

After applying the above `StorageCluster`, Portworx will restart with Security enabled using an auto-generated system secret and stork secret. These two secrets are used for internal Portworx communication between nodes and services.

## Enabling authorization with a Portworx Manifest​

To enable authorization you must simply edit your Portworx `yaml` configuration to add the appropriate information. You must first create a Kubernetes Secret which holds the values of the environment variables. Then populate the environment variables required from your Secret. Here is an example of how to setup an environment variable from a Secret:

-
Generate the following random secret keys:

```

PORTWORX_AUTH_SYSTEM_KEY=$(cat /dev/urandom | base64 | fold -w 64 | head -n 1) \

PORTWORX_AUTH_SYSTEM_APPS_KEY=$(cat /dev/urandom | base64 | fold -w 64 | head -n 1) \

PORTWORX_AUTH_SHARED_SECRET=$(cat /dev/urandom | base64 | fold -w 64 | head -n 1)

```

-
Create a secret for all PX-Security keys:

- Kubernetes

- OpenShift

```

kubectl create secret generic pxkeys \

  --from-literal=system-secret=$PORTWORX_AUTH_SYSTEM_KEY \

  --from-literal=shared-secret=$PORTWORX_AUTH_SHARED_SECRET \

  --from-literal=stork-secret=$PORTWORX_AUTH_SYSTEM_APPS_KEY

```

```

oc create secret generic pxkeys \

  --from-literal=system-secret=$PORTWORX_AUTH_SYSTEM_KEY \

  --from-literal=shared-secret=$PORTWORX_AUTH_SHARED_SECRET \

  --from-literal=stork-secret=$PORTWORX_AUTH_SYSTEM_APPS_KEY

```

-
Edit your Portworx manifest YAML to include the following:

```

...

  name: stork

  env:

    - name: "PX_SHARED_SECRET"

      valueFrom:

        secretKeyRef:

          name: pxkeys

          key: stork-secret

...

  name: portworx

  args:

  [..."-jwt_issuer", "myissuer", ...]

  env:

    - name: "PORTWORX_AUTH_JWT_SHAREDSECRET"

      valueFrom:

        secretKeyRef:

          name: pxkeys

          key: shared-secret

    - name: "PORTWORX_AUTH_SYSTEM_KEY"

      valueFrom:

        secretKeyRef:

          name: pxkeys

          key: system-secret

    - name: "PORTWORX_AUTH_SYSTEM_APPS_KEY"

      valueFrom:

        secretKeyRef:

          name: pxkeys

          key: stork-secret

...

```

## PVCs and Stork with authorization​

### Creating volumes​

Portworx authorization provides a method of protection for creating volumes through Kubernetes. Users must provide a token when requesting volumes in order to create a private volume. These tokens must be saved in a Secret, normally in the same namespace as the PVC.

The key in the Secret which holds the token must be named `auth-token`.

Then the annotations of the PVC can be used to point to the secret holding the token. The following table shows the annotation keys used to point to the secret:

NameDescription

`openstorage.io/auth-secret-name`Name of the secret which has the token

`openstorage.io/auth-secret-namespace`Optional key which contains the namespace of the secret reference by `auth-secret-name`. If omitted, the namespace of the PVC will be used as default

### Create a Secure PVC​

-
Find or create your token Secret:

For operator installs, a user token is automatically created and refreshed under `px-user-token` in your `StorageCluster` namespace.

- Kubernetes

- OpenShift

```

USER_TOKEN=$(kubectl get secrets px-user-token -n <px-namespace> -o json | jq -r '.data["auth-token"]' | base64 -d)

```

```

USER_TOKEN=$(oc get secrets px-user-token -n <px-namespace> -o json | jq -r '.data["auth-token"]' | base64 -d)

```

For all other configurations, create your own token secret:

- Kubernetes

- OpenShift

```

kubectl create secret generic px-user-token \

  -n <px-namespace> --from-literal=auth-token=$USER_TOKEN

```

```

oc create secret generic px-user-token \

   -n <px-namespace> --from-literal=auth-token=$USER_TOKEN

```

-
Before creating pvc, make sure you've created a storageclass which can authenticate using the secrets. For example.

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: portworx-sc

provisioner: pxd.portworx.com

parameters:

  repl: "1"

  csi.storage.k8s.io/provisioner-secret-name: px-user-token

  csi.storage.k8s.io/provisioner-secret-namespace: <px-namespace>

  csi.storage.k8s.io/node-publish-secret-name: px-user-token

  csi.storage.k8s.io/node-publish-secret-namespace: <px-namespace>

  csi.storage.k8s.io/controller-expand-secret-name: px-user-token

  csi.storage.k8s.io/controller-expand-secret-namespace: <px-namespace>

allowVolumeExpansion: true

```

-
Create a PVC request, specifying your volume size, accessModes, and authorizations:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pvc-auth

  annotations:

    volume.beta.kubernetes.io/storage-class: portworx-sc

    openstorage.io/auth-secret-name: px-user-token

    openstorage.io/auth-secret-namespace: <px-namespace>

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

For secure CSI volume creation, see Securing your CSI volumes.

### Stork​

When using CRDs consumed by Stork, you must use the same authorization model described above for the PVCs. Here is an example:

```

apiVersion: volumesnapshot.external-storage.k8s.io/v1

kind: VolumeSnapshot

metadata:

  name: mysql-snap1

  annotations:

    openstorage.io/auth-secret-name: px-user-token

    openstorage.io/auth-secret-namespace: default

spec:

  persistentVolumeClaimName: mysql-data

```

### Reference​

For more information on Kubernetes Secret which holds the environment variables See Kubernetes Secrets

In this topic:
