# Store Certificates as Kubernetes Secrets

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/certs (Portworx Enterprise latest)

Store Certificates as Kubernetes Secrets | Portworx Enterprise Documentation

Sometimes you need to store an SSL certificate as a Kubernetes secret. This document walks through an example of how to secure a third-party S3-compatible objectstore for use with Portworx.

## Create the secret​

- Kubernetes

- OpenShift

-
Copy your certificate to the location where `kubectl` is configured for this Kubernetes cluster. Copy the `public.crt` file to the `/opt/certs` folder.

-
Create the secret:

```

kubectl -n kube-system create secret generic px-s3-certs --from-file=/opt/certs/

```

-
Confirm that the secret was created correctly:

```

kubectl -n kube-system describe secret px-s3-certs

```

-
Copy your certificate to the location where `oc` is configured for your cluster. Copy the `public.crt` file to the `/opt/certs` folder.

-
Create the secret:

```

oc -n kube-system create secret generic px-s3-certs --from-file=/opt/certs/

```

-
Confirm that the secret was created correctly:

```

oc -n kube-system describe secret px-s3-certs

```

## Provide the secret to Portworx​

Based on your Portworx installation type, provide the secret to Portworx by performing the steps in one of the following sections.

### Portworx Operator​

Update the Portworx `StorageCluster` to mount the secret and the environment variable:

- Kubernetes

- OpenShift

```

kubectl -n kube-system edit storagecluster portworx

```

```

oc -n kube-system edit storagecluster portworx

```

```

spec:

  volumes:

  - name: objectstore-cert

    mountPath: /etc/pwx/objectstore-cert

    secret:

      secretName: px-s3-certs

      items:

      - key: public.crt

        path: public.crt

  env:

  - name: "AWS_CA_BUNDLE"

    value: "/etc/pwx/objectstore-cert/public.crt"

```

After saving the modified `StorageCluster`, Portworx will restart in a rolling update.

In this topic:
