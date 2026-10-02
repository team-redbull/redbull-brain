# Place replicas within the same domain

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/replicas-on-the-same-cluster-domain (Portworx Enterprise 3.6)

Place replicas within the same domain | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Once your Portworx cluster is operational, the replica 2 volumes will distribute their replicas across the two cluster domains. You can control this behavior using the `Metro DR domain protection` flag, which is enabled by default.

You can run the following command to check if the protection flag is enabled in your setup:

- Kubernetes

- OpenShift

```

PX_POD=$(kubectl get pods -l name=portworx -n <portworx-namespace> -o jsonpath='{.items[0].metadata.name}') \

kubectl exec $PX_POD -n <portworx-namespace> --  /opt/pwx/bin/pxctl cluster options list | grep Metro

```

```

PX_POD=$(oc get pods -l name=portworx -n <portworx-namespace> -o jsonpath='{.items[0].metadata.name}') \

oc exec $PX_POD -n <portworx-namespace> --  /opt/pwx/bin/pxctl cluster options list | grep Metro

```

If you want the volume replica of a specific volume (for example, monitoring data volumes) to be created within the same cluster domain, label the volume with `disable-domain-protection`. This label disables the `Metro DR domain protection` flag at the individual volume level, rather than at the cluster level.

caution

The volumes with the `disable-domain-protection` label will not be protected by Synchronous DR. In the event of a disaster, you might lose the data associated with these volumes.

To force both the replica provision in the same cluster domain use the VPS. If you do not want to enforce this behavior and the goal is to simply relax the Metro DR domain protection, then you can skip step 1 and use only `disable-domain-protection: "true"` in the StorageCluster spec.

-
Create a custom volume placement strategy for `replicaAffinity`, so that volume replicas are always in the same cluster domain:

```

apiVersion: portworx.io/v1beta2

kind: VolumePlacementStrategy

metadata:

   name: vps-domain-filter

spec:

   replicaAffinity:

   - matchExpressions:

     - key: domain

       operator: In

       values:

       - <domain-name>

```

Replace `<domain-name>` with the domain name where you want the replicas to be placed.

-
Create the following StorageClass:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

    name: disable-domain-protection-sc

provisioner: pxd.portworx.com

parameters:

   repl: "2"

   disable-domain-protection : "true"

   placement_strategy: "vps-domain-filter"

allowVolumeExpansion: true

```

If you are not using the VPS, then remove `placement_strategy: "vps-domain-filter"` from the above spec.

-
Save and apply the above spec:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-storageclass>.yaml

```

```

oc apply -f <your-storageclass>.yaml

```

-
Create a PVC which references the StorageClass you created above, specifying the StorageClass:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

   name: <application>-pvc

spec:

   storageClassName: disable-domain-protection-sc

   accessModes:

     - ReadWriteOnce

   resources:

   requests:

     storage: 2Gi

```

-
Save and apply your PVC with the following command:

- Kubernetes

- OpenShift

```

kubectl apply -f <your-storageclass>.yaml

```

```

oc apply -f <your-storageclass>.yaml

```

The above PVC will have its replicas placed within the same cluster domain.
