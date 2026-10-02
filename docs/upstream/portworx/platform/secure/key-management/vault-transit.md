# Vault Transit

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/vault-transit (Portworx Enterprise 3.6)

Vault Transit | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx can be integrated with Vault Transit to encrypt volumes. This topic explains how to connect a Portworx cluster to a Vault development server and enable Vault Transit, which can be used to store secrets for encrypting volumes.

Vault Transit manages key generation for in-transit data encryption. With Vault Transit, you do not need to set a cluster wide secret to encrypt volumes and PVCs. By default, Portworx uses generated keys from Vault Transit as passphrase for volume encryption.

## Prerequisites​

- Vault is installed

## Configure Vault Transit environment​

- Run the following command to enable the Transit secrets engine:

```

vault secrets enable transit

```

- If you configured Vault strictly with policies, then the Vault Transit token provided to Portworx should follow the following policies:

```

# Enable transit secrets engine

path "sys/mounts/transit" {

  capabilities = [ "create", "read", "update", "delete", "list" ]

}

# To read enabled secrets engines

path "sys/mounts" {

  capabilities = [ "read" ]

}

# Manage the transit secrets engine

path "transit/*" {

  capabilities = [ "create", "read", "update", "delete", "list" ]

}

# Read and List capabilities on mount to determine which version of kv backend is supported

path "sys/mounts/*"

{

capabilities = ["read", "list"]

}

# V1 backends (Using default backend)

# Provide full access to the portworx subkey

path "secret/*"

{

capabilities = ["create", "read", "update", "delete", "list"]

}

# V1 backends (Using custom backend)

# Provide full access to the portworx subkey

# Provide -> VAULT_BACKEND_PATH=custom-backend (required)

path "custom-backend/*"

{

capabilities = ["create", "read", "update", "delete", "list"]

}

# V2 backends (Using default backend )

# Provide full access to the data/portworx subkey

path "secret/data/*"

{

capabilities = ["create", "read", "update", "delete", "list"]

}

# V2 backends (Using custom backend )

# Provide full access to the data/portworx subkey

# Provide -> VAULT_BACKEND_PATH=custom-backend (required)

path "custom-backend/data/*"

{

capabilities = ["create", "read", "update", "delete", "list"]

}

```

## Set the Vault Transit secrets engine for Portworx​

Depending on whether you are performing a fresh install or modifying an existing installation, proceed to one of the following sections.

### New Installation​

To set Vault Transit as the secrets store, follow these steps:

-
Sign in to the Portworx Central console.
The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
The system displays the Generate Portworx Enterprise Spec page.

-
From the Portworx Version dropdown menu, select the Portworx version to install.

-
From the Platform dropdown menu, select the platform.

-
From the Distribution Name dropdown menu, select the distribution.

-
Click Customize.

-
Complete the required configuration in the Basic, Storage, Network, and Deployment tabs.

-
From the Default Secret Store Type dropdown menu, select Vault Transit.

### Existing Installation​

Edit the `StorageCluster` object by setting the value of the `specs.secretsProvider` field to `vault-transit`.

```

spec:

  secretsProvider: vault-transit

```

Editing Operator spec will restart all Portworx pods.

### Authenticate Portworx​

See Authenticate Vault with Portworx to authenticate Portworx with Vault Transit.

#### (Optional) Customize the key path​

Vault Transit generates the keys by writing to a `transit` key path. For example:

```

$ vault write -f transit/keys/my-key

Success! Data written to: transit/keys/my-key

```

By default, Portworx uses the transit key path `pwx-encryption-key` (full path: `transit/keys/pwx-encryption-key`) for key generation. To use a custom Vault Transit key path, provide the base64-encoded value in the `px-vault` Secret under the `VAULT_ENCRYPTION_KEY` field.

```

apiVersion: v1

kind: Secret

metadata:

  name: px-vault

  namespace: portworx

type: Opaque

data:

  VAULT_ADDR: (required)<base64 encoded value of the vault endpoint address>

  VAULT_TOKEN: (required)<base64 encoded value of the vault token>

  VAULT_CACERT: (recommended)<base64 encoded file path where the CA Certificate is present on all the nodes>

  VAULT_CAPATH: (recommended)<base64 encoded file path where the Certificate Authority is present on all the nodes>

  VAULT_CLIENT_CERT: (recommended)<base64 encoded file path where the Client Certificate is present on all the nodes>

  VAULT_CLIENT_KEY: (recommended)<base64 encoded file path where the Client Key is present on all the nodes>

  VAULT_TLS_SERVER_NAME: (recommended)<base64 encoded value of the TLS server name>

  VAULT_ENCRYPTION_KEY: (optional)<base64 encoded value of the transit key path for portworx>

  VAULT_NAMESPACE: (optional)<base64 encoded value of the global vault namespace for portworx>

```

note

-
If your authentication method uses TLS certificates or keys such as `VAULT_CACERT`, `VAULT_CAPATH`, `VAULT_CLIENT_CERT`, `VAULT_CLIENT_KEY`, ensure that these files reside in directories accessible to the Portworx pod through HostPath volume mounts. Portworx by Everpure recommends using `/opt/pwx` or `/etc/pwx` as file paths.

-
Portworx by Everpure does not recommend changing the value of `VAULT_ENCRYPTION_KEY` once deployed as the previous secret keys and volumes might be inoperative if the key path is changed.

## Use Vault Transit with Portworx​

- Encrypt Kubernetes PVCs with Vault Transit

- Encrypt Portworx Volumes using Vault Transit

In this topic:
