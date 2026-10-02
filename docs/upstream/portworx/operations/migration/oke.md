# Migration with Stork on OKE

Source: https://docs.portworx.com/portworx-enterprise/operations/migration/oke (Portworx Enterprise latest)

Migration with Stork on OKE | Portworx Enterprise Documentation

Pairing with an OKE cluster requires the following additional steps because you also need to pass in your Oracle credentials which will be used to generate the authentication token.

## Create a Secret with your Oracle credentials​

Follow how to generate an API signing key from the Oracle documentation to create your API signing key. Note down the `PATH` where you store the API signing key.

On the source cluster, create a secret in the `kube-system` namespace with your Oracle credentials file:

```

kubectl create secret generic --from-file=$HOME/.oci/config --from-file $HOME/.oci/oci.pem -n  kube-system oci-creds

```

```

secret/oci-creds created

```

In this example, the API signing key is stored under the path `$HOME/.oci/oci.pem`, and the OCI config file is stored under `$HOME/.oci/config`.

## Pass the Secret to Stork​

You need to provide the credentials created in the previous step to Stork. When deploying through the Portworx Operator, add the following to the `stork` section of the StorageCluster spec:

```

spec:

 stork:

    enabled: true

    volumes:

    - name: oci-creds

      mountPath: /root/.oci/

      readOnly: true

      secret:

        secretName: oci-creds

    env:

    - name: OCI_CLI_KEY_FILE

      value: /root/.oci/oci.pem

    - name: OCI_CLI_CONFIG_FILE

      value: /root/.oci/config

```

note

Make sure that your OCI configuration file does not have a `key_file` argument pointing to your local path. Your local path to the key file will not match with what is being presented to the Stork container.

In this topic:
