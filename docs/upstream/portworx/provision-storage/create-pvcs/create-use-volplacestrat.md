# Create and use VolumePlacementStrategies

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/create-use-volplacestrat (Portworx Enterprise latest)

Create and use VolumePlacementStrategies | Portworx Enterprise Documentation

This topic explains how to create and apply a VolumePlacementStrategy custom resource (CR) in your cluster. You can use this strategy to influence the placement of volumes created by Portworx for specific workloads.
For more information on Volume Placement Strategies, see Volume Placement Strategies.

## Create a VolumePlacementStrategy custom resource​

-
Create a YAML file containing the following common fields. All VolumePlacementStrategy CRDs use these fields:

- `apiVersion` as `portworx.io/v1beta2`

- `kind` as `VolumePlacementStrategy`

- `metadata.name` with the name of your strategy

Add any of the following affinity or antiaffinity sections to the `spec`:

- replicaAffinity

- replicaAntiAffinity

- volumeAffinity

- volumeAntiAffinity

The following example adds a volumeAffinity rule to colocate Postgres volumes for performance:

```

apiVersion: portworx.io/v1beta2

kind: VolumePlacementStrategy

metadata:

  name: postgres-volume-affinity

spec:

  volumeAffinity:

    - matchExpressions:

      - key: app

        operator: In

        values:

          - postgres

```

-
Save and apply your spec with the `kubectl apply` command:

```

kubectl apply -f yourVolumePlacementStrategy.yaml

```

## Use the strategy in storage configurations​

After you create your `VolumePlacementStrategy`, you can use it with your `StorageClass` or reference it directly in a PersistentVolumeClaim (PVC).

### Use with a StorageClass​

You can associate your `VolumePlacementStrategy` with a `StorageClass` and then reference that `StorageClass` in your PVC.

-
Create a StorageClass named `storageclass_volumestrategy.yaml`.
This must include a reference to the `VolumePlacementStrategy` you created in the Create a VolumePlacementStrategy custom resource step above by using the `placement_strategy` parameter and specifying the name of your VolumePlacementStrategy:

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: postgres-storage-class

provisioner: pxd.portworx.com

parameters:

  placement_strategy: "postgres-volume-affinity"

```

-
Save and apply your StorageClass:

```

kubectl apply -f storageclass_volumestrategy.yaml

```

-
Create a PVC that uses the `storageClass`:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

   name: postgres-pvc

spec:

   storageClassName: postgres-storage-class

   accessModes:

     - ReadWriteOnce

   resources:

     requests:

       storage: 2Gi

```

-
Save and apply your PVC:

```

kubectl apply -f yourPVC.yaml

```

### Reference directly in a PVC​

You can also reference your `VolumePlacementStrategy` directly in the PVC using an annotation.

-
Create a PVC which references the `VolumePlacementStrategy` you created in the Create a VolumePlacementStrategy custom resource step above by specifying `placement_strategy` as an annotation with the name of your `VolumePlacementStrategy`:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  annotations:

    placement_strategy: "postgres-volume-affinity"

  name: postgres-pvc

spec:

  storageClassName: postgres-storage-class

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

-
Save and apply your PVC:

```

kubectl apply -f yourPVC.yaml

```

After applying the `VolumePlacementStrategy`, `StorageClass`, and PVC, Portworx places the volumes according to the rules defined in the strategy. Portworx also follows these rules during volume restores.

For information on the CRD Reference for VolumePlacementStrategies, see VolumePlacementStrategy CRD reference.

## KubeVirt VMs and CSI clone​

Starting with Portworx Enterprise 3.5.0, KubeVirt RWX Block VMs with only a single cloned root disk provisioned using `cloneStrategy: csi-clone` and no additional non-cloned data disks do not honor user-defined VPS rules at volume creation time. In this configuration, Portworx applies clone co-location behavior, placing the cloned volume replicas on the same nodes as the source volume.

To allow VPS rules to be honored, use one of the following approaches:

-
Switch to copy-based cloning: Configure the StorageClass or StorageProfile to use copy-based cloning instead of CSI clone.

Annotate the StorageClass:

```

oc annotate sc <storageClassName> cdi.kubevirt.io/clone-strategy=copy --overwrite

```

Or patch the StorageProfile:

```

oc patch storageprofile <storageProfileName> --type merge -p '{"spec":{"cloneStrategy":"copy"}}'

```

-
Add a blank data disk: Add at least one blank non-cloned data disk to the VM using the same StorageClass. With a non-cloned volume present, Portworx applies VPS rules during provisioning. Add the following entry to `spec.dataVolumeTemplates` in the VM spec:

```

- metadata:

    name: <data-disk-name>

    annotations:

      cdi.kubevirt.io/storage.usePopulator: "false"

  spec:

    source:

      blank: {}

    storage:

      accessModes:

        - ReadWriteMany

      resources:

        requests:

          storage: <size>Gi

      storageClassName: <storageClassName>

      volumeMode: Block

```

For more information, see Manage Shared Block Device (RWX Block) for KubeVirt VMs.

In this topic:
