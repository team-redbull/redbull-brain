# BackupLocation CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/backuplocations (Portworx Enterprise 3.6)

BackupLocation CRD reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

BackupLocation represents a BackupLocation object.

## BackupLocation​

FieldDescriptionType

`apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`cluster`ClusterItem is the spec used to store the credentials associated with the cluster
Only one of AWSClusterConfig, AzureClusterConfig or GCPClusterConfig should be specified and
should match the Type field. Members of the config can be specified inline or
through the SecretConfig`object`

`kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`location`BackupLocationItem is the spec used to store a backup location
Only one of S3Config, AzureConfig or GoogleConfig should be specified and
should match the Type field. Members of the config can be specified inline or
through the SecretConfig`object`

`status`BackupLocationStatus represents the status of a BackupLocation resource`object`

### `cluster` fields​

FieldDescriptionType

`cluster.awsClusterConfig`S3Config specifies the config required to connect to an S3-compliant
objectstore`object`

`cluster.awsClusterConfig.accessKeyID`AccessKeyId holds the accessKey for S3 endpoint`string`

`cluster.awsClusterConfig.disableSSL`Disable SSL option if using with a non-AWS S3 objectstore which doesn't
have SSL enabled`boolean`

`cluster.awsClusterConfig.endpoint`Endpoint will be defaulted to s3.amazonaws.com by the controller if not provided`string`

`cluster.awsClusterConfig.region`Region will be defaulted to us-east-1 by the controller if not provided`string`

`cluster.awsClusterConfig.secretAccessKey`SecretAccessKey holds the secretAccessKey for S3 endpoint`string`

`cluster.awsClusterConfig.sse`SSE (Server Side Encryption) type for the S3 bucket.
supported option: "AES256", "aws:kms"`string`

`cluster.awsClusterConfig.storageClass`The S3 Storage Class to use when uploading objects. Glacier storage
classes are not supported`string`

`cluster.awsClusterConfig.useIam`UseIam when set stork will use the instance IAM role associated with the nodes
on which stork pods run`boolean`

`cluster.azureClusterConfig`AzureConfig specifies the config required to connect to Azure Blob Storage`object`

`cluster.azureClusterConfig.clientID`ClientId holds the client ID for the azure account`string`

`cluster.azureClusterConfig.clientSecret`ClientSecret holds the client secret for the azure account`string`

`cluster.azureClusterConfig.environment`Azure-Environment type for azure blob storage
supported option: "azure-public", "azure-china"`string`

`cluster.azureClusterConfig.resourceGroupName`Resource group name`string`

`cluster.azureClusterConfig.storageAccountKey`StorageAccountKey holds the key for the storage account.
Not required when UseWorkloadIdentity is set in BackupLocationItem.`string`

`cluster.azureClusterConfig.storageAccountName`StorageAccountName holds the name of the storage account`string`

`cluster.azureClusterConfig.subscriptionID`SubscriptionID holds the subscription ID for the azure account`string`

`cluster.azureClusterConfig.tenantID`TenantID holds the tenant ID for the azure account`string`

`cluster.encryptionKey`Path is either the bucket or any other path for the backup location`string`

`cluster.gcpClusterConfig`GoogleConfig specifies the config required to connect to Google Cloud Storage`object`

`cluster.gcpClusterConfig.accountKey`AccountKey holds the account key for the google account`string`

`cluster.gcpClusterConfig.projectID`ProjectID holds the project ID for the google account`string`

`cluster.type`ClusterType is the type of the cluster`string`

### `location` fields​

FieldDescriptionType

`location.azureConfig`AzureConfig specifies the config required to connect to Azure Blob Storage`object`

`location.azureConfig.clientID`ClientId holds the client ID for the azure account`string`

`location.azureConfig.clientSecret`ClientSecret holds the client secret for the azure account`string`

`location.azureConfig.environment`Azure-Environment type for azure blob storage
supported option: "azure-public", "azure-china"`string`

`location.azureConfig.resourceGroupName`Resource group name`string`

`location.azureConfig.storageAccountKey`StorageAccountKey holds the key for the storage account.
Not required when UseWorkloadIdentity is set in BackupLocationItem.`string`

`location.azureConfig.storageAccountName`StorageAccountName holds the name of the storage account`string`

`location.azureConfig.subscriptionID`SubscriptionID holds the subscription ID for the azure account`string`

`location.azureConfig.tenantID`TenantID holds the tenant ID for the azure account`string`

`location.encryptionKey`EncryptionKey is deprecated. Instead use EncryptionV2Key field to pass the encryption key.`string`

`location.encryptionV2Key`EncryptionV2Key will be used to pass encryption key.`string`

`location.googleConfig`GoogleConfig specifies the config required to connect to Google Cloud Storage`object`

`location.googleConfig.accountKey`AccountKey holds the account key for the google account`string`

`location.googleConfig.projectID`ProjectID holds the project ID for the google account`string`

`location.nfsConfig.mountOptions`MountOptions holds the mount options for the NFS server`string`

`location.nfsConfig.nfsIOTimeoutInSecs`NFSIOTimeoutInSecs holds the NFS IO timeout in seconds`string`

`location.nfsConfig.serverAddr`ServerAddr holds the server address for the NFS server`string`

`location.nfsConfig.subPath`SubPath holds the subpath for the NFS server`string`

`location.path`Path is either the bucket or any other path for the backup location`string`

`location.s3Config`S3Config specifies the config required to connect to an S3-compliant
objectstore`object`

`location.s3Config.accessKeyID`AccessKeyId holds the accessKey for S3 endpoint`string`

`location.s3Config.disableSSL`Disable SSL option if using with a non-AWS S3 objectstore which doesn't
have SSL enabled`boolean`

`location.s3Config.endpoint`Endpoint will be defaulted to s3.amazonaws.com by the controller if not provided`string`

`location.s3Config.region`Region will be defaulted to us-east-1 by the controller if not provided`string`

`location.s3Config.secretAccessKey`SecretAccessKey holds the secretAccessKey for S3 endpoint`string`

`location.s3Config.sse`SSE (Server Side Encryption) type for the S3 bucket.
supported option: "AES256", "aws:kms"`string`

`location.s3Config.storageClass`The S3 Storage Class to use when uploading objects. Glacier storage
classes are not supported`string`

`location.s3Config.useIam`UseIam when set stork will use the instance IAM role associated with the nodes
on which stork pods run`boolean`

`location.type`BackupLocationType is the type of the backup location`string`

`location.useWorkloadIdentity`UseWorkloadIdentity when set, stork will use cloud provider's workload identity
credentials instead of static credentials for authentication. This allows each cluster
to use its own identity to access the storage account.
For Azure: Uses AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_FEDERATED_TOKEN_FILE environment variables
For AWS: Uses IAM roles for service accounts (IRSA)
For GCP: Uses Workload Identity`boolean`

`location.validate`Validate triggers validation when set to true. After validation completes,
this field is reset to false and the result is stored in Status.Validation.`boolean`

### `status` fields​

FieldDescriptionType

`status.sync`Sync contains the status of the last sync operation`object`

`status.sync.lastUpdateTime`LastUpdateTime is the timestamp of the last operation attempt`string`

`status.sync.reason`Reason provides additional details about the operation status`string`

`status.sync.status`Status is the current status of the operation`string`

`status.validation`Validation contains the status of the last validation operation`object`

`status.validation.lastUpdateTime`LastUpdateTime is the timestamp of the last operation attempt`string`

`status.validation.objectLock`ObjectLock indicates whether the backup location bucket has object lock enabled`boolean`

`status.validation.reason`Reason provides additional details about the operation status`string`

`status.validation.retentionPeriodDays`RetentionPeriodDays is the retention period in days configured on the object-locked bucket`integer`

`status.validation.status`Status is the current status of the operation`string`

In this topic:
