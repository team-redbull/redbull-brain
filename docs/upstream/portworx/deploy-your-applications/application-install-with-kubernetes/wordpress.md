# Deploy WordPress and MySQL with Portworx

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/wordpress (Portworx Enterprise 3.6)

Deploy WordPress and MySQL with Portworx | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

You can deploy WordPress, an open-source content management system, with Portworx on Kubernetes. Portworx enables reliable and persistent storage to ensure WordPress runs with HA and has Shared4 volumes for file uploads. You can horizontally scale the WordPress container. The cluster automatically repairs itself in the event of a node failure.

The following collection of tasks describe how to deploy WordPress and MySQL with Portworx:

- Dynamically provision a volume for MySQL

- Dynamically provision a volume for WordPress

- Create a Kubernetes secret for storing your MySQL password

- Deploy MySQL

- Deploy WordPress

- Validate the cluster functionality

## Dynamically provision a volume for MySQL​

-
Create a file called `mysql-sc.yaml`, specifying the following fields and values:

- apiVersion: as `storage.k8s.io/v1`

- kind: as `StorageClass`

- metadata.name: with the name of your `StorageClass` object (this example uses `mysql-sc`)

- provisioner: as `pxd.portworx.com`. For details about the Portworx-specific parameters, refer to the Portworx Volume section of the Kubernetes website.

- parameters.repl: with the number of replicas Portworx should create (this example creates two replicas)

- parameters.priority_io: with the type of the storage pool (this example uses a high-priority storage pool)

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: mysql-sc

provisioner: pxd.portworx.com

parameters:

  repl: "3"

  priority_io: "high"

```

For more information on how to configure a storage class, see StorageClass.

-
Apply the spec:

```

kubectl apply -f mysql-sc.yaml

```

-
Create a file called `mysql-pvc.yaml` with the following content:

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: mysql-pvc

  annotations:

    volume.beta.kubernetes.io/storage-class: mysql-sc

spec:

  accessModes:

    - ReadWriteOnce

  resources:

    requests:

      storage: 2Gi

```

note

This PVC references the `mysql-sc` storage class. As a result, Kubernetes will automatically create a new PVC for each replica.

-
Apply the spec:

```

kubectl apply -f mysql-pvc.yaml

```

## Dynamically provision a volume for WordPress​

- Create a file called `wordpress-sc.yaml` with the following content:

```

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: wordpress-sc

provisioner: pxd.portworx.com

parameters:

  repl: "3"

  priority_io: "high"

  shared: "true"

```

note

The `sharedv4: "true"` flag creates a globally shared namespace volume which can be used by multiple Pods.

-
Apply the spec:

```

kubectl apply -f wordpress-sc.yaml

```

-
Create a file called `wordpress-pvc.yaml` with the following content:

```

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: wp-pvc

  labels:

    app: wordpress

  annotations:

    volume.beta.kubernetes.io/storage-class: wordpress-sc

spec:

  accessModes:

    - ReadWriteMany

  resources:

    requests:

      storage: 1Gi

```

note

This PVC references the `wordpress-sc` storage class. As a result, Kubernetes will automatically create a new PVC for each replica.

-
Apply the spec:

```

kubectl apply -f wordpress-pvc.yaml

```

## Create a Kubernetes secret for storing your MySQL password​

A secret is an object that contains sensitive data. To create a secret, you can use the `kubectl create secret` command. Note that, to protect your sensitive data, the `kubectl get` and `kubectl describe` commands do not display the content of a secret.

-
Use the `echo` command to save your MySQL password to a file called `./password.txt`, replacing `<YOUR-PASSWORD>` with your actual password:

```

echo -n '<YOUR-PASSWORD' > ./password.txt

```

-
To create a new secret, enter the `kubectl create secret` command, specifying:

-
The `generic` parameter. This instructs Kubernetes to create a secret based on a file, directory, or specified literal value.

-
The name of your secret (this example uses `mysql-pass`)

-
The `--from-file` flag with the name of the file in which you stored your password

```

kubectl create secret generic mysql-pass --from-file=./password.txt

```

-
Use the `kubectl get secrets` command to verify that Kubernetes created the secret:

```

kubectl get secrets

```

## Deploy MySQL​

-
Create a file named `mysql-service.yaml` with the following content:

```

apiVersion: v1

kind: Service

metadata:

  name: wordpress-mysql

  labels:

    app: wordpress

spec:

  ports:

    - port: 3306

  selector:

    app: wordpress

    tier: mysql

  clusterIP: None

```

-
Apply the spec:

```

kubectl apply -f mysql-service.yaml

```

-
Create a file named `mysql-deployment.yaml` with the following content:

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: wordpress-mysql

  labels:

    app: wordpress

spec:

  selector:

    matchLabels:

      app: wordpress

  strategy:

    type: Recreate

  template:

    metadata:

      labels:

        app: wordpress

        tier: mysql

    spec:

      # Use the Stork scheduler to enable more efficient placement of the pods

      schedulerName: stork

      containers:

      - image: mysql:5.6

        imagePullPolicy:

        name: mysql

        env:

          # $ kubectl create secret generic mysql-pass --from-file=password.txt

          # make sure password.txt does not have a trailing newline

        - name: MYSQL_ROOT_PASSWORD

          valueFrom:

            secretKeyRef:

              name: mysql-pass

              key: password.txt

        ports:

        - containerPort: 3306

          name: mysql

        volumeMounts:

        - name: mysql-persistent-storage

          mountPath: /var/lib/mysql

      volumes:

      - name: mysql-persistent-storage

        persistentVolumeClaim:

          claimName: mysql-pvc

```

Note the following about this `Deployment`:

- Kubernetes creates a single-instance MySQL database

- Kubernetes creates an environment variable called `MYSQL_ROOT_PASSWORD` that contains your MySQL password

- Portworx mounts the Portworx persistent volume in the `/var/lib/mysql` directory

- The Stork scheduler will place your Pods closer to where their data is located

-
Apply the spec:

```

kubectl apply -f mysql-deployment.yaml

```

## Deploy WordPress​

-
Create a file called `wordpress-service.yaml` with the following content:

```

apiVersion: v1

kind: Service

metadata:

  name: wordpress

  labels:

    app: wordpress

spec:

  ports:

    - port: 80

      nodePort: 30303

  selector:

    app: wordpress

    tier: frontend

  type: NodePort

```

Note that the `spec.type` field is set to `NodePort`. Kubernetes exposes the service on each node and makes it accessible from outside the cluster. For more details, see the Type NodePort section of the Kubernetes documentation.

-
Apply the spec:

```

kubectl apply -f wordpress-service.yaml

```

-
Create a file called `wordpress-deployment.yaml` with the following content:

```

apiVersion: apps/v1

kind: Deployment

metadata:

  name: wordpress

  labels:

    app: wordpress

spec:

  selector:

    matchLabels:

      app: wordpress

  replicas: 3

  strategy:

    type: Recreate

  template:

    metadata:

      labels:

        app: wordpress

        tier: frontend

    spec:

      # Use the Stork scheduler to enable more efficient placement of the pods

      schedulerName: stork

      containers:

      - image: wordpress:4.8-apache

        name: wordpress

        imagePullPolicy:

        env:

        - name: WORDPRESS_DB_HOST

          value: wordpress-mysql

        - name: WORDPRESS_DB_PASSWORD

          valueFrom:

            secretKeyRef:

              name: mysql-pass

              key: password.txt

        ports:

        - containerPort: 80

          name: wordpress

        volumeMounts:

        - name: wordpress-persistent-storage

          mountPath: /var/www/html

      volumes:

      - name: wordpress-persistent-storage

        persistentVolumeClaim:

          claimName: wp-pvc

```

Note the following about this `Deployment`

- Portworx will create three replicas of each volume

- The Stork scheduler will place your Pods closer to where their data is located

- Kubernetes will create an environment variable called `WORDPRESS_DB_PASSWORD` that contains your MySQL password

-
Apply the spec:

```

kubectl apply -f wordpress-deployment.yaml

```

## Validate the cluster functionality​

-
List your Pods:

```

kubectl get pods

```

-
Display your services:

```

kubectl get services

```

## Clean up​

-
Enter the following command to delete the Kubernetes secret:

```

kubectl delete secret mysql-pass

```

-
Use the `kubectl delete` to delete your WordPress deployment and PVC:

```

kubectl delete -f wordpress-deployment.yaml

kubectl delete -f wordpress-pvc.yaml

```

-
Use the `kubectl delete` to delete your MySQL deployment and PVC:

```

kubectl delete -f mysql-deployment.yaml

kubectl delete -f mysql-pvc.yaml

```

In this topic:
