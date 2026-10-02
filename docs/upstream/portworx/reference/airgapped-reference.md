# Air-gapped install bootstrap script reference

Source: https://docs.portworx.com/portworx-enterprise/reference/airgapped-reference (Portworx Enterprise 3.6)

Air-gapped install bootstrap script reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

To download the air-gapped installation bootstrap script on an internet-connected host with the same architecture and OS version as the Kubernetes cluster nodes intended for Portworx installation, use the following command:

```

./px-ag-install.sh [image-commands] [options] '[arguments...]'

```

note

The script name `px-ag-install.sh` reflects the default name specified in the installation instructions, but can be whatever you named the script file when you downloaded it.

### Image commands​

CommandDescriptionRequired?

`pull`Pulls the Portworx container images locally

`push <registry[/repo]>`Pushes the Portworx images into remote container registry server

`load node1 [node2 [...]]`Loads the images tarball to remote nodes (note: ssh-access required)

### Options​

OptionDescriptionRequired?

`--help`Displays help output

`-I`, `--include <image>`Specify additional images to include

`-E`, `--exclude <glob>`Specify images to EXCLUDE (e.g. -E 'csi')

`-n`, `--dry-run`Show commands instead of running

`-V`, `--version`Print version of the script

`-v`Verbose output

### Load-specific options​

OptionDescriptionRequired?

`-e`, `--rsh <command>`specify the remote shell to use (default ssh)

`-L`, `--load-cmd <command>`specify the remote container-load command to use (default auto)

`-t <prefix>`specify temporary tarball filename (default px-agtmp.tar)

`--pks`assume PKS environment; transfer images using 'bosh' command

### Examples​

-
Pull images from default container registries, push them to custom registry server (default repositories)

```

px-ag-install.sh pull push your-registry.company.com:5000

```

-
Pull images from default container registries, push them to custom registry server and portworx repository

```

px-ag-install.sh pull

px-ag-install.sh push your-registry.company.com:5000/portworx

```

-
Push images to password-protected remote registry, then import docker/podman configuration as kubernetes secret

```

docker login your-registry.company.com:5000

px-ag-install.sh pull

px-ag-install.sh push your-registry.company.com:5000/portworx

px-ag-install.sh import-secrets

```

-
Pull images, then load to given nodes using ssh

```

px-ag-install.sh pull

px-ag-install.sh load node1 node2 node33 node444

```

-
Pull images, then load to given nodes using ssh and root-account

```

px-ag-install.sh -e "ssh -l root" pull load node1 node2 node33 node444

```

-
Load images to given nodes using ssh and password '5ecr3t'

```

px-ag-install.sh -e "sshpass -p 5ecr3t ssh" load node1 node2 node33 node444

```

-
Pull ONLY busybox image, load it to given nodes

```

px-ag-install.sh -E '*' -I docker.io/busybox:latest pull load node1 node2 node33 node444

```

In this topic:
