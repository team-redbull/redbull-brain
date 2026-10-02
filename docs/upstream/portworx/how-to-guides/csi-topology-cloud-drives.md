# CSI topology for FlashArray cloud drives

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/csi-topology-cloud-drives (Portworx Enterprise latest)

CSI topology for FlashArray cloud drives | Portworx Enterprise Documentation

The CSI topology feature for FlashArray Cloud Drives (FACD) allows applications to provision and use cloud drives only on FlashArrays that are in the same zone as a given node. This improves fault tolerance for replicas, performance, and manageability for large clusters.

## Prerequisites​

To use the CSI topology feature with FACD, you must meet the following prerequisites:

- Portworx version 3.0.0 or newer installed on a new Kubernetes cluster deployed on infrastructure that meets the minimum requirements for Portworx.

- Portworx Operator version 23.5.1 or newer.

- One or more FlashArrays are reachable from worker nodes.

- All nodes must have management access to all arrays.

- All nodes must support iSCSI, FC, and NVMe technologies.

important

- You cannot enable this feature on an existing Portworx installation.

- When using FACD CSI topology with Secure Multi-Tenancy (SMT), you must use the same pod name across all FlashArrays in your `pure.json` configuration. The Portworx Operator applies the `pod` value from the first matching `deviceSpecs` entry cluster-wide as the system metadata device spec. If FlashArrays in different zones have different pod names, nodes in zones where that pod does not exist will fail to provision storage. For more information, see Customize Portworx system volumes for secure multi-tenancy.

## Enable CSI topology​

To enable CSI topology, specify the `topology.portworx.io/zone` label to describe the topology of each FlashArray.

### Prepare your environment​

Before installing Portworx, label your Kubernetes nodes with the correct topology, specifically indicating the zone for each FlashArray. This step is crucial for proper management and access control, especially when working with multiple FlashArrays.

- Kubernetes

- OpenShift

-
To label your nodes, run the following commands for each node, specifying the appropriate zone:

```

kubectl label node <nodeName> topology.portworx.io/zone=zone-1

kubectl label node <nodeName> topology.portworx.io/zone=zone-2

```

Ensure that the nodes are labeled with the correct zone before installing Portworx on them. In setups like OpenShift Container Platform, this step becomes particularly important. If you are managing multiple FlashArrays and want to control node access to specific FlashArrays, then you can configure different MachineSets accordingly.

By labeling the nodes, you help ensure proper topology-aware storage deployment and access control for the respective zones.

-
Create a `px-pure-secret` containing the information for your FlashArrays with the `topology.portworx.io/zone` label. For example:

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-1"

      }

    },

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-2"

      }

    }

  ]

}

```

-
Label your Kubernetes nodes specifying the topology for each FlashArray, for example:

```

oc label node <nodeName> topology.portworx.io/zone=zone-1

oc label node <nodeName> topology.portworx.io/zone=zone-2

```

-
Create a `px-pure-secret` containing the information for your FlashArrays with the `topology.portworx.io/zone` label. For example:

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-1"

      }

    },

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-2"

      }

    }

  ]

}

```

### Add Environment Variable while generating the specs​

- Navigate to Portworx Central and log in, or create an account.

- Select Portworx Enterprise from the product catalog and click Continue.

- On the Product Line page, choose any option depending on which license you intend to use, then select Continue to start the spec generator.

- Install Portworx with FlashArray and on the Deployment page in Generate Portworx Enterprise Spec, specify the following in the Environment Variables tab:

- Name: `FACD_TOPOLOGY_ENABLED`

- Value: `true`

### Apply the specs and verify​

- Kubernetes

- OpenShift

-
Deploy the Operator:

```

kubectl apply -f 'https://install.portworx.com/<version-number>?comp=pxoperator'

```

```

serviceaccount/portworx-operator created

podsecuritypolicy.policy/px-operator created

clusterrole.rbac.authorization.k8s.io/portworx-operator created

clusterrolebinding.rbac.authorization.k8s.io/portworx-operator created

deployment.apps/portworx-operator created

```

-
Deploy the StorageCluster:

```

kubectl apply -f 'https://install.portworx.com/<version-number>?operator=true&mc=false&kbver=&b=true&kd=type%3Dgp2%2Csize%3D150&s=%22type%3Dgp2%2Csize%3D150%22&c=px-cluster-XXXX-XXXX&eks=true&stork=true&csi=true&mon=true&tel=false&st=k8s'

```

```

storagecluster.core.libopenstorage.org/px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-8dfd338e915b created

```

-
Verify if the cloud drives for a given node are provisioned on arrays that are in the same zone:

```

pxctl sv pool show

```

```

PX drive configuration:

Pool ID: 0

Type:  Default

UUID:  xxxxxxxx-xxxx-xxxx-xxxx-0d1797392d56

IO Priority:  HIGH

Labels:  topology.portworx.io/zone=zone-2,beta.kubernetes.io/arch=amd64,medium=STORAGE_MEDIUM_SSD,iopriority=HIGH,topology.portworx.io/region=region-2,kubernetes.io/hostname=dev-leather-forger-1,kubernetes.io/arch=amd64,kubernetes.io/os=linux,beta.kubernetes.io/os=linux

Size: 250 GiB

Status: Online

Has metadata:  No

Balanced:  Yes

    ....

```

You will see that the `Labels` flag is set for your volumes.

-
Deploy the Operator:

```

oc apply -f 'https://install.portworx.com/<version-number>?comp=pxoperator'

```

```

serviceaccount/portworx-operator created

podsecuritypolicy.policy/px-operator created

clusterrole.rbac.authorization.k8s.io/portworx-operator created

clusterrolebinding.rbac.authorization.k8s.io/portworx-operator created

deployment.apps/portworx-operator created

```

-
Deploy the StorageCluster:

```

oc apply -f 'https://install.portworx.com/<version-number>?operator=true&mc=false&kbver=&b=true&kd=type%3Dgp2%2Csize%3D150&s=%22type%3Dgp2%2Csize%3D150%22&c=px-cluster-XXXX-XXXX&eks=true&stork=true&csi=true&mon=true&tel=false&st=k8s&e==AWS_ACCESS_KEY_ID%3XXXX%2CAWS_SECRET_ACCESS_KEY%3XXXX&promop=true'

```

```

storagecluster.core.libopenstorage.org/px-cluster-XXXXXXX-XXXX-XXXX-XXXX-8dfd338e915b created

```

-
Verify if the cloud drives for a given node are provisioned on arrays that are in the same zone:

```

pxctl sv pool show

```

```

PX drive configuration:

Pool ID: 0

Type:  Default

UUID:  xxxxxxxx-xxxx-xxxx-xxxx-0d1797392d56

IO Priority:  HIGH

Labels:  topology.portworx.io/zone=zone-2,beta.kubernetes.io/arch=amd64,medium=STORAGE_MEDIUM_SSD,iopriority=HIGH,topology.portworx.io/region=region-2,kubernetes.io/hostname=dev-leather-forger-1,kubernetes.io/arch=amd64,kubernetes.io/os=linux,beta.kubernetes.io/os=linux

Size: 250 GiB

Status: Online

Has metadata:  No

Balanced:  Yes

    ....

```

You will see that the `Labels` flag is set for your volumes.

In this topic:
