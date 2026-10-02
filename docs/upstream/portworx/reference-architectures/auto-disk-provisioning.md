# Automatic driveset provisioning

Source: https://docs.portworx.com/portworx-enterprise/reference-architectures/auto-disk-provisioning (Portworx Enterprise 3.6)

Automatic driveset provisioning | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

In cloud environments, Portworx can dynamically create drivesets based on an input disk template whenever a new instance is created and use those drivesets for the Portworx cluster.
 Portworx fingerprints the drivesets and attaches them to the instance in the autoscaling cluster. In this way, each ephemeral instance receives its own identity.

### Why would I need this?​

- You do not need to manage the lifecycle of drivesets. Instead, only provide disk specifications, and Portworx will manage the lifecycle of drivesets.

- When an instance terminates, the AutoScaling group automatically adds a new instance to the cluster. Portworx gracefully handles this scenario by re-attaching the drivesets to the new instance and assigning it the identity of the previous one. This ensures that the instance’s data is retained without storage downtime.

## 📄️AWS

Learn EBS volume template that Portworx uses as reference

## 📄️GCP

Learn the GCP disk template that Portworx uses as reference.

## 📄️VMware vSphere

Learn architecture of VMware vSphere

In this topic:
