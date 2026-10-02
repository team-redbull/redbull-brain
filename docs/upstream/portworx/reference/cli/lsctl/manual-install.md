# Manually install a Portworx license server

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/lsctl/manual-install (Portworx Enterprise latest)

Manually install a Portworx license server | Portworx Enterprise Documentation

Perform the steps in this topic to manually install a Portworx license server.

## Prerequisites​

- The Docker service installed and running

- The `docker-compose` command available

## Manually install a Portworx license server​

-
To determine the latest image for the license-server, run the following command:

```

latest_stable=$(curl -fsSL https://install.portworx.com/pxcentral-air-gapped | \

   awk '/px-els:/{print $2}' | tr -d \" )

echo $latest_stable

```

```

docker.io/portworx/px-els:2.3.2

```

-
Pull the license server from Portworx:

```

docker pull $latest_stable

```

note

If your cluster is air-gapped, you must first pull the Portworx license server Docker images either to your docker registry or directly to the nodes:

-
If you have a company-wide docker-registry server, pull the Portworx license server from Portworx:

```

curl -o px-ag-install.sh https://install.portworx.com/air-gapped

sh px-ag-install.sh -E '*' -I $latest_stable pull push <company-registry-hostname>

```

-
If you do not have a company-wide docker-registry server, pull the Portworx license server image onto a computer that can access the internet and send it to your air-gapped cluster nodes:

```

sh px-ag-install.sh -E '*' -I $latest_stable pull load <air-gapped-node1> <air-gapped-node2...>

```

-
Create and start the following `docker-compose.yml` file, adding any options to the following services.px-els-main.command: line:

-
If your cluster is air-gapped, add `-air-gapped` and `-nic` with the network interface your host uses to connect with the rest of the cluster.

-
If you're using SSL, add `-enable-ssl` and specify the location of your SSL certificate with optional CA and key-file with the `-ssl-certs </path/to/server-bundle.crt>` and `-ssl-key /path/to/server.key` flags.

```

# update image version below with current $latest_stable

version: '2.2'

services:

  px-els-main:

    container_name: px-els

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

```

docker-compose up -d

```

```

Creating px-els ... done

```

-
Verify the license server's status by entering the following command:

```

docker-compose logs -f

```

```

Attaching to px-els

...

time="2022-12-14T08:23:43Z" level=info msg="License server RUNNING as PxProxyServer{id=0xc0001a4f30,ver=px-els/2.3.2-0-g64173d7,addr=:7070,SSL=false} ..."

```

The message beginning with `License server RUNNING` indicates success.

-
Once the License Server is operational, log in to it by entering the `lsctl login` command, specifying the username `-u admin` and default password `-p 'Adm1n!Ur'` credentials with the endpoint of your license server:

```

/opt/pwx-ls/bin/lsctl login -u admin -p 'Adm1n!Ur' http://<host>:<port>

```

note

If you enabled SSL, you must first log in using the `lsctl login -u admin https://...` command before using any other lsctl commands.

-
Verify the deployment completed successfully:

```

/opt/pwx-ls/bin/lsctl info health

```

```

INFO[0000] ELS instanceID TPAXKSG96V6J reports healthy status

```

-
Connect your Portworx cluster or clusters to the license server. From one of your Portworx worker nodes, Enter the following `pxctl` command, specifying the `<host>` and `<port>` of your license server:

```

/opt/pwx/bin/pxctl license setls http://<host>:<port>/fne/bin/capability

```

```

Successfully set license server.

```

-
(Recommended) Create a backup server and enable high availability.

important

You cannot enable high availability after adding your licenses.

If you did not enable high availability prior to adding your licenses, the `lsctl ha conf` command will fail. If this happens to you, please contact Portworx support to update your license.

Once you've installed your license server and, optionally, your backup license server, you're ready to add your licenses.

In this topic:
