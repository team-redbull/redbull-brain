# Operation control with systemd

Source: https://docs.portworx.com/portworx-enterprise/operations/troubleshooting/operation-control-with-systemd (Portworx Enterprise latest)

Operation control with systemd | Portworx Enterprise Documentation

This guide shows how you can perform systemctl operations using kubectl or oc to control the Portworx systemd service. Portworx already manages the lifecycle of the systemd service and hence these operations should not be required in a properly functioning cluster.

caution

These operations should be performed only for debugging/troubleshooting purposes.

#### Service control​

note

You should not stop the Portworx systemd service while applications are still using it. Doing so can cause docker and applications to hang on the system. Migrate all application pods using `kubectl drain` or `oc drain` from the node before stopping the Portworx systemd service.

stop / start / restart the PX-OCI service

note

This is the equivalent of running `systemctl stop portworx`, `systemctl start portworx` … on the node.

- Kubernetes

- Openshift

```

kubectl label nodes minion2 px/service=start

kubectl label nodes minion5 px/service=stop

kubectl label nodes --all px/service=restart

```

```

oc label nodes minion2 px/service=start

oc label nodes minion5 px/service=stop

oc label nodes --all px/service=restart

```

enable / disable the PX-OCI service

note

This is the equivalent of running `systemctl enable portworx`, `systemctl disable portworx` on the node.

- Kubernetes

- Openshift

```

kubectl label nodes minion2 minion5 px/service=enable

```

```

oc label nodes minion2 minion5 px/service=enable

```

In this topic:
