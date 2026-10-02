# Enable IPv6 support in Portworx

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/ipv6 (Portworx Enterprise 3.6)

Enable IPv6 support in Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports IPv6 networking for Kubernetes deployments. Portworx also supports KubeVirt VMs with IPv6 networking. This page provides guidance on supported platforms and known limitations. Use this information to ensure compatibility and optimal functionality in environments that require IPv6.

## Supported platforms​

Portworx supports IPv6 on Red Hat OpenShift versions 4.15 or later on bare metal.

## IPv6 limitations​

The following features are not supported when using IPv6:

- Portworx installation behind a proxy

- Portworx Central License Server

- Portworx Backup

- Asynchronous and synchronous disaster recovery (DR)

By default, Portworx uses IPv6 if the network interfaces it uses (for example, `dataInterface` and `mgmtInterface`) are configured with only an IPv6 address.

If the host uses a dual-stack configuration, you must explicitly configure Portworx to use IPv6. To configure IPv6 as the preferred network IP address, set the following environment variable in the `StorageCluster` specification:

```

env:

  - name: PX_PREFER_IPV6_NETWORK_IP

    value: "true"

```

In this topic:
