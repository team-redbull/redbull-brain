# CSI topology for FlashArray Direct Access volumes and FlashBlade Direct Access filesystems

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/csi-topology (Portworx Enterprise 3.6)

CSI topology for FlashArray Direct Access volumes and FlashBlade Direct Access filesystems | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

The CSI topology feature for FlashArray Direct Access volumes and FlashBlade Direct Access filesystems allows applications to provision storage on a FlashArray Direct Access volume or FlashBlade Direct Access filesystem that is in the same set of Kubernetes nodes where the application pod is located.

## Prerequisites​

In order to use the CSI topology feature with a FlashArray Direct Access volume or FlashBlade Direct Access filesystem, you must meet the following prerequisites:

- Install Portworx version 2.11.0 or newer on a local disk or a FlashArray cloud drive. vSphere cloud drives are not supported.

- Install Stork version 2.11 or newer.

## Enable CSI topology​

When you enable CSI topology, you'll specify `Labels` that describe the topology for each FlashArray. The keys must match a set of specific strings, but you can define your own values. The following CSI topology `Labels` keys are available:

- `topology.portworx.io/region`

- `topology.portworx.io/zone`

- `topology.portworx.io/datacenter`

- `topology.portworx.io/provider`

- `topology.portworx.io/row`

- `topology.portworx.io/rack`

- `topology.portworx.io/chassis`

- `topology.portworx.io/hypervisor`

note

If you are a PSO user, you can use `topology.purestorage.com` labels when you migrate from PSO to Portworx using the pso2px tool.

### Enable on a new cluster​

To enable the CSI topology feature, perform the following steps:

-
Add the following to your StorageCluster `spec`:

```

csi:

  enabled: true

  topology:

    enabled: true

```

-
Create a `px-pure-secret` containing the information for your FlashArrays. Include `Labels` that specify the topology for each FlashArray. The keys must match a set of specific strings, but you can define your own values. For example:

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-0",

        "topology.portworx.io/region": "region-0"

      }

    }

  ]

}

```

-
Label your Kubernetes nodes with labels that correspond to the `Labels` from the previous step. For example:

```

kubectl label node <nodeName> topology.portworx.io/zone=zone-0

kubectl label node <nodeName> topology.portworx.io/region=region-0

```

-
Apply the StorageCluster spec with the following command:

```

kubectl apply -f <storage-cluster-yaml-file>

```

-
Specify the placement strategy by defining the `nodeAffinity` in your Pod or StatefulSet. For example:

```

spec:

  affinity:

    nodeAffinity:

      requiredDuringSchedulingIgnoredDuringExecution:

        nodeSelectorTerms:

        - matchExpressions:

          - key: topology.portworx.io/zone

            operator: In

            values:

            - zone-0

          - key: topology.portworx.io/region

            operator: In

            values:

            - region-0

```

-
In your StorageClass, choose one of the following strategies so that the PVC uses your topology strategy:

-
Create a StorageClass with `volumeBindingMode` set to `WaitForFirstConsumer`. For example:

-
FlashArray:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: fio-sc-fada

provisioner: pxd.portworx.com

parameters:

  backend: "pure_block"

  max_bandwidth: "10G"

  max_iops: "30000"

  csi.storage.k8s.io/fstype: ext4

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

-
FlashBlade:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: fio-sc-fbda

provisioner: pxd.portworx.com

parameters:

  backend: "pure_file"

  pure_export_rules: "*(rw)"

mountOptions:

  - nfsvers=4.1

  - tcp

volumeBindingMode: WaitForFirstConsumer

allowVolumeExpansion: true

```

-
Create a StorageClass that explicitly defines `allowedTopologies` in addition to setting `volumeBindingMode` to `WaitForFirstConsumer`. For example:

-
FlashArray:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: fio-sc-fada

provisioner: pxd.portworx.com

parameters:

  backend: "pure_block"

  max_bandwidth: "10G"

  max_iops: "30000"

  csi.storage.k8s.io/fstype: ext4

volumeBindingMode: WaitForFirstConsumer

allowedTopologies:

  - matchLabelExpressions:

      - key: topology.portworx.io/rack

        values:

          - rack-0

          - rack-1

```

-
FlashBlade:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: fio-sc-fbda

provisioner: pxd.portworx.com

parameters:

  backend: "pure_file"

  pure_export_rules: "*(rw,no_root_squash)"

mountOptions:

  - nfsvers=3

  - tcp

allowVolumeExpansion: true

allowedTopologies:

  - matchLabelExpressions:

      - key: topology.portworx.io/zone

        values:

          - zone-1

      - key: topology.portworx.io/region

        values:

          - c360

```

### Enable on an existing cluster​

-
Edit the cluster's StorageCluster object to include the following:

```

csi:

  enabled: true

  topology:

    enabled: true

```

-
Delete the existing `px-pure-secret` for your FlashArray or FlashBlade:

```

kubectl delete secret --namespace <stc-namespace> px-pure-secret

```

-
Create a new `px-pure-secret` using the following command:

```

kubectl create secret generic px-pure-secret --namespace <stc-namespace> --from-file=<pure.json_file_path>

```

Include `Labels` that specify the topology for each FlashArray or FlashBlade. The keys must match a set of specific strings, but you can define your own values. For example:

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<managementEndpoint>",

      "APIToken": "<apiToken>",

      "Labels": {

        "topology.portworx.io/zone": "zone-0",

        "topology.portworx.io/region": "region-0"

      }

    }

  ]

}

```

-
Label your Kubernetes nodes with labels that correspond to the `Labels` from the previous step. For example:

```

kubectl label node <nodeName> topology.portworx.io/zone=zone-0

kubectl label node <nodeName> topology.portworx.io/region=region-0

```

-
Restart Portworx on all nodes using the following command:

```

kubectl label nodes --all px/service=restart

```

-
Get all Portworx pods using the following command:

```

kubectl get pods --namespace <px-namespace> -l name=portworx -o wide

```

-
Delete Portworx pods for each node one by one using the following command:

```

kubectl delete pods --namespace <px-namespace> <px-pod-name>

```

-
Wait for the Portworx pods to come up in the node. You can monitor the pods after deletion using the following command:

```

kubectl get pods --namespace <px-namespace> -l name=portworx -o wide | grep <node-name>

```

-
Delete the Portworx pods for next node. Repeat until Portworx pods are restarted for all nodes.

-
Wait for Portworx pods to be up in all nodes.

-
Validate that topology is enabled in a node by describing `csinode` with the following command:

```

kubectl describe csinode <node-name>

```

```

Name:               <node-name>

...

Spec:

  Drivers:

    pxd.portworx.com:

      Node ID:        <node-id>

      Topology Keys:  [topology.portworx.io/region topology.portworx.io/zone]

```

## Related topics​

- Configure Pure Storage FlashArray as a Direct Access volume

- Configure Pure Storage FlashBlade as a Direct Access filesystem

In this topic:
