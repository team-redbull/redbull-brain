# Migration with Stork on GKE

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/gke (Portworx Enterprise 3.6)

Migration with Stork on GKE | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Pairing with a GKE cluster requires the following additional steps. You also need to pass in your Google Cloud credentials, which will be used to generate access tokens.

## Create a service account​

Use the guide from Google Cloud to generate a service-account key and save it as gcs-key.json. You can also create this using the following command:

```

gcloud iam service-accounts keys create gcs-key.json --iam-account <your_iam_account>

```

## Create a Secret from the service-account key​

On the source cluster, create a secret in the `kube-system` namespace with the service account JSON file created in the previous step:

- Kubernetes

- OpenShift

```

kubectl create secret generic --from-file=gcs-key.json -n kube-system gke-creds

```

```

secret/gke-creds created

```

```

oc create secret generic --from-file=gcs-key.json -n kube-system gke-creds

```

```

secret/gke-creds created

```

## Pass the Secret to Stork​

The credentials created in the previous step need to be provided to Stork. When deployed through Portworx Operator, add the following to the `stork` section of the StorageCluster spec:

```

stork:

  enabled: true

  volumes:

  - name: gke-creds

    mountPath: /root/.gke

    readOnly: true

    secret:

      secretName: gke-creds

  env:

  - name: GOOGLE_APPLICATION_CREDENTIALS

    value: /root/.gke/gcs-key.json

```

## Update ClusterRoleBinding​

Create a `ClusterRoleBinding` to give your account the cluster-admin role:

- Kubernetes

- OpenShift

```

kubectl create clusterrolebinding stork-cluster-admin-binding --clusterrole=cluster-admin --user=<your_iam_account>

```

```

oc create clusterrolebinding stork-cluster-admin-binding --clusterrole=cluster-admin --user=<your_iam_account>

```

In this topic:
