# Cluster Topology awareness

Source: https://docs.portworx.com/portworx-enterprise/concepts/cluster-topology-awareness (Portworx Enterprise latest)

Cluster Topology awareness | Portworx Enterprise Documentation

Kubernetes node labels provide cluster topology information such as rack, zone, and region to Portworx clusters. Portworx uses this information to make volume replica placement decisions. The way Portworx responds to zone, region, and rack information is as follows:

## Zone and Region information​

Zone

If Portworx nodes are provided with the information about their zones, they can influence the `default` replica placement. In case of replicated volumes Portworx will always try to keep the replicas of a volume in different zones. This placement is not `strictly` user driven and if zones are provided, Portworx will automatically default to placing replicas in different zones for a volume.

Region

If Portworx nodes are provided with the information about their region, they can influence the `default` replica placement. In case of replicated volumes Portworx will always try to keep the replicas of a volume in the same region. This placement is not `strictly` user driven and if regions are provided, Portworx will automatically default to placing replicas in same region for a volume.

### How are Zones and Regions determined​

For different environments, the following table shows how zones are determined:

Cloud providerZone

Public clouds, such as AWS, Azure, Google Cloud, or IBM CloudDetected by Portworx using cloud providers APIs.

VMware vSphere or VMware vSphere Kubernetes ServiceValue of the zone label `topology.portworx.io/zone` determines the zone for that node. If the label is not specified, all nodes are treated as part of a single default zone.

Pure FlashArrayValue of the zone label `topology.portworx.io/zone` determines the zone for a FlashArray. Follow Enable CSI Topology for FlashArray Cloud Drive to ensure that the nodes are labeled with the correct zone before installing Portworx on them.

Note: If a cluster has no zones, all nodes are assumed to be in a single zone. Most vSphere setups and most FlashArray cloud setups are configured as a single zone.

For Kubernetes or OpenShift clusters, the nodes in the cluster automatically have failure domain labels applied to them. These labels correspond to the cloud provider's infrastructure characteristics, such as regions and availability zones.

Portworx parses these labels to update its understanding of the cluster topology. You don't need to perform any additional steps.

Label NamePurpose

`topology.kubernetes.io/region`Region in which the node resides

`topology.kubernetes.io/zone`Zone in which the node resides

## Rack information​

If Portworx nodes are provided with the information about their racks, they can use this information to honor the rack placement strategy provided during volume creation. If Portworx nodes are aware of their racks, and a volume is instructed to be created on specific racks, Portworx will make a best effort to place the replicas on those racks. The placement is user driven and has to be provided during volume creation.

To provide rack information to Portworx, label Kubernetes or OpenShift nodes with `px/rack=rack1`, where px/rack is the key and rack1 is the value identifying the rack of which the node is a part of. Make sure the label is a string not starting with a special character or a number.

### Providing rack information to a node​

Run the following command to list the existing nodes and their labels.

- Kubernetes

- OpenShift

```

kubectl get nodes --show-labels

```

```

oc get nodes --show-labels

```

```

```output

NAME      STATUS    AGE       VERSION   LABELS

vm-1      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-1,node-role.kubernetes.io/master=

vm-2      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-2

vm-3      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-3

```

To indicate node `vm-2` is placed on `rack1` update the node label in the following way:

- Kubernetes

- OpenShift

```

kubectl label nodes vm-2 px/rack=rack1

```

```

oc label nodes vm-2 px/rack=rack1

```

Now let's check your provided node labels.

- Kubernetes

- OpenShift

```

kubectl get nodes --show-labels

```

```

oc get nodes --show-labels

```

```

NAME      STATUS    AGE       VERSION   LABELS

vm-1      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-1,node-role.kubernetes.io/master=

vm-2      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-2,px/rack=rack1

vm-3      Ready     14d       v1.7.4    beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/hostname=vm-3

```

This verifies that node vm-2 has the new `px/rack` label.

Double check if the rack information is reflected in the Portworx cluster.

```

pxctl cluster provision-status

```

```

NODE        NODE STATUS        POOL        POOL STATUS .....   ZONE           REGION        RACK

vm-2        Online                0        Online      .....   default        default       rack1

vm-3        Online                0        Online      .....   default        default       default

```

The node vm-2 which was labelled `rack1` is reflected on the Portworx node while the unlabelled node vm-3 is still using the `default` rack info.

All the subsequent updates to the node labels will be automatically picked up by the Portworx nodes. A deletion of a `px/rack` label will also be reflected.

## Replicating volume data across racks​

Once the nodes are updated with rack info you can specify how the volume data can spread across your different racks.

Following is an example of a storage class that replicates its volume data across racks `rack1` and `rack2`

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: px-postgres-sc

provisioner: pxd.portworx.com

parameters:

  repl: "2"

  shared: "true"

  racks: "rack1,rack2"

```

Any PVC created using the above storage class will have a replication factor of 2 and will store one copy of its data on `rack1` and the other copy on `rack2`.

To do the same for regions and zones, you can use `regions` and `zones` as parameters in the StorageClass respectively.

In this topic:
