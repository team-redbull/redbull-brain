# Application setup with bucket access

Source: https://docs.portworx.com/portworx-enterprise/operations/operate-kubernetes/storage-operations/object/application-setup (Portworx Enterprise 3.6)

Application setup with bucket access | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page describes how to use a PXBucketAccess object with your application. The steps below apply to both Pure FlashBlade and AWS S3 buckets.

-
In your application's `deployment.yaml` file, add all environment variables for your buckets as Kubernetes deployment secret references. For example:

```

env:

- name: S3_ACCESS_KEY

  valueFrom:

    secretKeyRef:

      name: px-os-credentials-s3-pba

      key: access-key-id

- name: S3_SECRET_KEY

  valueFrom:

    secretKeyRef:

      name: px-os-credentials-s3-pba

      key: secret-access-key

- name: S3_BUCKET_NAME

  valueFrom:

    secretKeyRef:

      name: px-os-credentials-s3-pba

      key: bucket-id

- name: S3_ENDPOINT

  valueFrom:

    secretKeyRef:

      name: px-os-credentials-s3-pba

      key: endpoint

- name: S3_REGION

  valueFrom:

    secretKeyRef:

      name: px-os-credentials-s3-pba

      key: region

```

- Kubernetes

- OpenShift

-
Apply the updates to your `deployment.yaml`:

```

kubectl apply -f deployment.yaml

```

-
Apply the updates to your `deployment.yaml`:

```

oc apply -f deployment.yaml

```

## Related topics​

- Portworx Object Service Reference

In this topic:
