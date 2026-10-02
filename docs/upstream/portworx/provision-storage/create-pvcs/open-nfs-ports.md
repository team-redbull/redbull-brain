# Open NFS ports

Source: https://docs.portworx.com/portworx-enterprise/provision-storage/create-pvcs/open-nfs-ports (Portworx Enterprise 3.6)

Open NFS ports | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

SharedV4 volumes utilize NFS services, and they therefore require specific open NFS ports to allow for communication between nodes in your cluster. Depending on how your cluster nodes are configured, your firewall may block some of these ports, or your NFS ports may differ from the defaults. To solve these issues, you may need to manually assign NFS ports and ensure that your firewall or ACL allows them to communicate.

Portworx supports the following types of ReadWriteMany volumes:

- sharedv4

- sharedv4 service

If a PersistentVolumeClaim (PVC) has ReadWriteMany (RWX) access mode, Portworx creates a sharedv4 service volume by default. Sharedv4 service volumes use NFSv4 by default, which means only port 2049 needs to be opened. However, sharedv4 volumes use NFSv3 by default. If your volumes use another port, see the Manually assign and open NFS ports section.

This document provides instructions for detecting and opening NFS ports according to various cluster configurations that you may have.

## Prerequisites​

- All of the use-cases in this document will require that the mandatory Portworx network port ranges are open between nodes in the cluster, as documented in system requirements.

- The `rpcbind` service must be enabled and running on each node in the cluster. Portworx Sharedv4 volumes use the NFS protocol, which requires the `rpcbind` service. This service helps NFS clients locate and connect to NFS services that provide Sharedv4 volumes.

## Determine which ports to open​

First, check what the existing NFS port configuration is for your nodes to see if they need to be remapped.

Enter the following command to find which ports NFS is using on your node:

```

rpcinfo -p

```

SharedV4 volumes communicate on the following standard ports/services:

- PortMapper: tcp/udp 111 (default on most Linux distributions)

- NFSd: tcp/udp 2049 (default on most Linux distributions)

- MountD: tcp/udp 20048 (depends on the Linux distribution)

If the ports listed from the above `rpcinfo` output on your nodes match these standard ports, proceed to Open standard NFS ports (most Linux distributions).

If the NFS ports on your OS do not match these ports, or your OS randomly chooses the ports for these services, proceed to Manually assign and open NFS ports.

## Open standard NFS ports (most Linux distributions)​

If your Linux distribution uses the standard ports identified in the previous section, you do not need to manually assign any ports for NFS, but you may need to open them.

Ensure that your ports are open on any firewalls and your ACL by entering the following commands:

```

iptables -I INPUT -p tcp -m tcp --match multiport --dports 111,2049,20048 -j ACCEPT

iptables -I OUTPUT -p tcp -m tcp --match multiport --dports 111,2049,20048 -j ACCEPT

```

Once you've determined that your hosts are using the standard ports and that you have opened those ports, you can start using SharedV4 volumes.

## Manually assign and open NFS ports​

For certain Linux distributions, the OS chooses the `mountd` port randomly every time the node reboots. To solve this, you must manually assign NFS ports, and how you accomplish this depends on your OS.

Only perform the steps in one of the following sections if one of the following is true:

- The `mountd` port is not fixed (and not the standard port of 20048) and is chosen at random by your Linux distribution.

- You wish to open a contiguous range of ports for Portworx and want to shift the default NFS ports to your Portworx port range.

In order to manually assign and open NFS ports, follow the steps in the section that applies for your OS.

### Assign NFS ports on the RedHat family of Linux (RHEL, CentOS, Fedora, etc)​

-
Modify the `/etc/sysconfig/nfs` file, uncommenting or adding the following fields and assigning the associated values:

- LOCKD_TCPPORT=9023

- LOCKD_UDPPORT=9024

- MOUNTD_PORT=9025

- STATD_PORT=9026

-
Enter the following command to restart the NFS server:

```

systemctl restart nfs-server

```

-
Open the newly assigned NFS ports on your access control list:

```

iptables -I INPUT -p tcp -m tcp --match multiport --dports 111,2049,9023,9025,9026 -j ACCEPT

iptables -I OUTPUT -p tcp -m tcp --match multiport --dports 111,2049,9023,9025,9026 -j ACCEPT

iptables -I INPUT -p udp -m udp --dport 9024  -j ACCEPT

iptables -I OUTPUT -p udp -m udp --dport 9024  -j ACCEPT

```

### Open NFS ports on Debian or Ubuntu Linux​

#### Debian 10 / Ubuntu​

-
Modify the `/etc/default/nfs-kernel-server` file. Uncomment or add the `RPCMOUNTDOPTS` field and add the `--port 9024` option to the value:

```

...

RPCMOUNTDOPTS="--manage-gids --port 9024"

```

-
Enter the following command to restart the `mountd` service:

```

systemctl restart nfs-mountd.service

```

-
Verify that the `mountd` service is running on the port that you configured by searching the output of `rpcinfo -p`:

```

rpcinfo -p | grep 'tcp.*mountd'

```

```

100005    1   tcp   9024  mountd

100005    2   tcp   9024  mountd

100005    3   tcp   9024  mountd

```

#### Debian 9 and lower​

-
Modify the `/run/sysconfig/nfs-utils` file, uncommenting or adding the following fields and assigning the associated values:

- `RPCNFSDARGS=" 8 --port 9023"`: append the `--port 9023` option to any existing values.

- `RPCMOUNTDARGS="--port 9024"`: add the `--port 9024` option.

- `STATDARGS="--port 9025 --outgoing-port 9026"`: add the `--port 9025` and `--outgoing-port 9026` options.

-
Enter the following commands to restart the NFS server:

```

systemctl daemon-reload

systemctl restart rpc-statd

systemctl restart rpc-mountd

systemctl restart nfs-server

```

-
Open the newly assigned NFS ports on your access control list:

```

iptables -I INPUT -p tcp -m tcp --match multiport --dports 111,2049,9023,9025,9026 -j ACCEPT

iptables -I OUTPUT -p tcp -m tcp --match multiport --dports 111,2049,9023,9025,9026 -j ACCEPT

iptables -I INPUT -p udp -m udp --dport 9024  -j ACCEPT

iptables -I OUTPUT -p udp -m udp --dport 9024  -j ACCEPT

```

### Open NFS ports on CoreOS​

The following sharedv4 NFS services run on a node when Portworx is installed with sharedv4 support:

- portmapper

- status

- mountd

- nfs and nfs_acl

- nlockmgr

View these services and the ports they are using by entering the following command:

```

rpcinfo -p

```

By default, services like `mountd` and `nlockmgr` run on random ports and must be fixed to a specific port.

#### Configure nfs, nfs_acl, and lockd ports​

By default, the `nfs-server.service` configuration file is located under the following directory:

```

/usr/lib/systemd/system/nfs-server.service

```

-
Check the status of the existing `nfs-server.service`:

```

systemctl status nfs-server

```

-
Copy the systemd unit file from the `usr` directory into the `etc` directory:

```

cp /usr/lib/systemd/system/nfs-server.service /etc/systemd/system/nfs-server.service

```

-
Open `/etc/systemd/system/nfs-server.service` in a text editor and, under the `[Service]` section, add the `--port 9023` value to the `ExecStart=/usr/sbin/rpc.nfsd` key:

```

[Service]

Type=oneshot

RemainAfterExit=yes

ExecStartPre=/usr/sbin/exportfs -r

ExecStart=/usr/sbin/rpc.nfsd --port 9023

ExecStop=/usr/sbin/rpc.nfsd 0

ExecStopPost=/usr/sbin/exportfs -au

ExecStopPost=/usr/sbin/exportfs -f

```

-
Update the `lockd` ports:

```

echo 9027 > /proc/sys/fs/nfs/nlm_udpport

echo 9028 > /proc/sys/fs/nfs/nlm_tcpport

```

-
Ensure that the `lockd` manager ports persist over node reboots by creating a `100-nfs-ports.conf` file under the `/etc/sysctl.d/` folder and adding the ports to it:

```

cat /etc/sysctl.d/100-nfs-ports.conf

fs.nfs.nlm_tcpport = 9027

fs.nfs.nlm_udpport = 9028

```

-
Reload the `systemd` daemon and restart the `nfs-server` service:

```

systemctl daemon-reload

systemctl restart nfs-server

```

-
Verify that the NFS services are running on the ports you configured by searching the output of `rpcinfo -p`:

```

rpcinfo -p | grep nfs

```

```

100003    3   tcp   9023  nfs

100003    4   tcp   9023  nfs

100227    3   tcp   9023  nfs_acl

```

```

rpcinfo -p | grep nlock

```

```

100021    1   udp   9027  nlockmgr

100021    3   udp   9027  nlockmgr

100021    4   udp   9027  nlockmgr

100021    1   tcp   9028  nlockmgr

100021    3   tcp   9028  nlockmgr

100021    4   tcp   9028  nlockmgr

```

#### Configure mountd services​

-
Check the status of the existing `nfs-server.service`:

```

systemctl status nfs-mountd

```

-
Copy the systemd unit file from `/usr` into `/etc`:

```

cp /usr/lib/systemd/system/nfs-mountd.service /etc/systemd/system/nfs-mountd.service

```

-
Open `/etc/systemd/system/nfs-mountd.service` in a text editor and, under the `[Service]` section, add the `--port 9024` value to the `ExecStart=/usr/sbin/rpc.mountd` key:

```

[Unit]

...

[Service]

Type=forking

ExecStart=/usr/sbin/rpc.mountd --port 9024

```

-
Reload the `systemd` daemon and restart the `nfs-server` service:

```

systemctl daemon-reload

systemctl restart nfs-server

```

-
Verify that the NFS services are running on the ports you configured by searching the output of `rpcinfo -p`:

```

rpcinfo -p | grep mountd

```

```

100005    1   udp   9024  mountd

100005    1   tcp   9024  mountd

100005    2   udp   9024  mountd

100005    2   tcp   9024  mountd

100005    3   udp   9024  mountd

100005    3   tcp   9024  mountd

```

#### Configure statd services​

-
Check the status of the existing `rpc-statd.service`:

```

systemctl status rpc-statd

```

-
Copy the systemd unit file from the `usr` directory into the `etc` directory:

```

cp /usr/lib/systemd/system/rpc-statd.service /etc/systemd/system/rpc-statd.service

```

-
Open `/etc/systemd/system/rpc-statd.service` in a text editor and, under the `[Service]` section, add the `--port 9025` and `--outgoing-port 9026` value to the `ExecStart=/usr/sbin/rpc.statd` key:

```

[Unit]

...

[Service]

Environment=RPC_STATD_NO_NOTIFY=1

Type=forking

PIDFile=/var/run/rpc.statd.pid

ExecStart=/usr/sbin/rpc.statd --port 9025 --outgoing-port 9026

```

-
Reload the `systemd` daemon and restart the `rpc-statd` service:

```

systemctl daemon-reload

systemctl restart rpc-statd

```

-
Verify that the NFS services are running on the ports you configured by searching the output of `rpcinfo -p`:

```

rpcinfo -p | grep status

```

```

100024    1   udp   9025  status

100024    1   tcp   9025  status

```

### Open NFS ports on PhotonOS​

-
Modify the `/etc/default/nfs-utils` file, adding parameters to assign ports to services:

```

MOUNTD_OPTS="--port 9024"

NFSD_OPTS="--port 9023"

STATD_OPTS="--port 9025 --outgoing-port 9026"

```

-
Add the `/etc/modprobe.d/lockd.conf` file to assign ports to the `nlockmgr` service and reconfigure runtime ports:

```

cat > /etc/modprobe.d/lockd.conf << .

options lockd nlm_tcpport=9027

options lockd nlm_udpport=9028

.

sysctl -w fs.nfs.nlm_tcpport=9027 fs.nfs.nlm_udpport=9028

```

-
Restart NFS services:

```

systemctl daemon-reload

systemctl restart nfs-server nfs-mountd rpc-statd

```

-
Open up the ports 9001 to 9028 in the `iptables` firewall, then restart the service:

```

# add Portworx ports 9001..9028 before "COMMIT"

sed -i~ '/^COMMIT/i -A INPUT -p tcp -m multiport --dports 111,9001:9028 -j ACCEPT' \

  /etc/systemd/scripts/ip4save

systemctl restart iptables

```

-
Verify that the NFS services are running on the ports that you just configured:

```

rpcinfo -p

```

```

program vers proto   port  service

 100000    4   tcp    111  portmapper

 100000    3   tcp    111  portmapper

 100000    2   tcp    111  portmapper

 100000    4   udp    111  portmapper

 100000    3   udp    111  portmapper

 100000    2   udp    111  portmapper

 100005    1   udp   9024  mountd

 100005    1   tcp   9024  mountd

 100005    2   udp   9024  mountd

 100005    2   tcp   9024  mountd

 100005    3   udp   9024  mountd

 100005    3   tcp   9024  mountd

 100024    1   udp   9025  status

 100024    1   tcp   9025  status

 100003    3   tcp   9023  nfs

 100003    4   tcp   9023  nfs

 100021    1   udp   9027  nlockmgr

 100021    3   udp   9027  nlockmgr

 100021    4   udp   9027  nlockmgr

 100021    1   tcp   9028  nlockmgr

 100021    3   tcp   9028  nlockmgr

 100021    4   tcp   9028  nlockmgr

```

In this topic:
