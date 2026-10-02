# Managing cloud credentials using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/credentials (Portworx Enterprise 3.6)

Managing cloud credentials using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Prerequisites​

This document provides instructions for managing your cloud credentials using `pxctl`.

The cloud provider credentials are stored in an external secret store. For more information about securing a third-party S3-compatible objectstore for use with Portworx, refer to the Certificates as Kubernetes Secrets page.

Before you use the below commands, you should configure a secret provider of your choice with Portworx. For more information, head over to the Key Management page.

## Overview​

You can use the `pxctl credentials` command to create, list, validate, or delete your cloud credentials. Then, Portworx will use these credentials, for example, to back up your volumes to the cloud.

Run the `/opt/pwx/bin/pxctl credentials` command with the `--help` flag to list the available subcommands and flags.

## List credentials​

To list all configured credentials, use this command:

```

pxctl credentials list

```

```

S3 Credentials

UUID						REGION			ENDPOINT			ACCESS KEY			SSL ENABLED	ENCRYPTION

XXXX                		us-east-1		s3.amazonaws.com    XXXX        		false		false

Azure Credentials

UUID						ACCOUNT NAME		ENCRYPTION

XXXX                		portworxtest		false

```

## Create and configure credentials​

You can create and configure credentials in multiple ways depending on your cloud provider and how you want to manage them.

### Create credentials on AWS by specifying your keys​

note

The `--s3-storage-class` flag requires Portworx Enterprise version 2.5.3 or higher

Enter the `pxctl credentials create` command, specifying:

-
The `--provider` flag with the name of the cloud provider (`s3`).

-
The `--s3-access-key` flag with your secret access key.

-
The `--s3-secret-key` flag with your access key ID.

-
The `--s3-region` flag with the name of the S3 region (`us-east-1`).

-
The `--s3-endpoint` flag with the name of the endpoint (`s3.amazonaws.com`).

-
(Optional) The `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer.

-
(Optional) The `--bucket` flag with the name of the bucket.

-
The name of your cloud credentials.

```

pxctl credentials create \

  --provider s3 \

  --s3-access-key <YOUR-SECRET-ACCESS-KEY>

  --s3-secret-key <YOUR-ACCESS-KEY-ID> \

  --s3-region us-east-1 \

  --s3-endpoint s3.amazonaws.com \

  --s3-storage-class STANDARD \

  --bucket <BUCKET-NAME> \

    <NAME>

```

```

Credentials created successfully

```

note

If you have not specified the bucket name, this command will create a bucket with the Portworx cluster UUID to use for the backups.

### Create credential on AWS with s3 encryption​

You can configure AWS s3 credentials to use server-side encryption, assuming the s3 object-store provider supports it.

Enter the `pxctl credentials create` command, specifying:

-
The `--provider` flag with the name of the cloud provider (`s3`).

-
The `--s3-access-key` flag with your secret access key

-
The `--s3-secret-key` flag with your access key ID

-
The `--s3-region` flag with the name of the S3 region (`us-east-1`)

-
The `--s3-endpoint` flag with the name of the endpoint (`s3.amazonaws.com`)

-
The optional `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer

-
The optional `--s3-sse` flag with `AES256` or `aws:kms`, depending on how you want to do the server side encryption. If using `aws:kms`, see the AWS s3 documentation.

-
The name of your cloud credentials

```

pxctl credentials create \

  --provider s3 \

  --s3-access-key <YOUR-SECRET-ACCESS-KEY>

  --s3-secret-key <YOUR-ACCESS-KEY-ID> \

  --s3-region us-east-1 \

  --s3-endpoint s3.amazonaws.com \

  --s3-sse AES256 \

    <NAME>

```

```

Credentials created successfully

```

### Create credentials on AWS using IAM​

note

This feature requires Portworx Enterprise version 2.5.1 or greater

Instead of storing your secret access key and access key ID on the host, you can grant Portworx bucket permissions using IAM. You can grant the EC2 instances on which Portworx is running, or you can grant permissions for a specific bucket.

#### Grant IAM permissions for your EC2 instance in general​

-
In AWS, grant IAM permissions for an EC2 instance with no bucket:

```

{

    "Version": "2012-10-17",

    "Statement": [

        {

            "Sid": "VisualEditor0",

            "Effect": "Allow",

            "Action": [

                "s3:PutObject",

                "s3:GetObject",

                "s3:ListAllMyBuckets",

                "s3:CreateBucket",

                "s3:ListBucket",

                "s3:DeleteObject",

                "s3:GetBucketLocation"

            ],

            "Resource": "*"

        }

    ]

}

```

-
Enter the following pxctl credentials create command, specifying the following:

- The `--provider` flag with the name of the cloud provider (`s3`).

- The `--s3-region` flag with the S3 region associated with your account

- The optional `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer

- The `use-iam` flag

- The name of your cloud credentials

```

./pxctl credentials create \

--provider s3 \

--s3-region us-east-1 \

--s3-storage-class STANDARD \

--use-iam \

<NAME>

```

```

Credentials created successfully, UUID:xxxxxxxx-xxxx-xxxx-xxxx-7890ef1d23ab

```

#### Grant IAM permissions for a specific bucket​

-
In AWS, grant IAM permissions for a specific bucket:

```

{

    "Version": "2012-10-17",

    "Statement": [

        {

            "Sid": "VisualEditor0",

            "Effect": "Allow",

            "Action": [

                "s3:ListAllMyBuckets",

                "s3:GetBucketLocation"

            ],

            "Resource": "*"

        },

        {

            "Sid": "VisualEditor1",

            "Effect": "Allow",

            "Action": "s3:*",

            "Resource": [

                "arn:aws:s3:::<bucket-name>",

                "arn:aws:s3:::<bucket-name>/*"

            ]

        }

    ]

}

```

-
Enter the following pxctl credentials create command, specifying the following:

- The `--provider` flag with the name of the cloud provider (`s3`)

- The `--s3-region` flag with your bucket's s3 region

- The optional `--s3-storage-class` flag with either the `STANDARD` or `STANDARD-IA` value, depending on which storage class you prefer

- The `--bucket` flag with your bucket's name

- The `use-iam` flag

- The name of your cloud credentials

```

./pxctl credentials create \

--provider s3 \

--s3-region <region> \

--s3-storage-class STANDARD \

--bucket <bucket-name> \

--use-iam \

<NAME>

```

```

Credentials created successfully, UUID:xxxxxxxx-xxxx-xxxx-xxxx-7890ef1d23ab

```

### Create credentials on Google by specifying the credential file​

note

This feature requires Portworx Enterprise version 2.10.1 or greater

-
Specify the following:

- The `--provider` flag with the name of the cloud provider (`google`)

- The `--google-project-id` flag with the relevant google project ID

- the `--google-json-key-file` flag with the path to the credentials

- The `--bucket` flag with your bucket's name

```

./pxctl credentials create \

--provider google \

--google-project-id <project-id> \

--google-json-key-file /path/to/gcloud.json \

--bucket <bucket-name> \

<NAME>

```

```

Credentials created successfully, UUID:xxxxxxxx-xxxx-xxxx-xxxx-7890ef1d23ab

```

### Create credentials using workload identity​

If you installed Portworx Enterprise on a cloud provider using workload identity authentication, you can create cloud credentials for CloudSnap backup and restore operations by using `pxctl`.

Instead of supplying access keys or relying on node-level IAM, this method uses workload identity for authentication. Portworx exchanges a projected service account token for short-lived cloud credentials at runtime, so no long-lived secrets are stored.

note

Before you create credentials, ensure that workload identity is configured on your cluster as described in Configure workload identity.
On AWS and Azure, the `StorageCluster` must include the `spec.workloadIdentity.credentials` block, and the corresponding webhook (`eks-pod-identity-webhook` on AWS or `azure-workload-identity` on Azure) must be running on the cluster. On Google Cloud, the `StorageCluster` must include the `spec.workloadIdentity.gcp.credentialsConfigMap` field that references the credential ConfigMap.

- AWS

- Azure

- GCP

note

This feature requires Portworx Enterprise version 3.4.0 or later, and Portworx Operator version 25.3.1 or later.

Run the following command:

```

pxctl credentials create <cred-name> \

  --provider <provider-name> \

  --use-workload-identity

```

```

Credentials created successfully

```

Replace:

- `<cred-name>` with the name of your cloud credentials.

- `<provider-name>` with the name of your cloud provider.

You can use this credential to create cloud snapshots. For more information, see Create and use cloud snapshots.

note

The `--s3-disable-ssl` flag is not supported with workload identity for AWS endpoints, because it enforces SSL.

note

This feature requires Portworx Enterprise version 3.6.1 or later, and Portworx Operator version 26.2.0 or later.

Run the following command:

```

pxctl cred create <cred-name> \

  --provider <provider-name> \

  --azure-account-name <storage-account-name> \

  --use-workload-identity

```

```

Credentials created successfully

```

Replace:

- `<cred-name>` with the name of your cloud credentials.

- `<provider-name>` with the name of your cloud provider.

- `<storage-account-name>` with the name of your Azure Storage account.

You can use this credential to create cloud snapshots. For more information, see Create and use cloud snapshots.

important

The managed identity used for installing Portworx must have permissions to upload and download blob data from the Azure Storage account that you specify in the credential.

note

This feature requires Portworx Enterprise version 3.6.2 or later, and Portworx Operator version 26.3.0 or later.

Run the following command:

```

pxctl cred create <cred-name> \

  --provider <provider-name> \

  --google-project-id <gcp-project-id> \

  --use-workload-identity

```

```

Credentials created successfully

```

Replace:

- `<cred-name>` with the name of your cloud credentials.

- `<provider-name>` with the name of your cloud provider.

- `<gcp-project-id>` with your GCP project ID.

You can use this credential to create cloud snapshots. For more information, see Create and use cloud snapshots.

important

The Google Cloud service account used for installing Portworx must have the `roles/storage.objectAdmin` role on the Google Cloud Storage bucket that you specify in the credential.

## Delete existing credentials​

To delete a particular set of credentials, you can run `pxctl credentials delete` with the `uuid` or the `name` as parameters like this:

```

pxctl credentials delete <uuid or name>

```

```

Credential deleted successfully

```

note

Don't forget to replace `<uuid or name>` with the actual `uuid` or `name` of the credentials you want to delete.

## Validate credentials​

If you want to validate a set of credentials for a particular cloud provider, run the following:

```

pxctl credentials validate <uuid or name>

```

```

Credential validated successfully

```

note

Don't forget to replace `<uuid or name>` with the actual `uuid` or `name` of the credentials you want to delete.

## Delete pending credential references from the KVDB​

Requests to delete cloudsnaps are long-running operations, and are executed asynchronously in the background. Portworx stores these requests in the KVDB so that it can resume delete operations if the node restarts or is otherwise interrupted. Portworx periodically retires these delete requests as part of a cleanup routine.

If the credentials for these cloudsnaps are configured through Kubernetes secrets, the credential object must be available at the time Portworx attempts to delete it. If the credential object is deleted while the cloudsnap delete requests are pending, these delete requests will fail and continue to remain in the KVDB where they will continue to log alerts about the failure to delete.

If this happens in your cluster, you can use the `pxctl credentials delete-refs` command to delete these pending references to credentials from the KVDB:

```

pxctl credentials delete-refs <name-or-UUID>

```

## Using --ca and --cert Flags vs. embedding certificates in volume mounts​

The `--ca` (Certificate Authority) and `--cert` (Certificate) flags provide a way to specify SSL/TLS certificates directly through the CLI when managing Portworx credentials. This method is particularly useful for temporary or dynamic configurations where certificates need to be supplied on-the-fly.

### Advantages of --ca and --cert flags​

- Allows quick updates and changes to the certificate settings without needing to modify volume configurations.

- Easier to script and automate credential updates within deployment pipelines or scripts.

Example:

```

pxctl credentials create \

--provider s3 \

--s3-endpoint s3.amazonaws.com \

--s3-access-key <your-access-key> \

--s3-secret-key <your-secret-key> \

--ca <path-to-ca.crt> \

--cert <path-to-client.crt>

```

On the other hand, embedding certificates in a volume mount is recommended for more static and secure configurations where certificates are managed as part of the Kubernetes secrets and configurations. This approach ensures that the certificates are consistently available and managed by Kubernetes, making it suitable for production environments where security and persistence are critical.

### Advantages of embedding certificates in volume mounts​

- Certificates are managed by Kubernetes and remain consistent across restarts and redeployments.

- Kubernetes secrets management ensures that certificates are securely stored and handled.

- Integrates well with Kubernetes management and deployment strategies, providing a more automated and robust solution.

For example, you can create a Kubernetes secret and mount it as a volume in your Portworx deployment:

```

apiVersion: v1

kind: Secret

metadata:

  name: portworx-certificates

type: Opaque

data:

  ca.crt: <base64-encoded-ca-crt>

  client.crt: <base64-encoded-client-crt>

---

apiVersion: apps/v1

kind: Deployment

metadata:

  name: portworx

spec:

  containers:

    - name: portworx

      volumeMounts:

        - name: certs

          mountPath: /etc/pwx/certs

  volumes:

    - name: certs

      secret:

        secretName: portworx-certificates

```

### Key differences​

- Configuration location: `--ca` and `--cert` flags configure certificates directly via CLI, while volume mounts embed certificates in the container filesystem managed by Kubernetes.

- Use case: `--ca` and `--cert` flags are suited for dynamic, temporary use cases, while volume mounts are suited for stable, persistent production environments.

## Related topics​

- For information about integrating Portworx with Kubernetes Secrets, refer to the Kubernetes Secrets page.

In this topic:
