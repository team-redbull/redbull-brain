# Upgrade Portworx Addon for TKGI cluster

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/upgrade-addon-for-tkgi (Portworx Enterprise latest)

Upgrade Portworx Addon for TKGI cluster | Portworx Enterprise Documentation

The Bosh Director ensures that upgrades to Portworx-enabled TKGI clusters are performed with minimal disruption to availability and functionality.

To upgrade your TKGI cluster seamlessly, make sure you are using the latest version of the Portworx add-on. Complete the following steps on a machine with access to the BOSH CLI.

### Check your current Bosh Director addon version​

Run the following to check the current runtime configuration and version:

```

bosh -e <director-environment> runtime-config

```

important

If your addon version is 2.0.0, you can skip the remaining steps and proceed with upgrading your TKGI environment.

### Upload a Portworx release to your Bosh Director environment​

- Clone the `portworx-stop-bosh-release` repositories:

```

git clone https://github.com/portworx/portworx-stop-bosh-release.git

cd portworx-stop-bosh-release

```

- Create the Portworx release with a final version (in this example, version 2.0.0) using the Bosh CLI:

```

mkdir src

bosh create-release --final --version=2.0.0

```

```

1. Verify that version 2.0.0 is included in the runtime config:

 ```bash

 cat master/runtime-configs/director-runtime-config.yaml

```

- Replace `<director-environment>` with your actual environment details and upload the release:

```

bosh -e <director-environment> upload-release

```

### Upgrade the addon on the Bosh Director​

-
Append your existing runtime config with the updated add-on definition from runtime-configs/director-runtime-config.yaml.

-
Update the runtime config in the Director:

```

bosh -e director-environment update-runtime-config runtime-configs/director-runtime-config.yaml

```

### Apply the changes in Tanzu Operations Manager​

After the runtime config is updated, perform the following steps:

- Log in to the Tanzu Operations Manager Interface.

- Go to the Installation Dashboard.

- Click on Review Pending Changes and apply the changes.

caution

If you cleared the Upgrade all clusters errands checkbox under Errands of the Tanzu Kubernetes Grid Integration Edition tile, run the following commands to reconfigure the add-on:

```

bosh manifest -d <deployment-name> >./<deployment-name>-manifest.yaml

bosh -d <deployment-name> deploy ./<deployment-name>-manifest.yaml

```

For all necessary flags for this command, refer to the Deploy details in the Bosh documentation.

### Additional steps for sharedv4 volumes​

If your cluster uses `sharedv4` volumes, ensure that Portworx unmounts them in alignment with Kubernetes add-on checks during upgrades.

-
Set the `BOSH_DEPLOYMENT` environment variable to your Portworx deployment:

```

export BOSH_DEPLOYMENT=<px-deployment-id>

```

-
Run the following script from the `scripts` folder in the `portworx-stop-bosh-release` directory:

```

fix-shared-vol-script.sh

```

After the add-on upgrade is complete, you can proceed to upgrade your TKGI cluster to the desired version.

In this topic:
