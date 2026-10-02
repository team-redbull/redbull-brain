# Google Cloud KMS

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/key-management/gcloud-kms (Portworx Enterprise latest)

Google Cloud KMS | Portworx Enterprise Documentation

Portworx integrates with Google Cloud KMS to store your Portworx secrets for Volume Encryption and Cloud Credentials. This topic explains how to configure a Portworx cluster with Google Cloud KMS.

## Google Cloud KMS authentication details​

Portworx requires the following Google Cloud credentials to use its APIs:

-
Google Application Credentials [GOOGLE_APPLICATION_CREDENTIALS]

Portworx requires permissions to use Google CloudKMS APIs. It requires the following predefined roles:

- roles/cloudkms.cryptoKeyEncrypterDecrypter

- roles/cloudkms.publicKeyViewer

For more information about these roles and permissions, see Google Cloud documentation.

-
Google KMS Public Key Resource ID [GOOGLE_KMS_RESOURCE_ID]

Portworx uses Google Cloud KMS asymmetric key pairs to encrypt and decrypt secrets. When creating the asymmetric key, set the purpose to Asymmetric decrypt. After creating the key, provide the full resource ID of the asymmetric key version to Portworx.
A typical asymmetric key resource ID has the following format:

```

projects/<Project ID>/locations/<Region>/keyRings/<Key Ring Name>/cryptoKeys/<Asymmetric Key Name>/cryptoKeyVersions/1

```

Portworx requires the above resource ID as an input argument.

For more information about asymmetric key pairs and how to create them, see the Google Cloud KMS documentation.

## Configure Google Cloud KMS with Portworx​

Provide the Google credentials to Portworx by using any one of these methods:

### Google instance IAM roles (Recommended)​

Grant the instances running Portworx the required permissions to access the Google Cloud API server. This is the preferred authentication method because it requires minimal configuration on each instance.

- Owner and Compute Admin Roles, or a Custom Role:

- Create a Custom Google IAM Role:
 If you prefer to grant Portworx only the minimal necessary access, create a custom IAM role that includes the required compute permissions. This role will enable Portworx to create, attach, and manage disks on VM instances.

- Create a `portworx-role.yaml` file with the following minimum permissions:

```

title: "Portworx Role"

description: "Portworx role for managed disks"

stage: "GA"

includedPermissions:

- compute.disks.addResourcePolicies

- compute.disks.create

- compute.disks.createSnapshot

- compute.disks.delete

- compute.disks.get

- compute.disks.getIamPolicy

- compute.disks.list

- compute.disks.removeResourcePolicies

- compute.disks.resize

- compute.disks.setIamPolicy

- compute.disks.setLabels

- compute.disks.update

- compute.disks.use

- compute.disks.useReadOnly

- compute.instances.attachDisk

- compute.instances.detachDisk

- compute.instances.get

- compute.nodeGroups.get

- compute.nodeGroups.getIamPolicy

- compute.nodeGroups.list

- compute.zoneOperations.get

- container.clusters.get

```

- Use the `portworx-role.yaml` file to create your custom role for Portworx:

```

gcloud iam roles create portworx_role --project=<your-gcp-project> \

--file=portworx-role.yaml

```

 Once you have created the custom IAM role, you need to assign that role to the GKE cluster nodes.

- Owner and Compute Admin Roles:
 These roles grant Portworx access to the Google Cloud Storage APIs for provisioning persistent disks. Ensure that the service account for the instances has these roles assigned.

- Cloud KMS Predefined Roles:
 The following predefined roles provide Portworx access to the Google Cloud KMS APIs for managing secrets:

```

roles/cloudkms.cryptoKeyEncrypterDecrypter

roles/cloudkms.publicKeyViewer

```

### Google Service Accounts​

#### Step 1: Create a service account​

Alternatively, you can give Portworx access to the GCP API server via a service account file and environment variables. Start by creating a service account in GCP and downloading its account file.

To access the GCP API server, Portworx requires a service account with the following roles:

- Owner and Compute Admin Roles, or a Custom Role:

- Create a Custom Google IAM Role:
 If you prefer to grant the service account only the minimal necessary access, create a custom IAM role that includes the required compute permissions. This role will enable Portworx to create, attach, and manage disks on VM instances.

- Create a `portworx-role.yaml` file with the following minimum permissions:

```

title: "Portworx Role"

description: "Portworx role for managed disks"

stage: "GA"

includedPermissions:

- compute.disks.addResourcePolicies

- compute.disks.create

- compute.disks.createSnapshot

- compute.disks.delete

- compute.disks.get

- compute.disks.getIamPolicy

- compute.disks.list

- compute.disks.removeResourcePolicies

- compute.disks.resize

- compute.disks.setIamPolicy

- compute.disks.setLabels

- compute.disks.update

- compute.disks.use

- compute.disks.useReadOnly

- compute.instances.attachDisk

- compute.instances.detachDisk

- compute.instances.get

- compute.nodeGroups.get

- compute.nodeGroups.getIamPolicy

- compute.nodeGroups.list

- compute.zoneOperations.get

- container.clusters.get

```

- Use the `portworx-role.yaml` file to create your custom role:

```

gcloud iam roles create portworx_role --project=<your-gcp-project> \

--file=portworx-role.yaml

```

 After creating the custom IAM role, bind it to the service account that will manage GCP disks.

- Owner and Compute Admin Roles:
 These roles grant access to the Google Cloud Storage APIs for provisioning persistent disks. Ensure that the service account has these roles assigned.

- Cloud KMS Predefined Roles:
 The following predefined roles provide access to the Google Cloud KMS APIs for managing secrets:

```

roles/cloudkms.cryptoKeyEncrypterDecrypter

roles/cloudkms.publicKeyViewer

```

Follow these steps to create a service account and download its corresponding account file:

- Create a service account in the "Service Account" section that has the above permissions.

- Go to IAM & admin -> Service Accounts -> (Instance Service Account) -> Select "Create Key" and download the `.json` file.

#### Step 2: Create a Kubernetes secret for the Google credentials.​

Copy the downloaded account file in a directory `gcloud-secrets/` and rename it `gcloud.json` to create a Kubernetes secret from it.

```

ls -1 gcloud-secrets

```

```

gcloud.json

```

Create a kubernetes secret with the following command

```

 kubectl -n kube-system create secret generic px-gcloud --from-file=gcloud-secrets/ --from-literal=gcloud-kms-resource-id=projects/<Project ID>/locations/<Region>/keyRings/<Key Ring Name>/cryptoKeys/<Asymmetric Key Name>/cryptoKeyVersions/1

```

Make sure to replace the `Project ID`, `Key Ring Name` and `Asymmetric Key Name` in the above command.

#### Step 3: Update the Portworx DaemonSet​

-
New installation

To update the Portworx DaemonSet, follow these steps:

-
Sign in to the Portworx Central console.
The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
The system displays the Generate Portworx Enterprise Spec page.

-
From the Portworx Version dropdown menu, select the Portworx version to install.

-
From the Platform dropdown menu, select Google Cloud.

-
From the Distribution Name dropdown menu, select the distribution.

-
Click Customize.

-
Complete the required configuration in the Basic, Storage, Network, and Deployment tabs.

-
From the Default Secret Store Type dropdown menu, select Google Cloud KMS.

-
Existing installation

For an existing Portworx cluster follow these steps:

 Step 3a: Update the Portworx DaemonSet to use the Google KMS secret store​
Edit the Portworx DaemonSet's `secret_type` field to `gcloud-kms`, so that all the new Portworx nodes will also start using Google Cloud KMS.

```

kubectl edit daemonset portworx -n kube-system

```

Add the `"-secret_type", "gcloud-kms"` arguments to the `portworx` container in the daemonset. It should look something like this:

```

containers:

  - args:

    - -c

    - testclusterid

    - -s

    - /dev/sdb

    - -x

    - kubernetes

    - -secret_type

    - gcloud-kms

    name: portworx

```

 Step 3b: Patch the Portworx DaemonSet​
Use the following command to patch the daemon set, so that it has access to the secret created Step 2

Create a patch file

```

cat <<EOF> patch.yaml

spec:

  template:

    spec:

      containers:

      - name: portworx

        env:

          - name: GOOGLE_KMS_RESOURCE_ID

            valueFrom:

              secretKeyRef:

                name: px-gcloud

                key: gcloud-kms-resource-id

          - name: GOOGLE_APPLICATION_CREDENTIALS

            value: /etc/pwx/gce/gcloud.json

        volumeMounts:

          - mountPath: /etc/pwx/gce

            name: gcloud-certs

      volumes:

        - name: gcloud-certs

          secret:

            secretName: px-gcloud

            items:

              - key: gcloud.json

                path: gcloud.json

EOF

```

Apply the patch

```

kubectl -n kube-system patch ds portworx --patch "$(cat patch.yaml)" --type=strategic

```

## Using Google Cloud KMS with Portworx​

- Encrypt Kubernetes PVCs with Google Cloud KMS

- Encrypt Portworx volumes using Google Cloud KMS

In this topic:
