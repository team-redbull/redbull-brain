# Cloud Snapshots and Recovery using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/cloud-snaps (Portworx Enterprise latest)

Cloud Snapshots and Recovery using pxctl | Portworx Enterprise Documentation

## Overview of cloud backups​

This document outlines how to back-up Portworx volumes to different cloud providers' object storage, including any S3-compatible object storage. To restore a specific backup, the user can restore the volume from that point in time.

Portworx helps administrators running persistent container workloads, on-prem or in the cloud, to safely backup their mission-critical database volumes to any supported cloud storage. Next, they can restore them on-demand. This way, Portworx enables a seamless DR integration for all the important business application data.

### Supported cloud providers​

Portworx Enterprise supports the following cloud providers:

- Amazon S3 and any S3-compatible Object Storage

- Azure Blob Storage

- Google Cloud Storage

## Performing cloud backups of a Portworx volume​

Portworx volumes can be backed up to cloud via `pxctl cloudsnap`. Run the `pxctl cloudsnap` command with the `--help` flag to list the available subcommands and flags.

### Login to the secrets database​

Note that the cloud credentials are stored in an external secret store. Hence, before creating the credentials, make sure that you have configured a secret provider of your choice.

Now, we can login to the secrets database by typing:

```

pxctl secrets kvdb login

```

```

Successful Login to Secrets Endpoint!

```

note

Kubernetes users: This is not required if you are using Portworx 2.0 and higher on Kubernetes and you have `-secret_type` as k8s in Daemonset

### Set the required cloud credentials​

For this, we will use the `pxctl credentials create` command. Run the `pxctl credentials create` command with the `--help` flag to list the available subcommands and flags.

#### Azure​

Here's how you can create the credentials for Azure:

```

pxctl credentials create --provider azure --azure-account-name portworxtest --azure-account-key zbJSSpOOWENBGHSY12ZLERJJV my-azure-cred

```

At this point, we can list the configured credentials as follows:

```

pxctl cloudsnap credentials list

```

```

Azure Credentials

UUID                        ACCOUNT NAME        ENCRYPTION

xxxxxxxx-xxxx-xxxx-xxxx-0d5d6d9b5742        portworxtest        false

```

note

The listing of credentials do mean that connection to a secret-store endpoint has been validated.

#### AWS​

If you are using AWS, Portworx creates a bucket (`ID` same as the cluster `UUID`) to upload cloudsnaps by default. Starting with Portworx version 1.5.0, users can upload to a pre-created bucket. Thus, the AWS credentials provided to Portworx should either:

- have the capability to create a bucket or

- the bucket provided to Portworx at a minimum must have the permissions mentioned below.

If you prefer that a user-specified bucket be used for cloudsnaps, specify the bucket id with the `--bucket` option while creating the credentials.
 With a user-specified bucket​
Consider you are using `us-east-1 region`, then you use the following command:

```

pxctl credentials create --provider s3  --s3-access-key <AccessKey> --s3-secret-key <secretKey> --s3-region us-east-1 --s3-endpoint s3.amazonaws.com --bucket bucket-id my-s3-cred

```

If you are using a different region, replace the `--s3-region` and `--s3-endpoint` parameters with the appropriate values. For more information about region-specific endpoints, check out the "Amazon Simple Storage Service (Amazon S3)" section on this page.

If you use the above command to create the credentials for an s3 endpoint that supports only virt-host-style access, then you will hit an error like below:

```

createCred: error validating credential during create: SecondLevelDomainForbidden: Please use virtual hosted style to access. status code: 403, request id: XXXX, host id:,

```

In this case, you should specify the `--disable-path-style` parameter while creating credentials as follows:

```

pxctl credentials create mycreds --provider=s3 --s3-disable-ssl --s3-region=us-east-1 --s3-access-key=<S3-ACCESS_KEY> --s3-secret-key=<S3-SECRET_KEY> --s3-endpoint=mys3-enpoint.com --disable-path-style --bucket=mybucket

```

```

Credentials created successfully, UUID:xxxxxxxx-xxxx-xxxx-xxxx-297ea41c8022

```

The user created/specified bucket at a minimum must have the following permissions:

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

                    "arn:aws:s3:::<bucket-name/*"

                ]

            }

        ]

 }

```

note

Replace `<bucket-name>` with name of your user-provided bucket.

 Without a user-specified bucket​

```

pxctl credentials create --provider s3  --s3-access-key XXXX --s3-secret-key XXXX --s3-region us-east-1 --s3-endpoint s3.amazonaws.com my-s3-cred

```

 Configure a cluster-wide proxy​
You can set up a cluster-wide proxy for Portworx to use when uploading cloud snaps to an S3 bucket. Portworx uses this proxy setting in conjunction with the `--use-proxy` flag on cloudsnap credentials to send backup data through the proxy. Perform the steps in this section to configure a cluster-wide proxy and create credentials that use it.

note

This proxy is currently used only by cloudsnaps, the rest of the Portworx network traffic does not use this proxy.

-
Update your Portworx cluster-wide options by entering the `pxctl cluster options update` command with the `--px-http-proxy` flag and the URL of your proxy:

```

pxctl cluster options update --px-http-proxy http://X.X.X.0:9999

```

-
Create credentials for your cloudsnap with or without a user-specified bucket, specifying the `--use-proxy` flag:

- With a user-specified bucket:

```

pxctl credentials create --use-proxy \

--provider s3  \

--s3-access-key <AccessKey> \

--s3-secret-key <secretKey> \

--s3-region us-east-1 \

--s3-endpoint s3.amazonaws.com \

--bucket bucket-id \

credentialName

```

- Without a user-specified bucket:

```

pxctl credentials create --use-proxy \

--provider s3 \

--s3-access-key <AccessKey> \

--s3-secret-key <secretKey> \

--s3-region us-east-1 \

--s3-endpoint s3.amazonaws.com \

credentialName

```

#### Google Cloud​

-
Make sure the user or service account used by Portworx has the following roles:

- Editor

- Storage

- Object Admin

- Storage Object Viewer

For more information about roles and permissions within GCP, see the Granting, changing, and revoking access to resources section of the GCP documentation.

-
Enter the `pxctl credentials create` command specifying:

- The `provider` flag with the name of the provider (`google`)

- The `--google-project-id` flag with your Google project ID

- The `--google-json-key-file` flag with the name of the JSON file containing your key

- The name of your cloud credentials

Example:

```

pxctl credentials create --provider google --google-project-id px-test --google-json-key-file px-test.json my-google-cred

```

#### Configure credentials​

`pxctl credentials create` enables the user to configure the credentials for each supported cloud provider.

An additional encryption key can also be provided for each credential. If provided, all the data being backed up to the cloud will be encrypted using this key. The same key needs to be provided when configuring the credentials for restore. This way, Portworx will be able to decrypt the data successfully.

These credentials can only be created once and cannot be modified. In order to maintain security, once configured, the secret parts of the credentials will not be displayed.

### List the credentials to verify​

Use `pxctl credentials list` to verify the credentials supplied as follows:

```

pxctl credentials list

```

```

S3 Credentials

UUID                        NAME        REGION            ENDPOINT                        ACCESS KEY            SSL ENABLED        ENCRYPTION        BUCKET        WRITE THROUGHPUT (KBPS)

xxxxxxxx-xxxx-xxxx-xxxx-8e8f9414ff77        my-s3-cred    us-east-1        X.X.X.121:9010,X.X.X.122:9010,X.X.X.123:9010    <aws-secret-key>        false            false            <nil>        1979

Google Credentials

UUID                        NAME            PROJECT ID        ENCRYPTION        BUCKET        WRITE THROUGHPUT (KBPS)

xxxxxxxx-xxxx-xxxx-xxxx-76aaf6fb10f4        my-google-cred        235475231246        false            <nil>        1502

Azure Credentials

UUID                        NAME            ACCOUNT NAME        ENCRYPTION        BUCKET        WRITE THROUGHPUT (KBPS)

xxxxxxxx-xxxx-xxxx-xxxx-b59e3d35a3a2        my-azure-cred        pwx-test        false            <nil>        724

```

`pxctl credentials list` only displays non-secret values of the credentials. Secrets are neither stored locally nor displayed. The credentials will be stored as part of the secret endpoint given to Portworx for persisting authentication across reboots.

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

You can find more details on how to manage your cloud credentials with `pxctl` by checking out the Credentials page.

### Perform cloud backups of single volumes​

The actual backup of the Portworx volume is done via the `pxctl cloudsnap backup`. Run the `pxctl cloudsnap backup` command with the `--help` flag to list the available subcommands and flags.

As an example, to back up a volume named `volume1`, you would use something like:

```

pxctl cloudsnap backup volume1 --cred-id xxxxxxxx-xxxx-xxxx-xxxx-3b0b06160332

```

Here are a few things to consider about this command:

- it is used to back up a single volume to the cloud provider of your choice using the specified credentials.

- it decides whether to take a full or an incremental backup depending on the existing backups for the volume, as follows:

- the first backup uploaded to the cloud is always a full backup.

- after that, subsequent backups are incremental.

- after 6 incremental backups, every 7th backup is a full backup.

- users can force a full backup any time by giving the `--full` flag.

- if only one credential is configured on the cluster, then the `cred-id` option may be skipped.

Next, we’re going to focus on the steps to perform a successful cloud backup:

- List all the available volumes to choose the volume to backup:

```

pxctl volume list

```

```

ID            NAME    SIZE    HA    SHARED    ENCRYPTED    IO_PRIORITY    SCALE    STATUS

56706279008755778    NewVol    4 GiB    1    no    no        LOW        1    up - attached on xx.xx.9.73

980081626967128253    evol    2 GiB    1    no    no        LOW        1    up - detached

```

- Now, run the backup command:

```

pxctl cloudsnap backup NewVol

```

```

Cloudsnap backup started successfully with id: xxxxxxxx-xxxx-xxxx-xxxx-985657757352

```

note

Note that, in this particular example, since only one credential is configured, there is no need to specify the credentials on the command line.

- While Portworx is working, let's check the progress of our backups:

```

pxctl cloudsnap status

```

```

NAME                    SOURCEVOLUME                                    STATE        NODE        BYTES-PROCESSED    TIME-ELAPSED    COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-c858e714689e    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-951325819047337066-incr    Backup-Done    xx.x.73.246    420044800    17.460186585s    Wed, 16 Jan 2019 22:27:30 UTC

xxxxxxxx-xxxx-xxxx-xxxx-985657757352    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463    Backup-Active    xx.x.73.246    1247805440    10.525438874s

```

You could also check the status of a particular job, by passing the `task-id` returned upon the successful execution of the `pxctl cloudsnap backup` command:

```

pxctl cloudsnap status --name xxxxxxxx-xxxx-xxxx-xxxx-985657757352

```

```

NAME                    SOURCEVOLUME                                    STATE        NODE        BYTES-PROCESSED    TIME-ELAPSED    COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-985657757352    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463    Backup-Active    xx.x.73.246    1840250880    16.57831394s

```

Once the volume is backed up to the cloud successfully, listing the remote cloudsnaps will display the backup that has just been completed.

### List your cloud backups​

Use the `pxctl cloudsnap list` command to list your cloud backups. Run the `pxctl cloudsnap list` command with the `--help` flag to list the available subcommands and flags.

```

pxctl cloudsnap list

```

```

SOURCEVOLUME                    SOURCEVOLUMEID            CLOUD-SNAP-ID                                        CREATED-TIME                TYPE        STATUS

volume20190116214922                590114184663672482        xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-619248560586769719        Wed, 16 Jan 2019 21:51:53 UTC        Manual        Done

volume20190116214922                590114184663672482        xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-951325819047337066-incr        Wed, 16 Jan 2019 22:27:13 UTC        Manual        Done

NewVol                        56706279008755778        xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463        Thu, 17 Jan 2019 00:03:59 UTC        Manual        Done

```

note

This command assumes that all your credentials are properly set up. If that is not the case, the cloud backups won't show up.

Run the following command to list cloudsnaps of a volume that are not present in the cluster, but the volume belonged to this cluster in the past:

```

pxctl cloudsnap list -d

```

```

SOURCEVOLUME	SOURCEVOLUMEID	CLOUD-SNAP-ID		CREATED-TIME	TYPE	STATUS	BELONGS-TO-CLUSTER	NAMESPACE

testvol	 521362534280354159	 xxxxxxxx-xxxx-xxxx-xxxx-a0c01d17b162/521362534280354159-116521897362456321	Wed, 24 Mar 2021 20:42:58 UTC	Manual Done	Yes

```

```

pxctl cloudsnap list -d -c 4f568y9-23446acd7-0987-24875

```

```

Failed to enumerate backups:  Invalid arguments, cloudsnaps of deleted voluemes/MissingSrcVolumes can be listed for current cluster only

```

The above command lists only the cloudsnaps of deleted volumes for current cluster. Therefore, the cluster-uuid/bucket input is not expected and returns error to the caller.

### Inspect a cloud snapshot​

The `pxctl cloudsnap list` command displays all the cloud snapshots for a given credential, source volume, or type of cloud snapshot. To view more details about a particular cloud snapshot, you must specify the `-i` flag with the ID of the cloud snapshot you want to inspect.

Example:

-
Start by listing your cloud snapshots with:

```

pxctl cloudsnap list

```

```

SOURCEVOLUME            SOURCEVOLUMEID            CLOUD-SNAP-ID                                        CREATED-TIME                TYPE        STATUS

agg-cs_journal_1        10769800556491614        xxxxxxxx-xxxx-xxxx-xxxx-f3e9050d0f68/10769800556491614-673132711323933325        Thu, 24 Oct 2019 19:02:08 UTC        Manual        Done

agg-cs_0            365276421799434338        xxxxxxxx-xxxx-xxxx-xxxx-f3e9050d0f68/365276421799434338-461608030527675278        Thu, 24 Oct 2019 19:02:47 UTC        Manual        Done

```

-
To inspect the first cloud snapshot (`xxxxxxxx-xxxx-xxxx-xxxx-f3e9050d0f68/10769800556491614-673132711323933325`) and print the output in JSON format, enter the following command:

```

pxctl -j cloudsnap list --cloudsnap-id xxxxxxxx-xxxx-xxxx-xxxx-f3e9050d0f68/10769800556491614-673132711323933325

```

```

{

  "ID": "xxxxxxxx-xxxx-xxxx-xxxx-f3e9050d0f68/10769800556491614-673132711323933325",

  "SrcVolumeID": "10769800556491614",

  "SrcVolumeName": "agg-cs_journal_1",

  "Timestamp": "2019-10-24T19:02:08Z",

  "Metadata": {

  "cloudsnapType": "Manual",

  "compression": "lz77",

  "sizeBytes": "2152751104",

  "starttime": "Thu, 24 Oct 2019 19:02:08 UTC",

  "status": "Done",

  "updatetime": "Thu, 24 Oct 2019 19:06:12 UTC",

  "version": "V2.00",

  "volume": "{\"DevSpec\":{\"size\":137438953472,\"format\":2,\"block_size\":4096,\"ha_level\":1,\"cos\":3,\"volume_labels\":{\"best_effort_location_provisioning\":\"true\",\"name\":\"vContainer\"},\"replica_set\":{},\"aggregation_level\":1,\"scale\":1,\"journal\":true,\"queue_depth\":128,\"force_unsupported_fs_type\":true,\"io_strategy\":{}},\"UsedSize\":0,\"PoolId\":0,\"ClusterId\":\"PX-INT-C0-BVT-MN-NS-BRANCH_476_24_Oct_19_04_49_UTC\",\"PublicSecretData\":null,\"Labels\":null}",

  "volumename": "agg-cs_journal_1"

  },

  "Status": "Done"

}

```

### Perform cloud backup of a group of volumes​

Run the `pxctl cloudsnap backup-group` command with the `--help` flag to list the available subcommands and flags.

#### Examples​

The below command takes a group cloud backup of volumes vol1 and vol2:

```

pxctl cloudsnap backup-group --volume_ids vol1,vol2

```

```

Group Cloudsnap backup started successfully with groupID:xxxxxxxx-xxxx-xxxx-xxxx-8eaca61a02ae

```

Then, you can grab the `groupID` from above and use it to check the status of the group cloud snapshot. The following command will show the status of each cloud snapshot in the group:

```

pxctl cloudsnap status --name xxxxxxxx-xxxx-xxxx-xxxx-8eaca61a02ae

```

```

NAME                                    SOURCEVOLUME                                                                    STATE           NODE            BYTES-PROCESSED TIME-ELAPSED    COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-bd24f945e6de    xxxxxxxx-xxxx-xxxx-xxxx-8f40a9e51c9a/201412281295404839-463199598055620776-incr Backup-Done     192.168.56.92   0 B             1.627836177s    Fri, 08 Mar 2019 22:12:14 UTC

xxxxxxxx-xxxx-xxxx-xxxx-2601da6d5fff    xxxxxxxx-xxxx-xxxx-xxxx-8f40a9e51c9a/592806372953104727-884041223239759095-incr Backup-Done     192.168.56.92   0 B             1.629703129s    Fri, 08 Mar 2019 22:12:14 UTC

```

You can also take a group cloud backup by selecting the volumes based on their labels. In the example below, we have 2 volumes with the label app=mysql:

```

 pxctl volume list --label app=mysql

```

```

ID                      NAME    SIZE    HA      SHARED  ENCRYPTED       IO_PRIORITY     STATUS          SNAP-ENABLED

592806372953104727      vol1    1 GiB   1       no      no              LOW             up - detached   no

201412281295404839      vol2    1 GiB   1       no      no              LOW             up - detached   no

```

To back them up as a group to the cloud backup, run the following:

```

pxctl cloudsnap backup-group --label app=mysql

```

```

Group Cloudsnap backup started successfully with groupID:xxxxxxxx-xxxx-xxxx-xxxx-2e66ef3986d1

```

### Extent based cloudsnaps​

note

This feature is not available in versions prior to 2.0.

With Portworx Enterprise 2.0, Portworx has enhanced the way cloud backups are done. Now, users can resume interrupted backups or restores.

For example, if the node performing backups or restores restarts, the backup/restore will resume once that node becomes operational.

This feature is also available for cloud backups of aggregated volumes. Here are a few points to consider in this regard:

-
For aggregated volumes, aggregated parts are backed up/restored sequentially.

-
Each aggregated part is backed up/restored on one of the nodes where the replica of that aggregated part is provisioned.

-
If not enough nodes are available to create the required aggregation level, aggregated volumes are restored to a non-aggregated volume(i.e. `aggregation=1`).

### Restore from a cloud backup​

Use `pxctl cloudsnap restore` to restore from a cloud backup. Run the `pxctl cloudsnap restore` command with the `--help` flag to list the available subcommands and flags.

This command is used to restore a successful backup from the cloud. It requires the cloudsnap ID and the credentials for the cloud storage provider or the object storage. Restore happens on any node where storage can be provisioned.

You can restore a backup of a Portworx to one of your Portworx volumes in the cluster. Once restored, the volume inherits the attributes from the backup (for example, file system, size, and block size). Starting with Portworx version 2.6, the replication level of the restored volume matches the replication level of the backed up volume. You can change the replication level by supplying a `--repl` value to the `pxctl cloudsnap restore` command.

To restore a backup from cloud, enter the following command:

```

pxctl cloudsnap restore --snap xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463

```

```

Cloudsnap restore started successfully on volume: 104172750626071399 with task name:xxxxxxxx-xxxx-xxxx-xxxx-f37b327d9225

```

Once a restore gets started, `pxctl` shows the id of the volume created to restore the cloud snap together with the task-id.

While the restore process is running, run the `pxctl cloudsnap status` command to see its status:

```

pxctl cloudsnap status

```

```

NAME                    SOURCEVOLUME                                    STATE        NODE        BYTES-PROCESSED    TIME-ELAPSED    COMPLETED

xxxxxxxx-xxxx-xxxx-xxxx-985657757352    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463    Backup-Done    xx.x.73.246    11988570112    3m29.825766964s    Thu, 17 Jan 2019 00:07:29 UTC

xxxxxxxx-xxxx-xxxx-xxxx-c858e714689e    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-951325819047337066-incr    Backup-Done    xx.x.73.246    420044800    17.460186585s    Wed, 16 Jan 2019 22:27:30 UTC

xxxxxxxx-xxxx-xxxx-xxxx-f37b327d9225    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/212160250617983239-283838486341798860    Restore-Done    xx.x.73.246    1079287808    3.174541219s    Thu, 17 Jan 2019 00:15:19 UTC

```

If you want to see the status of a particular process, run the `pxctl cloudsnap status` command and pass it the `--name` flag with the name of the task you want to inspect:

```

pxctl cloudsnap status --name xxxxxxxx-xxxx-xxxx-xxxx-f37b327d9225

```

```

xxxxxxxx-xxxx-xxxx-xxxx-f37b327d9225    xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/212160250617983239-283838486341798860    Restore-Done    xx.x.73.246    1079287808    3.174541219s    Thu, 17 Jan 2019 00:15:19 UTC

```

If the restore command fails, it shows the reason why it failed.

Note that the restored volume will not be attached or mounted automatically.

note

- As long as the backup was taken from a Portworx cluster of version 2.0 or greater, Portworx restores cloudsnaps with the same `repl` value of the volume the backup was taken from.

- With Portworx Enterprise 2.1.0, users can choose to do optimized restores. Optimized restores create a snapshot of every successful restore and use that snapshot for the next incremental restore of the same volume. For more details about optimized restores, visit the Enabling optimized restores section.

### The naming scheme for cloud backups​

Cloud backups adhere to the following naming scheme: `<bucket-id>/<vol-id>-<snap-id>`.

Example:

- `xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/56706279008755778-725134927222077463`

For incremental backups, Portworx adds the `-incr` suffix as follows: `<bucket-id>/<vol-id>-<snap-id>-incr`.

Example:

- `xxxxxxxx-xxxx-xxxx-xxxx-14223ac55170/590114184663672482-951325819047337066-incr`

### Deleting a Cloud Backup​

note

This feature is only supported starting with Portworx version 1.4 or later.

To delete a cloud backup, run:

```

pxctl cloudsnap delete

```

The command will flag a cloudsnap for deletion and a job will take care of deleting objects associated with these backups from the objectstore.

Only cloudsnaps which do not have any dependant cloudsnaps (ie incrementals) can be deleted. If there are dependent cloudsnaps then the command will throw an error and will show the list of cloudsnaps that need to be deleted first.

note

For Portworx versions above and including 2.1, delete requests are queued and processed in the background. Since querying cloud to figure out dependent backups can take a while, user requests to delete the backups are added to a queue and an immediate response is returned to the user. If a cloud backup could not be deleted because of other dependent backups, an alert is logged and this will be deleted when all other dependent backups are deleted by the user.

As an example, to delete the backup `pqr9-cl1/538316104266867971-807625803401928868`, you could run the following:

```

pxctl cloudsnap delete --snap pqr9-cl1/538316104266867971-807625803401928868

```

```

Cloudsnap deleted successfully

pxctl cloudsnap list

SOURCEVOLUME     CLOUD-SNAP-ID                    CREATED-TIME            STATUS

dvol        pqr9-cl1/520877607140844016-50466873928636534    Fri, 07 Apr 2017 20:22:43 UTC    Done

```

note

Portworx cloudsnap deletes are optimized with S3 batch-deletes API.

### Cloud backup schedules​

Cloud backup schedules allow backups to be uploaded to cloud at periodic intervals of time. These schedules can be managed through `pxctl`.

Run the `pxctl cloudsnap schedules` with the `--help` flag to list the available subcommands and flags.

#### Creating a cloud backup schedule​

Cloud backup schedules can be created using `pxctl cloudsnap schedules create`. Run the `pxctl cloudsnap schedules create` command with the `--help` flag to list the available subcommands and flags.

Let's look at a simple example:

```

 pxctl cloudsnap schedules create testVol --daily 21:00 --max 15 --cred-id xxxxxxxx-xxxx-xxxx-xxxx-01615119a442

```

```

 Cloudsnap schedule created successfully

```

The above command creates a daily schedule that retains a maximum of 15 backups in the cloud. Use the `--max` parameter to indicate the number of backups you want to retain in the cloud. Then, the most recent `--max` number of backups are retained and older backups are deleted periodically.

note

Note that, while listing cloud backups, you may see more than the `--max` number of backups. Due to the incremental nature of backups, we may need to retain more than `--max` backups in order to allow `--max` backups to be restored at any given time.

#### Listing Cloud Backup Schedules​

You can list the backup schedules that are currently configured using the following command:

```

pxctl cloudsnap schedules list

```

```

UUID                        VOLUMEID            MAX-BACKUPS        FULL        SCHEDULE(UTC)

xxxxxxxx-xxxx-xxxx-xxxx-34e6f816c2d1        648038464574631167        15            false        daily @21:00

```

#### Deleting a Cloud Backup Schedule​

Run the following to delete a backup schedule:

```

pxctl cloudsnap schedules  delete --uuid xxxxxxxx-xxxx-xxxx-xxxx-34e6f816c2d1

```

```

Cloudsnap schedule deleted successfully

```

## Related topics​

- For information about creating and managing cloud snapshots of your Portworx volumes through Kubernetes, refer to the Create and use cloud snapshots page.

In this topic:
