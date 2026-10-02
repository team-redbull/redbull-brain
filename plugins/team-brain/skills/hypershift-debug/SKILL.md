---
name: hypershift-debug
description: "Systematic, read-only-first debugging of HyperShift hosted-cluster problems on our MCE hubs: stuck deletions and finalizers, NodePool/CAPI machines not progressing, hosted control plane pods, missing CRDs. Use when a HostedCluster, NodePool or hosted control plane namespace misbehaves."
---

<!--
Adapted from openshift/hypershift `.claude/skills/debug-cluster/SKILL.md` @ d1eba2a7a57c (Apache-2.0; see
plugins/team-brain/third_party/openshift-hypershift/LICENSE and /NOTICE). Changes: `kubectl`→`oc`, AWS subskill and
AWS-specific text removed, team guardrails and our context added. Re-diff against upstream when bumping.
-->

## Ground rules (team)

- **Read-only first.** Everything under "check" is `get`/`describe`/`logs`. **Never run** a finalizer patch, a delete, an
  uninstall/reinstall or any `oc apply/patch/delete` yourself — show the exact command, say what it will affect (which
  cluster, which hub), and let the user run it. Hosted-cluster actions run against the **MCE hub**, not the hosted cluster.
- **Identify the hub and the version first**: which MCE hosts this cluster, its OCP/HyperShift version
  (`knowledge/meta/fleet-versions.md` maps it to the `release-4.NN` ref). Names in this repo are placeholders
  (`<hc-namespace>`, `<hcp-namespace>`, `<cluster-name>`); use the real ones only in the live session, never write them to the brain.
- **Look up before guessing**: `brain-lookup` first (our `knowledge/`, `incidents/`), then `search_code repo=hypershift
  ref=release-4.NN` for where a condition or error string is produced. Cite `path:line @ ref`.
- Our NodePools normally use the **Agent** platform (CAPI provider `cluster-api-provider-agent`) on Metal3 bare metal:
  when machines are stuck, also check `agents.agent-install.openshift.io`, InfraEnv and BareMetalHost state
  (`oc get agents,infraenv -A`, `oc get bmh -A`) — see `knowledge/baremetal/` — not only CAPI `Machine`s. Verify
  deployment names with `oc get deploy -n <hcp-namespace>` (e.g. the CAPI provider deployment name varies).
- Anything learned that no doc said → `team-brain:brain-learn`.

# HyperShift hosted-cluster debugging

This skill provides structured debugging workflows for common HyperShift hosted-cluster issues.

## When to Use This Skill

This skill automatically applies when:
- Investigating hosted-cluster deletion issues
- Debugging stuck resources or finalizers
- Troubleshooting control plane problems
- Analyzing NodePool lifecycle issues
- Reviewing operator logs for cluster problems

## Key Components to Understand

### Resource Hierarchy
- **HostedCluster (HC)**: Main cluster resource in the management cluster
- **HostedControlPlane (HCP)**: Control plane representation of the HC in HCP namespace
- **NodePool (NP)**: Worker node pool resources
- **CAPI Resources**: Cluster API resources (Cluster, Machine, etc.) in HCP namespace

### Operators
- **hypershift-operator (HO)**: Manages HC and NP resources
- **control-plane-operator (CPO)**: Manages HCP and control plane components
- **hosted-cluster-config-operator (HCCO)**: Manages configuration and in-cluster resources for hosted clusters

### Namespaces
- **HC namespace**: Where HostedCluster and NodePool resources live (e.g., `default`, `clusters`)
- **HCP namespace**: Where control plane pods and CAPI resources run (e.g., `clusters-<cluster-name>`)

## Common Debugging Scenarios

### Scenario: Hosted Cluster Stuck Deleting

When a hosted-cluster is stuck in deleting state, follow this systematic debugging process:

#### 1. Node Pools Deletion
Check and verify NodePool deletion is progressing:

```bash
# Check NodePool resources in HC namespace
oc get nodepool -n <hc-namespace>

# Check CAPI cluster resource status in HCP namespace
oc get cluster -n <hcp-namespace> -o yaml

# Check CAPI provider pod logs
oc logs -n <hcp-namespace> deployment/capi-provider

# Check CAPI machines status in HCP namespace
oc get machines -n <hcp-namespace>
oc describe machines -n <hcp-namespace>

# Review HyperShift operator logs for NodePool issues
oc logs -n hypershift deployment/operator --tail=100 | grep -i nodepool
oc logs -n hypershift deployment/operator --tail=100 | grep -i <cluster-name>
```

**What to look for:**
- Finalizers blocking NodePool deletion
- CAPI machines that aren't terminating
- Provider errors preventing machine deletion
- HO logs showing reconciliation errors

#### 2. HostedControlPlane Resource Deletion
Verify HCP resource and pods are being cleaned up:

```bash
# Check HCP resource status
oc get hostedcontrolplane -n <hcp-namespace> -o yaml

# Check pods in HCP namespace
oc get pods -n <hcp-namespace>

# Check for stuck pods
oc get pods -n <hcp-namespace> --field-selector=status.phase!=Running

# Review control-plane-operator logs
oc logs -n <hcp-namespace> deployment/control-plane-operator --tail=100
```

**What to look for:**
- HCP finalizers blocking deletion
- Pods with finalizers or in Terminating state
- CPO logs showing errors in resource cleanup
- PVC or other resources preventing namespace deletion

#### 3. HCP Namespace Deletion
Investigate why the HCP namespace isn't being removed:

```bash
# Check namespace status
oc get namespace <hcp-namespace> -o yaml

# List all remaining resources in namespace
oc api-resources --verbs=list --namespaced -o name | \
  xargs -n 1 oc get --show-kind --ignore-not-found -n <hcp-namespace>

# Check for resources with finalizers
oc get all -n <hcp-namespace> -o json | \
  jq '.items[] | select(.metadata.finalizers != null) | {kind: .kind, name: .metadata.name, finalizers: .metadata.finalizers}'

# Review HO logs for namespace cleanup
oc logs -n hypershift deployment/operator --tail=100 | grep -i namespace
```

**What to look for:**
- Resources with finalizers preventing deletion
- API resources that HO should have cleaned up
- Webhook or admission controller errors
- Namespace stuck in Terminating state

#### 4. HostedCluster Resource Deletion
Final check on the HostedCluster resource itself:

```bash
# Check HostedCluster status
oc get hostedcluster -n <hc-namespace> <cluster-name> -o yaml

# Check HostedCluster finalizers
oc get hostedcluster -n <hc-namespace> <cluster-name> -o jsonpath='{.metadata.finalizers}'

# Review HO logs for HostedCluster deletion
oc logs -n hypershift deployment/operator --tail=200 | grep -i "hostedcluster.*<cluster-name>"
```

**What to look for:**
- Finalizers blocking HostedCluster deletion
- HO errors in reconciliation loop
- Dependencies that haven't been cleaned up
- Cloud resources that failed to delete

#### Quick Debugging Checklist

When investigating cluster deletion issues:
- [ ] Check resource status and conditions
- [ ] Review relevant operator logs (HO, CPO)
- [ ] Inspect finalizers on stuck resources
- [ ] Verify CAPI resources are reconciling
- [ ] Check for events indicating failures
- [ ] Look for provider errors
- [ ] Verify namespace cleanup progress
- [ ] Check for webhook or admission errors

#### Common Issues and Resolutions

##### Issue: NodePool won't delete
- **Cause**: CAPI machines stuck due to provider errors
- **Resolution**: Check provider credentials, investigate machine deletion errors in HO logs

##### Issue: Machines stuck in "Deleting" phase with "WaitingForInfrastructureDeletion"
- **Cause**: Cluster resource deleted before machine resources, blocking CAPI controller reconciliation
- **Root Cause**: CAPI machine controllers require the cluster resource to be "ready" to proceed with deletion
- **Symptoms**:
  - Machines show `InfrastructureReady: 1 of 2 completed`
  - CAPI logs show cluster resource is not ready
  - Instances still running but controller can't terminate them
- **Resolution**: Provider-specific cleanup is required. See provider-specific troubleshooting:
  - Platform-specific cleanup: check the CAPI provider for the NodePool's platform (for us usually the **Agent** provider — Agent CRs and BareMetalHosts, not cloud instances)

##### Issue: HCP namespace stuck in Terminating
- **Cause**: Resources with finalizers or failing webhooks
- **Resolution**: List all resources in namespace, remove finalizers from orphaned resources, check webhook availability

##### Issue: HostedCluster stuck with finalizers
- **Cause**: Dependencies not fully cleaned up (NodePools, HCP, cloud resources)
- **Resolution**: Verify all dependent resources are deleted, check HO logs for reconciliation errors

##### Issue: Control plane pods not terminating
- **Cause**: PVCs or other resources with protection finalizers
- **Resolution**: Check PVC status, review storage class finalizers, inspect CPO logs

### Scenario: HyperShift CRDs Missing or Corrupted

When HyperShift CRDs are accidentally deleted or corrupted (e.g., after using `hypershift destroy infra`), you'll need to reinstall HyperShift.

**⚠️ WARNING: HyperShift reinstallation should be a last resort.** Only proceed if CRDs are genuinely missing or corrupted and cannot be recovered through other means. Reinstallation will cause downtime and may impact existing hosted-clusters.

#### Symptoms:
- Commands like `oc get hostedclusters` fail with: `error: the server doesn't have a resource type "hostedclusters"`
- HyperShift operator logs show errors about missing CRDs
- CRDs for HostedCluster, NodePool, or CAPI resources are missing

#### Check for Missing CRDs:
```bash
# Check if critical HyperShift CRDs exist
oc get crd hostedclusters.hypershift.openshift.io
oc get crd nodepools.hypershift.openshift.io

# Count HyperShift CRDs (should be ~9)
oc get crd | grep hypershift | wc -l

# Count CAPI CRDs (should be ~50)
oc get crd | grep cluster.x-k8s.io | wc -l
```

#### Resolution: Reinstall HyperShift

**🤖 AI Assistant Note:** When this scenario is encountered, Claude should guide and suggest the reinstallation steps to the user but NEVER execute the reinstallation commands itself. The user must explicitly run these commands. Provide clear instructions and explanations, but do not use the Bash tool to perform the actual reinstallation.

##### Step 1: Gather Required Parameters
```bash
# You'll need these for reinstallation:
# - Platform/provider configuration used originally (ours: Agent/bare metal)
# - Provider credentials (if applicable)
# - Any custom configuration flags used in original installation
```


##### Step 2: Completely Uninstall HyperShift
```bash
hypershift install render | oc delete -f -
```

This will:
- Remove the HyperShift operator deployment
- Delete all HyperShift CRDs (HostedCluster, NodePool, etc.)
- Clean up RBAC resources, webhooks, and other components

##### Step 3: Reinstall HyperShift
```bash
hypershift install \
  [provider-specific-flags] \
  --enable-defaulting-webhook true
```

Add any other flags that were part of your original installation.


##### Step 4: Verify Installation
```bash
# Check operator is running
oc get deploy -n hypershift
oc get pods -n hypershift

# Verify CRDs are installed
oc get crd | grep hostedcluster
oc get crd | grep nodepool
oc get crd | grep cluster.x-k8s.io | wc -l

# Test API accessibility
oc get hostedclusters -A

# Check operator logs for errors
oc logs -n hypershift deployment/operator --tail=50

# Verify controllers are running
oc logs -n hypershift deployment/operator --tail=100 | grep "Starting workers"
```

**Expected Results After Reinstallation:**
- Operator deployment: 2/2 READY
- HostedCluster CRD: Present
- NodePool CRD: Present
- CAPI CRDs: ~50 installed
- HyperShift CRDs: ~9 total
- Controllers: HostedCluster, NodePool, and other controllers with workers started
- Webhooks: Mutating webhook configured
- API: `oc get hostedclusters -A` returns successfully (even if no clusters exist)

**Important Notes:**
- Reinstallation does NOT affect existing hosted-clusters if their resources still exist
- If CRDs were deleted, any existing HostedCluster/NodePool resources are gone
- You may need to recreate hosted-clusters if their definitions were lost
- Ensure you use the same configuration flags as the original installation

## General Debugging Tips

### Checking Finalizers
```bash
# List all finalizers on a resource
oc get <resource-type> <name> -n <namespace> -o jsonpath='{.metadata.finalizers}'

# Remove a specific finalizer (use with caution!)
oc patch <resource-type> <name> -n <namespace> -p '{"metadata":{"finalizers":null}}' --type=merge
```

### Operator Logs
```bash
# HyperShift operator logs with context
oc logs -n hypershift deployment/operator --tail=500 --timestamps

# Control plane operator logs
oc logs -n <hcp-namespace> deployment/control-plane-operator --tail=500 --timestamps

# Follow logs in real-time
oc logs -n hypershift deployment/operator -f
```

### Resource Events
```bash
# Get events for a specific resource
oc describe <resource-type> <name> -n <namespace>

# Get all events in a namespace, sorted by time
oc get events -n <namespace> --sort-by='.lastTimestamp'
```

### Conditions and Status
```bash
# Check resource conditions
oc get <resource-type> <name> -n <namespace> -o jsonpath='{.status.conditions}' | jq .

# Check specific condition
oc get hostedcluster <name> -n <namespace> -o jsonpath='{.status.conditions[?(@.type=="Available")]}'
```

## Additional Resources

- HyperShift operator code: `hypershift-operator/controllers/hostedcluster/`
- Control plane operator code: `control-plane-operator/controllers/`
- API definitions: `api/hypershift/v1beta1/`
- E2E test examples: `test/e2e/`
