# Enable TLS Certificate Verification for vCenter

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/verify-ssl-vcenter (Portworx Enterprise 3.6)

Enable TLS Certificate Verification for vCenter | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise connects to the vCenter API over HTTPS to create and manage cloud drives on vSphere. If vCenter uses a certificate signed by a private certificate authority (CA), provide the CA certificate to Portworx Enterprise to enable certificate verification.

Portworx Enterprise uses the CA certificate to verify the identity of vCenter when connecting to the vCenter API. You can either store the certificate in the secret that contains your vCenter credentials, or mount the certificate as a file on the node and reference its path. In both cases, set `VSPHERE_INSECURE` to `false`.

## Prerequisites​

Before you enable certificate verification, ensure that your environment meets the following requirements:

- Portworx Enterprise 3.6.2.2 or later is installed on vSphere with cloud drives.

- Your vCenter credentials are stored in the `px-vsphere-secret` secret or your configured Vault secret. For more information, see Install Portworx on VMware vSphere.

- Obtain the CA certificates required to validate the certificate presented by vCenter.

- You have `openssl` available to inspect and validate certificates.

## How Portworx verifies the vCenter certificate​

The `VSPHERE_INSECURE` environment variable determines whether Portworx verifies the certificate presented by vCenter.

VSPHERE_INSECURECA certificateBehavior

`true`ProvidedPortworx connects without certificate verification and ignores the configured CA certificate.

`true`Not providedPortworx connects to vCenter without certificate verification.

`false` or unsetProvidedPortworx verifies the vCenter certificate by using the configured CA certificate.

`false` or unsetNot providedPortworx cannot initialize the vSphere provider and reports an error.

caution

Before you set `VSPHERE_INSECURE` to false or if it is unset, ensure that you have configured a valid CA certificate. Portworx does not fall back to a connection without certificate verification if validation fails.

## Check the vCenter certificate chain​

Before configuring certificate verification, identify the CA certificates required to validate the certificate presented by vCenter.

-
Download the trusted CA certificates from vCenter.

You can select Download trusted root CA certificates from the vSphere landing page.

Alternatively, download the certificates from:

```

https://<vcenter-fqdn>/certs/download.zip

```

Replace `<vcenter-fqdn>` with the fully qualified domain name (FQDN) of your vCenter Server.

Extract the downloaded archive.

note

Files with `.0` or `.1` extensions contain CA certificates in PEM format. Files with `.r0` or `.r1` extensions contain certificate revocation lists and should not be included in the CA bundle.

-
Inspect the certificate presented by vCenter:

```

openssl s_client -connect <vcenter-fqdn>:443 -showcerts </dev/null

```

In the output, entry `0` is the vCenter certificate. Use the `i:` line to identify the CA that issued the certificate.

important

Identify the issuing CA from the `i:` line rather than from the certificate file name or organization (`O=`) field. The downloaded certificate bundle might contain a VMware Certificate Authority (VMCA) root certificate whose organization matches the vCenter fully qualified domain name (FQDN), even when a different CA issued the vCenter certificate. Using the wrong CA certificate causes certificate verification to fail.

-
Inspect candidate CA certificates:

```

openssl x509 -in <certificate-file> -noout -subject -issuer

```

-
Determine which certificates to include, based on your CA hierarchy:

CA hierarchyCertificates to include

Default VMCAThe VMCA root certificate that signs the vCenter certificate.

Enterprise PKI with an intermediate CAThe issuing intermediate CA and root CA certificates.

PKI with multiple intermediate CAsEach CA certificate from the issuer of the vCenter certificate through the root CA.

important

- Include any intermediate CA certificates required to build the certificate chain. If an intermediate certificate is missing, certificate verification can fail with an `x509: certificate signed by unknown authority` error.

- Do not include the vCenter server certificate in the CA bundle. Include the CA certificates required to validate the vCenter certificate chain instead. This allows Portworx to continue validating the vCenter certificate when it is renewed by the same CA.

## Enable TLS certificate verification​

### Step 1: Prepare the CA bundle​

-
Combine the required CA certificates into a PEM file:

```

cat intermediate-ca.pem root-ca.pem > vcenter-ca-bundle.pem

```

note

When the CA bundle contains multiple certificates, Portworx Enterprise uses the appropriate valid certificate to verify the vCenter certificate and ignores certificates that are expired or invalid.

-
Verify the CA bundle against vCenter:

```

openssl s_client -connect <vcenter-fqdn>:443 \

  -CAfile vcenter-ca-bundle.pem </dev/null 2>/dev/null | grep "Verify return code"

```

A successful validation returns:

```

Verify return code: 0 (ok)

```

If validation fails, verify that the bundle contains the complete CA certificate chain. Repeat Check the vCenter certificate chain.

### Step 2: Add the CA certificate to your secret provider​

Use one of the following options to provide the CA certificate to Portworx Enterprise.

important

If you configure both options, `VSPHERE_CA_CERT_FILE` takes precedence. Portworx Enterprise reads the certificate from the specified path and ignores the `VSPHERE_CA_CERT` key in your secret.

#### Option 1: Store the certificate in your credentials secret​

- Kubernetes Secret

- Vault Secret

Add the CA bundle as the `VSPHERE_CA_CERT` key to the secret that contains your vCenter credentials. The following command creates the secret if it does not exist and updates it if it does:

```

kubectl create secret generic px-vsphere-secret \

  --namespace <px-namespace> \

  --from-literal=VSPHERE_USER=<vcenter-server-user> \

  --from-literal=VSPHERE_PASSWORD=<vcenter-server-password> \

  --from-file=VSPHERE_CA_CERT=./vcenter-ca-bundle.pem \

  --dry-run=client -o yaml | kubectl apply -f -

```

Add the CA bundle as a `VSPHERE_CA_CERT` field in the Vault secret that holds your vSphere credentials. Portworx reads the certificate from the secret provider configured for cloud provider credentials through `secretProviderPerFeature.cloudProviderCred`.
For more information, see Configure multiple secrets providers and Vault Secret Provider.

#### Option 2: Mount the certificate as a file​

Instead of storing the certificate in your credentials secret, you can mount the CA bundle from a separate secret and set the `VSPHERE_CA_CERT_FILE` environment variable to its path. This option lets you choose your own secret and key names.

Update your `StorageCluster` to mount the secret and reference the mounted path:

```

spec:

  env:

  - name: VSPHERE_CA_CERT_FILE

    value: "/etc/pwx/vcenter-certs/ca.crt"

  volumes:

  - name: vcenter-ca-cert

    mountPath: /etc/pwx/vcenter-certs

    readOnly: true

    secret:

      secretName: vcenter-ca-cert

      items:

      - key: ca.crt

        path: ca.crt

```

Portworx Enterprise reads the certificate directly from the path that you specify in `VSPHERE_CA_CERT_FILE`.

### Step 3: Enable certificate verification​

Set `VSPHERE_INSECURE` to `false` in the `spec.env` section of your `StorageCluster`:

```

spec:

  env:

  - name: VSPHERE_INSECURE

    value: "false"

```

Apply the updated `StorageCluster` configuration.

note

- Changing `VSPHERE_INSECURE` results in a rolling restart of all Portworx pods. Plan this change accordingly.

- Portworx applies the CA certificate configuration during startup. Therefore, certificate configuration changes require a cold restart of the Portworx storage process to take effect. A rolling restart initiated by the Portworx Operator, a node reboot, or a Portworx service restart triggered by applying the `px/service=restart` label to a node performs a cold restart.
Do not use `kubectl delete pod` to apply certificate configuration changes. Deleting a Portworx pod can result in a warm restart that reconnects to the existing Portworx process without reinitializing the vSphere provider. As a result, the updated certificate configuration might not take effect.

### Step 4: Verify the configuration​

After Portworx applies the configuration:

-
Verify that all Portworx nodes are online:

```

pxctl status

```

-
Validate that Portworx can connect to vCenter by using the credentials and CA certificate stored in your secret provider:

```

pxctl clouddrive credentials-validate --secret

```

This command validates the vCenter credentials and confirms that the account has the permissions that Portworx requires. For more information, see pxctl clouddrive.

## Rotate the CA certificate​

When you rotate the CA certificate used to sign the vCenter certificate, replace the existing CA bundle with the new CA certificates. This ensures that Portworx uses only the new CA certificates for verification.

-
Back up the secret that contains your vCenter credentials and CA bundle.

-
Replace the existing CA bundle in the secret with the new CA certificates. For more information, see Step 2: Add the CA certificate to your secret provider.

-
Verify that Portworx can connect to vCenter by using the new CA certificates. For more information, see Step 4: Verify the configuration.

-
If certificate verification fails, restore the secret from the backup and troubleshoot the failure. For more information, see Troubleshoot certificate verification.

note

You do not need to update the CA configuration when vCenter renews its server certificate using the same CA.

## Troubleshoot certificate verification​

If Portworx cannot verify the vCenter certificate, review the following common issues:

IssueCauseResolution

`x509: certificate signed by unknown authority`The CA bundle does not contain the complete certificate chain required to verify vCenter.Portworx Enterprise logs the complete certificate chain when this error occurs. Review the Portworx logs to identify the missing certificates, and then add the issuing CA and any required intermediate CA certificates to the bundle.

`VSPHERE_INSECURE is false but no vCenter CA certificate was provided`Certificate verification is enabled, but no CA certificate is configured.Configure `VSPHERE_CA_CERT`, or temporarily set `VSPHERE_INSECURE` to `true` while resolving the certificate configuration.

`VSPHERE_CA_CERT value contains no valid PEM certificate`The configured certificate is not valid PEM data.Verify that the CA certificate is in PEM format and includes the `BEGIN CERTIFICATE` and `END CERTIFICATE` delimiters.

`VSPHERE_INSECURE=true: ignoring the configured vCenter CA certificate`Portworx Enterprise logs this warning when a CA certificate is configured but certificate verification is disabled. This is not an error.Set `VSPHERE_INSECURE` to `false` to enable certificate verification.

`x509: certificate has expired or is not yet valid`A certificate in the validation chain is outside its validity period.Renew or replace the affected certificate.

Portworx continues to connect without certificate verification after configurationThe updated configuration has not been applied to the vSphere provider, because Portworx did not perform a cold restart.Restart Portworx by labeling the affected nodes with `px/service=restart`. For more information, see Step 3: Enable certificate verification.

## Disable TLS certificate verification​

caution

Changing `VSPHERE_INSECURE` triggers a rolling restart of the Portworx pods. Plan this change accordingly.

To temporarily disable certificate verification, set `VSPHERE_INSECURE` to `true` in the `StorageCluster` specification:

```

spec:

  env:

  - name: VSPHERE_INSECURE

    value: "true"

```

You can leave `VSPHERE_CA_CERT` configured while certificate verification is disabled. Portworx ignores the configured CA certificate when `VSPHERE_INSECURE` is set to `true`.

important

When certificate verification is disabled, traffic between Portworx and vCenter remains encrypted, but Portworx does not verify the identity of vCenter. Disable certificate verification only temporarily while resolving certificate issues.

In this topic:
