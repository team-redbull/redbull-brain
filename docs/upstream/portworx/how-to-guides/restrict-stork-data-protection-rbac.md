# Run Portworx with Restricted RBAC

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/restrict-stork-data-protection-rbac (Portworx Enterprise 3.6)

Run Portworx with Restricted RBAC | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx supports restricted RBAC mode for storage-only deployments that do not require data protection capabilities such as application backups, restores, migrations, and disaster recovery. With this feature, you can run Portworx with minimal cluster-wide permissions to meet security compliance and least-privilege requirements.

By default, the Portworx Operator and Stork use broad RBAC permissions that rely on wildcard rules to support all Portworx features. On OpenShift Container Platform, this also includes the Cache Agent used by the OpenShift Dynamic Plugin. When you configure restricted permissions, the ClusterRoles for these components use specific rules instead of wildcard rules. This change disables data protection workflows, including backups, restores, migrations, and disaster recovery, and limits Stork to scheduling and monitoring operations. As a result, you can’t use Portworx Backup and DR if you run Stork with restricted RBAC.

When the operator runs with restricted permissions, all components that the operator manages, including Stork and the Cache Agent, are automatically limited by the operator's permissions. The operator can't grant any component permissions that exceed its own. Portworx generates Kubernetes events on the StorageCluster resource to indicate RBAC configuration status:

- `DataProtectionRBACRestricted`: Occurs when `spec.stork.restrictDataProtectionRBAC` is `true`. This confirms that Stork (and, on OpenShift, the Cache Agent) is running with restricted RBAC, and data protection features aren’t available.

- `DataProtectionRBACMisconfigured`: Occurs when the Operator ClusterRole lacks wildcard permissions, but `spec.stork.restrictDataProtectionRBAC` is `false`. This mismatch causes Stork (and, on OpenShift, the Cache Agent) to run in restricted mode, even though the configuration requests full permissions. To avoid this warning, ensure that the Operator ClusterRole has wildcard permissions if you want these components to run with full permissions, or set `spec.stork.restrictDataProtectionRBAC` to `true`.

The operator ClusterRole isn't reconciled automatically. You must manually update the operator ClusterRole to change permission levels.

important

- OpenShift Container Platform: Restricted RBAC is supported for Stork and the Cache Agent. The Portworx Operator runs with broad permissions.

- Other platforms: Both the Portworx Operator and Stork can run with restricted RBAC. The Cache Agent doesn't apply to these platforms.

## Prerequisites​

Make sure you're running:

- Portworx Operator version 26.1.0 or later.

- Portworx Enterprise version 3.4.3 or later.

## Configure restricted RBAC​

Complete the following steps to enable restricted RBAC for your Portworx deployment.

### Fresh installations​

Use Portworx Central to generate a deployment specification that enables restricted RBAC.

- Other Platforms

- OpenShift Container Platform

When generating the Portworx specification using Portworx Central, enable the Restrict Data Protection RBAC option in Customize > Deployment > Component Settings. This configuration:

- Generates the operator specification with a restricted ClusterRole that uses specific rules instead of wildcard permissions.

- Sets `spec.stork.restrictDataProtectionRBAC: true` in the StorageCluster resource.

For complete installation instructions, see the installation guide for your platform.

When generating the Portworx specification using Portworx Central, enable the Restrict Data Protection RBAC option in Customize > Deployment > Component Settings. This configuration sets `spec.stork.restrictDataProtectionRBAC: true` in the StorageCluster resource to restrict Stork and Cache Agent RBAC.

For complete installation instructions, see the installation guide for your platform.

### Existing installations​

Update your existing Portworx deployment to enable restricted RBAC.

- Other Platforms

- OpenShift Container Platform

-
Extract the restricted Operator ClusterRole rules from the Portworx installer endpoint by running the following command:

```

curl -s "https://install.portworx.com/<version>?comp=pxoperator&kbver=<k8s-version>&ns=portworx&rdpr=true" | \

  yq eval-all 'select(.kind == "ClusterRole" and .metadata.name == "portworx-operator") | .rules'

```

Replace:

- `<version>` with your Portworx version (for example, `3.6.0`).

- `<k8s-version>` with your Kubernetes version (for example, `1.31.0`).

-
Edit the existing `portworx-operator` ClusterRole and replace the `rules` section with the rules you extracted in the previous step:

```

kubectl edit clusterrole portworx-operator

```

After you save the changes, the operator ClusterRole is updated to restricted mode.

-
Edit your StorageCluster resource:

```

kubectl edit storagecluster -n portworx

```

-
Add the `spec.stork.restrictDataProtectionRBAC` field:

```

spec:

  stork:

    enabled: true

    restrictDataProtectionRBAC: true

```

After you save the changes, the Portworx Operator automatically updates the Stork ClusterRole to restricted mode.

Complete the following steps to enable restricted RBAC for Stork and the Cache Agent:

-
Edit your StorageCluster resource:

```

kubectl edit storagecluster -n portworx

```

-
Add the `spec.stork.restrictDataProtectionRBAC` field:

```

spec:

  stork:

    enabled: true

    restrictDataProtectionRBAC: true

```

-
Save the changes.

The Portworx Operator automatically updates the Stork and Cache Agent ClusterRoles to restricted mode.

In this topic:
