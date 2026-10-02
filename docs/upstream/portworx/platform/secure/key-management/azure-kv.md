# Azure Key Vault

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/azure-kv (Portworx Enterprise latest)

Azure Key Vault | Portworx Enterprise Documentation

Portworx can integrate with Azure Key Vault Secrets to store your encryption secrets, credentials or passwords. This topic explains how to deploy a Portworx cluster that connects to an Azure Key Vault. The Azure Key Vault could be used to store secrets used for encrypting volumes.

## Setting up Azure Key Vault​

Peruse Create a key vault using the Azure portal official docs for help on setting up Azure Key Vault in your setup.

Once, the Azure Key Vault is setup you will also require to register and authenticate the application which will allow application to perform operations and permission on Azure Key Vault.

## Register Azure application in Azure AD​

Follow Registering an application with Microsoft Entra ID doc for help on registering application with azure active directory. There are multiple ways to do it, azure cli to directly from the portal.

For example, you can register application using following command.

note

Make you have az cli installed and have access to Azure.

```

az ad sp create-for-rbac -n "<you_application_name>" --role Contributor --scopes /subscriptions/<subscription id>

# If you don't specify a password, one will be created for you.

```

```

Creating 'Contributor' role assignment under scope '/subscriptions/<subscription id>'

The output includes credentials that you must protect. Be sure that you do not include these credentials in your code or check the credentials into your source control. For more information, see https://aka.ms/azadsp-cli

{

  "appId": "xxxxxxxx-63xx-4axx-86xx-xxxd9ad33xxx",

  "displayName": "<you_application_name>",

  "password": "_5j8Q~-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxdhY",

  "tenant": "xxxxxxxx-f4b7-xxxx-bexx-773895b9xxxx"

}

```

## Granting permission to the Azure application​

Portworx will need application that has Azure Key Vault `set/get/list/delete` secrets permissions.

Please follow Authorizing an application to use a key or secret doc for help on granting Azure Key Vault permission to your registered app.

For example

```

az keyvault set-policy --name "<policy_name>" --spn <registered app ID> --key-permissions set get list delete

```

## Authentication details for Portworx​

Following are the authentication details required by Portworx to connect Azure Key Vault -

- `AZURE_VAULT_URL`: Azure Key Vault URL

- `AZURE_TENANT_ID`: Azure Active Directory ID

- `AZURE_CLIENT_ID`: Azure application ID which is registered with Azure active directory and has access to azure key vault mentioned in `AZURE_VAULT_URL`

- `AZURE_CLIENT_SECRET`: Azure application secret id, you may need to generate one if not created already. Follow doc to generate new secret key for your application

- `AZURE_ENVIRONMENT`(optional): Azure environment or az cloud list. Default cloud name is `AzurePublicCloud`.

note

You can retrieve the value of the `AZURE_ENVIRONMENT` variable by entering the following command:

```

az account show | jq '.environmentName'

```

## Authenticate Portworx with Azure Key Vault​

To authenticate Portworx using Azure Key Vault environment variables, follow these steps:

-
Sign in to the Portworx Central console.
The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
The system displays the Generate Portworx Enterprise Spec page.

-
From the Portworx Version dropdown menu, select the Portworx version to install.

-
From the Platform dropdown menu, select Azure.

-
From the Distribution Name dropdown menu, select the distribution.

-
Click Customize.

-
Complete the required configuration in the Basic, Storage, Network, and Deployment tabs.

-
In the Deployment tab, under the Environment Variables section, enter all the Azure environment variables mentioned in Authentication details for Portworx.

-
From the Default Secret Store Type dropdown menu, select Azure Key Vault.

## Setting cluster wide secret key​

A cluster wide secret key is a common key that can be used to encrypt all your volumes. You can set the cluster secret key using the following command.

```

/opt/pwx/bin/pxctl secrets set-cluster-key --secret <cluster-wide-secret-key>

```

This command needs to be run just once for the cluster. If you have added the cluster secret key through the config.json, the above command will overwrite it. Even on subsequent Portworx restarts, the cluster secret key in config.json will be ignored for the one set through the CLI.

important

Make sure that the secret key has been created in Azure Key Vault Secrets.

In this topic:
