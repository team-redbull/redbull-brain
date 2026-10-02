# Enable pay-as-you-go billing

Source: https://docs.portworx.com/portworx-enterprise/platform/license/enable-pay-as-you-go-license (Portworx Enterprise 3.6)

Enable pay-as-you-go billing | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

After you have set up your cluster using any of the paid, trial, or free Portworx licenses, you can enable pay-as-you-go billing by acquiring a pay-as-you-go SaaS key from the Everpure support team and performing the following steps based on your cluster environment.

## Enable pay-as-you-go billing on internet connected clusters​

### Prerequisites​

- You have a pay-as-you-go SaaS key that was acquired by contacting the Everpure support team.

- HTTPS port 443 is open

- Hosts for activating the SaaS key:

- rest.zuora.com

- flex1327.compliance.flexnetoperations.com

tip

Run the dig rest.zuora.com +noall +answer command to check if the host is reachable or not.

Alternatively, you can run the following command:

```

$ curl https://rest.zuora.com

{"message":"no Route matched with those values"}

```

### Enable pay-as-you-go billing​

The examples below use the portworx namespace, you should update this to the correct namespace for your environment.

-
Run the following command on one of the node to activate your SaaS key:

```

pxctl license activate saas --key <SAAS_KEY>

```

note

If you already have a Portworx cluster and run the above command, your PAYG (pay-as-you-go) license will be activated. You can then follow the verifying steps to check if your SaaS key is activated. However, if you are installing a new Portworx cluster, you should follow the procedure in this section to activate your SaaS key before installing Portworx.

-
Create a Kubernetes Secret

Run the following command to a Kubernetes secret and place your pay-as-you-go SaaS key into it:

```

kubectl create secret generic px-saas \

--from-literal=saas-key=<SAAS_KEY> -n portworx

```

-
Update your StorageCluster spec

Patch the pay-as-you-go Secret into your cluster. Follow the steps appropriate for your cluster's install method:

Patch the STC using the Secret you created previous step:

```

kubectl patch stc $stc --type='json' \

-p='[{"op": "add", "path": "/spec/env/0","value": {"name": "SAAS_ACCOUNT_KEY_STRING", "valueFrom":{"secretKeyRef":{"name": "px-saas", "key": "saas-key"}}}}]' -n portworx

```

The above step patches your StorageCluster stc and appends the following under the env: parameter. This will enable pay-as-you-go billing on your cluster.

```

env:

- name: "SAAS_ACCOUNT_KEY_STRING"

  valueFrom:

    secretKeyRef:

              name: px-saas

              key: saas-key

```

Wait for a few minutes and then verify if the automatic rolling upgrade is successful by running the following command. You will observe that the new pods have been created recently with new `px-cluster-<id>`. You can also see the latest timestamp under AGE, as shown in the following example:

```

kubectl get pods -n portworx -l name=portworx

```

```

NAME                                                    READY   STATUS    RESTARTS   AGE

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-ef93c42d8aeb-b66td   2/2     Running   0          6m56s

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-ef93c42d8aeb-fqdgj   2/2     Running   0          5m16s

px-cluster-xxxxxxxx-xxxx-xxxx-xxxx-ef93c42d8aeb-t8ldc   2/2     Running   0          9m

```

-
Verify if your SaaS key activated

Check your SaaS key license usage by running pxctl status from one of the worker nodes:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Healthy

License: PX-Enterprise Usage Based (expires in 209 days)

...

```

## Enable pay-as-you-go billing on air-gapped clusters​

You can enable pay-as-you-go billing for an air-gapped cluster with no outbound connectivity by acquiring a pay-as-you-go account key from Portworx.

note

Once you enable a pay-as-you-go license for an air-gapped cluster with no outbound connectivity, you currently can't switch to any other license.

### Prerequisites​

- An air-gapped Portworx Kubernetes cluster

- You have an air-gapped SaaS key for an air-gapped cluster, acquired by contacting the Everpure support team.

### Enable pay-as-you-go billing on an air-gapped cluster​

-
Activate the pay-as-you-go license key that you received from Portworx.

```

pxctl license activate saas --key <pay-as-you-go-key>

```

-
Verify if the license is activated.

```

/opt/pwx/bin/pxctl  status

```

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Healthy

License: PX-Enterprise Usage-Based-Airgapped

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-0d74f9801263

```

-
Download your consumption report.

```

pxctl service usage-report –download \

–month <month number to download report for> \

—year <year for which to download report>

```

This command creates a tarball on your system, which you can email to the support team for billing.

## Reactivate pay-as-you-go billing when a cluster is moved into air-gapped environment​

When you convert a cluster with a pay-as-you-go billing model to an air-gapped cluster, you need to transfer your Portworx license as well.

Follow the instructions on this page to transfer your pay-as-you-go Portworx license to your air-gapped cluster.

### Prerequisite​

You have an air-gapped SaaS key for an air-gapped cluster, acquired by contacting the Everpure support team.

### Move your license to an air-gapped cluster​

-
Delete the px-saas-key Secret that was previously used to enable pay-as-you-go billing for your non-air-gapped environment.

-
Edit your StorageCluster spec and remove the following env section for the SAAS_ACCOUNT_KEY_STRING environment variable:

```

env:

- name: "SAAS_ACCOUNT_KEY_STRING"

  valueFrom:

    secretKeyRef:

              name: px-saas

              key: saas-key

```

-
Once it is removed, all Portworx pods will restart.

-
Once Portworx is online, run the following command:

```

pxctl license activate saas --key <pay-as-you-go-key>

```

-
Verify that your SaaS key is activated. Check your SaaS key license usage by running pxctl status from one of the worker nodes:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Healthy

License: PX-Enterprise Usage Based (expires in 209 days)

...

```

To see more detailed information about your license run pxctl license list

```

pxctl license list

```

```

DESCRIPTION                                             ENABLEMENT                      ADDITIONAL INFO

      Number of nodes maximum                                           1000

      Number of volumes per cluster maximum                            16384

      Volume capacity [TB] maximum                                        40

      Node disk capacity [TB] maximum                                    256

      Node disk capacity extension                                       yes

      Number of snapshots per volume maximum                              64

      Number of attached volumes per node maximum                       1024

      Storage aggregation                                                yes

      Shared volumes                                                     yes

      Volume sets                                                        yes

      BYOK data encryption                                               yes

      Limit BYOK encryption to cluster-wide secrets                       no

      Resize volumes on demand                                           yes

      Snapshot to object store [CloudSnap]                               yes

      Number of CloudSnaps daily per volume maximum                    unlim

      Cluster-level migration [Kube-motion/Data Migration]               yes

      Disaster Recovery [PX-DR]                                          yes

      Autopilot Capacity Management                                      yes

      OIDC Security                                                      yes

      Bare-metal hosts                                                   yes

      Virtual machine hosts                                              yes

      Product SKU                                             PX-Enterprise Usage Based       expires in 209 days

      For information on purchase, upgrades and support, see

      https://docs.portworx.com/knowledgebase/support.html

```

Verify that the license is activated:

```

pxctl status

```

```

Status: PX is operational

Telemetry: Disabled or Unhealthy

Metering: Healthy

License: PX-Enterprise Usage-Based-Airgapped

Node ID: xxxxxxxx-xxxx-xxxx-xxxx-0d74f9801263

```

You can see that the license has been updated to `PX-Enterprise Usage-Based-Airgapped`.

In this topic:
