# Portworx Support Policy for RHEL-qualified Distributions and Kernels

Source: https://docs.portworx.com/portworx-enterprise/support/kernels-distros-support-policy (Portworx Enterprise latest)

Portworx Support Policy for RHEL-qualified Distributions and Kernels | Portworx Enterprise Documentation

Portworx tests and certifies its software on a broad range of Linux distributions and kernel versions to ensure optimal functionality, stability, and performance. This policy outlines the support model for Linux kernel versions to provide a consistent and secure experience.

For an up-to-date list of supported Linux kernel versions, see the Supported Kernels page. This page lists validated kernel versions across supported Linux distributions and is updated regularly as kernel support evolves.

important

Portworx by Everpure recommends upgrading to a supported release to benefit from the latest kernel compatibility and enhancements.

## Supported Kernel Versions​

Portworx supports Linux kernel versions that are actively maintained by their respective Linux distributions and have not reached end of life (EOL).

Portworx maintains compatibility with newly released kernel versions in recent product releases and extended maintenance releases (EMRs). This approach ensures kernel compatibility without compromising quality or stability.

Portworx supports a newly released kernel version in:

- The latest Portworx version

- The most recent Extended Maintenance Release (EMR), if it differs from the latest version.
 For information on EMR versions, see Portworx Enterprise Life Cycle Support Policy.

note

Portworx Enterprise 3.4 is the first EMR version to follow this model.

## Limitations​

Portworx does not backport support for new kernel versions to earlier Portworx versions other than the most recent Extended Maintenance Release (EMR). To maintain kernel compatibility, upgrade to a supported version.

## Kernel Update Categories and Support Timelines​

Portworx distinguishes between minor patch updates and major kernel version updates when determining support timelines.

For example, a Red Hat Enterprise Linux (RHEL) kernel version may appear as `5.14.0-503.40.1.el9_5`.

### Minor patch and security updates​

- Definition: Updates that change only the `.M.P.elA_B` portion of the kernel version.
 For example, `5.14.0-503.40.1.el9_5` to `5.14.0-503.41.1.el9_5`

- Support timeline: Portworx aims to validate and support these within 14 days, assuming no Portworx-level changes are required.

- Availability: Supported kernel versions are available on the Portworx mirrors page.

### Major kernel updates requiring a Portworx release​

- Definition: Updates where the `X.Y.Z-NNN` portion changes, indicating a major kernel revision.
 For example,`5.14.0-503.40.1.el9_5` to `5.14.0-504.1.1.el9_6`

- Support timeline: Portworx typically supports major kernel updates within 8 to 12 weeks, as these require a new release.

## Appendix: Understanding RHEL kernel versioning​

Red Hat Enterprise Linux (RHEL) kernel versions follows the format: `X.Y.Z-NNN.M.P.elA_B`.

ComponentDescriptionExample (5.14.0-503.40.1.el9_5)

Upstream Kernel Version (X.Y.Z)The base Linux mainline kernel version5.14.0

Package Release/Build Iteration (-NNN.M.P)Red Hat's internal build iteration that includes bug fixes, patches, and enhancements503.40.1

Enterprise Linux Version Tag (.elA_B)RHEL major release and update streamel9_5

In this topic:
