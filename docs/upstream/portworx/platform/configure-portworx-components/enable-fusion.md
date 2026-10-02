# Enable Portworx Fusion Controller

Source: https://docs.portworx.com/portworx-enterprise/platform/configure-portworx-components/enable-fusion (Portworx Enterprise latest)

Enable Portworx Fusion Controller | Portworx Enterprise Documentation

Portworx Fusion Controller provides a unified, application-aware platform that combines Everpure Fusion’s fleet-level management with Portworx’s Kubernetes-native data services. It is supported only on clusters deployed on the Everpure FlashArray storage platform running OpenShift Container Platform (OCP).

After you enable Portworx Fusion Controller:

- The Fusion Controller uses the secret that contains the Fusion Coordinator endpoint and required LDAP credentials to connect to the Fusion Coordinator.

- Portworx Enterprise automatically synchronizes Fusion presets and exposes them as Kubernetes `StorageClass` objects.

- You can reference these storage classes when provisioning volumes or creating virtual machines.

For information on how to enable Portworx Fusion Controller, see Portworx Fusion Controller Documentation.
