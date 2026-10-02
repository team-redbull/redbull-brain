# Portworx Enterprise Life Cycle Support Policy

Source: https://docs.portworx.com/portworx-enterprise/support/support-policy (Portworx Enterprise latest)

Portworx Enterprise Life Cycle Support Policy | Portworx Enterprise Documentation

The Portworx Enterprise Life Cycle Support policy provides customers and partners information to effectively plan, deploy, and maintain their Portworx Enterprise software environments. Our goal is to provide transparency into release numbering, release types, field qualification levels, and support policies. This is intended to provide customers sufficient planning opportunities to effectively maintain operations on the latest supported versions of our software products.

## Release Numbering and Types​

Portworx leverages a three-digit numerical release numbering convention in the X.Y.Z format to identify each version as it progresses through the Product Life Cycle.

The release types and corresponding numbering conventions are listed below:

-
Major Releases: Major Releases are designated when incrementing the X value (X.0.0) and represent changes to platform, deployment methods, and/or market shifting capabilities. (For example, PX-DR was introduced in PX 2.0.0.).

-
Feature Releases: Feature Releases (FR) are the first release after incrementing the Y value (X.Y.0) and include new features, capabilities, and enhancements. (For example, new distro support or new Kubernetes version support may be included as part of such releases.)

-
Maintenance Releases: Maintenance releases are the subsequent releases following a Feature Release and are designated by incrementing the Z value (X.Y.Z). These releases include bug fixes and security patches. New OS/kernel support may be added as part of these releases.

## Release Lifespan​

Maintenance releases are the mechanism by which Portworx continues development for Major and Feature Releases during their lifespan. Each FR and its subsequent maintenance releases are considered a release line. Development on release lines progresses according to the following schedule:

-
Active Development: For a period of ninety (90) days after the initial release of the FR, maintenance releases for bug fixes and security patches will be released via periodic updates.

-
Maintenance Phase: For an additional ninety (90) days following the Active Development phase, maintenance releases will be released only for high-priority bug fixes and critical security advisories. Only critical or high vulnerability fixes will be backported to previous minor or major versions.

-
Extended Maintenance Release: Every year, one release line will be designated as an Extended Maintenance Release (EMR), and maintenance on that release line will extend to eighteen (18) months from the date of the initial Feature Release.

-
End of Life: When maintenance on a release line ends, that release line will be declared End of life (EOL) and no further maintenance is provided. The EOL date for a release line is the extended maintenance end date for an Extended Maintenance Release (EMR). For releases not designated as EMR, the EOL date is the maintenance end date.

## Field Qualification​

All releases go through extensive internal quality and regression testing before being designated ready for General Availability (GA) and supported for customer use.

When maintenance on a release line is concluded, that line will be declared End-of-Life (EOL) and no further maintenance work will be performed.

## Upgrade Recommendations and Support Policy​

Generally, Portworx recommends upgrading on a semi-annual basis to the latest Feature Release line. Once on that release line, to ensure that you have the latest bug fixes and security patches, you should upgrade to the latest Maintenance Release for that line as they are released.

Portworx generally supports the latest release line, two (2) previous feature release lines, and up to two (2) Extended Maintenance Release lines. For a duration of six (6) months every other year, two (2) EMRs will be supported to enable customers to upgrade from the previous EMR to the latest EMR.

While Portworx will declare release lines EOL for development purposes, we will never declare a software release line as end-of-support. Portworx will always attempt to assist any customer operating under a valid support agreement. For customers running on an EOL release, the approaches, tools, and remedies available may be limited. If a customer experiences a problem caused by a software bug or security vulnerability on an EOL release, the only path to remediation may require a software update before the issue can be fully resolved.

The table below summarizes the current supported versions, associated release lifespan phases, and estimated target end dates. Target end dates are subject to change as actual dates are announced in new release communications.

VersionGA dateActive Development end dateMaintenance end dateExtended Maintenance end dateEnd of life dateDocumentation

3.7.nSeptember 08, 2026December 08, 2026March 08, 2027N/AMarch 08, 2027Release Notes
Installation Prerequisites

3.6.nApril 06, 2026July 06, 2026October 06, 2026October 06, 2027October 06, 2027Release Notes
Installation Prerequisites

3.5.nNovember 19, 2025February 19, 2026August 19, 2026N/AAugust 19, 2026Release Notes
Installation Prerequisites

3.4.nSeptember 08, 2025December 08, 2025March 08, 2026March 08, 2027March 08, 2027Release Notes
Installation Prerequisites

3.3.nJune 23, 2025September 23, 2025December 23, 2025N/ADecember 23, 2025Release Notes
Installation Prerequisites

3.2.nOctober 31, 2024January 31, 2025April 30, 2025April 30, 2026April 30, 2026Release Notes
Installation Prerequisites

3.1.nJanuary 31, 2024April 30, 2024July 31, 2024July 31, 2025July 31, 2025Release Notes
Installation Prerequisites

3.0.nJuly 11, 2023October 11, 2023April 30, 2024N/AApril 30, 2024Release Notes
Installation Prerequisites

2.13.nFebruary 23, 2023May 23, 2023August 23, 2023August 23, 2024August 23, 2024Release Notes
Installation Prerequisites

Everpure reserves the right to update this Policy from time to time, as noted by the Last updated date below.

In this topic:
