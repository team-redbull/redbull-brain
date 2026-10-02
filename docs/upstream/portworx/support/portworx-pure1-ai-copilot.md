# Portworx on Pure1 AI copilot

Source: https://docs.portworx.com/portworx-enterprise/support/portworx-pure1-ai-copilot (Portworx Enterprise latest)

Portworx on Pure1 AI copilot | Portworx Enterprise Documentation

Everpure AI copilot is an AI-powered capability that enables you to interact with your Portworx storage clusters using natural language. This conversational interface uses telemetry data from Portworx clusters and Everpure Pure1 to provide real-time insights and troubleshooting capabilities. For more information, see the AI Copilot user guide.

note

This feature requires an active Pure1 account and telemetry-enabled Portworx clusters. To enable telemetry and Pure1 integration, see Enable Pure1 integration.

## Key features​

Pure1 AI copilot provides insights across several key operational areas:

-
Portworx fleet information: Gain fleet-wide visibility with cluster summaries, node-level details, and a breakdown of clusters by volume count. Copilot helps you understand your global storage landscape at a glance.

-
Capacity and utilization: Track storage usage trends with summaries of utilization, identification of top and least utilized nodes, and detailed PVC usage statistics. These insights help you optimize resources and avoid over-provisioning.

-
Cluster health: Monitor volume, cluster, and pool capacity, along with storage configuration limits, node status, and licensing information. Copilot highlights failure points such as volume resize or initialization issues and detects NFS dependencies that may impact stability.

-
License management: Stay ahead of license expirations with proactive queries that reveal upcoming renewals. Copilot simplifies compliance and life-cycle planning across your fleet.

-
Software versions: Ensure version consistency and audit compliance with cluster version insights. Copilot helps identify clusters that need upgrades or fall outside approved baselines.

-
Documentation access: Retrieve release notes and technical documentation by using natural language. Copilot accelerates troubleshooting, configuration, and decision-making with fast, contextual answers.

## Prerequisites​

Make sure the following prerequisites are met before using Portworx on Pure1 AI Copilot:

- You must have a Pure1 account to access AI Copilot. If you don’t have an account, contact your Everpure account or sales representative.

- Cluster must have internet access to send diagnostic data to Pure1.

- You must enable telemetry to collect diagnostic data from the Portworx cluster and send it to Pure1. For more information about how to send diagnostic data to Pure1, see Enable Pure1 integration.

## How to use​

- Log in to Pure1 Manage.

- Navigate to AI Copilot.

- (Optional) At the beginning of the chat, select the Cloud Native Storage filter chip to view query suggestions for Portworx.

- Use the text box to enter your own question, or select a suggested query to get started.

## Example queries​

The following are example queries you can ask AI Copilot based on your role:

Persona or roleExample queryBenefit

Platform engineerShow clusters sorted by storage utilization.Enables proactive scaling and helps avoid capacity-related issues.

Kubernetes adminShow volumes that are more than 80% utilized.Speeds up problem resolution and supports better data hygiene.

DevOps engineerCheck the health for Portworx on cluster `abc`.Accelerates troubleshooting by identifying common Kubernetes issues.

IT managerWhich licenses are expiring in the next 30 days?Supports compliance checks and renewal planning.

Support / SREHow do I fix the Secure Boot install error?Provides context-aware, actionable troubleshooting guidance.

All usersList all my Portworx clusters.
 What is new in the latest version of Portworx Enterprise?Offers a fleet overview and surfaces updates for optimal usage.

In this topic:
