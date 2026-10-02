# Configure pre-exec and post-exec rules for Stork migrations

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/migration-pre-post-exec-rule (Portworx Enterprise latest)

Configure pre-exec and post-exec rules for Stork migrations | Portworx Enterprise Documentation

This page explains how to use `pre-exec` and `post-exec` rules with `Stork` migrations.

- A `pre-exec` rule runs before volume migrations and helps create consistent snapshots by pausing writes, flushing logs, or freezing a virtual machine (VM).

- A `post-exec` rule runs after volume snapshots are created and helps applications return to normal operations, for example, resuming writes or unfreezing a VM.

The examples show how to configure rules for a MySQL app and for KubeVirt VMs.

## Pre-exec rule​

Use a `pre-exec` rule to pause writes before migration. This helps ensure the application is in a consistent state when migration begins.

- MySQL

- KubeVirt VM

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: mysql-pre-migration

  namespace: portworx

rules:

  - podSelector:

      app: mysql

    actions:

      - type: command

        background: true

        value: mysql --user=root --password=$MYSQL_ROOT_PASSWORD -Bse 'FLUSH TABLES WITH READ LOCK; SYSTEM ${WAIT_CMD};'

```

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: vm-pre-migration

  namespace: portworx

rules:

  - podSelector:

      vm.kubevirt.io/name: vm-linux

    container: compute

    actions:

      - type: command

        value: /usr/bin/virt-freezer --freeze --unfreezeTimeoutSeconds 30 --name vm-linux --namespace pre-freeze-linux

```

## Post-exec rule​

Use a `post-exec` rule to resume normal application operation after migration. This helps ensure that writes and I/O continue safely on the source cluster.

- MySQL

- KubeVirt VM

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: mysql-post-migration

  namespace: portworx

rules:

  - podSelector:

      app: mysql

    actions:

      - type: command

        value: mysql --user=root --password=$MYSQL_ROOT_PASSWORD -Bse 'FLUSH LOGS; UNLOCK TABLES;'

```

```

apiVersion: stork.libopenstorage.org/v1alpha1

kind: Rule

metadata:

  name: vm-post-migration

  namespace: portworx

rules:

  - podSelector:

      vm.kubevirt.io/name: vm-linux

    container: compute

    actions:

      - type: command

        value: /usr/bin/virt-freezer --unfreeze --name vm-linux --namespace pre-freeze-linux

```

## Migration schedule​

After creating rules, refer to them in a migration schedule.

note

- You can also use `pre-exec` and `post-exec` rules when running a direct migration using storkctl create migration, not only with migration schedules.

- Virtual machine (VM) migration with `pre-exec` and `post-exec` rules might fail if the VM is rebooted while a rule is executing. Subsequent migrations succeed once the VM is back online.

- MySQL

- KubeVirt

```

storkctl create migrationschedule \

  -c <cluster-pair> \

  --namespaces <mysql1> \

  --pre-exec-rule <mysql-pre-migration> \

  --post-exec-rule <mysql-post-migration> \

  <mysql-schedule>

```

```

storkctl create migrationschedule \

  -c <cluster-pair> \

  --namespaces <vm-pod-workloads> \

  --pre-exec-rule <vm-pre-migration> \

  --post-exec-rule <vm-post-migration> \

  <vm-nonvm-schedule>

```

In this topic:
