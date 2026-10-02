# Secure Boot for Portworx Enterprise

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/secure-boot (Portworx Enterprise latest)

Secure Boot for Portworx Enterprise | Portworx Enterprise Documentation

UEFI Secure Boot allows only signed and trusted kernel modules to load during system boot. When you enable Secure Boot, the system validates modules using enrolled certificates. Although optional, enabling Secure Boot adds an extra layer of security by verifying module authenticity before loading.

note

Secure Boot is supported only with Portworx Enterprise version 3.6.0 or later.

Portworx Enterprise kernel modules are signed and compatible with Secure Boot. To run Portworx Enterprise with Secure Boot enabled, you must manually enroll the Portworx Enterprise signing certificate into the system’s Machine Owner Key (MOK) list. You perform this process once per node before installing Portworx Enterprise to ensure that the kernel recognizes and allows Portworx Enterprise modules to load successfully.

After you enroll the certificate, it persists on the node across reboots, kernel upgrades, and OS updates. You must repeat the enrollment process for any new nodes added to the cluster.

note

-
Portworx Enterprise supports only RHEL, RHCOS, and Ubuntu worker nodes for Secure Boot.

-
Portworx Enterprise does not automate enrolling the signing certificate into the system’s MOK list. You must complete the steps manually using the VM or host console.

-
Portworx Secure Boot signing certificates have a default validity of 10 years. Portworx Enterprise raises a cluster-wide alert `SecureBootCertExpiring`, 180 days before the certificate expires. You can view the alert by running:

```

pxctl alerts show -t cluster

```

```

Type     ID                      Resource           Severity  Count  LastSeen                  FirstSeen                 Description

CLUSTER  SecureBootCertExpiring  instant-tb-314227  WARN      3      Feb 25 20:35:51 UTC 2026  Feb 25 17:55:19 UTC 2026  Portworx secure boot certificate will expire in 180 days (expiration date: 2026-08-24). Please renew the certificate soon.

```

At that time, Portworx begins publishing kernel modules signed with both the existing certificate and a new certificate to ensure a smooth transition. If the existing certificate expires and the new certificate is not enrolled, Secure Boot-enabled systems fail to load Portworx kernel modules, and Portworx Enterprise installation or upgrade fails. To avoid service disruption, you must manually enroll the new certificate using `mokutil`.

## Prerequisites​

Ensure that your cluster meets the following requirements before you deploy Portworx Enterprise on Secure Boot-enabled clusters.

- Enable Secure Boot in your system's BIOS or UEFI firmware settings. For more information, see your hardware manufacturer or cloud provider documentation on enabling Secure Boot.

## Enroll the Portworx Secure Boot certificate​

Before you install or upgrade Portworx Enterprise on a Secure Boot enabled system, you must manually enroll the Portworx Secure Boot signing certificate.

warning

Ensure that you have access to the BIOS (for example, via VGA, serial, or out-of-band (OOB) management) before starting this procedure. You must interrupt the boot process during early boot (before the Linux kernel starts), typically during the GRUB boot phase, to complete the MOK enrollment steps.

Optional: VM Template-Based Enrollment (Recommended for Virtualized Environments)

If you deploy Portworx Enterprise on a virtualized platform, enroll the Secure Boot certificate in a golden VM template by following this procedure. You need to complete this step only once. All virtual machines cloned from the template automatically inherit the enrolled certificate, eliminating the need to enroll it on each node.

In virtualized environments, UEFI Secure Boot keys (PK, KEK, DB) are stored in the VM firmware (NVRAM). When you convert a VM into a template, the Secure Boot database is preserved. New VMs deployed from the template inherit the same trusted certificates.

If the Secure Boot issuing certificate (`portworx-public.der`) is replaced or renewed, update the template with the new certificate before deploying additional VMs.

-
Ensure that your server has secure boot enabled:

```

# sudo mokutil --sb-state

```

If secure boot is enabled, you should see an output similar to:

```

SecureBoot enabled

```

-
Download the Portworx Secure Boot certificate.

```

# wget https://mirrors.portworx.com/build-results/pxfuse/certs/<certificate-directory>/portworx-public.der

```

Replace `<certificate-directory>` with the directory that you want to download the certificate from.

note

Portworx by Everpure recommends using the latest certificate available in the most recent year directory.

-
Enroll the signing certificate in the system’s MOK list:

```

# sudo mokutil --import portworx-public.der

```

The system prompts you to set a temporary password. You must enter this password during early boot (before the Linux kernel starts) to complete the MOK enrollment.

-
Reboot the system. The Shim UEFI key management utility starts during the system startup.

tip

You have approximately 10 seconds to respond to the MOK prompt during boot.

-
Select Enroll MOK.

-
Select Continue.

-
Select Yes and enter the password you provided in Step 2. The key is imported into the system’s firmware.

-
Select Reboot.

-
Verify that the Portworx Secure Boot signing certificate has been enrolled on the rebooted node:

```

# sudo keyctl list %:.platform

```

You should see an output similar to:

```

1 key in keyring:

...

539287833: ---lswrv     0     0 asymmetric: Pure Storage, Inc.: Portworx Secure Boot CA @2025: 255a9319658e380873b864b1b22460ed18676cf8

```

In this topic:
