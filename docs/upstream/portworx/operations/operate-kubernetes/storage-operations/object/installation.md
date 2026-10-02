# Install Portworx Object service

Source: https://docs.portworx.com/portworx-enterprise/operations/operate-kubernetes/storage-operations/object/installation (Portworx Enterprise 3.6)

Install Portworx Object service | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page describes how to install Portworx Object Service.

## Prerequisites​

To install Portworx Object Service, you must meet the following prerequisites:

- Provide access to an AWS S3 or Pure FlashBlade secret access key ID and secret access key

## Installation​

Portworx Object Service objects are managed by Stork, and they interact with a target Portworx Enterprise instance. The Portworx Object Service SDK is located in the target Portworx Enterprise instance. This allows you to create buckets, delete buckets, and provide or revoke access to buckets.

Additionally, you must provide access to the backend bucket service through environment variables. Because Portworx Object Service is in early access, extra steps are required to enable and set up the Portworx Object Service controller. The following steps allow Portworx Enterprise to create and provide access to buckets on behalf of the credentials provided:

-
Enable the Portworx Object Service controller flag in Stork by adding the following `args` to your StorageCluster spec:

```

spec:

  ...

  stork:

    enabled: true

    args:

      px-object-controller: "true"

```

-
Create a new Kubernetes secret with your AWS S3 or Pure FlashBlade access key ID and secret access key:

- Kubernetes

- OpenShift

-
For AWS S3, add the following:

```

kubectl create secret generic px-object-s3-admin-credentials \

    --from-literal=access-key-id=ACCESS_KEY \

    --from-literal=secret-access-key=SECRET_ACCESS_KEY

```

-
For Pure FlashBlade, add the following:

```

kubectl create secret generic px-object-fb-admin-credentials \

    --from-literal=access-key-id=ACCESS_KEY \

    --from-literal=secret-access-key=SECRET_ACCESS_KEY

```

-
For AWS S3, add the following:

```

oc create secret generic px-object-s3-admin-credentials \

    --from-literal=access-key-id=ACCESS_KEY \

    --from-literal=secret-access-key=SECRET_ACCESS_KEY

```

-
Add environment variables for bucket credentials to your StorageCluster spec.

-
For AWS S3, add the following:

```

spec:

  env:

  - name: OBJECT_SERVICE_S3_ACCESS_KEY_ID

    valueFrom:

      secretKeyRef:

        name: px-object-s3-admin-credentials

        key: access-key-id

  - name: OBJECT_SERVICE_S3_SECRET_ACCESS_KEY

    valueFrom:

      secretKeyRef:

        name: px-object-s3-admin-credentials

        key: secret-access-key

```

- `OBJECT_SERVICE_S3_ACCESS_KEY_ID`: An AWS S3 Access Key ID credential generated in the AWS Portal.

- `OBJECT_SERVICE_S3_SECRET_ACCESS_KEY`: An AWS S3 Secret Access Key credential generated in the AWS Portal.

-
For Pure FlashBlade, add the following:

```

spec:

  env:

  - name: OBJECT_SERVICE_FB_ACCESS_KEY_ID

    valueFrom:

      secretKeyRef:

        name: px-object-fb-admin-credentials

        key: access-key-id

  - name: OBJECT_SERVICE_FB_SECRET_ACCESS_KEY

    valueFrom:

      secretKeyRef:

        name: px-object-fb-admin-credentials

        key: secret-access-key

```

- `OBJECT_SERVICE_FB_ACCESS_KEY_ID`: A Pure FlashBlade Access Key ID credential provided by the FlashBlade admin.

- `OBJECT_SERVICE_FB_SECRET_ACCESS_KEY`: A Pure FlashBlade Secret Access Key credential provided by the FlashBlade admin.

## Related topics​

- Portworx Object Service Reference

In this topic:
