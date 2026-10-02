# SchedulePolicy CRD reference

Source: https://docs.portworx.com/portworx-enterprise/reference/crd/schedulepolicies (Portworx Enterprise latest)

SchedulePolicy CRD reference | Portworx Enterprise Documentation

SchedulePolicy represents a policy for executing actions on a schedule.

## SchedulePolicy​

FieldDescriptionType

`apiVersion`APIVersion defines the versioned schema of this representation of an object.
Servers should convert recognized schemas to the latest internal value, and
may reject unrecognized values.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources`string`

`kind`Kind is a string value representing the REST resource this object represents.
Servers may infer this from the endpoint the client submits requests to.
Cannot be updated.
In CamelCase.
More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds`string`

`policy`Policy`object`

### `policy` fields​

FieldDescriptionType

`policy.daily`Daily policy that will be triggered daily at a specified time`object`

`policy.daily.forceFullSnapshotDay`ForceFullSnapshotDay specifies day of the week for full snapshot to take place`string`

`policy.daily.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.daily.retain`Retain Number of objects to retain for daily policy. Defaults to
@DefaultDailyPolicyRetain`integer`

`policy.daily.time`Time when the policy should be triggered. Expected format is
time.Kitchen eg 12:04PM or 12:04pm`string`

`policy.interval`Interval policy that will be triggered at the specified interval`object`

`policy.interval.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.interval.retain`Retain Number of objects to retain for interval policy. Defaults to
@DefaultIntervalPolicyRetain`integer`

`policy.monthly`Monthly policy that will be triggered on the specified date of the month
at the specified time`object`

`policy.monthly.date`Date of the month when the policy should be triggered. If a given date
doesn't exist in a month, it will be skipped. For example, if 30 is specified,
it'll be skipped in February.
This field is used when SelectiveMonthlyPolicy and RelativeMonthlyPolicy are not set (legacy behavior)`integer`

`policy.monthly.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.monthly.relativeMonthlyPolicy`RelativeMonthlyPolicy allows triggering on specific weekday of specific week
For example: "First Monday", "Last Friday", "Third Wednesday"
If SelectiveMonthlyPolicy is not set and this is set, this takes precedence over legacy Date/Time/Retain fields`object`

`policy.monthly.relativeMonthlyPolicy.day`Day of the week when the policy should be triggered. Only one day can be specified.
Valid values are: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
(case-insensitive, abbreviated forms like Sun, Mon also work)`string`

`policy.monthly.relativeMonthlyPolicy.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.monthly.relativeMonthlyPolicy.retain`Retain Number of objects to retain for relative monthly policy. Defaults to
@DefaultMonthlyPolicyRetain`integer`

`policy.monthly.relativeMonthlyPolicy.time`Time when the policy should be triggered. Expected format is
time.Kitchen eg 12:04PM or 12:04pm`string`

`policy.monthly.relativeMonthlyPolicy.weeklyIndex`WeeklyIndex specifies which occurrence of the day in the month
1 = First, 2 = Second, 3 = Third, 4 = Fourth, 5 = Last`integer`

`policy.monthly.retain`Retain Number of objects to retain for monthly policy. Defaults to
@DefaultMonthlyPolicyRetain
This field is used when SelectiveMonthlyPolicy and RelativeMonthlyPolicy are not set (legacy behavior)`integer`

`policy.monthly.selectiveMonthlyPolicy`SelectiveMonthlyPolicy allows triggering on specific months only
If set, this takes precedence over RelativeMonthlyPolicy and legacy Date/Time/Retain fields`object`

`policy.monthly.selectiveMonthlyPolicy.date`Date of the month when the policy should be triggered. If a given date
doesn't exist in a month, it will be skipped. For example, if 30 is specified,
it'll be skipped in February.`integer`

`policy.monthly.selectiveMonthlyPolicy.months`Months specify the list of months on which schedule needs to be taken.
If it is empty, the schedule will be taken on every month of the year.
Valid values are: January, February, March, April, May, June, July,
August, September, October, November, December (case-insensitive)
Example: "January,March,June,December" or "jan,mar,jun,dec"`string`

`policy.monthly.selectiveMonthlyPolicy.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.monthly.selectiveMonthlyPolicy.retain`Retain Number of objects to retain for selective monthly policy. Defaults to
default value 12`integer`

`policy.monthly.selectiveMonthlyPolicy.time`Time when the policy should be triggered. Expected format is
time.Kitchen eg 12:04PM or 12:04pm`string`

`policy.monthly.time`Time when the policy should be triggered. Expected format is
time.Kitchen eg 12:04PM or 12:04pm
This field is used when SelectiveMonthlyPolicy and RelativeMonthlyPolicy are not set (legacy behavior)`string`

`policy.weekly`Weekly policy that will be triggered on the specified day of the week at
the specified time`object`

`policy.weekly.biweekly`Biweekly indicates if the policy should trigger once every two weeks
instead of every week. When true, the policy triggers on the specified
days in active weeks and skips all days in inactive weeks.`boolean`

`policy.weekly.day`Day of the week when the policy should be triggered. Valid format are
specified in `Days` above`string`

`policy.weekly.options`Options to be passed in to the driver. These will be passed in
to the object being triggered`object`

`policy.weekly.retain`Retain Number of objects to retain for weekly policy. Defaults to
@DefaultWeeklyPolicyRetain`integer`

`policy.weekly.time`Time when the policy should be triggered. Expected format is
time.Kitchen eg 12:04PM or 12:04pm`string`

## SchedulePolicy examples​

### Interval SchedulePolicy​

An interval `SchedulePolicy` includes the following fields and values:

-
apiVersion: the version of the Stork scheduler (this example uses `stork.libopenstorage.org/v1alpha1`)

-
kind: as `SchedulePolicy`

-
metadata.name: the name of the `SchedulePolicy` object (this example uses `testpolicy`)

-
policy.interval.intervalMinutes: the interval, in minutes, after which Portworx triggers the operation (this example triggers the operation every minute)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: testpolicy

policy:

  interval:

    intervalMinutes: 1

```

### Daily SchedulePolicy​

A daily `SchedulePolicy` includes the following fields and values:

-
apiVersion: the version of the Stork scheduler (this example uses `stork.libopenstorage.org/v1alpha1`)

-
kind: as `SchedulePolicy`

-
metadata.name: the name of the `SchedulePolicy` object (this example uses `testpolicy`)

-
policy.daily.time: the time of the day when Portworx will trigger the operation (this example triggers the operation every day at 10:14 PM)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: testpolicy

policy:

  daily:

    time: "10:14PM"

```

### Weekly SchedulePolicy​

A weekly `SchedulePolicy` includes the following fields and values:

-
apiVersion: the version of the Stork scheduler (this example uses `stork.libopenstorage.org/v1alpha1`)

-
kind: as `SchedulePolicy`

-
metadata.name: the name of the `SchedulePolicy` object (this example uses `testpolicy`)

-
policy.weekly.day: the day of the week when Portworx will trigger the operation (this example triggers the operation every Thursday)

-
policy.weekly.time: the time of the day when Portworx will trigger the operation (this example triggers the operation at 10:13 PM)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: testpolicy

policy:

  weekly:

    day: "Thursday"

    time: "10:13PM"

```

### Monthly SchedulePolicy​

A monthly `SchedulePolicy` includes the following fields and values:

-
apiVersion: the version of the Stork scheduler (this example uses `stork.libopenstorage.org/v1alpha1`)

-
kind: as `SchedulePolicy`

-
metadata.name: the name of the `SchedulePolicy` object (this example uses `testpolicy`)

-
policy.monthly.day: the day of the month when Portworx will trigger the operation (this example triggers the operation on the 14th of every month)

-
policy.monthly.time: the time of the day when Portworx will trigger the operation (this example triggers the operation at 8:05 PM)

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: SchedulePolicy

metadata:

  name: testpolicy

policy:

  monthly:

    date: 14

    time: "8:05PM"

```

In this topic:
