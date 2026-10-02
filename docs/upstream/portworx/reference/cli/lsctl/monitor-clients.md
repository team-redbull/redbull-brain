# Monitor clients and licenses

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/lsctl/monitor-clients (Portworx Enterprise 3.6)

Monitor clients and licenses | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can monitor your licenses using the `lsctl` command. The following represent some of the more common monitoring operations you can perform:

- View the nodes using Portworx licenses

- View which individual license features are leased-out to nodes

## View the nodes using Portworx licenses​

Enter the `lsctl client ls` command to list all of the Portworx nodes using licenses from the license server:

```

/opt/pwx-ls/bin/lsctl client ls

```

```

CLUSTER ID                                       NODE ID                               LEASE EXPIRY

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-9c5413128f51  xxxxxxxx-xxxx-xxxx-xxxx-d32e4aa08dae  in 166h52m11s

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-9c5413128f51  xxxxxxxx-xxxx-xxxx-xxxx-838515e01522  in 166h52m11s

```

note

Backup license servers retrieve lease expiration information from the primary license server every 5 minutes. If the lease interval is set to a short period of time, 15 minutes for example, Portworx will refresh the lease more frequently than the backup license server syncs. In this situation, you will see slightly different lease expiration times depending on which license server you run the `lsctl client ls` command on.

## View which individual licenses are leased-out to nodes​

Enter the `lsctl client usage` command to list all of the Portworx nodes using licenses, display what those licenses are, and the number of licenses being consumed by that node:

```

/opt/pwx-ls/bin/lsctl client usage

```

```

CLUSTER ID                                       NODE ID                               LICENSE  COUNT  LEASE EXPIRY

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-9c5413128f51  xxxxxxxx-xxxx-xxxx-xxxx-d32e4aa08dae  Nodes    1      in 166h51m43s

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-9c5413128f51  xxxxxxxx-xxxx-xxxx-xxxx-838515e01522  Nodes    1      in 166h51m43s

```

In this topic:
