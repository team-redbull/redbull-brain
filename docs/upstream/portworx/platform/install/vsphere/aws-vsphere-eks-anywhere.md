# Install Portworx on vSphere with Amazon EKS Anywhere

Source: https://docs.portworx.com/portworx-enterprise/platform/install/vsphere/aws-vsphere-eks-anywhere (Portworx Enterprise latest)

Install Portworx on vSphere with Amazon EKS Anywhere | Portworx Enterprise Documentation

Portworx can be installed on a Kubernetes cluster running on vSphere and managed by Amazon EKS Anywhere.

Note on production use

Portworx on vSphere with Amazon EKS Anywhere is currently undergoing requalification. If you’re interested in deploying on this environment for production workloads, please contact your Everpure representative or Portworx Support.

### Prerequisites​

Before you install Portworx on vSphere, ensure that you meet the following prerequisites:

EnvironmentResources

Install

Note: Default Bottlerocket base image is not supported.Ubuntu 20.04.4 LTS
 Ubuntu 18.04.6 LTS

Deployment Host

Note: The same vSphere host where you deploy EKS-Anywhere.VM OS: Linux
vCPU: 4
 Memory: 16 GB
 Disk storage: 200 GB

Control-Plane VMsMinimum: 1
 Recommended: 3
vCPUs: 2
 RAM: 8 GB
 OS Volume: 25 GB

Worker Node VMsMinimum: 3 (for storage cluster)
 vCPUs: 8
RAM: 16 GB
 OS Volume: 25 GB

### Step 1: vCenter user for Portworx​

Provide Portworx with a vCenter server user that has either the full admin role, or for increased security, a custom-created role with the following minimum vSphere privileges:

- Datastore

- Allocate space

- Browse datastore

- Low level file operations

- Remove file

- Host

- Local operations

- Reconfigure virtual machine

- Virtual machine

- Change Configuration

- Add existing disk

- Add new disk

- Add or remove device

- Advanced configuration

- Change Settings

- Extend virtual disk

- Modify device settings

- Remove disk

If you created a custom role with the permissions above, select Propagate to children when assigning the user to the role.

note

All commands in the subsequent steps need to be run on a machine with `kubectl` access.

### Step 2: Create a secret with your vCenter user and password​

Create a secret using the following steps.

- Kubernetes Secret

- Vault Secret

-
Get VCenter user and password by running the following commands:

- For `VSPHERE_USER`: `echo '<vcenter-server-user>' | base64`

- For `VSPHERE_PASSWORD`: `echo '<vcenter-server-password>' | base64`

-
Update the following Kubernetes Secret template by using the values obtained in step 1 for `VSPHERE_USER` and `VSPHERE_PASSWORD`.

```

apiVersion: v1

kind: Secret

metadata:

  name: px-vsphere-secret

  namespace: <px-namespace>

type: Opaque

data:

  VSPHERE_USER: XXXX

  VSPHERE_PASSWORD: XXXX

```

-
Apply the above spec to update the spec with your VCenter username and password:

```

kubectl apply -f <updated-secret-template.yaml>

```

tip

To enable TLS certificate verification for vCenter, add the CA certificate used to verify the vCenter certificate to this secret with the `VSPHERE_CA_CERT` key. For more information, see Enable TLS Certificate Verification for vCenter.

When using Portworx with vSphere, you can supply the vSphere credentials by creating a secret in Vault. To configure and store secret key for vSphere in Vault, follow these steps:

#### Step 1: Create the Secret​

Store vSphere credentials (username and password) as key-value pairs at the path `secret/vsphereCredentials`. If you are not using a custom backend path, use `secret` as shown. If you are using a custom secret path, replace `secret` with your custom path.

Run the following command, substituting the placeholder values with your actual credentials:

```

vault kv put secret/vsphereCredentials VSPHERE_PASSWORD=<vsphere_password> VSPHERE_USER=<vsphere_user>

```

If your custom secret path is, for example, customPath:

```

vault kv put customPath/vsphereCredentials VSPHERE_PASSWORD=<vsphere_password> VSPHERE_USER=<vsphere_user>

```

#### Step 2: Retrieve and Verify the Secret​

To ensure that the secret was created correctly, use this command:

```

vault kv get secret/vsphereCredentials

```

The command should return an output similar to the following:

```

========== Data ==========

Key                 Value

---                 -----

VSPHERE_PASSWORD    <vsphere_password>

VSPHERE_USER        <vsphere_user>

```

important

- Ensure that the correct vSphere credentials are securely stored in Vault before Portworx installation.

- Ensure that the ports 17001-17020 on worker nodes are reachable from the control plane node and other worker nodes.

### Step 3: Generate Portworx spec​

-
Sign in to the Portworx Central console.
 The system displays the Welcome to Portworx Central! page.

-
In the Portworx Enterprise section, select Generate Cluster Spec.
 The system displays the Generate Spec page.

-
For Platform, select vSphere, then click Customize at the bottom of the Summary section.

-
On the Basic page, select the latest version of Portworx from the Portworx Version drop-down, the Built-in option for etcd. TLS for internal KVDB is enabled, by default. If Cert-Manager is already running in your Kubernetes cluster, deselect the Deploy Cert-Manager for TLS certificates option to avoid installation failures. Click Next.

-
On the Storage page, select Cloud as your environment, and vSphere as your cloud platform. Select the Create Using a Spec option to configure your storage devices, specify the following, and click Next:

- In the vCenter Endpoint field, specify the hostname or IP address of your vCenter server.

- In the vCenter datastore prefix field, specify the prefix name of the vCenter datastore you want to use.

- In the Kubernetes Secret Name field, specify the name of the secret that you specified in Step 2, which is `px-vsphere-secret`.

- In the vCenter Port field, enter port 443, if it is not auto filled.

-
Choose your network and click Next.

-
On the Deployment page, enable Stork, CSI, Monitoring, and Telemetry in Advanced Settings and click Finish to generate the spec.

### Apply specs​

Apply the Operator and StorageCluster specs you generated in the section above using the `kubectl apply` command:

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

kubectl apply -f 'https://install.portworx.com/<version-number>?operator=true&mc=false&kbver=&b=true&kd=type%3Dgp2%2Csize%3D150&s=%22type%3Dgp2%2Csize%3D150%22&c=px-cluster-XXXX-XXXX&eks=true&stork=true&csi=true&mon=true&tel=false&st=k8s&e==AWS_ACCESS_KEY_ID%3XXXX%2CAWS_SECRET_ACCESS_KEY%3XXXX&promop=true'

```

```

storagecluster.core.libopenstorage.org/px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-8dfd338e915b created

```

 Monitor the Portworx pods​

-
Enter the following `kubectl get` command, waiting until all Portworx pods show as ready in the output:

```

kubectl get pods -o wide -n <px-namespace> -l name=portworx

```

-
Enter the following `kubectl describe` command with the ID of one of your Portworx pods to show the current installation status for individual nodes:

```

kubectl -n <px-namespace> describe pods <portworx-pod-id>

```

```

Events:

  Type     Reason                             Age                     From                  Message

  ----     ------                             ----                    ----                  -------

  Normal   Scheduled                          7m57s                   default-scheduler     Successfully assigned <px-namespace>/portworx-qxtw4 to k8s-node-2

  Normal   Pulling                            7m55s                   kubelet, k8s-node-2   Pulling image "portworx/oci-monitor:2.5.0"

  Normal   Pulled                             7m54s                   kubelet, k8s-node-2   Successfully pulled image "portworx/oci-monitor:2.5.0"

  Normal   Created                            7m53s                   kubelet, k8s-node-2   Created container portworx

  Normal   Started                            7m51s                   kubelet, k8s-node-2   Started container portworx

  Normal   PortworxMonitorImagePullInPrgress  7m48s                   portworx, k8s-node-2  Portworx image portworx/px-enterprise:2.5.0 pull and extraction in progress

  Warning  NodeStateChange                    5m26s                   portworx, k8s-node-2  Node is not in quorum. Waiting to connect to peer nodes on port 9002.

  Warning  Unhealthy                          5m15s (x15 over 7m35s)  kubelet, k8s-node-2   Readiness probe failed: HTTP probe failed with statuscode: 503

  Normal   NodeStartSuccess                   5m7s                    portworx, k8s-node-2  PX is ready on this node

```

note

In your output, the image pulled will differ based on your chosen Portworx license type and version.

 Monitor the cluster status​
Use the `pxctl status` command to display the status of your Portworx cluster:

```

PX_POD=$(kubectl get pods -l name=portworx -n <px-namespace> -o jsonpath='{.items[0].metadata.name}')

kubectl exec $PX_POD -n <px-namespace> -- /opt/pwx/bin/pxctl status

```

In this topic:
