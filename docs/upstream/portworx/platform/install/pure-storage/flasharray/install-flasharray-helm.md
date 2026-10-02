# Installation of Portworx with FlashArray using Helm

Source: https://docs.portworx.com/portworx-enterprise/platform/install/pure-storage/flasharray/install-flasharray-helm (Portworx Enterprise 3.6)

Installation of Portworx with FlashArray using Helm | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This page provides step-by-step instructions for deploying Portworx Enterprise with FlashArray as the backend storage using Portworx Helm charts.

The following collection of tasks describe how to install Portworx with FlashArray:

Complete all the tasks to install Portworx.

## Prerequisites​

- Ensure that system requirements are met.

- Ensure your Kubernetes cluster is configured to use FlashArray. For more information, see Prepare your Environment for Installing Portworx Enterprise with FlashArray.

- Ensure you have Helm 3.x (3.18.0 or later) installed on the client machine. For information about installing Helm, see Installing Helm.

- Review the Helm compatibility matrix and the configurable parameters.

## Deploy Portworx​

For this example we will deploy Portworx in the `portworx` namespace. If you want to install it in a different namespace, use the `-n <px-namespace>` flag.

-
To install Portworx, add the `portworx/helm` repository to your local Helm repository.

```

helm repo add portworx https://raw.githubusercontent.com/portworx/helm/master/stable/

```

```

"portworx" has been added to your repositories

```

-
Verify that the repository has been successfully added.

```

helm repo list

```

```

NAME    	URL

portworx	https://raw.githubusercontent.com/portworx/helm/master/stable/

```

-
Create a `px_install_values.yaml` file and add the following parameters.

- `openshiftInstall` – Set to `true` to install Portworx Enterprise on OpenShift Container Platform (OCP).

- Environment variable `PURE_FLASHARRAY_SAN_TYPE` – Set based on the SAN protocol used to connect to FlashArray. Possible values are:

- ISCSI

- NVMEOF-RDMA

- NVMEOF-TCP

- FC

```

openshiftInstall: true

drives: size=150

envs:

- name: PURE_FLASHARRAY_SAN_TYPE

  value: ISCSI

```

-
In many cases, you may want to customize Portworx configurations, such as enabling monitoring or specifying specific storage devices. You can pass the custom configuration to the `px_install_values.yaml` yaml file.

note

- You can refer to the Portworx Helm chart parameters for a list of configurable parameters and values.yaml file for configuration file template.

- The default clusterName is `mycluster`. However, it's recommended to change it to a unique identifier to avoid conflicts in multi-cluster environments.

-
Install Portworx using the following command:

note

To install a specific version of Helm chart, you can use the `--version` flag. Example: `helm install <px-release> portworx/portworx --version <helm-chart-version>`.

```

helm install <px-release> portworx/portworx -n <portworx> -f px_install_values.yaml --debug

```

-
You can check the status of your Portworx installation.

```

helm status <px-release> -n portworx

```

```

NAME: px-release

LAST DEPLOYED: Thu Sep 26 05:53:17 2024

NAMESPACE: portworx

STATUS: deployed

REVISION: 1

TEST SUITE: None

NOTES:

Your Release is named "px-release"

Portworx Pods should be running on each node in your cluster.

Portworx would create a unified pool of the disks attached to your Kubernetes nodes.

No further action should be required and you are ready to consume Portworx Volumes as part of your application data requirements.

```

## Update Portworx configuration​

If you need to update the configuration of Portworx, you can modify the parameters in the `px_install_values.yaml` file specified during the Helm installation. This allows you to change the values of configuration parameters.

-
Create or edit the `px_install_values.yaml` file to update the desired parameters.

```

vim px_install_values.yaml

```

```

monitoring:

    telemetry: false

    grafana: true

```

-
Apply the changes using the following command:

```

helm upgrade <px-release> portworx/portworx -n <portworx> -f px_install_values.yaml

```

```

Release "px-release" has been upgraded. Happy Helming!

NAME: px-release

LAST DEPLOYED: Thu Sep 26 06:42:20 2024

NAMESPACE: portworx

STATUS: deployed

REVISION: 2

TEST SUITE: None

NOTES:

Your Release is named "px-release"

Portworx Pods should be running on each node in your cluster.

Portworx would create a unified pool of the disks attached to your Kubernetes nodes.

No further action should be required and you are ready to consume Portworx Volumes as part of your application data requirements.

```

-
Verify that the new values have taken effect.

```

helm get values <px-release> -n <portworx>

```

You should see all the custom configurations passed using the `px_install_values.yaml` file.

## What to do next​

Create a PVC:

- For FlashArray cloud drives, see Create your first PVC.

- For FlashArray Direct Access volumes, see Configure FlashArray as a Direct Access volume.

In this topic:
