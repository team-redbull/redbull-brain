# Create buckets using the Portworx Object Service

Source: https://docs.portworx.com/portworx-enterprise/operations/operate-kubernetes/storage-operations/object/create-buckets (Portworx Enterprise latest)

Create buckets using the Portworx Object Service | Portworx Enterprise Documentation

This page describes how to create and provide access to a Portworx Bucket Claim using either Pure FlashBlade or AWS S3.

## Pure FlashBlade​

Use the following steps to get started with dynamically provisioned buckets.

### Provision a new bucket​

-
Create a new file named `pxbucketclass.yaml`, removing `region` and replacing `object.portworx.io/endpoint` with your desired Pure FlashBlade endpoint:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketClass

metadata:

  name: pbclass-fb

deletionPolicy: Delete

parameters:

  object.portworx.io/backend-type: PureFBDriver

  object.portworx.io/endpoint: fb.s3.example.com

```

-
Create the PXBucketClass object:

```

kubectl apply -f pxbucketclass.yaml

```

-
Create a new file named `pxbucketclaim.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketClaim

metadata:

  name: fb-pbc

  namespace: default

spec:

  bucketClassName: pbclass-fb

```

-
Create the PXBucketClaim object:

```

kubectl apply -f pxbucketclaim.yaml

```

-
Once the bucket is provisioned, its `PROVISIONED` state will be listed as `true` in the CustomResource:

```

kubectl get pxbucketclaim

```

```

NAME     PROVISIONED   BUCKETID                                     BACKENDTYPE

fb-pbc   true          px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   PureFBDriver

```

### Provide access to the PXBucketClaim​

-
Create a new file named `pxbucketaccess.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketAccess

metadata:

  name: fb-pba

  namespace: default

spec:

  bucketClassName: pbclass-fb

  bucketClaimName: fb-pbc

```

-
Once the bucket access is granted, its `ACCESSGRANTED` state will be marked as `true` in the CustomResource:

```

kubectl get pxbucketaccess

```

```

NAME     ACCESSGRANTED   CREDENTIALSSECRETNAME      BUCKETID                                     BACKENDTYPE

fb-pba   true            px-os-credentials-fb-pba   px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   PureFBDriver

```

-
A secret `px-os-credentials-fb-pba` is created with all necessary bucket info:

```

kubectl get secret px-os-credentials-fb-pba -o yaml

```

```

apiVersion: v1

data:

  access-key-id: <access-key-id>

  bucket-id: <bucket-id>

  endpoint: <endpoint>

  secret-access-key: <secret-access-key>

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

## AWS S3​

Use the following steps to get started with dynamically provisioned buckets.

### Provision a new bucket​

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
Create a new file named `pxbucketclaim.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketClaim

metadata:

  name: s3-pbc

  namespace: default

spec:

  bucketClassName: pbclass-s3

```

-
Create the PXBucketClaim object:

- Kubernetes

- OpenShift

```

kubectl apply -f pxbucketclaim.yaml

```

```

oc apply -f pxbucketclaim.yaml

```

- Once the bucket is provisioned, its `PROVISIONED` state will be listed as `true` in the `CustomResource`:

- Kubernetes

- OpenShift

```

kubectl get pxbucketclaim

```

```

NAME     PROVISIONED   BUCKETID                                     BACKENDTYPE

s3-pbc   true          px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   S3Driver

```

```

oc get pxbucketclaim

```

```

NAME     PROVISIONED   BUCKETID                                     BACKENDTYPE

s3-pbc   true          px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   S3Driver

```

### Provide Access to the PXBucketClaim​

-
Create a new file named `pxbucketaccess.yaml`:

```

apiVersion: object.portworx.io/v1alpha1

kind: PXBucketAccess

metadata:

  name: s3-pba

  namespace: default

spec:

  bucketClassName: pbclass-s3

  bucketClaimName: s3-pbc

```

-
Once the bucket access is granted, its `ACCESSGRANTED` state will be marked as `true` in the CustomResource:

- Kubernetes

- OpenShift

```

kubectl get pxbucketaccess

```

```

NAME     ACCESSGRANTED   CREDENTIALSSECRETNAME      BUCKETID                                     BACKENDTYPE

s3-pba   true            px-os-credentials-s3-pba   px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   S3Driver

```

```

oc get pxbucketaccess

```

```

NAME     ACCESSGRANTED   CREDENTIALSSECRETNAME      BUCKETID                                     BACKENDTYPE

s3-pba   true            px-os-credentials-s3-pba   px-os-xxxxxxxx-xxxx-xxxx-xxxx-ac6595c2b721   S3Driver

```

- A secret `px-os-credentials-s3-pba` is created with all necessary bucket info:

- Kubernetes

- OpenShift

```

kubectl get secret px-os-credentials-s3-pba -o yaml

```

```

apiVersion: v1

data:

  access-key-id: <access-key-id>

  bucket-id: <bucket-id>

  endpoint: <endpoint>

  region: <region>

  secret-access-key: <secret-access-key>

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

  access-key-id: <access-key-id>

  bucket-id: <bucket-id>

  endpoint: <endpoint>

  region: <region>

  secret-access-key: <secret-access-key>

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

## Related topics​

- Portworx Object Service Reference

In this topic:
