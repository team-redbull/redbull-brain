# Enable Pure1 integration for upgrades

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/enable-pure1-upgrades (Portworx Enterprise latest)

Enable Pure1 integration for upgrades | Portworx Enterprise Documentation

This page covers enabling Pure1 integration for the following cases:

- You had a running Portworx cluster prior to Portworx 2.8.0, and you are now upgrading to 2.12.0 or later

- You installed Portworx 2.12.0, but did not enable Pure1 integration and want to do so now

## Prerequisites​

- Portworx Operator 1.10.0 or later

- A cluster running Portworx 2.12.0 or using an Operator-based installation

- Outbound access to the internet to allow connection to Pure1

note

If you're using a daemonset-based Portworx installation, you must migrate to an Operator-based install, then:

- If you did not previously enable telemetry for your daemonset-based installation, upgrade to version 2.12 before enabling Pure1 integration.

- If you previously enabled telemetry for your daemonset-based installation, when you migrate that to an Operator-based installation, telemetry is still enabled.

## Enable telemetry​

Telemetry to Pure1 is enabled by default when you generate the StorageCluster spec from Portworx Central, unless you disable it by setting `spec.monitoring.telemetry.enabled` to `false`.

For information about enabling telemetry, see Portworx Telemetry.

In this topic:
