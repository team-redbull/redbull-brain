# Import existing buckets using the Portworx Object Service

Source: https://docs.portworx.com/portworx-enterprise/operations/operate-kubernetes/storage-operations/object/import-buckets (Portworx Enterprise 3.6)

Import existing buckets using the Portworx Object Service | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page describes how to import existing buckets using either AWS S3 or Pure FlashBlade.

## AWS S3​

Use the following steps to get started with pre-provisioned buckets:

-
Create a new file named `pxbucketclass.yaml`, replacing `region` and `object.portworx.io/endpoint` with your desired AWS S3 region and endpoint:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketClass

metadata:

  name: pbclass-s3

region: us-west-1

deletionPolicy: Delete

parameters:

  object.portworx.io/backend-type: S3Driver

  object.portworx.io/endpoint: s3.us-west-1.amazonaws.com

```

-
Create the PXBucketClass object:

- Kubernetes

- OpenShift

```

kubectl apply -f pxbucketclass.yaml

```

```

oc apply -f pxbucketclass.yaml

```

-
Create a new file named `pxbucketaccess.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketAccess

metadata:

  name: s3-pba-existing

  namespace: default

spec:

  bucketClassName: pbclass-s3

  existingBucketId: bucket-name-aws

```

-
Once the bucket access is granted, its `ACCESSGRANTED` state will be marked as `true` in the CustomResource:

- Kubernetes

- OpenShift

```

kubectl get pxbucketaccess

```

```

NAME              ACCESSGRANTED   CREDENTIALSSECRETNAME               BUCKETID               BACKENDTYPE

s3-pba-existing   true            px-os-credentials-s3-pba-existing   existing-bucket-id     S3Driver

```

```

oc get pxbucketaccess

```

```

NAME              ACCESSGRANTED   CREDENTIALSSECRETNAME               BUCKETID               BACKENDTYPE

s3-pba-existing   true            px-os-credentials-s3-pba-existing   existing-bucket-id     S3Driver

```

- A secret `px-os-credentials-s3-pba-existing` will be created with all necessary bucket info:

- Kubernetes

- OpenShift

```

kubectl get secret px-os-credentials-s3-pba -o yaml

```

```

apiVersion: v1

data:

  access-key-id: <ACCESS-KEY-ID>

  bucket-id: <BUCKET-ID>

  endpoint: <ENDPOINT>

  region: <REGION>

  secret-access-key: <SECRET-ACCESS-KEY>

kind: Secret

metadata:

  creationTimestamp: "2022-08-03T21:27:25Z"

  finalizers:

  - finalizers.object.portworx.io/access-secret

  name: px-os-credentials-s3-pba

  namespace: default

  resourceVersion: "16022682"

  uid: xxxxxxxx-xxxx-xxxx-xxxx-9e9d30aba97c

type: Opaque

```

```

oc get secret px-os-credentials-s3-pba -o yaml

```

```

apiVersion: v1

data:

  access-key-id: <ACCESS-KEY-ID>

  bucket-id: <BUCKET-ID>

  endpoint: <ENDPOINT>

  region: <REGION>

  secret-access-key: <SECRET-ACCESS-KEY>

kind: Secret

metadata:

  creationTimestamp: "2022-08-03T21:27:25Z"

  finalizers:

  - finalizers.object.portworx.io/access-secret

  name: px-os-credentials-s3-pba

  namespace: default

  resourceVersion: "16022682"

  uid: xxxxxxxx-xxxx-xxxx-xxxx-9e9d30aba97c

type: Opaque

```

## Pure FlashBlade​

Use the following steps to get started with pre-provisioned buckets:

-
Create a new file named `pxbucketclass.yaml`, replacing `region` and `object.portworx.io/endpoint` with your desired Pure FlashBlade region and endpoint:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketClass

metadata:

  name: pbclass-fb

deletionPolicy: Delete

parameters:

  object.portworx.io/backend-type: PureFBDriver

  object.portworx.io/endpoint: fb.fb.endpoint.example.com

```

-
Create the PXBucketClass object:

```

kubectl apply -f pxbucketclass.yaml

```

-
Create a new file named `pxbucketaccess.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketAccess

metadata:

  name: fb-pba-existing

  namespace: default

spec:

  bucketClassName: pbclass-fb

  existingBucketId: bucket-name-aws

```

-
Once the bucket access is granted, its `ACCESSGRANTED` state will be marked as `true` in the CustomResource:

```

kubectl get pxbucketaccess

```

```

NAME              ACCESSGRANTED   CREDENTIALSSECRETNAME               BUCKETID               BACKENDTYPE

fb-pba-existing   true            px-os-credentials-fb-pba-existing   existing-bucket-id     PureFBDriver

```

-
A secret `px-os-credentials-fb-pba-existing` is created with all necessary bucket info:

```

kubectl get secret px-os-credentials-fb-pba -o yaml

```

```

apiVersion: v1

data:

  access-key-id: <ACCESS-KEY-ID>

  bucket-id: <BUCKET-ID>

  endpoint: <ENDPOINT>

  region: <REGION>

  secret-access-key: <SECRET-ACCESS-KEY>

kind: Secret

metadata:

  creationTimestamp: "2022-08-03T21:27:25Z"

  finalizers:

  - finalizers.object.portworx.io/access-secret

  name: px-os-credentials-fb-pba

  namespace: default

  resourceVersion: "16022682"

  uid: xxxxxxxx-xxxx-xxxx-xxxx-9e9d30aba97c

type: Opaque

```

## Related topics​

- Portworx Object Service Reference

In this topic:
