# Migration with Stork on EKS

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/eks (Portworx Enterprise 3.6)

Migration with Stork on EKS | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Pairing with an EKS cluster requires the following additional steps because you also need to pass in your AWS credentials which will be used to generate the IAM token.

## Create a Secret with your AWS credentials​

On the source cluster, create a secret in the `<stork-deployment-namespace>` namespace with your AWS credentials file:

- Kubernetes

- OpenShift

```

kubectl create secret generic --from-file=$HOME/.aws/credentials -n <stork-deployment-namespace> aws-creds

```

```

oc create secret generic --from-file=$HOME/.aws/credentials -n <stork-deployment-namespace> aws-creds

```

```

secret/aws-creds created

```

## Pass the Secret to Stork​

The credentials created in the previous step need to be provided to Stork. When deployed through Portworx Operator, add the following to the `stork` section of the StorageCluster spec:

```

stork:

  enabled: true

  volumes:

  - name: aws-creds

    mountPath: /root/.aws/

    readOnly: true

    secret:

      secretName: aws-creds

```

In this topic:
