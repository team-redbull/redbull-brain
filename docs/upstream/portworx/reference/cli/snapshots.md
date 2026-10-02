# Snapshots operations using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/snapshots (Portworx Enterprise latest)

Snapshots operations using pxctl | Portworx Enterprise Documentation

Snapshots are efficient, point-in-time, read-only copies of volumes. You can use snapshots to read data, restore a volume, or create clones.

Portworx supports different snapshot implementations based on the datastore:

- PX-StoreV1: Uses the copy-on-write (CoW) technique.

- PX-StoreV2: Uses the redirect-on-write (RoW) technique.

The redirect-on-write (RoW) technique is generally more efficient than copy-on-write (CoW) for snapshot management because it reduces write overhead and improves storage efficiency.

You can create snapshots in one of the following ways:

- Manually, by running the `pxctl volume snapshot create` command (referred to as user-created snapshots).

- Automatically, by configuring a snapshot schedule for the volume.

## Creating snapshots​

Here's an example of how to create a snapshot:

```

pxctl volume snapshot create --name mysnap --label color=blue,fabric=wool myvol

```

```

Volume snap successful: 234835613696329810

```

The string of digits in the output is the volume ID of the new snapshot. You can use this ID(`234835613696329810`) or the name(`mysnap`), to refer to the snapshot in subsequent `pxctl` commands.

The label values allow you to tag the snapshot with descriptive information of your choosing. You can use them to filter the output of the `pxctl volume list` command.

There is an implementation limit of 64 snapshots per volume.

## Listing Snapshots​

To list existing snapshots, you can use `pxctl volume list`. Run the `pxctl volume list` command with the `--help` flag to list the available subcommands and flags.

### User created snapshots​

To list your user created snapshots, use one of the following commands:

```

pxctl volume list --snapshot

```

```

ID          NAME                                    SIZE    HA  SHARED  ENCRYPTED   COMPRESSED  IO_PRIORITY SCALE   STATUS

234835613696329810  mysnap                                  1 GiB   1   no  no      no      LOW     1   up - detached

```

note

The above command shows only snapshots.

(or)

```

pxctl volume list --all

```

```

ID          NAME                                    SIZE    HA  SHARED  ENCRYPTED   COMPRESSED  IO_PRIORITY SCALE   STATUS

234835613696329810  mysnap                                  1 GiB   1   no  no      no      LOW     1   up - detached

1125771388930868153 myvol                                   1 GiB   1   no  no      no      LOW     1   up - detached

```

note

The above command shows all volumes, including snapshots.

### Scheduled snapshots​

To list all your scheduled snapshots, run this command:

```

pxctl volume list --snapshot-schedule

```

```

ID          NAME                                    SIZE    HA  SHARED  ENCRYPTED   COMPRESSED  IO_PRIORITYSCALE    STATUS

423119103642927058  myvol_periodic_2018_Feb_26_21_12                    1 GiB   1   no  no      no      LOW     1up - detached

```

### Filtering the results​

You can filter the results with the `–parent` and `–label` options. For instance, `–parent myvol` will show only snapshots whose parent is `myvol` (i.e. `mysnap`):

```

pxctl volume list --parent myvol --snapshot

```

```

ID          NAME    SIZE    HA  SHARED  ENCRYPTED   COMPRESSED  IO_PRIORITY SCALE   STATUS

234835613696329810  mysnap  1 GiB   1   no  no      no      LOW     1   up - detached

```

Giving labels restricts the list to snapshots that have all of the specified labels. For instance, –`label fabric=wool` would again show `mysnap` but `–label fabric=cotton` won't.

```

pxctl volume list --parent myvol --snapshot --label fabric=wool

```

```

ID          NAME    SIZE    HA  SHARED  ENCRYPTED   COMPRESSED  IO_PRIORITY SCALE   STATUS

234835613696329810  mysnap  1 GiB   1   no  no      no      LOW     1   up - detached

```

## Deleting snapshots​

To delete a snapshot, run `pxctl volume delete` with the `name` or the `id` of the snapshot you want to delete as an argument:

```

pxctl volume delete mysnap

```

```

Delete volume 'mysnap', proceed ? (Y/N): y

Volume mysnap successfully deleted.

```

note

- Only detached snapshots can be deleted.

- To avoid I/O pauses during deletion and to reclaim storage space on thin-provisioned backends, such as a storage area network (SAN) or a FlashArray, enable non-blocking device delete (NBDD), which performs discards in the background before deleting volumes or snapshots. For more information, see Non-Blocking Device Delete.

## Restoring snapshots​

In order to restore a volume from snapshot use the `pxctl volume restore` command:

```

/opt/pwx/bin/pxctl volume restore -h

```

```

Restore volume from snapshot

Usage:

  pxctl volume restore [flags]

Aliases:

  restore, r

Examples:

pxctl volume restore [flags] volName

Flags:

  -h, --help              help for restore

  -s, --snapshot string   snapshot-name-or-ID

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

```

In the below example parent volume `myvol` is restored from its snapshot `mysnap`. Make sure volume is detached in order to restore from the snapshot.

```

pxctl volume restore --snapshot mysnap myvol

```

```

Successfully started restoring volume myvol from mysnap.

```

To restore a volume from the trash can, specify the --trashcan flag:

```

pxctl volume restore --trashcan trashedvol myvol

```

```

Successfully started restoring volume myvol from trashedvol.

```

## Snapshot schedule policies​

You can use the `pxctl sched-policy` command to create and manage your snapshot schedule policies.

The example below creates a policy named `p1` with the following properties:

- Portworx performs periodic backups every 60 minutes and keeps the last periodic 5 backups.

- Portworx performs weekly backups every Sunday at 12:00 and keeps the last 4 weekly backups.

Run the following command to create the `p1` backup policy:

```

pxctl sched-policy create --periodic 60,5 --weekly sunday@12:00,4 p1

```

You can add schedule policies either when a volume gets created or afterward.

Here is an example of how you can add a schedule policy when the volume is created:

```

pxctl volume create --policy p1 vol1

```

The following example adds or updates a schedule policy later:

```

pxctl volume snap-interval-update --policy p1 vol1

```

The example below removes a policy from a volume by setting the snap interval to 0:

```

pxctl volume snap-interval-update --periodic 0 vol1

```

For more information on how to create, list, update, and delete your snapshot schedule policies with `pxctl`, see this page.

## Snapshot schedules​

If you create a volume and a snapshot schedule at the same time, you can use and combine as needed the following four scheduling options:

- –-periodic,

- –-daily,

- –-weekly and

- –-monthly.

Scheduled snapshots have names of the form `<Parent-Name>_<freq>_<creation_time>`, where `<freq>` denotes the schedule frequency (i.e., periodic, daily, weekly, monthly):

```

myvol_periodic_2018_Feb_26_21_12

myvol_daily_2018_Feb_26_12_00

```

As an example, to create a new volume named `myvol` and to schedule:

- a periodic snapshot for every 60 min and a

- daily snapshot at 8:00 am and a

- weekly snapshot on Friday at 23:30 pm and

- monthly snapshot on the 1st of the month at 6:00 am.

you would run this command:

```

pxctl volume create --periodic 60 --daily @08:00 --weekly Friday@23:30 --monthly 1@06:00 myvol

```

Here's another example. In order to create a volume named `myvol` and to schedule:

- 10 periodic snapshots that trigger every 120 min and

- 3 daily snapshots that trigger at 8:00 am

you would run the following:

```

pxctl volume create --periodic 120,10 --daily @08:00,3 myvol

```

note

Once the count is reached, the oldest existing one will be deleted if necessary.

### Changing a snapshot schedule​

To change the snapshot schedule for a given volume, use the `pxctl volume snap-interval-update` command. Run the `pxctl volume snap-interval-update` command with the `--help` flag to list the available subcommands and flags.

In the below example, the old snapshot schedule is replaced with a daily snapshot triggered at 15:00 pm (5 snapshots are kept):

```

pxctl volume snap-interval-update --daily @15:00,5 myvol

```

### Disabling scheduled snapshots​

To disable scheduled snapshot for a given volume, use `--periodic 0` on `snap-interval-update`:

```

pxctl volume snap-interval-update --periodic 0 myvol

```

### View the snapshot schedule for a volume​

To view the snapshot schedule for a volume, use the `pxctl volume inspect` command as follows:

```

pxctl volume inspect myvol

```

```

Volume	:  1125771388930868153

	Name            	 :  myvol

	Size            	 :  1.0 GiB

	Format          	 :  ext4

	HA              	 :  1

	IO Priority     	 :  LOW

	Creation time   	 :  Feb 26 18:06:31 UTC 2018

	Snapshot        	 :  daily @15:00,keep last 5

	Shared          	 :  no

	Status          	 :  up

	State           	 :  Attached: minion1

	Device Path     	 :  /dev/pxd/pxd1125771388930868153

	Reads           	 :  54

	Reads MS        	 :  152

	Bytes Read      	 :  1105920

	Writes          	 :  53

	Writes MS       	 :  841

	Bytes Written   	 :  16891904

	IOs in progress 	 :  0

	Bytes used      	 :  48 MiB

	Replica sets on nodes:

		Set  0

			Node 		 :  X.X.X.84 (Pool 0)

	Replication Status	 :  Up

```

## Related topics​

For information about creating snapshots of your Portworx volumes, refer to the Create and use snapshots page.

In this topic:
