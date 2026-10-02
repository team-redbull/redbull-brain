# Upgrade Portworx using Helm on FlashArray and OCP vSphere

Source: https://docs.portworx.com/portworx-enterprise/platform/upgrade/upgrade-portworx-helm (Portworx Enterprise latest)

Upgrade Portworx using Helm on FlashArray and OCP vSphere | Portworx Enterprise Documentation

This page provides instructions on how to upgrade Portworx using Helm.

note

Upgrading from previous Portworx Helm chart version to 4.0.0 is not supported.

## Prerequisites​

- You must have installed Portworx using Helm.

- Review the release notes for the version you plan to upgrade to. This ensures you are aware of any breaking changes, new features, and deprecated configurations.

- Portworx Enterprise Release Notes

- Portworx Operator Release Notes

- Portworx Stork Release Notes

- Portworx Autopilot Release Notes

- Review the Helm compatibility matrix and the configurable parameters.

## Upgrade Portworx​

By default, Portworx is installed in the `kube-system` namespace. If you have installed it in a different namespace, use the `-n <namespace>` flag. In this example, we will upgrade Portworx that was installed in the `portworx` namespace.

-
Download the latest Portworx Helm chart version from the `portworx/helm` repository to your local repository:

```

helm repo update

```

```

Hang tight while we grab the latest from your chart repositories...

...Successfully got an update from the "portworx" chart repository

Update Complete. ⎈Happy Helming!⎈

```

-
If you have installed Portworx with custom configuration and need to change any configuration parameters, update your `px_install_values.yaml` file. This file contains your current configuration.

note

Ensure that you review the configuration values for the new version to align with any changes in the latest release.

-
Upgrade Portworx using the following command:

```

helm upgrade <px-release> portworx/portworx -n <portworx> -f px_install_values.yaml

```

```

Release "px-release" has been upgraded. Happy Helming!

NAME: px-release

LAST DEPLOYED: Thu Sep 26 06:51:46 2024

NAMESPACE: portworx

STATUS: deployed

REVISION: 3

TEST SUITE: None

NOTES:

Your Release is named "px-release"

Portworx Pods should be running on each node in your cluster.

Portworx would create a unified pool of the disks attached to your Kubernetes nodes.

No further action should be required and you are ready to consume Portworx Volumes as part of your application data requirements.

```

-
Verify the Helm release values to ensure they reflect the updated configuration:

```

helm get values <px-release> -n <portworx>

```

You should see all the custom configurations passed using the `px_install_values.yaml` file.

In this topic:
