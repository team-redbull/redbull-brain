# Configure FlashBlade as a Direct Access filesystem

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/pure-flashblade (Portworx Enterprise latest)

Configure FlashBlade as a Direct Access filesystem | Portworx Enterprise Documentation

## Use FlashBlade as a Direct Access filesystem​

Once you've configured Portworx to work with your FlashBlade, you can create a StorageClass and reference it in any PVCs you create.

### Create a StorageClass​

The StorageClass describes how volumes should be created and managed in Kubernetes. It specifies the NFS endpoint, back-end type (`pure_file` for FlashBlade), and NFS export rules which control the access permissions for the mounted filesystem.

- STC for multiple NFS endpoints

- STC for basic NFS endpoints

-
Create a StorageClass spec, specifying your own values for the following:

- parameters.pure_nfs_endpoint with endpoint of the FlashBlade you want to specify.

- parameters.backend: with `pure_file`

- allowedTopologies with zone and region where you want the volume from this FlashBlade to be provisioned.

- mountOptions with any CSI mount options you desire

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-multiple-nfs

provisioner: pxd.portworx.com

parameters:

  pure_nfs_endpoint: "<nfs-endpoint-1>"

  backend: "pure_file"

allowedTopologies:

  - matchLabelExpressions:

  - key: topology.portworx.io/zone

    values:

      - <zone-1>

  - key: topology.portworx.io/region

    values:

      - <region-1>

mountOptions:

  - nfsvers=3

  - tcp

allowVolumeExpansion: true

```

-
Apply this spec to create a StorageClass:

note

To ensure successful PVC creation, verify that the labels in the `allowedTopologies` section uniquely identify a single FlashBlade endpoint from the `pure.json` file. For example, if you specify `topology.portworx.io/zone: <zone-1>` in the StorageClass, and both FlashBlades listed in the `pure.json` file qualify, Portworx will fail the creation of PVCs for FlashBlade Direct Access volumes and display the following error message:

```

  Events:

  Type     Reason                Age               From                                                                               Message

  ----     ------                ----              ----                                                                               -------

  Normal   Provisioning          1s (x4 over 10s)  pxd.portworx.com_px-csi-ext-6f77f7c664-xxxx                                        External provisioner is provisioning volume for claim "default/pure-multiple-nfs"

  Warning  ProvisioningFailed    1s (x4 over 9s)   pxd.portworx.com_px-csi-ext-6f77f7c664-xxx                                         failed to provision volume with StorageClass "portworx-multiple-nfs": rpc error: code = Internal desc = Failed to create volume: multiple storage backends match volume provisioner, unable to determine which backend the provided NFSEndpoint matches to

  Normal   ExternalProvisioning  0s (x3 over 10s)  persistentvolume-controller                                                        Waiting for a volume to be created either by the external provisioner 'pxd.portworx.com' or manually by the system administrator. If volume creation is delayed, please verify that the provisioner is running and correctly registered.

```

- Create a StorageClass spec, specifying your own values for the following:

-
parameters.backend: with `pure_file`

-
parameters.pure_export_rules with any NFS export rules you desire

-
mountOptions with any CSI mount options you desire

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-pso-fb-v3

provisioner: pxd.portworx.com

parameters:

  backend: "pure_file"

  pure_export_rules: "*(rw)"

mountOptions:

  - nfsvers=3

  - tcp

allowVolumeExpansion: true

```

- Apply this spec to create a StorageClass:

```

kubectl apply -f <fb-storageclass.yml>

```

```

storageclass.storage.k8s.io/portworx-multiple-nfs created

```

### Create a PVC​

note

The Pure export rules for accessing FlashBlade defined is by the specified `accessModes` in the PVC specification:

- `*(rw)`: This rule is set for ReadWriteOnce, ReadWriteMany, and ReadWriteOncePod PVC access modes. It allows clients to perform both read and write operations on the storage.

- `*(ro)`: This rule is applied for ReadOnlyMany PVC access mode. It ensures that the storage can only be accessed in read-only mode, preventing modifications to the data.

- Reference the StorageClass you created by entering the StorageClass name in the `spec.storageClassName` field:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pure-multiple-nfs

spec:

  accessModes:

    - ReadWriteMany

  resources:

    requests:

      storage: 10Gi

  storageClassName: portworx-multiple-nfs

```

- Apply the spec to create a PVC:

```

kubectl apply -f <fb-pvc.yml>

```

```

persistentvolumeclaim/pure-multiple-nfs created

```

## Add or modify NFS endpoints for existing volumes​

If you need to assign or change an NFS endpoint for existing FlashBlade Direct Access volumes that utilize a StorageClass where `pure_nfs_endpoint` was not specified, or if you want to modify the `pure_nfs_endpoint` after the volume has been created, run the following command. Replace `<fb-management-endpoint>` with the endpoint you wish to add or modify for a volume:

```

pxctl volume update --pure_nfs_endpoint "<fb-nfs-endpoint>" <existing-fb-pvc>

```

```

Update Volume: Volume update successful for volume pvc-80406c8d-xxx-xxxx

```

note

The mount over the newly assigned NFS endpoint will occur during the next mount cycle.

## Related topics​

- Pure.json file reference

- Disk provisioning on Pure Storage FlashArray

- CSI topology for FlashArray and FlashBlade Direct Access volumes

In this topic:
