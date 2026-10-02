# Manage snapshot schedule policies using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/sched-policy (Portworx Enterprise 3.6)

Manage snapshot schedule policies using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Overview​

This document explains how to manage your snapshot schedule policies using the `pxctl` command-line tool. Run the `pxctl sched-policy` command with the `--help` flag to list the available subcommands and flags.

### Create a schedule policy​

To create a snapshotting policy, use the `pxctl sched-policy create` command. Run the `pxctl sched-policy create` command with the `--help` flag to list the available subcommands and flags.

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

### List schedule policies​

Run the following command to list your schedule policies:

```

pxctl sched-policy list

```

```

Policy	Description

p1		periodic 1h0m0s,keep last 5, weekly Sunday@12:00,keep last 4

```

### Update schedule policies​

To update a schedule policy, use the `pxctl sched-policy update` command. Run the `pxctl sched-policy update` command with the `--help` flag to list the available subcommands and flags.

Continuing our previous example with the `p1` schedule policy, let's make it so that our policy creates periodic backups every 120 minutes instead of 60:

```

pxctl sched-policy update --periodic 120,5 --weekly sunday@12:00,4 p1

```

Now, let's make sure our new settings are applied:

```

pxctl sched-policy list

```

```

Policy	Description

p1		periodic 2h0m0s,keep last 5, weekly Sunday@12:00,keep last 4

```

### Delete a schedule policy​

To delete a schedule policy, run the `pxctl sched-policy delete` command with the name of the policy you want to delete as a parameter:

```

pxctl sched-policy delete p1

```

In this topic:
