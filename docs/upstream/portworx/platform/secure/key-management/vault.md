# Vault

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/vault (Portworx Enterprise 3.6)

Vault | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx integrates with HashiCorp Vault to store encryption keys, secrets, and credentials securely. This topic explains how to connect a Portworx cluster to a Vault development server endpoint and use Vault to manage secrets for volume encryption, as well as credentials such as vSphere credentials.

You can configure Portworx to use Vault for volume encryption while using Kubernetes Secrets for vSphere credentials, or use Vault for both volume encryption and vSphere credentials.

Updating the secrets provider

If you were using Kubernetes Secret to store vSphere credentials, make sure you do not have a secret in your cluster named `px-vsphere-secret`, and that the StorageCluster spec does not have the `VSPHERE_USER` and `VSPHERE_PASSWORD` environment variables set. Otherwise, those settings will take precedence over the Vault credential store. As a result, Portworx will not use the Vault credentials for vSphere credentials and will instead rely on the Kubernetes secret store.

To delete environment variables from the StorageCluster, run the following commands:

```

## Get the StorageCluster name

kubectl get storagecluster -n <portworx>

## Edit the StorageCluster

kubectl edit storagecluster -n <portworx> <stc_name> ## replace <stc_name> with the name of your StorageCluster

```

In the `env` section, remove the following lines:

```

env:

  - name: VSPHERE_INSECURE

    value: "true"

  - name: VSPHERE_USER

    valueFrom:

      secretKeyRef:

        name: px-vsphere-secret

        key: VSPHERE_USER

  - name: VSPHERE_PASSWORD

    valueFrom:

      secretKeyRef:

        name: px-vsphere-secret

        key: VSPHERE_PASSWORD

```

## Set up Vault​

Set up and deploy Vault by following the instructions in the Install Vault section of the Vault documentation. This includes installation, setting up policies, and configuring secrets.

note

To run a dev server, use the `vault server -dev` command. This will only run on 127.0.0.1:8200, and cannot be connected by the container. Ensure the server endpoint is securely exposed to the Portworx clusters.

## Authenticate Vault with Portworx​

### Step 1: Choose the Vault authentication method​

Authentication methods are responsible for authenticating Portworx with Vault. Based on your Vault configuration and the authentication method you choose, you must use one of the following two methods:

- Using Token authentication: A static Vault token is provided to Portworx.

- Using Kubernetes authentication: Portworx uses Kubernetes service account to fetch and refresh Vault tokens.

- Using Vault AppRole authentication: Portworx uses Vault AppRole's Role ID and Secret ID to authenticate and generate Vault Tokens.

#### Using token authentication method​

With this method, Portworx requires a Vault static token that you should provide through a Kubernetes secret. For information on the credentials, see Vault credentials reference.

Create the Kubernetes secret with the name `px-vault` in the `portworx` namespace. If `PX_SECRETS_NAMESPACE` is set, create the secret in the defined namespace. The following is an example:

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

  VAULT_BACKEND_PATH: (optional)<base64 encoded value of the custom backend path if different than the default "secret">

  VAULT_NAMESPACE: (optional)<base64 encoded value of the global vault namespace for portworx>

```

Portworx searches for this secret with name `px-vault` under the `portworx` namespace.

note

If the `VAULT_TOKEN` provided in the secret above is refreshed, then you must manually update this secret.

After configuring Vault using the Vault authentication method, proceed to Step 2.

#### Using Kubernetes authentication method​

This method allows Portworx to authenticate with Vault using a Kubernetes service account token. For more information about how to set up Kubernetes Vault authentication, see Vault documentation.

-
Create a `ServiceAccount` for Vault authentication delegation.

Run the following `kubectl create` or `oc create` commands to create a `ServiceAccount` and `ClusterRoleBinding`. Vault uses this `ServiceAccount` and its associated token to authenticate requests from Portworx. Vault uses the Kubernetes TokenReview API.

- Kubernetes

- OpenShift

```

kubectl apply -f - <<EOF

apiVersion: v1

kind: ServiceAccount

metadata:

  name: vault-auth

  namespace: portworx

secrets:

  - name: vault-auth-token

EOF

```

```

serviceaccount/vault-auth created

```

```

kubectl apply -f - <<EOF

apiVersion: v1

kind: Secret

metadata:

  name: vault-auth-token

  namespace: portworx

  annotations:

    kubernetes.io/service-account.name: vault-auth

type: kubernetes.io/service-account-token

EOF

```

```

secret/vault-auth-token created

```

```

kubectl create clusterrolebinding vault-tokenreview-binding --clusterrole=system:auth-delegator --serviceaccount=portworx:vault-auth

```

```

clusterrolebinding.rbac.authorization.k8s.io/vault-tokenreview-binding created

```

```

oc apply -f - <<EOF

apiVersion: v1

kind: ServiceAccount

metadata:

  name: vault-auth

  namespace: portworx

secrets:

  - name: vault-auth-token

EOF

```

```

serviceaccount/vault-auth created

```

```

oc apply -f - <<EOF

apiVersion: v1

kind: Secret

metadata:

  name: vault-auth-token

  namespace: portworx

  annotations:

    kubernetes.io/service-account.name: vault-auth

type: kubernetes.io/service-account-token

EOF

```

```

secret/vault-auth-token created

```

```

oc create clusterrolebinding vault-tokenreview-binding --clusterrole=system:auth-delegator --serviceaccount=portworx:vault-auth

```

```

clusterrolebinding.rbac.authorization.k8s.io/vault-tokenreview-binding created

```

-
Enable Kubernetes authentication in Vault.
Enter the following `vault auth` command to enable Kubernetes authentication in Vault:

```

vault auth enable kubernetes

```

-
Create a Kubernetes authentication configuration in Vault.
Enter the following export commands to get the JWT token and CA certificate of Kubernetes ServiceAccount:

- Kubernetes

- OpenShift

```

export SA_JWT_TOKEN=$(kubectl get secret vault-auth-token -n portworx \

  -o jsonpath="{.data.token}" | base64 --decode; echo)

export SA_CA_CRT=$(kubectl get secret vault-auth-token -n portworx \

  -o jsonpath="{.data['ca\.crt']}" | base64 --decode; echo)

```

```

  export SA_JWT_TOKEN=$(oc get secret vault-auth-token -n portworx \

    -o jsonpath="{.data.token}" | base64 --decode; echo)

  export SA_CA_CRT=$(oc get secret vault-auth-token -n portworx \

    -o jsonpath="{.data['ca\.crt']}" | base64 --decode; echo)

```

Enter the following vault write command, replacing `<kubernetes-endpoint>` with your Kubernetes API-server endpoint to write a Kubernetes authentication configuration to Vault:

```

vault write auth/kubernetes/config \

token_reviewer_jwt="$SA_JWT_TOKEN" \

kubernetes_host="<kubernetes endpoint>" \

kubernetes_ca_cert="$SA_CA_CRT" \

issuer="https://kubernetes.default.svc.cluster.local" # Optional

```

-
Create a Kubernetes authentication role for Portworx, named `portworx`, in Vault:

```

vault write auth/kubernetes/role/portworx \

  bound_service_account_names=portworx \

  bound_service_account_namespaces=<namespace> \

  policies=portworx \

  ttl=<ttl>

```

-
Provide Vault credentials to Portworx.
For information on the credentials, see Vault credentials reference.

Portworx reads the Vault credentials required to authenticate with Vault through a Kubernetes secret. Create the Kubernetes secret in the namespace where Portworx is deployed, for example `portworx` or `portworx`. If `PX_SECRETS_NAMESPACE` is set, create the secret in the defined namespace. For example:

```

apiVersion: v1

kind: Secret

metadata:

  name: px-vault

  namespace: portworx

type: Opaque

data:

  VAULT_ADDR: <base64 encoded value of the vault endpoint address>

  VAULT_BACKEND_PATH: <base64 encoded value of the custom backend path if different than the default "secret">

  VAULT_CACERT: <base64 encoded file path where the CA Certificate is present on all the nodes>

  VAULT_CAPATH: <base64 encoded file path where the Certificate Authority is present on all the nodes>

  VAULT_CLIENT_CERT: <base64 encoded file path where the Client Certificate is present on all the nodes>

  VAULT_CLIENT_KEY: <base64 encoded file path where the Client Key is present on all the nodes>

  VAULT_TLS_SERVER_NAME: <base64 encoded value of the TLS server name>

  VAULT_AUTH_METHOD: a3ViZXJuZXRlcw== # base64 encoded value of "kubernetes"

  VAULT_AUTH_KUBERNETES_ROLE: cG9ydHdvcng= # base64 encoded value of the kubernetes auth role "portworx"

  VAULT_NAMESPACE: <base64 encoded value of the global vault namespace for portworx>

```

During installation, Portworx creates a Kubernetes role binding that grants read access to Kubernetes secrets from only the defined namespace.

#### Using AppRole authentication method​

This method allows Portworx to authenticate with Vault using `AppRole` authentication. `AppRole` authentication requires a Role ID and a Secret ID. For more information about how to set up AppRole authentication, refer to the Vault AppRole documentation.
 Setup AppRole in Vault​

- Enable AppRole in Vault using the following command:

```

vault auth enable approle

```

-
Create a policy that will be used by Vault tokens. Use the policies defined in Vault security policies, and store the policy in portworx.hcl:

```

vault policy write portworx portworx.hcl

```

-
Create a role named `my-role` with the token policy `my-policies` using a command similar to the following:

```

vault write auth/approle/role/my-role \

  token_num_uses=10 \

  token_ttl=20m \

  token_max_ttl=30m  \

  token_policies=my-policy

```

`token_num_uses`, `token_ttl`, `token_max_ttl`, and `token_policies` are restrictions on how the generated token can be used to log in to Vault using AppRole.

note

There are two additional parameters, `secret_id_ttl` and `secret_id_num_uses`, that you might see in the reference. Portworx by Everpure recommends setting `secret_id_ttl` and `secret_id_num_uses` to `0`. If the Secret ID is expired, you need to update `VAULT_APPROLE_SECRET_ID` in either the Kubernetes secret or the environment variable as specified in the following section.

-
Obtain the Role ID and Secret ID of `my-role` for authentication using the following commands:

```

vault read auth/approle/role/my-role/role-id

```

```

role_id     xxxxxxxx-xxxx-xxxx-xxxx-67221c5c2f63

```

```

vault write -f auth/approle/role/my-role/secret-id

```

```

secret_id               xxxxxxxx-xxxx-xxxx-xxxx-6018fcceff64

secret_id_accessor      xxxxxxxx-xxxx-xxxx-xxxx-6ef26b7bcf86

```

 Provide Vault AppRole credentials to Portworx​
Portworx reads the Vault credentials required to authenticate with Vault through a Kubernetes secret.

Create the Kubernetes secret with the name `px-vault` in the `portworx` namespace. In the case `PX_SECRETS_NAMESPACE` is set, create the secret in the defined namespace.

```

apiVersion: v1

kind: Secret

metadata:

  name: px-vault

  namespace: portworx

type: Opaque

data:

  VAULT_ADDR: <base64 encoded value of the vault endpoint address>

  VAULT_BACKEND_PATH: <base64 encoded value of the custom backend path if different than the default "secret">

  VAULT_CACERT: <base64 encoded file path where the CA Certificate is present on all the nodes>

  VAULT_CAPATH: <base64 encoded file path where the Certificate Authority is present on all the nodes>

  VAULT_CLIENT_CERT: <base64 encoded file path where the Client Certificate is present on all the nodes>

  VAULT_CLIENT_KEY: <base64 encoded file path where the Client Key is present on all the nodes>

  VAULT_TLS_SERVER_NAME: <base64 encoded value of the TLS server name>

  VAULT_AUTH_METHOD: YXBwcm9sZQ== # base64 encoded value of "approle"

  VAULT_APPROLE_ROLE_ID: <base64 encoded value of the Role ID>

  VAULT_APPROLE_SECRET_ID: <base64 encoded value of the Secret ID>

  VAULT_NAMESPACE: <base64 encoded value of the global vault namespace for portworx>

```

For AppRole authentication, the three additional parameters are `VAULT_AUTH_METHOD`, `VAULT_APPROLE_ROLE_ID`, and `VAULT_APPROLE_SECRET_ID`.

### Step 2: Setup Vault as the secrets provider for Portworx​

#### New Installation​

To set Vault as the secrets store, follow these steps:

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
From the Default Secret Store Type dropdown menu, select Vault.

#### Existing Installation​

Edit your `StorageCluster` object, setting the value of the `specs.secretsProvider` field to `vault`.

```

spec:

  secretsProvider: vault

```

## Vault security policies​

If you configured Vault strictly with policies, then the Vault token provided to Portworx should follow one of the following policies:

```

# Read and List capabilities on mount to determine which version of kv backend is supported

path "sys/mounts/"

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

note

Portworx supports only the kv backend of Vault.

You can set all the above Vault related fields and the cluster secret key using the Portworx CLI, which is explained in the next section.

Run the following command to create a policy that by using the above policies

```

vault policy write portworx portworx.hcl

```

## Vault credentials reference​

important

The file paths specified for `VAULT_CACERT`, `VAULT_CAPATH`, `VAULT_CLIENT_CERT`, and `VAULT_CLIENT_KEY` must reside in directories accessible to the Portworx pods through HostPath volume mounts. Portworx by Everpure recommends using `/opt/pwx` or `/etc/pwx` as file paths.

Portworx requires the following Vault credentials to use its APIs:

-
Vault Address [VAULT_ADDR]

Vault server address expressed as a URL and port. For example: `https://192.168.11.11:8200`

-
Vault Token [VAULT_TOKEN]

Vault authentication token. Refer to the Vault tokens page for more information about Vault tokens. If you are using the Kubernetes authentication method of Vault, then you need not provide the actual token to Portworx.

-
Vault Backend Path [VAULT_BACKEND_PATH]

The custom backend path if different than the default `secret`

-
Vault CA Certificate [VAULT_CACERT]

Path to a PEM-encoded CA certificate file that needs to be present on all Portworx nodes. This file is used to verify the SSL certificate of Vault server. This variable takes precedence over `VAULT_CAPATH`.

-
Vault CA Path [VAULT_CAPATH]

Path to a directory of PEM-encoded CA certificate files that needs to be present on all Portworx nodes.

-
Vault Client Certificate [VAULT_CLIENT_CERT]

Path to a PEM-encoded client certificate that needs to be present on all Portworx nodes. This file is used for TLS communication with the Vault server.

-
Vault Client Key [VAULT_CLIENT_KEY]

Path to an unencrypted, PEM-encoded private key which corresponds to the matching client certificate. This key file needs to be present on all Portworx nodes.

-
Vault TLS Server Name [VAULT_TLS_SERVER_NAME]

Name to use as the SNI host when you connect using TLS.

-
Vault Auth Method [VAULT_AUTH_METHOD]

Specifies the authentication method that Portworx should use while authenticating with Vault. "Kubernetes" is the currently supported authentication method.

-
Vault Auth Kubernetes Role [VAULT_AUTH_KUBERNETES_ROLE]

Name of the Kubernetes "Auth Role" created in Vault for Portworx. This field is set only when using the Kubernetes authentication method.

-
Vault Namespace [VAULT_NAMESPACE]

Allows you to set a global Vault namespace for the Portworx cluster. All Vault requests by Portworx use this Vault namespace, if you do not provide an override.

## Using Vault with Portworx​

- Encrypt Kubernetes PVCs with Vault

- Encrypt Portworx Volumes using Vault

In this topic:
