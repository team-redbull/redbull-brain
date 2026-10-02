# How to enable TLS for Internal KVDB

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/internal-kvdb-tls (Portworx Enterprise latest)

How to enable TLS for Internal KVDB | Portworx Enterprise Documentation

Portworx supports Transport Layer Security (TLS) for internal key-value database (KVDB) communication. Enabling TLS ensures encrypted communication among KVDB nodes and between Portworx nodes and the KVDB cluster, enhancing the security posture of clusters using internal KVDB.

Portworx supports Transport Layer Security (TLS) for internal KVDB communication on the following platforms:

- Amazon Elastic Kubernetes Service (EKS)

- Amazon EKS with hybrid nodes

- Azure Kubernetes Service (AKS)

- Google Kubernetes Engine (GKE)

- IBM Cloud Kubernetes Service (IKS)

- Tanzu Kubernetes Grid Integrated Edition (TKGI)

- Rancher Kubernetes Engine 2 (RKE2)

- Oracle Container Engine for Kubernetes (OKE)

- Mirantis Kubernetes Engine (MKE)

- Google Anthos

- OpenShift Container Platform (OCP)

- Kubernetes Operations (KOPS)

- VMware vSphere Kubernetes Service (VKS)

- Red Hat OpenShift Service on AWS (ROSA) and

- Azure Red Hat OpenShift (ARO)

note

On Amazon EKS with hybrid nodes, the EKS control plane must be able to reach the cert-manager webhook. Otherwise, cert-manager cannot issue certificates, preventing TLS from being enabled. If the on-premises pod network is not routable from the virtual private cloud (VPC), either deploy and manage cert-manager separately and set `spec.certManager.enabled` to `false`, or pin the Portworx-managed cert-manager workloads to cloud nodes. For more information, see Enable TLS for the internal KVDB.

If you are newly installing Portworx Enterprise and want TLS configured on the internal KVDB, see Configure TLS for new installations.

If your Portworx cluster is already running KVDB without TLS and you want to migrate to a secure TLS configuration, you need to schedule a maintenance window for this migration and begin your migration. For more information, see Migrate an existing Portworx cluster to TLS.

Before you begin, learn How TLS for Internal KVDB works in Portworx Enterprise.

## How TLS for internal KVDB works​

The internal KVDB uses etcd. When TLS is enabled, Portworx sets up TLS for both peer-to-peer and client-server communication.

This section explains how the Portworx Operator sets up and manages TLS using cert-manager and etcd.

When `spec.kvdb.enableTLS` and `spec.certManager.enabled` fields are set to `true`, the Portworx Operator manages the certificate lifecycle and configures `etcd` to use TLS for both peer-to-peer and client-server communication.

If you don't want the Portworx Operator to manage `cert-manager`, omit the `certManager` field from the spec. This allows you to manage `cert-manager` manually.

note

Starting with Google Anthos version 1.30, cert-manager is no longer included by default.

-
For Anthos clusters upgraded to version 1.30 from version 1.29 or earlier, cert-manager remains active but is no longer managed by Anthos. You can manage cert-manager yourself or uninstall it and allow Portworx to manage the installation instead by setting the `spec.certManager.enabled` field to `true`.

-
For new Portworx installations on Anthos versions 1.30 or later, you can either install cert-manager manually or enable the `spec.certManager.enabled` field in the `StorageCluster` custom resource to let Portworx install it.

### Certificate provisioning​

The Operator uses cert-manager to generate and manage TLS certificates.

It creates the following resources:

- A self-signed Certificate Authority (CA) issuer

- A CA certificate

- A CA-based issuer

- A server certificate for all KVDB nodes

- A client certificate for Portworx components

The certificates are stored in Kubernetes secrets. The Operator mounts these secrets into Portworx pods and uses them to configure `etcd`.

### etcd TLS configuration​

The Operator configures `etcd` with the following:

- Peer certificates for secure communication between KVDB nodes

- A shared server certificate for client access with appropriate DNS SANs

- A client certificate for access by Portworx components

### Certificate rotation​

`cert-manager` renews both client and peer and server certificates one month before expiration.

The following table summarizes the types, purpose, validity, and rotation of TLS certificates used by KVDB.

Certificate typePurposeValidityRotation

CA certificateSigns other certificates10 yearsManual

Server certificateUsed for peer and client-server TLS1 yearAuto (1 month early)

Client certificateUsed by Portworx to access KVDB1 yearAuto (1 month early)

## Configure TLS for new installations​

Set up TLS during initial Portworx deployment by enabling the required flags in the `StorageCluster` custom resource.

### Prerequisites​

-
The minimum supported version of Portworx Enterprise is `3.3.0`, and the minimum supported version of the Portworx Operator is `25.2.1`.

Note: We recommend using the latest versions of Portworx Enterprise and the Portworx Operator.

### Enable TLS for internal KVDB​

To enable TLS for the internal KVDB during initial Portworx deployment, edit the `StorageCluster` custom resource and set `spec.kvdb.internal` to `true` (if not already set). Then, enable TLS by setting `spec.kvdb.enableTLS` to `true`.

If you want the operator to install `cert-manager` automatically, also set `spec.certManager.enabled` to `true`.

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworx

spec:

  kvdb:

    internal: true

    enableTLS: true

  certManager:

    enabled: true # Set this to true only if you want Portworx to install cert-manager

```

## Migrate an existing cluster to TLS​

If your Portworx cluster is already running without TLS, you can migrate to a secure TLS configuration.

The following are the key actions performed automatically during TLS migration:

-
The Operator updates all Portworx pods on KVDB nodes simultaneously.

-
All KVDB nodes transition from using non-TLS endpoints to TLS endpoints.

-
The Operator updates the Portworx pods on non-KVDB nodes in controlled batches.

-
All Portworx nodes begin using the provided certificates and TLS endpoints.

-
The Operator removes the migration annotation after completion.

Note: This annotation is not removed from the StorageCluster if you're running Portworx version 3.4.0 or later.

-
The Operator adds the following to the `StorageCluster` custom resource based on the Operator version you are running.

- Operator 25.3.0 or later

- Operator 25.2.1 and 25.2.2

StorageCluster Condition

```

- lastTransitionTime: "2025-07-07T14:12:19Z"

  message: Portworx cluster is KVDB TLS enabled

  source: InternalKvdbTls

  status: "True"

  type: KVDBTLSEnabled

```

StorageCluster Annotation

```

portworx.io/kvdb-tls-enabled: "true"

```

### Prerequisites​

- The minimum supported version of Portworx Enterprise is `3.3.0`, and the minimum supported version of the Portworx Operator is `25.2.1`.

Note: We recommend using the latest versions of Portworx Enterprise and the Portworx Operator.

- Ensure that Portworx upgrade is complete and the KVDB nodes are in a healthy state, before planning the maintenance window for KVDB TLS migration.

- Verify that internal KVDB is enabled.

- Ensure that the `portworx-operator` pod can connect to all KVDB nodes.

- Schedule a maintenance window for the migration.

The following prerequisites are required only if you are running Portworx Operator version 25.2.1.

-
If you are running KubeVirt virtual machines on this cluster, add the following annotation in the `StorageCluster` before proceeding with the TLS migration:

```

operator.libopenstorage.org/evict-vms-during-update: "false"

```

-
Ensure the value of the `spec.updateStrategy.rollingUpdate.disruption.allow` field is set to `true` in the StorageCluster.

Example `StorageCluster`:

```

apiVersion: core.libopenstorage.org/v1

kind: StorageCluster

metadata:

  name: portworxx

  namespace: <px-namespace>

spec:

  updateStrategy:

    type: RollingUpdate

    rollingUpdate:

      maxUnavailable: 10 # Use this field to define the maximum number of nodes that can be upgraded concurrently. Nodes are migrated to KVDB TLS in batches of at least 10 or `maxUnavailable`, whichever is greater, to ensure efficient upgrades.

      minReadySeconds: 0

      disruption:

        allow: true

```

### Why you need a maintenance window​

Portworx KVDB is internally backed by etcd, which does not support a mixed deployment of TLS and non-TLS enabled nodes. Due to this limitation, all KVDB nodes must be updated simultaneously during the migration from non-TLS to TLS. As a result, KVDB temporarily loses quorum while the Portworx pods on these nodes are restarted.

During this period, the remaining non-KVDB Portworx nodes—still configured to communicate over non-TLS—will have their requests to KVDB rejected. To address this, the Portworx Operator automatically restarts the remaining Portworx pods in controlled batches, reconfiguring them to use TLS for KVDB communication.

warning

Application Disruption: Applications may experience disruption if all replicas of a volume are hosted on nodes that are being updated simultaneously, as the corresponding Portworx pods are restarted during the migration process.

### Start the migration​

Start the TLS migration by updating the `StorageCluster` resource with required fields.

note

Do not perform any Portworx or Kubernetes platform upgrades while the KVDB TLS migration is in progress.

To migrate from non-TLS to TLS KVDB in an existing cluster:

-
Verify that all KVDB nodes are healthy using the following command:

```

pxctl service kvdb members

```

```

Kvdb Cluster Members:

ID					PEER URLs				CLIENT URLs				LEADER	HEALTHY	DBSIZE

xxxxxxxx-xxxx-xxxx-xxxx-be2442595b23	[http://portworx-2.internal.kvdb:9018]	[http://portworx-2.internal.kvdb:9019]	false	true	2.2 MiB

xxxxxxxx-xxxx-xxxx-xxxx-bb345f4c2c0e	[http://portworx-3.internal.kvdb:9018]	[http://portworx-3.internal.kvdb:9019]	false	true	2.2 MiB

xxxxxxxx-xxxx-xxxx-xxxx-58bcc254fe30	[http://portworx-1.internal.kvdb:9018]	[http://portworx-1.internal.kvdb:9019]	true	true	2.2 MiB

```

-
Edit the `StorageCluster` to add the `portworx.io/migration-to-kvdb-tls: "true"` annotation and update the `spec` to enable TLS:

```

metadata:

  annotations:

    portworx.io/migration-to-kvdb-tls: "true"

spec:

  kvdb:

    internal: true

    enableTLS: true

  certManager:

    enabled: true  # Set to true only if you want Portworx to install cert-manager

```

### Verify the migration​

Verify migration on all KVDB nodes using the following steps.

-
Run the following command on a Portworx node:

```

pxctl service kvdb members

```

-
Confirm that both peer and client URLs use the `https` scheme.

Example output:

```

Kvdb Cluster Members:

ID					PEER URLs				CLIENT URLs				LEADER	HEALTHY	DBSIZE

xxxxxxxx-xxxx-xxxx-xxxx-be2442595b23	[https://portworx-2.internal.kvdb:9018]	[https://portworx-2.internal.kvdb:9019]	false	true	2.2 MiB

xxxxxxxx-xxxx-xxxx-xxxx-bb345f4c2c0e	[https://portworx-3.internal.kvdb:9018]	[https://portworx-3.internal.kvdb:9019]	false	true	2.2 MiB

xxxxxxxx-xxxx-xxxx-xxxx-58bcc254fe30	[https://portworx-1.internal.kvdb:9018]	[https://portworx-1.internal.kvdb:9019]	true	true	2.2 MiB

```

-
Check the `StorageCluster` status using the `kubectl describe stc <px-cluster-name> -n <px-namespace>` command.

```

status:

   conditions:

   - Last Transition Time:  2025-06-23T09:38:50Z

     Message: KVDB TLS migration completed

     Source: InternalKvdbTls

     Status: Completed

     Type: Migration

```

note

If you set the value of the `spec.updateStrategy.rollingUpdate.disruption.allow` field to `true` in the StorageCluster before starting the migration, you can revert the change after migration is successful.

### Troubleshooting​

KVDB TLS migration is stuck after KVDB nodes are migrated

On OpenShift Container Platform (OCP), if the migration status in the StorageCluster (STC) appears stalled for more than 15–20 minutes, verify that all KVDB nodes have migrated to TLS by running the `pxctl sv key-status` command on a KVDB node to confirm that all peer URLs use the HTTPS scheme.

For non-KVDB nodes that have not yet transitioned to TLS, restarting the Portworx or oci-monitor pods on those nodes typically allows the migration to proceed.

To check whether a Portworx pod has migrated to TLS, inspect the pod specification to see if the KVDB TLS certificates are mounted. The following script lists Portworx pods that do not have the KVDB TLS certificates mounted:

```

kubectl get pods -lname=portworx -n portworx -o json | jq -r '

  .items[] |

  {

    ns: .metadata.namespace,

    name: .metadata.name,

    containers: (

      (.spec.containers + (.spec.initContainers // [])) |

      map(.volumeMounts[]?.mountPath)

    )

  } |

  select(.containers | index("/etc/pwx/kvdbcerts") | not) |

  "\(.name)"

'

```

In this topic:
