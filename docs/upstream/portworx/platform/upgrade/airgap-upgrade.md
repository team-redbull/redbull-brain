# Upgrade an Air-Gapped Portworx Cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/upgrade/airgap-upgrade (Portworx Enterprise 3.6)

Upgrade an Air-Gapped Portworx Cluster | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

During installation on an internet-connected Kubernetes cluster, Portworx fetches the resources necessary for installation from the internet automatically. However, while installing Portworx on an air-gapped cluster, you would have to perform an extra step to pre-stage these resources within the air-gapped environment.

Similarly, to upgrade your Portworx installation on an air-gapped cluster, you will fetch updated container images, and then pre-stage them within the air-gapped cluster.

Since Portworx leverages a component of the Kubernetes control plane to make enhanced Kubernetes scheduling decisions based on storage layout, these steps are also required if your cluster's Kubernetes control plane is updated as well.

caution

If you do not perform these pre-staging steps before upgrading either Portworx or Kubernetes on an air-gapped cluster, your pods can enter crash loops and cause service disruptions.

Follow the instructions on this page to get the updated container images, pre-stage them within the air-gapped cluster, and then proceed to upgrade your Portworx installation.

## Prerequisites​

- You must have an existing Portworx Kubernetes cluster that is healthy and operational.

- You should be using the same internal or private container registry as used during the installation.

- Kubernetes platform upgrades: Before you upgrade your OS kernels that require a Kubernetes node reboot, you must update the Portworx file system dependencies to prevent storage nodes from entering a `StorageDown` state after node restarts. For more information, see Update Portworx file system dependencies.

note

To check what registry you are currently using, query your existing StorageCluster by running the following command:

```

STORAGECLUSTER_NAME=$(kubectl -n <px-namespace> get storagecluster -o jsonpath='{.items[0].metadata.name}')

kubectl get stc -n <px-namespace> $STORAGECLUSTER_NAME -o jsonpath='{.spec.image}{"\n"}'

```

## Get the updated container images​

- Kubernetes

- Openshift

-
Set an environment variable for the Kubernetes version that you are using:

```

KBVER=$(kubectl version --short 2>/dev/null | awk -F'[v+_-]' '/Server Version: / {print $3}')

```

-
Set an environment variable to the latest major version of Portworx:

```

PXVER=<portworx-version>

```

note

For the latest Portworx version, see Portworx Release Notes.

-
On an internet-connected host with the same architecture and OS version as the Kubernetes cluster nodes intended for Portworx installation, download the air-gapped installation bootstrap script for the specified Kubernetes and Portworx versions:

```

curl -o px-ag-install.sh -L "https://install.portworx.com/$PXVER/air-gapped?kbver=$KBVER"

```

-
Pull the container images required for the specified versions:

```

sh px-ag-install.sh pull

```

-
Log in to the container registry using the docker command:

```

docker login <your-private-registry>

```

-
Push the container images to the same private container registry that is accessible to your air-gapped nodes. Do not include `http://` in your private registry path:

```

sh px-ag-install.sh push <your-registry-path>

```

For example:

```

sh px-ag-install.sh push myregistry.net:5443

```

For example, to push the new images to a specific repo (consult your StorageCluster definition as per the note in the Prerequisites):

```

sh px-ag-install.sh push myregistry.net:5443/px-images

```

-
Set an environment variable for the Kubernetes version that you are using:

```

KBVER=$(oc version --short 2>/dev/null | awk -F'[v+_-]' '/Server Version: / {print $3}')

```

-
Set an environment variable to the latest major version of Portworx:

```

PXVER=<portworx-version>

```

note

For the latest Portworx version, see Portworx Release Notes.

-
On an internet-connected host with the same architecture and OS version as the Kubernetes cluster nodes intended for Portworx installation, download the air-gapped installation bootstrap script for the specified Kubernetes and Portworx versions:

```

curl -o px-ag-install.sh -L "https://install.portworx.com/$PXVER/air-gapped?kbver=$KBVER"

```

-
Pull the container images required for the specified versions:

```

sh px-ag-install.sh pull

```

-
Log in to the container registry using the docker command:

```

docker login <your-private-registry>

```

-
Push the container images to the same private container registry that is accessible to your air-gapped nodes. Do not include `http://` in your private registry path:

```

sh px-ag-install.sh push <your-registry-path>

```

For example:

```

sh px-ag-install.sh push myregistry.net:5443

```

For example, to push the new images to a specific repo (consult your StorageCluster definition as per the note in the Prerequisites):

```

sh px-ag-install.sh push myregistry.net:5443/px-images

```

### Create a version manifest configmap for Portworx Operator​

- Kubernetes

- Openshift

-
Download the Portworx version manifest:

```

curl -o versions.yaml "https://install.portworx.com/$<portworx-version>/version?kbver=$<kubernetes-version>&opver=$<operator-version>"

```

Replace:

- `<portworx_version>` with the Portworx version you want to use.

- `<kubernetes-version>` with the Kubernetes version you want to use.

- `<operator-version>` with the Operator version you want to use.

-
Update (deleting/recreating) the `px-versions` configmap from the downloaded version manifest:

```

kubectl -n <px-namespace> delete configmap px-versions

kubectl -n <px-namespace> create configmap px-versions --from-file=versions.yaml

```

-
Download the Portworx version manifest:

```

curl -o versions.yaml "https://install.portworx.com/$<portworx-version>/version?kbver=$<kubernetes-version>&opver=$<operator-version>"

```

Replace:

- `<portworx_version>` with the Portworx version you want to use.

- `<kubernetes-version>` with the Kubernetes version you want to use.

- `<operator-version>` with the Operator version you want to use.

-
Update (deleting/recreating) the `px-versions` configmap from the downloaded version manifest:

```

oc -n <px-namespace> delete configmap px-versions

oc -n <px-namespace> create configmap px-versions --from-file=versions.yaml

```

## Upgrade Portworx installation​

note

-
Skip this section if you are upgrading only the Kubernetes control plane version.

-
If using configmap, update the version manifest for Portworx Operator. Otherwise, you might not see the expected image versions.

-
If you override the default PodDisruptionBudget in GKE environments, ensure that the `maxUnavailable` is less than the `storage-pdb-min-available` value for a balanced speed and disruption. Portworx by Everpure recommends using the following configurations for surge upgrades:

- `maxSurge=1`

- `maxUnavailable=0`

-
Log in to the custom container registry using your JFrog credentials.
The registry automatically creates the following sample config.json file:

```

cat /root/.docker/config.json

{

        "auths": {

                <custom registry name>: {

            "auth": <Base 64 version of Jfrog username: Jfrog token>

                }

        }

}

```

Replace `custom registry name` with the name of the custom registry and `Base 64 version of JFrog username: JFrog token` with the base 64 version of your JFrog username and token.

-
Use the config.json file, and create a registry secret to pull container images from the custom container registry:

```

kubectl create secret generic regcred -n portworx \

--from-file=.dockerconfigjson=/root/.docker/config.json \

--type=kubernetes.io/dockerconfigjson

```

After creating the `regcred` registry secret, add the registry secret in the Kubernetes Docker Registry Secret field.

-
Retrieve the name of your Portworx StorageCluster within the appropriate namespace:

```

kubectl get storagecluster -n <px-namespace>

```

```

NAME                                            STATUS   VERSION   AGE

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx Online   2.10.3    43d

```

If your cluster is installed in a different namespace, specify it using the `-n` flag.

-
Modify the StorageCluster resource to update Portworx to the desired version:

```

kubectl edit storagecluster -n <px-namespace> <storagecluster-name>

```

In the editor, make the following changes in the StorageCluster:

- Update the `spec.image` field to your desired Portworx version.

- (optional) For smart upgrade, ensure that the `spec.updateStrategy.rollingUpdate.disruption.allow` parameter is set to `false` and the maximum number of nodes that can be upgraded at a time is set using the `spec.updateStrategy.rollingUpdate.maxUnavailable` parameter.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

   name: portworx

   namespace: <px-namespace>

spec:

   image: portworx/oci-monitor:<desired-version>

   # For smart upgrades, ensure that the below lines are uncommented and `disruption.allow` is set to false. You can use the `maxUnavailable` field to control the maximum number of Portworx nodes that can be upgraded at a time.

   #updateStrategy:

   #   type: RollingUpdate

   #   rollingUpdate:

   #      maxUnavailable: 5

   #      minReadySeconds: 0

   #      disruption:

   #         allow: false

```

note

- If there are any component images configured in the StorageCluster, such as the `spec.stork.image` or `spec.autopilot.image` fields, you need to update the image fields to the latest version.

- To look up recent versions, refer to the following release notes:

- Portworx release notes

- Autopilot release notes

- Stork release notes

-
Verify that the upgrade is complete by checking the Portworx version on the nodes:

```

kubectl get storagenodes -n <px-namespace> -l name=portworx

```

```

NAME       ID                                     STATUS   VERSION          AGE

node-1-1   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   Online   <desired-version>   10d

```

In this topic:
