# License operations using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/license (Portworx Enterprise latest)

License operations using pxctl | Portworx Enterprise Documentation

This document explains how to manage your Portworx licenses with `pxctl license`. The CLI lets you add, activate, and transfer licenses. It also gives details about the installed licenses, and it shows what features are available within a given license.

Run the `pxctl license` command with the `--help` flag to list the available subcommands and flags.

## List available licenses​

You can use `pxctl license list` to list installed licenses as follows:

```

pxctl license list

```

```

DESCRIPTION				ENABLEMENT	ADDITIONAL INFO

Number of nodes maximum			1000

Number of volumes maximum		100000

Volume capacity [TB] maximum		  40

Storage aggregation			 yes

Shared volumes				 yes

Volume sets				 yes

BYOK data encryption			 yes

Resize volumes on demand		 yes

Snapshot to object store [CloudSnap]	 yes

Cluster-level migration [Kubemotion]	 yes

Bare-metal hosts			 yes

Virtual machine hosts			 yes

Product SKU				Trial		expires in 6 days, 12:13

LICENSE EXPIRES: 2019-04-07 23:59:59 +0000 UTC

For information on purchase, upgrades and support, see

https://docs.portworx.com/knowledgebase/support.html

```

As you can see, the command gives details on the features allowed under the current licenses and it also lists the SKU.

## Activate a license​

The easiest way to activate a license is to get an activation id from Portworx, Inc.. Next, run the following command on your Portworx node:

```

pxctl license activate <activation-id>

```

note

You can also execute the `pxctl license activate` command inside a Pod as follows:

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl license activate <activation-id>

```

However, there are cases where the servers are configured without access to the Internet. Such customers should request an offline-activation license file, and install it like this:

```

pxctl license add <license file>

```

## Connect to a license server​

You can connect a Portworx cluster to a license server using the `pxctl license setls` command.

info

To establish a connection with the license server, it is essential to use the original configuration of the main license server in the `pxctl license setls` command. This means providing either its IP addresses or hostnames, as initially set up. For reliability, avoid using load balancers, virtual IPs, or alternating between IP addresses and symbolic hostnames.

To see the list of available flags and example usage, enter the `--help` flag.

Connect your Portworx cluster to a license server by entering the `pxctl license setls` command with the following:

- Optional: The `--add` option with a comma delimited list of additional feature licenses you want to add. This will add any of the specified feature licenses, as long as the license server has enough available feature license seats.

- The license server endpoint.

```

pxctl license setls --add <feature-license>,<feature-license> <license-server-endpoint>

```

In this topic:
