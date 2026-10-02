# Advanced configuration and automation

Source: https://docs.portworx.com/portworx-enterprise/deploy-your-applications/application-install-with-kubernetes/postgresql/advanced-configuration (Portworx Enterprise latest)

Advanced configuration and automation | Portworx Enterprise Documentation

As your PostgreSQL environment grows more sophisticated, so do the strategies needed to keep performance high and administration overhead low. Portworx’s advanced features such as hyperconvergence with Stork, topology-aware volume placement, and Autopilot-driven capacity management enable you to fine-tune how data is accessed, replicated, and scaled within your cluster. By aligning storage and compute resources more closely, you can reduce latency, achieve hands-off scaling, and maintain resilience across fault domains, all while minimizing manual interventions.

## Hyperconvergence with Stork​

Hyperconvergence with Stork bridges the gap between where data is stored and where the PostgreSQL pods run, reducing cross-node traffic and improving overall performance. By scheduling pods on the same nodes that hold their storage replicas, you can cut down on I/O latency, increase throughput, and streamline operations particularly in large or rapidly scaling clusters.

### Benefits​

- Improved performance: Faster reads and writes with local data access.

- Operational flexibility: Automatic pod re-scheduling on node failures.

- Simplicity: Reduces the need for complex custom affinity rules.

For more information, refer to the Stork documentation.

### Implementation​

- Install Stork (often part of the Portworx Operator).

- Use an annotation like `stork.libopenstorage.org/preferLocalNodeOnly: "true"`.

- Verify pods are scheduled on nodes that hold the volume replicas.

## Topology awareness and volume placement​

Properly distributing storage replicas across multiple fault domains or availability zones is crucial for maintaining both high availability and consistent performance. By leveraging topology-aware scheduling, Portworx ensures that your PostgreSQL data is placed intelligently, minimizing the impact of node failures and reducing cross-zone network overhead. This approach not only safeguards data integrity but also helps maintain low‑latency access for mission-critical workloads.

Key benefits

- Storage availability: Spread volumes and replicas across the cluster.

- Performance: Avoid placing all replicas on the same underlying disks.

- Application resilience: Coupled with Stork, you can ensure your PostgreSQL primary and secondaries are distributed properly.

Example volume placement strategy

```

apiVersion: portworx.io/v1beta2

kind: VolumePlacementStrategy

metadata:

  name: test-vps

spec:

  volumeAntiAffinity:

    - enforcement: required

      topologyKey: topology.kubernetes.io/zone

      matchExpressions:

      - key: "name"

        operator: In

        values:

        - "${pvc.labels.name}"

  replicaAffinity:

    - enforcement: required

      topologyKey: topology.kubernetes.io/zone

```

You can use this example volume placement to achieve the volume placements illustrated in the following figure:

For more information, refer to the volume placement strategy documentation.

## Capacity management and Autopilot​

As workloads evolve, so do their storage requirements. Relying on manual processes to expand capacity can introduce downtime and operational complexity. By continuously monitoring resource utilization, Portworx Autopilot intelligently scales storage volumes when thresholds are exceeded. This hands-off approach ensures your PostgreSQL clusters stay responsive, helping you avoid sudden space shortages and maintain steady performance as demands grow.

For more information, refer to the Portworx Autopilot documentation.

Key benefits

- Hands-off scaling: Automatically expand volumes or pools when thresholds are met.

- Cost efficiency: Only grow storage when needed.

- Proactive management: Detect usage spikes early to avoid downtime.

Example Autopilot policy

```

apiVersion: autopilot.libopenstorage.org/v1alpha1

kind: AutopilotRule

metadata:

  name: volume-capacity-autoscale

spec:

  conditions:

    - type: "LabelSelector"

      key: "app"

      value: "postgres"

    - type: "VolumeUsage"

      operator: "Gt"

      value: "80"

  actions:

    - name: "openstorage.io.action.volume/resize"

      params:

        resizePercentage: "20"

```

The example policy above triggers at 80% usage and expands the volume by 20%.

For more information, refer to the Portworx Autopilot documentation.

In this topic:
