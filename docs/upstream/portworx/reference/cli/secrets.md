# Manage your secrets using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/secrets (Portworx Enterprise latest)

Manage your secrets using pxctl | Portworx Enterprise Documentation

This section provides instructions for managing your authentication credentials and endpoints with the `pxctl secrets` command. Currently, `pxctl` provides support for the following secret store providers:

- AWS KMS

- Google Cloud KMS

- KVDB

- IBM Key Protect

With Portworx, secrets are neither stored locally nor displayed. Instead, the credentials are stored as part of the secret endpoint given to Portworx for persisting authentication across reboots. You can manage your secrets through the `pxctl secrets` command. To see the list of available sub-commands and flags, run:

```

pxctl secrets --help

```

```

Manage Secrets. Supported secret stores AWS KMS | Vault | DCOS Secrets | IBM Key Protect | Kubernetes Secrets | Google Cloud KMS

Usage:

  pxctl secrets [flags]

  pxctl secrets [command]

Available Commands:

  aws                        AWS secret-endpoint commands

  dump-cluster-wide-secret   Dumps the cluster-wide secret and the associated key for this cluster.

  gcloud                     Google Cloud KMS commands

  ibm                        IBM Key Protect commands

  kvdb                       kvdb secret-endpoint commands

  set-cluster-key            Sets an existing secret as a cluster-wide (default) secret to be used for volume encryption

  upload-cluster-wide-secret Uploads the provided key and secret as a cluster-wide (default) secret.

Flags:

  -h, --help   help for secrets

Global Flags:

      --ca string            path to root certificate for ssl usage

      --cert string          path to client certificate for ssl usage

      --color                output with color coding

      --config string        config file (default is $HOME/.pxctl.yaml)

      --context string       context name that overrides the current auth context

  -j, --json                 output in json

      --key string           path to client key for ssl usage

      --output-type string   use "wide" to show more details

      --raw                  raw CLI output for instrumentation

      --ssl                  ssl enabled for portworx

Use "pxctl secrets [command] --help" for more information about a command.

```

Before using the `pxctl secrets` command to manage your secrets, make sure you've configured a secret store provider. See the Secret store management page for more details.

note

To use encrypted volumes and ACLs, you need to ensure that Portworx is authenticated with the secrets endpoint.

## AWS KMS​

You can use the `pxctl` CLI tool to:

- Generate AWS KMS secrets

- List your AWS KMS secrets.

### Generate a secret​

To generate a new KMS Data Key, run the `pxctl secrets aws generate-kms-data-key` command with the `--secret_id` flag as shown in the following example:

```

pxctl secrets aws generate-kms-data-key --secret_id mysecret

```

```

KMS Data Key successfully created.

```

### List your AWS KMS secrets​

You can list your AWS KMS secrets with:

```

pxctl secrets aws list-secrets

```

For more details on how to create data keys in AWS KMS and use them to encrypt your Portworx volumes, see the AWS KMS page.

## Google Cloud KMS​

With `pxctl`, you can create and list Google Cloud KMS secrets.

### Create a new secret​

You can create a new secret in Google Cloud KMS running `pxctl secrets gcloud create-secret` with the following flags:

- `secret-id` with the id of the secret.

- `passphrase` with the secret passphrase Portworx will associate with `secret-id`.

As an example, here's how you can generate a new secret in Google Cloud KMS:

```

pxctl secrets gcloud create-secret --secret_id mysecret --passphrase mysecretpassphrase

```

```

Created secret with id:  mysecret

```

This creates a new key-value pair `mysecret=mysecretpassphrase`. Portworx will use Google Cloud KMS to encrypt the passphrase `mysecretpassphrase` and store it in its internal metadata store. To use this passphrase for encrypting volumes, you have to provide the secret ID `mysecret` while creating/attaching the volume.

#### Known issue​

note

Fixed in Portworx Enterprise version 2.10.1

- When the passphrase is over 200 bytes long, users might see the error `crypto/rsa: message too long for RSA public key size`.

### List existing secrets​

To list your secrets, run:

```

pxctl secrets gcloud list-secrets

```

## Kubernetes Secrets​

To find out how to configure Portworx with Kubernetes Secrets, see the Kubernetes Secrets page.

## Vault​

note

To install and configure Vault, see the Vault install page.

For a step-by-step guide on how you can connect your Portworx cluster to a Vault endpoint and then use the Vault endpoint to store secrets, see theVault page.

## KVDB​

You can use the `pxctl` CLI utility to store, list and retrieve KVDB secrets.

### Store a secret​

To store a secret in KVDB you can run the `pxctl secrets kvdb put-secret` command and pass it the following flags:

- `--secret_id` with the ID of the secret

- `--secret_value` with the value of the secret.

Here's an example:

```

pxctl secrets kvdb put-secret --secret_id my_secret_id secret_id --secret_value my_secret_value

```

```

Secret Put succeeded

```

### List existing secrets​

Use the following commands to list your secrets:

```

pxctl secrets kvdb list-secrets

```

```

Secret ID

my_secret_id

```

### Retrieve a secret​

You can retrieve a secret by running `pxctl secrets kvdb get-secret` with the `--secret_id` flag as follows:

```

pxctl secrets kvdb get-secret --secret_id my_secret_id

```

```

Secret: [my_secret_id]:[my_secret]

```

## IBM Key Protect​

You can use `pxctl` to list the IDs of your IBM Key Protect secrets by running the following command:

```

pxctl secrets ibm list-secrets

```

## Set a cluster-wide key​

To set an existing secret as the default cluster-wide secret for volume encryption, run the `pxctl secrets set-cluster-key` command and pass it the following flags:

- `--secret` with the secret ID of an existing secret,

- `--overwrite` to overwrite the existing cluster-wide secret. Use this command with caution because any existing volumes encrypted with the old secret will be unusable.

The following example sets `my_secret_id` as the cluster-wide secret:

```

pxctl secrets set-cluster-key --secret my_secret_id

```

## Dump and upload cluster-wide secrets​

See the dump and upload cluster-wide secrets page for details.

In this topic:
