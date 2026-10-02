# Wipe Portworx from an air-gapped cluster

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/px-wipe-airgapped (Portworx Enterprise latest)

Wipe Portworx from an air-gapped cluster | Portworx Enterprise Documentation

When wiping Portworx in Kubernetes, a number of Docker images are fetched from registries on the internet. If your nodes don't have access to the public container registries, you can load these images onto your nodes manually. Perform the steps below to wipe Portworx from an air-gapped cluster.

## Step 1: Download the wiper script​

Download the wiper script and save it to any node which has cluster admin access (`kubectl` or `oc`) to your cluster.

Alternately, you can also use `curl`:

```

curl -o px-wipe.sh -L "https://install.portworx.com/3.0/px-wipe"

```

## Step 2: Download the images that the wiper script will use​

If you followed your platform's [air-gapped install] instructions, you should already have all the necessary images available for your nodes:

- Airgapped Bare Metal

- EKS Airgapped

- Air-gapped on OpenShift vSphere

If you did not, or require different versions of images uploaded, follow one of the steps below:

- Step 2a: Push to local registry server: If you have access to a local registry server on an intranet, you can place the images that the wiper script will use there.

- Step 2b: Push directly to your nodes: If you do not have access to a local registry server on an intranet, you must place the images directly on your nodes.

### Step 2a: Push to local registry server, accessible by air-gapped nodes​

```

curl -fsSL "https://install.portworx.com/3.0/air-gapped" | sh -s -- \

    -E '*' -I portworx/talisman:1.1.0 -I portworx/px-node-wiper:2.5.0 pull push <YOUR_REGISTRY_LOCATION>

```

For example:

```

curl -fsSL "https://install.portworx.com/3.0/air-gapped" | sh -s -- \

    -E '*' -I portworx/talisman:1.1.0 -I portworx/px-node-wiper:2.5.0 pull push myregistry.net:5443

```

### Step 2b: Push directly to your nodes​

```

curl -fsSL "https://install.portworx.com/3.0/air-gapped" | sh -s -- \

    -E '*' -I portworx/talisman:1.1.0 -I portworx/px-node-wiper:2.5.0 pull load node1 node22 node333

```

## Step 3: Run the wiper script​

If you uploaded the container images to your local registry server, you will need to run the wiper script downloaded earlier with your registry server image names:

```

REGISTRY=myregistry.net:5443

bash px-wipe.sh -I $REGISTRY/portworx/talisman -wi $REGISTRY/portworx/px-node-wiper

```

Otherwise, if you uploaded container images directly to nodes, you can run the script without any arguments:

```

bash px-wipe.sh

```

In this topic:
