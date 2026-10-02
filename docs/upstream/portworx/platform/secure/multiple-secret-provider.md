# Configure Multiple Secrets Providers

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/multiple-secret-provider (Portworx Enterprise 3.6)

Configure Multiple Secrets Providers | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise supports configuring multiple secrets providers in a single deployment, allowing you to select a different secrets store for each feature. You can assign a secrets provider per feature, such as using Kubernetes Secrets for volume encryption and Vault for storing cloud provider credentials like vSphere or FlashArray access tokens. This enables finer-grained control over how and where sensitive data is stored.

Portworx Enterprise lets you configure secrets providers independently for the following features:

- Cloud provider credentials: Used to store cloud provider credentials like vSphere credentials or FlashArray access tokens.

- Volume encryption: Used to store and manage encryption keys for encrypted volumes.

- Cloudsnap encryption: Used to store the credentials required for authenticating to the mentioned cloud provider.

For each feature, select one of the following supported secret providers based on your security and operational requirements, and see the corresponding documentation for instructions on setting up each secret provider:

- AWS KMS

- Azure Key Vault

- Google Cloud KMS

- IBM key management services

- Kubernetes Secrets

- HashiCorp Vault

- HashiCorp Vault Transit

## Prerequisites​

Ensure that your cluster meets the following prerequisites before you configure multiple secrets providers:

- Portworx Enterprise version 3.6.0 or later is installed.

- Operator version 26.1.0 or later is installed.

## Procedure​

You can configure multiple secrets providers in your Portworx cluster using either Portworx Central or the StorageCluster custom resource.

### Using Portworx Central​

To configure multiple secrets providers using Portworx Central, follow these steps:

-
Sign in to the Portworx Central console.
The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
The system displays the Generate Portworx Enterprise Spec page.

-
From the Portworx Version dropdown menu, select the Portworx Enterprise version to install.

-
From the Platform dropdown menu, select Pure FlashArray or vSphere.

-
From the Distribution Name dropdown menu, select the distribution.

-
Click Customize.

-
Complete the required configuration in the Basic, Storage, Network, and Deployment tabs.

-
In the Deployment tab, enable the Configure Secrets Store Type per Feature toggle.
The system displays the secrets store type dropdown menu for cloud provider credentials, volume encryption, and cloudsnap.

-
From the Secrets store type for Cloud Provider Credentials dropdown menu, select the secrets store to securely store cloud provider credentials.

important

-
If you select the secrets store for cloud provider credentials from the Secrets store type for Cloud Provider Credentials dropdown menu, Portworx Enterprise uses the selected secrets store type for cloud provider credentials, regardless of the Default Secret Store Type selected.

-
If you do not select the secrets store for cloud provider credentials from the Secrets store type for Cloud Provider Credentials dropdown menu, Portworx Enterprise uses Default Secret Store Type for cloud provider credentials.

- If the Default Secret Store Type is set to Kubernetes, Portworx Enterprise uses Kubernetes Secrets for cloud credentials.

- If the Default Secret Store Type is set to Vault, Portworx Enterprise first checks Kubernetes Secrets. If the credential is not found, it then checks Vault and uses Vault for cloud credentials.

- If the Default Secret Store Type is set to any other provider (such as AWS KMS), Portworx Enterprise still defaults to Kubernetes Secrets for cloud credentials.
If the credential is missing in Kubernetes and the Default Secret Store Type is not Vault, the operation fails without checking any other secret store type.

-
From the Secrets store type for Volume Encryption dropdown menu, select the secrets store to store encryption keys and related metadata for encrypted Portworx volumes.

Updating the secrets provider

If you change the secret store type for volume encryption from one secrets provider to another (for example, from Kubernetes Secrets to Vault), Portworx Enterprise does not automatically migrate secrets. You must manually create the required secrets in the target provider before making the configuration change.

For example, if a Kubernetes secret has the name `<your-secret-name>` and the key `<your-secret-key>` with the value `<your-secret-passcode>`, create a Vault secret with the same name and key before transitioning to Vault as the secrets provider.

The following example shows how to create a Kubernetes secret when using the Kubernetes secrets provider:

```

kubectl create secret generic <your-secret-name> -n portworx --from-literal=your-secret-key=<your-secret-passcode>

```

Create a Vault secret with the same name and key, as shown in the example below. Here, `<customPath>` is a custom backend path provided in the `px-vault` secret see Vault credentials reference for more information:

```

vault kv put <customPath>/<your-secret-name> <your-secret-key>=<your-secret-passcode>

```

-
From the Secrets store type for Cloud Snap dropdown menu, select the secrets store to store credentials and configuration required for CloudSnap operations.

-
Click Finish.

-
In the summary page, enter a name for the specification in the Spec Name field, and tags in the Spec Tags field.

-
Click Download .yaml to download the yaml file with the customized specification or Save Spec to save the specification.

### Using the StorageCluster custom resource​

To manually configure multiple secrets providers by editing the StorageCluster custom resource, follow these steps:

-
Locate your StorageCluster:

```

kubectl get storageclusters -A

```

-
Edit the StorageCluster in the appropriate namespace:

```

kubectl edit storagecluster <storage-cluster-name> -n <namespace>

```

For example, if your cluster is named `px-cluster` and deployed in the `portworx` namespace:

```

kubectl edit storagecluster px-cluster -n portworx

```

-
In the spec section of the StorageCluster resource, add the multiple secrets providers configuration:

```

apiVersion: core.libopenstorage.org/v1

metadata:

  name: px-cluster

  namespace: portworx

  spec:

   secretsProvider: k8s          # existing default

   secretProviderPerFeature:     # new (optional)

        cloudProviderCred: vault

        volumeEncryption: k8s

        cloudSnap: vault

```

important

-
If you do not configure a secrets store for cloud provider credentials in `cloudProviderCred`, Portworx Enterprise uses `secretsprovider` as secrets store for cloud provider credentials.

-
If `secretsprovider` is `k8s`, Portworx Enterprise uses Kubernetes Secrets.

-
If `secretsprovider` is `vault`, Portworx Enterprise first checks Kubernetes Secrets. If the credential is not found, it then checks Vault and uses Vault for cloud credentials.

-
If `secretsprovider` is any other provider (such as AWS KMS), Portworx Enterprise still defaults to Kubernetes Secrets for cloud provider credentials.
If the credential is missing in Kubernetes and `secretsprovider` is not `vault`, the operation fails without checking any other secret store type.

-
If you configure a secrets store for cloud provider credentials in `cloudProviderCred`, Portworx Enterprise uses that secrets store type for cloud provider credentials, regardless of the `secretsprovider` configured.

-
If you change the secret store type for volume encryption from one secrets provider to another (for example, from Kubernetes Secrets to Vault), Portworx Enterprise does not automatically migrate secrets. You must manually create the required secrets in the target provider before making the configuration change.

For example, if a Kubernetes secret has the name `<your-secret-name>` and the key `<your-secret-key>` with the value `<your-secret-passcode>`, create a Vault secret with the same name and key before transitioning to Vault as the secrets provider.

The following example shows how to create a Kubernetes secret when using the Kubernetes secrets provider:

```

kubectl create secret generic <your-secret-name> -n portworx --from-literal=your-secret-key=<your-secret-passcode>

```

Create a Vault secret with the same name and key, as shown in the example below. Here, `<customPath>` is a custom backend path provided in the `px-vault` secret see Vault credentials reference for more information:

```

vault kv put <customPath>/<your-secret-name> <your-secret-key>=<your-secret-passcode>

```

-
Verify the configuration to confirm that multiple secrets providers is configured:

```

kubectl get storagecluster <storage-cluster-name> -n <namespace> -o yaml | grep -A 3 secretProviderPerFeature

```

You should see output similar to:

```

secretProviderPerFeature:

    cloudProviderCred: vault

    cloudSnap: vault

    volumeEncryption: k8s

```

In this topic:
