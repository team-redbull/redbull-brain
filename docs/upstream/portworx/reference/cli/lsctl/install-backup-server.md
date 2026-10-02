# Install a backup license server

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/lsctl/install-backup-server (Portworx Enterprise latest)

Install a backup license server | Portworx Enterprise Documentation

After you've created your license server, but before you add licenses, you can create a backup license server. A backup license server synchronizes with your main license server to provide high availability (HA), which protects your Portworx clusters from interruption in the event that your primary server experiences a problem.

## Prerequisites​

- The Docker service installed and running

- The `docker-compose` command available

- Your existing license server's credentials; you must use the same credentials for both the main and backup license servers.

## Determine the latest image​

To determine the latest image for the license-server, run the following command:

```

latest_stable=$(curl -fsSL https://install.portworx.com/pxcentral-air-gapped | \

    awk '/px-els:/{print $2}' | tr -d \" )

echo $latest_stable

```

```

docker.io/portworx/px-els:2.3.2

```

## Enable HA​

note

If your cluster is air-gapped, you must first pull the Portworx license server Docker images to either your docker registry or directly to the nodes. For example:

```

curl -o px-ag-install.sh https://install.portworx.com/air-gapped

# push image to the company's registry server

sh px-ag-install.sh -E '*' -I $latest_stable pull push <company-registry-hostname>

# alternatively, push the image directly to the air-gapped nodes

sh px-ag-install.sh -E '*' -I $latest_stable pull load <air-gapped-node1> <air-gapped-node2...>

```

-
Create and start the following `docker-compose.yml` file, specifying the following:

-
If your cluster is air-gapped, add `-air-gapped` and `-nic` with the network interface your host uses to connect with the rest of the cluster.

-
If you're using SSL, add `-enable-ssl`, and specify the location of your SSL certificate with optional CA and key-file with the `-ssl-certs </path/to/server-bundle.crt>` and `-ssl-key /path/to/server.key` flags.

```

# update image version below with current $latest_stable

version: '2.2'

services:

  px-els-main:

    container_name: px-els-backup

    image: portworx/px-els:1.0.0

    # command: -air-gapped -nic eth0 -extl-port 7070

    # command: -enable-ssl -ssl-certs /ssl/server-bundle.crt -ssl-key /ssl/server.key

    privileged: true

    network_mode: host

    restart: always

    volumes:

      - /opt/pwx-ls/bin:/export_bin

      - /var/lib/pwx-ls:/data

      - /proc:/hostproc

      - /opt/pwx-ls/ssl:/ssl

    healthcheck:

        test: ["CMD", "curl", "-fI", "http://127.0.0.1:7069/api/1.0/instances/~/health"]

        interval: 2m30s

        timeout: 30s

        retries: 3

```

note

- You must use the same credentials for both the main and backup license servers.

- You can change the admin password with the `lsctl users passwd admin` command.

```

docker-compose up -d

```

```

Creating px-els ... done

```

-
Verify the license server's status by entering the `docker-compose logs` command with the `-f` (follow-logs) option:

```

docker-compose logs -f

```

```

Attaching to px-els-backup

...

time="2022-12-14T08:23:43Z" level=info msg="License server RUNNING as PxProxyServer{id=0xc0001a4f30,ver=px-els/2.3.2-0-g64173d7,addr=:7070,SSL=false} ..."

```

The message beginning with `License server RUNNING` indicates success.

-
Log in to your main license server and enable high availability (HA). Enter the `lsctl ha conf` command and the `-m` (main endpoint) flag with the endpoint of your main license server and the `-b` (backup endpoint) flag with the endpoint of your backup license server:

```

/opt/pwx-ls/bin/lsctl login -u admin -p '<password>' http://<main-host>:<main-port>

/opt/pwx-ls/bin/lsctl ha conf -m http://<main-host>:<main-port> -b http://<backup-host>:<backup-port>

```

```

WARN[0000] Changed main URL from http://<host>:7070 to http://X.X.X.0:7070/fne/bin/capability

WARN[0000] Changed backup URL from <host> to http://X.X.X.1:7070/fne/bin/capability

INFO[0000] Backup license server updated

INFO[0000] Main license server updated (restarting in 15 seconds)

> Restarting Main license server: .....................

INFO[0048] Successfully set up Main/Backup license servers for HA

```

-
Verify your HA configuration:

```

/opt/pwx-ls/bin/lsctl ha info

```

```

High Availability configuration (Main):

                            Main URI : http://X.X.X.129:7070/fne/bin/capability

                          Backup URI : http://xx.xx.97.67:7070/fne/bin/capability

     Synchronization to Main enabled : false                                          (Mandatory on backup server)

            Synchronization pagesize : 100

            Synchronization interval : 5m

         Synchronization retry count : 1

Synchronization retry repeat interval : 1m

    Active license server identifier : AC1F6B221662/ETHERNET

    Backup license server identifier : 000C2909B6BD/ETHERNET

```

Once you've created and configured your license servers, you can populate the licenses on the main license server.

In this topic:
