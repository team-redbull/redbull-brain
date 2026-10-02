# How to upgrade AWS gp2 to gp3 volumes

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/aws-gp3-volumes (Portworx Enterprise 3.6)

How to upgrade AWS gp2 to gp3 volumes | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Add a gp3 drive​

To add a gp3 drive, enter the `pxctl service drive add` command with the `-s` option, specifying the following:

- `type=gp3`

- `size=` with a size value

- `iops=` with your desired iops value

```

pxctl service drive add -s "type=gp3,size=200,iops=3500"

```

```

Adding drives may make storage offline for the duration of the operation.

Are you sure you want to proceed ? (Y/N): y

```

## Upgrade a gp2 drive to a gp3 drive​

Perform the following steps to upgrade your existing AWS cloud drives from gp2 to gp3:

-
Find the EBS volume ID of the volume you want to convert by running the following `pxctl clouddrive inspect` command, specifying the `--node-id` of the node where your volume is attached:

```

pxctl clouddrive inspect --node <px-node-id>

```

```

Drive Set Configuration

Number of drives in the Drive Set:  2

NodeID:  xxxxxxxx-xxxx-xxxx-xxxx-987d406fbc14

NodeIndex:  0

InstanceID:  i-0ea9e24fe13f6e1b9

Zone:  us-east-1b

State:  In Use

Labels:  map[]

Drive  0

	ID:  vol-0e67322e9bcccfacd

	Type:  gp2

	Size:  150 Gi

	Iops:  450

	Path:  /dev/nvme2n1

	Used for:  kvdb

Drive  1

	ID:  vol-0b181a78f74d37ea5

	Type:  gp2

	Size:  500 Gi

	Iops:  1500

	Path:  /dev/nvme1n1

	Used for:  data

```

-
Using the AWS CLI or AWS console, convert the volume type:

```

aws ec2 modify-volume --volume-type gp3 --volume-id vol-0c0accbf72047052e

```

```

{

    "VolumeModification": {

        "VolumeId": "vol-0c0accbf72047052e",

        "ModificationState": "modifying",

        "TargetSize": 150,

        "TargetIops": 3000,

        "TargetVolumeType": "gp3",

        "OriginalSize": 150,

        "OriginalIops": 450,

        "OriginalVolumeType": "gp2",

        "Progress": 0,

        "StartTime": "2021-06-29T10:52:43+00:00"

    }

}

```

-
Once you've successfully converted the volume type, make the Portworx node aware of the volume type change by cycling it through maintenance mode:

```

pxctl service maintenance --enter

```

```

This is a disruptive operation, PX will restart in maintenance mode.

Are you sure you want to proceed ? (Y/N): y

Entering Maintenance mode...

```

```

pxctl service maintenance --exit

```

```

Exiting Maintenance mode...

```

Repeat this process on all nodes where converted EBS volumes are attached.

-
Verify volume type in output of `pxctl clouddrive inspect --node <px node-id>` command.

```

pxctl clouddrive inspect --node xxxxxxxx-xxxx-xxxx-xxxx-987d406fbc14

```

```

Drive Set Configuration

Number of drives in the Drive Set:  2

NodeID:  xxxxxxxx-xxxx-xxxx-xxxx-987d406fbc14

NodeIndex:  0

InstanceID:  i-0ea9e24fe13f6e1b9

Zone:  us-east-1b

State:  In Use

Labels:  map[]

Drive  0

	ID:  vol-0e67322e9bcccfacd

	Type:  gp3

	Size:  150 Gi

	Iops:  450

	Path:  /dev/nvme2n1

	Used for:  kvdb

Drive  1

	ID:  vol-0b181a78f74d37ea5

	Type:  gp3

	Size:  500 Gi

	Iops:  1500

	Path:  /dev/nvme1n1

	Used for:  data

```

Repeat this process on all nodes where converted EBS volumes are attached.

In this topic:
