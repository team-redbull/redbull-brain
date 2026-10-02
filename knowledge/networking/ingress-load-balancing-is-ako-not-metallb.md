---
title: Service type LoadBalancer is provided by AKO (Avi / NSX ALB) — MetalLB is not an option here
type: knowledge
area: networking
tags: [ako, avi, nsx-alb, metallb, loadbalancer, ingress]
applies_to: []
confidence: verified
last_verified: 2026-10-03
owners: [platform-team]
source: team-decision
---

# LoadBalancer services use AKO, not MetalLB

## Symptom

Upstream docs, Red Hat docs and generated answers often suggest MetalLB for bare-metal
`type: LoadBalancer` services or for exposing hosted control planes.

## Decision

In our environment load balancing is done with **AKO (Avi Kubernetes Operator / NSX ALB)**.
MetalLB is not an option. Any design, runbook or fix that depends on MetalLB has to be translated
to AKO (VIPs come from Avi; config through AKO CRDs / annotations).

## Scope & caveats

All clusters, bare metal and vSphere, including HyperShift hosted clusters' service publishing.

## History

- 2026-10-03: seeded
