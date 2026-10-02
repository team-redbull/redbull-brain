# Verify Portworx Docker image signatures with Cosign

Source: https://docs.portworx.com/portworx-enterprise/how-to-guides/verify-cosign (Portworx Enterprise 3.6)

Verify Portworx Docker image signatures with Cosign | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

This document explains how to ensure you are using a signed and verified Portworx container image for deploying container on your Kubernetes cluster. You can verify that a Portworx container image matches a trusted signature using Cosign. Cosign is part of the Sigstore project and is commonly used for container image signing and verification.

To verify Portworx image signature with Cosign, complete the following steps:

- Download Portworx Cosign public key

- Verify the image signature with Cosign

## Prerequisites​

Cosign is installed (v3.0.2 and above) on a machine that will access the image registry.

## Download Portworx Cosign public key​

-
Log in to Portworx Central and select Support.

-
In the Document and Other Guides section, locate Portworx Cosign Public Keys and click on Download Key.

-
Check the public key is downloaded and make a note of file path.

## Verify the image signature with Cosign​

Use the Cosign CLI to verify the Portworx image signature:

```

cosign verify --key <PATH_TO_COSIGN_PUBLIC_KEY> <PORTWORX_IMAGE_REFERENCE>

```

For example, to verify the Portworx Enterprise 3.5.2 Docker image:

```

cosign verify --key ~/Downloads/portworx-public-key-v1.pem portworx/px-enterprise:3.5.2

```

```

Verification for index.docker.io/portworx/px-enterprise:3.5.2 --

The following checks were performed on each of these signatures:

  - The cosign claims were validated

  - Existence of the claims in the transparency log was verified offline

  - The signatures were verified against the specified public key

[{"critical":{"identity":{"docker-reference":"index.docker.io/portworx/px-enterprise:3.5.2"},"image":{"docker-manifest-digest":"sha256:f8c5c8e953567e3823d1f599fb790xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx1244ca"},"type":"https://sigstore.dev/cosign/sign/v1"},"optional":{}}]

```

Note the following about the output:

- Cosign validated the signature metadata ensuring it adheres to the Cosign specification.

- The signature was found in the Sigstore transparency log.

- Cosign used the public key you provided to confirm that signature was created by the corresponding private key and that the signer is trusted.

This confirms that the Portworx Enterprise v3.5.2 image is provided by Portworx. In addition, this ensures that the image has not been altered and the signature is publicly auditable via Sigstore.

In this topic:
