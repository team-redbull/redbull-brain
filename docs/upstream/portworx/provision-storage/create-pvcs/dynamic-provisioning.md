# Dynamic Provisioning of PVCs

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/dynamic-provisioning (Portworx Enterprise latest)

Dynamic Provisioning of PVCs | Portworx Enterprise Documentation

This document describes how to dynamically provision a volume using Kubernetes and Portworx. With dynamic provisioning and StorageClasses, you do not need to create Portworx volumes manually; volumes are created automatically when a PersistentVolumeClaim (PVC) is created.

### Provision volumes​

#### Step 1: Create Storage Class.​

```

kubectl create -f examples/volumes/portworx/portworx-volume-sc.yaml

```

Example:

```

kind: StorageClass

apiVersion: storage.k8s.io/v1

metadata:

  name: portworx-sc

provisioner: pxd.portworx.com

parameters:

  repl: "1"

```

Download example

Verifying storage class is created:

```

kubectl describe storageclass portworx-sc

```

```

     Name: 	        	portworx-sc

     IsDefaultClass:	No

     Annotations:		<none>

     Provisioner:		pxd.portworx.com

     Parameters:		repl=1

     No events.

```

#### Step 2: Create Persistent Volume Claim.​

```

kubectl create -f examples/volumes/portworx/portworx-volume-pvcsc.yaml

```

Example:

```

kind: PersistentVolumeClaim

apiVersion: v1

metadata:

  name: pvcsc001

  annotations:

    volume.beta.kubernetes.io/storage-class: portworx-sc

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

Download example

Verifying persistent volume claim is created:

```

kubectl describe pvc pvcsc001

```

```

Name:	      	pvcsc001

Namespace:      default

StorageClass:   portworx-sc

Status:	      	Bound

Volume:         pvc-xxxxxxxx-xxxx-xxxx-xxxx-08002729a32b

Labels:	      	<none>

Capacity:	      2Gi

Access Modes:     RWO

No Events.

```

Persistent Volume is automatically created and is bounded to this pvc.

Verifying persistent volume is created:

```

kubectl describe pv pvc-xxxxxxxx-xxxx-xxxx-xxxx-08002729a32b

```

```

Name: 	      	pvc-xxxxxxxx-xxxx-xxxx-xxxx-08002729a32b

Labels:        	<none>

StorageClass:  	portworx-sc

Status:	      	Bound

Claim:	      	default/pvcsc001

Reclaim Policy: Delete

Access Modes:     RWO

Capacity:	     2Gi

Message:

Source:

Type:	      	PortworxVolume (a Portworx Persistent Volume resource)

VolumeID:   	374093969022973811

No events.

```

#### Step 3: Create Pod which uses Persistent Volume Claim with storage class.​

```

kubectl create -f examples/volumes/portworx/portworx-volume-pvcscpod.yaml

```

Example:

```

apiVersion: v1

kind: Pod

metadata:

  name: pvpod

spec:

  containers:

  - name: test-container

    image: gcr.io/google_containers/test-webserver

    volumeMounts:

    - name: test-volume

      mountPath: /test-portworx-volume

  volumes:

  - name: test-volume

    persistentVolumeClaim:

      claimName: pvcsc001

```

Download example

Verifying pod is created:

```

kubectl get pod pvpod

```

```

NAME      READY     STATUS    RESTARTS   AGE

pvpod       1/1     Running   0          48m

```

note

To access PV/PVCs with a non-root user refer here

### Delete volumes​

For dynamically provisioned volumes using StorageClass and PVC (PersistenVolumeClaim), if a PVC is deleted, the corresponding Portworx volume will also get deleted. This is because Kubernetes, for PVC, creates volumes with a reclaim policy of deletion. So the volumes get deleted on PVC deletion.

To delete the PVC and the volume, you can run `kubectl delete -f <pvc_spec_file.yaml>`

In this topic:
