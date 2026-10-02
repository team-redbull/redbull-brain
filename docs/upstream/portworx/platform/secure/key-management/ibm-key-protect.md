# IBM key management services

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/ibm-key-protect (Portworx Enterprise 3.6)

IBM key management services | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx integrates with IBM Key Protect and Hyper Protect Crypto Services (HPCS) to store your encryption keys/secrets and credentials. This topic explains how to configure Portworx with IBM Key Protect or HPCS. IBM Key Protect and HPCS can be used to store Portworx secrets for Volume Encryption and Cloud Credentials.

note

IBM Hyper Protect Crypto Services with Unified Key Orchestrator is not supported.

## IBM Key Protect or HPCS authentication details​

Portworx requires the following IBM Key Protect or HPCS credentials to use its APIs:

-
Service Instance ID [IBM_SERVICE_INSTANCE_ID]

The Instance ID of the IBM Key Protect or HPCS service can be found by running the following command

```

ibmcloud resource service-instance <name-of-your-service>

```

This should output something like. The ID from the below CRN is `0647c737-906d-blah-8a68-2c187e11b29b`

```

crn:v1:bluemix:public:kms:us-south:a/fb474855a3e76c1ceblahf57e0f1a9f:0647c737-906d-blah-8a68-2c187e11b29b::

```

-
Service API Key [IBM_SERVICE_API_KEY]

Follow this IBM document to retrieve the API Key.

-
Customer Root Key [IBM_CUSTOMER_ROOT_KEY]

Follow this IBM document to create a Customer Root Key

-
Base URL [IBM_BASE_URL]

The base URL specifies the URL where your Key Protect or HPCS instance resides. It is region specific.
 The default value is: `https://keyprotect.us-south.bluemix.net`.

note

- If you are using IBM HPCS, take the key management endpoint URL from the overview page of your HPCS service on IBM Cloud.

- The base URL is mandatory if Portworx is running on an IBM (IKS or ROKS) air-gapped cluster. To get the Key Protect endpoint URL for your region, refer to the IBM Key Protect documentation. For example, the IBM_BASE_URL for the `us-south` region is `https://private.us-south.kms.cloud.ibm.com`.

-
Token URL [IBM_TOKEN_URL]

Default value which will be used is: `https://iam.bluemix.net/oidc/token`.

note

The token URL is mandatory if Portworx is running on an IBM (IKS or ROKS) air-gapped cluster. To get the IAM service private endpoint URL for your region, refer to the IBM Cloud API documentation. For example, the IBM_TOKEN_URL for the `us-south` region is `https://private.us-south.iam.cloud.ibm.com/identity/token`.

## Configure IBM Key Protect or HPCS with Portworx​

This section is applicable for users running their cluster on IKS or ROKS.

### Step 1: Provide IBM key management credentials to Portworx​

Create a Kubernetes secret named `px-ibm` in the `portworx` namespace using the command below.
For more information on how Portworx is integrated with IBM Key protect, see IBM documentation.

- Kubernetes

- OpenShift

```

kubectl create secret generic -n portworx px-ibm \

--from-literal=IBM_SERVICE_API_KEY=<IBM_SERVICE_API_KEY> \

--from-literal=IBM_INSTANCE_ID=<IBM_INSTANCE_ID> \

--from-literal=IBM_CUSTOMER_ROOT_KEY=<IBM_CUSTOMER_ROOT_KEY> \

--from-literal=IBM_BASE_URL=<IBM_BASE_URL>

```

```

oc create secret generic -n portworx px-ibm \

--from-literal=IBM_SERVICE_API_KEY=<IBM_SERVICE_API_KEY> \

--from-literal=IBM_INSTANCE_ID=<IBM_INSTANCE_ID> \

--from-literal=IBM_CUSTOMER_ROOT_KEY=<IBM_CUSTOMER_ROOT_KEY> \

--from-literal=IBM_BASE_URL=<IBM_BASE_URL>

```

### Step 2: Set up IBM key management as the secret provider for Portworx.​

Depending upon your requirements, proceed to one of the following sections.

#### New installation​
 Using helm chart​
While deploying Portworx using helm chart on an IKS cluster, by default Portworx is configured to use IBM Key Protect and HPCS as a secrets provider. Follow these instructions to install the helm chart.

In a non-IKS cluster, set the `secretType` as `ibm-kp` in the helm chart's values.yml configuration file.

note

Use the `ibm-kp` `secretType` for both IBM Key Protect and HPCS.

 Using the Portworx spec generator​

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
From the Default Secret Store Type dropdown menu, select IBM Key Protect.

#### Existing installation​

To configure IBM Key Protect or HPCS as the secrets provider for an existing Portworx cluster, follow these steps:
 Step 2a: Add Permissions to access kubernetes secrets​
Portworx needs permissions to access the `px-ibm` secret created in Step 1. The following Kubernetes spec grants portworx access to all the secrets defined under the `portworx` namespace.

```

cat <<EOF | kubectl apply -f -

```

```

# Namespace to store credentials

apiVersion: v1

kind: Namespace

metadata:

  name: portworx

<!--

---

# Role to access secrets under portworx namespace only

kind: Role

apiVersion: rbac.authorization.k8s.io/v1

metadata:

  name: px-role

  namespace: portworx

rules:

- apiGroups: [""]

  resources: ["secrets"]

  verbs: ["get", "list", "create", "update", "patch"]

---

-->

# Allow portworx service account to access the secrets under the portworx namespace

kind: RoleBinding

apiVersion: rbac.authorization.k8s.io/v1

metadata:

  name: px-role-binding

  namespace: portworx

subjects:

- kind: ServiceAccount

  name: px-account

  namespace: portworx

roleRef:

  kind: Role

  name: px-role

  apiGroup: rbac.authorization.k8s.io

EOF

```

 Step 2b: Edit the Portworx spec​

-
Get the name of the StorageCluster running in your IBM cluster:

```

kubectl get storagecluster  -A

```

```

NAMESPACE     NAME           CLUSTER UUID   STATUS   VERSION   AGE

portworx   px-ocpkptest   xxxxxxxx-xxxx-xxxx-xxxx-65502f548d97  Online   2.12.1    5h49m

```

-
Run the following command to edit the above StorageCluster, then set the `secretsProvider` field of the `spec` section to `ibm-kp`:

```

kubectl edit storageCluster px-ocpkptest -n portworx

```

-
After the StorageCluster spec is edited, manually restart Portworx pods to use IBM Key Protect or HPCS.

## Using IBM key management services with Portworx​

- Encrypt Kubernetes PVCs with IBM key management services

- Encrypt Portworx Volumes using IBM Key Protect

In this topic:
