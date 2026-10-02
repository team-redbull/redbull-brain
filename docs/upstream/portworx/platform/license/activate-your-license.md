# Activate the Enterprise License

Source: https://docs.portworx.com/portworx-enterprise/platform/license/activate-your-license (Portworx Enterprise latest)

Activate the Enterprise License | Portworx Enterprise Documentation

To activate the Enterprise license on your cluster, you either need an activation ID If your cluster is connected to the internet, or you need a license file if your cluster is in an air-gapped environment. Contact the Everpure support team (support@purestorage.com) to obtain this activation ID or license file. To get the license file for an air-gapped environment, you need to provide the cluster UUID to the support team.
 For more information, see:

- Activate your license using an Activation ID

- Activate your license using a license file for an air-gapped cluster

Once applied, the Portworx Enterprise license is locked to a single Portworx cluster via the unique UUID identifier of the cluster. Such a license (or license-file) will not work on other clusters. If needed, you can transfer a valid enterprise license between two Portworx clusters. For more information, Transfer Licenses.

### Activate your license using an Activation ID​

If your cluster is connected to the internet, you can activate the license using an activation ID. This license activation process requires an active internet connection from the Portworx nodes to the license server. The process automatically registers the cluster UUID, and generates and installs the license on the cluster. Upon activating the license on one Portworx node, all the remaining Portworx nodes automatically update to the new license.

-
Use the activation ID provided by the support team, and activate the license:

```

pxctl license activate <your-activation-id>

```

You can also run the pxctl license activate command inside a pod as follows:

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl license activate <activation-id>

```

-
Check the current cluster status again:

```

pxctl status

```

### Activate your license using a license file for an air-gapped cluster​

If your cluster is in an air-gapped environment, you need to provide the cluster UUID to the Everpure support team to obtain a license file.

-
Get your Cluster UUID. The Cluster UUID information is available via pxctl cluster list command.

```

pxctl cluster list

```

```

Cluster ID: MY_FAVORITE_PX_CLUSTER

Cluster UUID: xxxxxxxx-xxxx-xxxx-xxxx-788c89cc40f1

Status: OK [...]

```

Provide this Cluster UUID to the support team, to receive your license file.

-
Upload the license file obtained on one of the Portworx nodes to activate the license, by running the following command:

```

pxctl license add license_file.bin

```

note

The license installation is a non-obtrusive process, which does not interfere with the data stored on the Portworx volumes, nor interrupts the active IO operations.

### Transfer licenses​

You can transfer a valid enterprise license between two Portworx clusters. Both Portworx clusters need to be operational at the time of license transfer. The source cluster must have a valid Portworx Enterprise license, while the destination cluster can have either a valid or expired Trial license or expired Portworx Enterprise license.

License transfer command requires clusterUUID from the source cluster, (available via pxctl cluster list command) and remote Portworx cluster node IP.

```

pxctl license transfer -h

```

```

NAME:

  pxctl license transfer - Transfer license to remote PX cluster

USAGE:

  pxctl license transfer <clusterUUID> <remoteIP>

DESCRIPTION:

  Command swaps licenses between the two Portworx clusters.

  Note that both Portworx clusters need to be operational at the time this

  command is ran.

  The source cluster must have a valid <Variable name='pxEnterprise'/> license, while the

  destination cluster can have either a valid or expired Trial license or expired <Variable name='pxEnterprise'/> license.

EXAMPLE:

  pxctl license transfer xxxxxxxx-xxxx-xxxx-xxxx-eb99128e3270 10.0.15.201

```

note

- The license transfer happens directly between the Portworx clusters, so at least one node from the source cluster must have a network connectivity to a node in the target Portworx cluster.

- After the successful license transfer, the two Portworx clusters swap identities and licenses (for example, Portworx cluster A will have Trial license originally from Portworx cluster B, while the cluster B will have the Portworx Enterprise license originally from cluster A)

For information on purchase, upgrades and support, contact support

## What to do next​

- Enable pay-as-you-go billing

In this topic:
