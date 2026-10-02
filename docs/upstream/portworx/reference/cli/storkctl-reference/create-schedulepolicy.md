# Create and delete SchedulePolicy with storkctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/create-schedulepolicy (Portworx Enterprise latest)

Create and delete SchedulePolicy with storkctl | Portworx Enterprise Documentation

This topic explains how to create and delete a SchedulePolicy using the `storkctl` command-line tool.

### How to use the storkctl command?​

To create a SchedulePolicy using `storkctl`, you can use the `create schedulepolicy` or `create sp` command with specific flags to define the schedule details.

note

In the `storkctl create` command, default values will be applied to all optional parameters in case you do not provide input. Additionally, validations are implemented that will generate relevant error messages in the event of invalid or incorrect inputs to the command.

### Create an interval-based schedule policy​

Run the following command to create a schedule policy with an interval-based recurrence. The specified operation associated with this schedule policy will be executed at regular intervals, and the interval duration is determined by the value provided with the `-i` flag:

```

storkctl create schedulepolicy <policy-name> \

-t Interval \

-i <interval-in-minutes> \

—-retain <number-of-backups-to-retain>

```

Example:

```

storkctl create schedulepolicy testpolicy -t Interval -i 1

```

```

kind: SchedulePolicy

metadata:

 name: testpolicy

policy:

 daily: null

 interval:

   intervalMinutes: 1

   options: null

   retain: 10

 monthly: null

 weekly: null

```

### Create a daily schedule policy​

Run the following command to create a schedule policy with a daily recurrence. The specified operation or task associated with this schedule policy will be executed at a particular time every day:

```

storkctl create schedulepolicy <policy-name> \

-t Daily --time <exact-time> \

—-retain <number-of-backups-to-retain> \

--force-full-snapshot-day <day-to-trigger-full-backup>

```

Example:

```

storkctl create schedulepolicy testpolicy -t Daily --time 10:14PM

```

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

 name: testpolicy

policy:

 daily:

   forceFullSnapshotDay: monday

   options: null

   retain: 30

   time: 10:14PM

 interval: null

 monthly: null

 weekly: null

```

### Create a weekly schedule policy​

Run the following command to create a schedule policy with a weekly recurrence. The specified operation or task associated with this schedule policy will be executed at a particular time on a specific day of each week:

```

storkctl create schedulepolicy <policy-name> \

-t Weekly \

--day-of-week <day> \

--time <exact-time> \

—-retain <number-of-backups-to-retain>

```

Example:

```

storkctl create schedulepolicy testpolicy -t Weekly --day-of-week Thursday --time 10:13PM

```

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

 name: testpolicy

policy:

 daily: null

 interval: null

 monthly: null

 weekly:

   day: thursday

   options: null

   retain: 7

   time: 10:13PM

```

### Create a monthly schedule policy​

Run the following command to create a schedule policy with a monthly recurrence. The specified operation or task associated with this schedule policy will be executed at a particular time and on a specific date of each month:

```

storkctl create schedulepolicy <policy-name> \

-t Monthly \

--time <exact-time> \

--date-of-month <date> \

—-retain <number-of-backups-to-retain>

```

Example:

```

storkctl create schedulepolicy testpolicy -t Monthly --time 8:05PM --date-of-month 14

```

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

 name: testpolicy

policy:

 daily: null

 interval: null

 monthly:

   date: 14

   options: null

   retain: 12

   time: 8:05PM

 weekly: null

```

### Create schedulepolicy command flags​

You can include one or more of the following flags when using the `storkctl create schedulepolicy` command based on your specific requirements:

note

During migration, you can disregard concerns related to the `retain` and `force-full-snapshot-day` flags. These flags are primarily used in backup operations that involve scheduling.

FlagDescriptionTypeDefault value

`--date-of-month`Specify the date of the month when Stork should trigger the operation.int1

`--day-of-week`Specify the day of the week when Stork should trigger the operation. You can use both the abbreviated or the full name of the day of the week.stringSunday

`--force-full-snapshot-day`For daily scheduled backup operations, specify on which day to trigger a full backup.stringMonday

`-h`, `--help`Help for schedule policy

`-i`, `--interval-minutes`Specify the interval, in minutes, after which Stork should trigger the operation.int30

`-t`, `--policy-type`Select Type of schedule policy to apply. Interval / Daily / Weekly / Monthly.stringInterval

`retain`Specify how many backups triggered as part of this schedule should be retained.intEach schedule policy type has its own default value for this flag:

- interval-based: 10

- daily: 30

- weekly: 7

- monthly: 12

`--time`Specify the time of the day in the 12 hour AM/PM format, when Stork should trigger the operation.string12:00AM

## Delete SchedulePolicy​

You can delete a schedule policy using the following command:

```

storkctl delete schedulepolicy <policy-name>

```

Example:

```

storkctl delete schedulepolicy mypolicy

```

This command examines whether the schedule policy named `mypolicy` is being used by any other resources, specifically by checking for dependencies with resources like Migration Schedules, Application Backup Schedules, or Volume Snapshot Schedules. If the schedule policy is currently in use by any of the mentioned resources, the deletion process is halted, and an appropriate error message is displayed. The error message also lists all the resources it is being used by, so that you can delete those resources:

```

error: cannot delete the schedule policy mypolicy.

The resource is linked to -> Migration Schedules : default/mypolicy

```

where, `default` is the namespace and `mypolicy` is the resource name (MigrationSchedule here).

In this topic:
