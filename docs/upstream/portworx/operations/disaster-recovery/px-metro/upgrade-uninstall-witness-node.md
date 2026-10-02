# Upgrade or uninstall witness node

Source: https://docs.portworx.com/portworx-enterprise/operations/disaster-recovery/px-metro/upgrade-uninstall-witness-node (Portworx Enterprise 3.6)

Upgrade or uninstall witness node | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Upgrade the Portworx OCI bundle​

Portworx provides a Docker-based installation utility to help deploy the Portworx OCI bundle. You can re-install this bundle by running the following Docker container on your host system:

```

REL="/3.0"  # Portworx v3.0 release

latest_stable=$(curl -fsSL "https://install.portworx.com$REL/?type=dock&stork=false&aut=false" | awk '/image: / {print $2}' | head -1)

# Download OCI bits (reminder, you will still need to run `px-runc install ..` after this step)

sudo docker run --entrypoint /runc-entry-point.sh \

    --rm -i --privileged=true \

    -v /opt/pwx:/opt/pwx -v /etc/pwx:/etc/pwx \

    $latest_stable

```

The following commands upgrade your Portworx OCI bundle to the latest stable:

```

latest_stable=$(curl -fsSL "https://install.portworx.com?type=dock&stork=false&aut=false" | awk '/image: / {print $2}' | head -1)

sudo docker run --entrypoint /runc-entry-point.sh \

    --rm -i --privileged=true \

    -v /opt/pwx:/opt/pwx -v /etc/pwx:/etc/pwx \

    $latest_stable --upgrade

sudo systemctl restart portworx

```

Once the update process is finished, you must restart the Portworx service.

note

If you are installing Portworx on RedHat Linux or RedHat CoreOS with CRI-O container runtime, you don't have to install Docker in order to install Portworx. Instead, simply replace `docker` command with `podman` (e.g. `sudo podman run --entrypoint...`).

## Uninstall the Portworx OCI bundle​

Run the following commands to uninstall the Portworx OCI bundle:

```

# 1: Remove systemd service (if any)

sudo systemctl stop portworx

sudo systemctl disable portworx

sudo rm -f /etc/systemd/system/portworx*

# NOTE: if the steps below fail, please reboot the node, and repeat the steps 2..5

# 2: Unmount oci (if required)

grep -q '/opt/pwx/oci /opt/pwx/oci' /proc/self/mountinfo && sudo umount /opt/pwx/oci

# 3: Remove binary files

sudo rm -fr /opt/pwx

# 4: [OPTIONAL] Remove configuration files. Doing this means UNRECOVERABLE DATA LOSS.

sudo chattr -ie /etc/pwx/.private.json

sudo rm -fr /etc/pwx

```

In this topic:
