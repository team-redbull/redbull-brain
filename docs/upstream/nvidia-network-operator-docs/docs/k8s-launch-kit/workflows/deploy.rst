.. license-header
  SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
  SPDX-License-Identifier: Apache-2.0

  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.

.. headings # #, * *, =, -, ^, "
.. include:: ../../common/vars.rst

****************
Deploy Workflow
****************

.. contents:: On this page
   :depth: 3
   :local:
   :backlinks: none

.. note::

   **Use this when:** you have generated manifests (from :doc:`generate`) and want to apply them to the cluster, or preview what would be applied.

================================================================================
Deploy to Cluster
================================================================================

Apply the generated manifests:

.. code-block:: bash

   l8k deploy

By default, ``l8k deploy`` reads the manifests in ``./deployment/`` (the output of ``l8k generate``) and uses ``$KUBECONFIG`` for cluster access.

You can also fold the deploy into the generate step by adding ``--deploy`` to ``l8k generate``:

.. code-block:: bash

   l8k generate --fabric ethernet --deployment-type sriov --multirail --deploy

================================================================================
Deployment Ordering
================================================================================

Launch Kit applies manifests in four phases. The first two block on reconciliation because everything else depends on them; the last two batch the remaining manifests so controllers reconcile concurrently:

#. **NicClusterPolicy** --- applied first, then awaited until the controller reports ``READY``. Per-component ``appliedStates[]`` are surfaced in the progress output ("ready: 7/12; pending: state-OFED, state-multus-cni, …") so an operator sees exactly which component is the laggard.
#. **NicNodePolicy** --- applied per group, awaited per policy (OFED driver, device plugins land here).
#. **Remaining manifests** --- every other CR (``SriovNetwork``, ``HostDeviceNetwork``, ``CIDRPool``, ``SpectrumXRailPoolConfig``, …) is applied in a single pass without per-manifest waits, so controllers reconcile concurrently.
#. **Verify** --- each manifest from phase 3 is polled until it reaches a terminal state. The four-state classification (READY / IN-PROGRESS / ERROR / MISSING) and per-Kind cross-checks (e.g., the SR-IOV silent-failure case where ``syncStatus=Succeeded`` but ``pfNames`` matched zero interfaces) are shared with :doc:`l8k validate <validate>`.

.. note::

   Example workload manifests (filenames matching ``*example*``) are **not** applied by ``l8k deploy``. They are fixtures consumed by the connectivity matrix in ``l8k validate --connectivity`` (or ``l8k deploy --verify``, see below) and are deployed only as part of that ping-matrix phase.

================================================================================
Deploy-wide Timeout
================================================================================

``l8k deploy`` has no per-manifest deadline. Pass ``--deploy-timeout <duration>`` to bound the whole apply + reconciliation phase end-to-end (e.g., ``45m``, ``2h``). Without the flag, deploy polls until every manifest reaches a terminal state or the user cancels --- the right default for SR-IOV configuration on large clusters where a single ``SriovNetworkNodePolicy`` reconciliation can outlast any small per-manifest budget.

.. code-block:: bash

   l8k deploy --deploy-timeout 90m

================================================================================
Dry-Run Mode
================================================================================

Preview what would be deployed without making changes:

.. code-block:: bash

   l8k deploy --dry-run

Dry-run mode is recommended before any first deployment and before production changes.

================================================================================
End-to-End Verification (--verify)
================================================================================

Pass ``--verify`` to chain a full data-plane verification right after a successful apply: ``l8k deploy --verify`` applies the manifests, waits for every controller to reconcile, then runs the connectivity ping matrix from :doc:`l8k validate <validate>` (apply the example DaemonSet, wait for every pod to be ``Ready``, ping every rail across every pod pair, clean up).

.. code-block:: bash

   l8k deploy --verify

The matrix's exit code propagates: a failed ping causes ``l8k deploy --verify`` to exit non-zero even though the manifests applied successfully. Combine with ``--keep`` (passed to validate) when debugging.

================================================================================
Manual Verification
================================================================================

You can also inspect the deployment manually:

.. code-block:: bash

   kubectl -n nvidia-network-operator get pods
   kubectl get nicclusterpolicy
   kubectl get nicnodepolicy

Per-group ``NicNodePolicy`` resources have names matching the group identifier (e.g., ``nicnodepolicy-group-0``). Each should reach the ``Ready`` state before workloads are applied.

If a deployment fails or stalls, see :doc:`../troubleshooting`.

================================================================================
See Also
================================================================================

- :doc:`Generate Workflow <generate>` --- producing the manifests
- :doc:`Heterogeneous Clusters <../heterogeneous-clusters>` --- per-group rollout strategies
- :doc:`Troubleshooting <../troubleshooting>` --- diagnosing failed deployments
- :doc:`Automation and CI/CD <../automation>` --- exit codes and JSON output for CI
