# Enable SSL Certificate Verification for FlashArray and FlashBlade

Source: https://docs.portworx.com/portworx-enterprise/platform/secure/verify-ssl-pure-arrays (Portworx Enterprise 3.6)

Enable SSL Certificate Verification for FlashArray and FlashBlade | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

Portworx Enterprise communicates with FlashArray and FlashBlade management endpoints over HTTPS. By default, these connections are encrypted, but Portworx does not verify the identity of the management endpoint.

Enable SSL certificate verification to have Portworx validate FlashArray and FlashBlade management certificates before establishing a trusted connection. Certificate verification helps protect management API communication from connections to untrusted or impersonated endpoints.

Configure certificate verification through the `SSLOptions` object in the `pure.json` configuration stored by your configured secret provider.

note

SSL certificate verification is disabled by default. Upgrading an existing Portworx cluster does not automatically enable certificate verification.

## Prerequisites​

Before you enable SSL certificate verification, ensure that your environment meets the following requirements:

- Portworx Enterprise 3.7.0 or later is installed.

- Your FlashArray and FlashBlade systems are already configured for use with Portworx Enterprise and `pure.json` is stored in your configured secret provider. For more information, see Prepare your environment for Portworx installation with FlashArray or Prepare your environment for Portworx installation with FlashBlade.

- The certificate presented by each management endpoint contains a Subject Alternative Name (SAN) that matches its `MgmtEndPoint` value in `pure.json`. If `MgmtEndPoint` is an IP address, the certificate must contain a matching IP SAN.

important

If an array uses a self-signed certificate that does not contain a SAN matching its `MgmtEndPoint`, replace or regenerate the certificate before enabling SSL certificate verification.

- The PEM-encoded CA certificates required to validate the array certificates if they are not trusted by the system CA store.

## Limitations​

Review the following limitations before you enable SSL certificate verification:

- SSL certificate verification settings apply to all FlashArray and FlashBlade systems configured in `pure.json`. You cannot configure certificate verification separately for individual arrays.

- SSL certificate verification validates certificates presented by FlashArray and FlashBlade systems but does not support mutual TLS (mTLS) client certificate authentication.

- SSL certificate verification does not apply to FADA and FBDA volume operations that use the FA/FB driver.

## Check the array certificates​

Before enabling certificate verification, verify the certificate presented by each FlashArray and FlashBlade management endpoint.

-
Verify that the certificate contains a SAN matching the MgmtEndPoint configured in pure.json:

```

openssl s_client -connect <management-endpoint>:443 </dev/null 2>/dev/null | \

  openssl x509 -noout -text | grep -A1 "Subject Alternative Name"

```

Example:

```

X509v3 Subject Alternative Name:

    DNS:flasharray1.example.com, IP Address:10.13.xx.xx

```

If the certificate does not contain a matching SAN, update the certificate before continuing.

-
If you use a private or enterprise CA, verify the certificate against your CA bundle:

```

openssl s_client -connect <management-endpoint>:443 \

  -CAfile ca.pem </dev/null 2>/dev/null | grep "Verify return code"

```

A successful validation returns:

```

Verify return code: 0 (ok)

```

Resolve any certificate validation errors before enabling SSL verification.

-
Repeat these checks for each FlashArray and FlashBlade MgmtEndPoint configured in pure.json.

## Enable SSL certificate verification​

### Step 1: Prepare the CA bundle​

important

Skip this step if all FlashArray and FlashBlade systems use certificates signed by a public CA. You do not need to provide a `CABundle`; Portworx Enterprise validates the certificates against the node's system CA pool.

Create a PEM file containing the required CA certificate chain and encode it as a single-line base64 string.

- Linux

- macOS

```

base64 -w 0 ca.pem

```

```

base64 -i ca.pem

```

note

If the certificate chain includes intermediate CA certificates, include the required CA chain in the PEM file before encoding it.

### Step 2: Configure SSLOptions​

Add the `SSLOptions` object to `pure.json`:

```

{

  "FlashArrays": [

    {

      "MgmtEndPoint": "<fa-management-endpoint>",

      "APIToken": "<fa-api-token>"

    }

  ],

  "FlashBlades": [

    {

      "MgmtEndPoint": "<fb-management-endpoint>",

      "APIToken": "<fb-api-token>",

      "NFSEndPoint": "<fb-nfs-endpoint>"

    }

  ],

  "SSLOptions": {

    "VerifySSL": true,

    "CABundle": "<base64-encoded-ca-bundle>"

  }

}

```

For field descriptions, see the `SSLOptions` object reference.

note

If the array certificates are trusted by the system CA store, configure `VerifySSL` as `true` and leave `CABundle` empty.

### Step 3: Update the stored configuration​

Update `pure.json` in the secret provider configured for your Portworx cluster.

- Kubernetes

- Vault

Update the `px-pure-secret` secret:

```

kubectl create secret generic px-pure-secret \

  --namespace <px-namespace> \

  --from-file=pure.json=<file-path> \

  --dry-run=client -o yaml | kubectl apply -f -

```

-
Update pure.json at the configured Vault path. For example:

```

vault kv put secret/pureJson pure.json=@<file-path>

```

-
Verify the stored value:

```

vault kv get secret/pureJson

```

### Step 4: Verify SSL certificate configuration​

Portworx reloads the updated `pure.json` during its credential refresh cycle.

After the configuration is applied:

-
Verify that Portworx can access the configured arrays:

```

pxctl status

```

-
Check for certificate-related alerts:

```

pxctl alerts show

```

-
If an array cannot be accessed, review the Portworx logs for certificate errors:

```

kubectl logs --since=10m \

  -n <px-namespace> \

  -l name=portworx \

  -c portworx | grep -iE "x509|tls|certificate"

```

Portworx does not fall back to an unverified connection when certificate verification fails. Correct the certificate or CA configuration before Portworx can establish a trusted connection to the affected management endpoint.

## Rotate the CA certificate​

When rotating a CA certificate, include both the existing and replacement CA certificates in `CABundle` while the array certificates are being updated. This helps maintain connectivity during the transition.

- Add the existing and replacement CA certificates to the PEM bundle and encode the bundle as described in Step 1: Prepare the CA bundle.

- Update `CABundle` in `pure.json` as described in Step 2: Configure SSLOptions.

- Update `pure.json` in your secret provider and allow Portworx to reload the configuration as described in Step 3: Update the stored configuration.

- Replace the management certificates on the FlashArray and FlashBlade systems.

- Verify that Portworx can connect to all management endpoints.

- After all arrays use certificates signed by the replacement CA, remove the old CA from `CABundle` and update `pure.json` again.

## Monitor certificate expiry​

During each credential refresh cycle, Portworx Enterprise checks the expiration date of the CA certificate in `CABundle`. Portworx Enterprise raises an alert when the certificate is within 30 days of expiration or has expired, allowing you to rotate the certificate before expiration affects connectivity to your arrays.

ConditionSeverity

The CA certificate in `CABundle` expires within 30 daysWarning

The CA certificate in `CABundle` has expiredAlarm

Certificate validation for an array failsWarning

To view these alerts, run:

```

pxctl alerts show

```

You can also monitor the alerts through your configured monitoring system. For more information, see Portworx Alerts and Monitor a Portworx cluster.

## Troubleshoot certificate verification​

Error or symptomCauseResolution

`x509: certificate signed by unknown authority`The certificate's signing CA is not trusted.Add the required CA and intermediate certificates to `CABundle`.

`x509: certificate is valid for <name>, not <endpoint>``MgmtEndPoint` does not match a SAN in the certificate.Update the certificate with the required SAN or use a `MgmtEndPoint` covered by the certificate.

`x509: certificate has expired or is not yet valid`The certificate is outside its validity period.Renew or replace the certificate.

`x509: cannot validate certificate ... because it doesn't contain any IP SANs``MgmtEndPoint` uses an IP address, but the certificate does not contain a matching IP SAN.Add the required IP SAN or use a DNS endpoint covered by the certificate.

CA bundle parsing fails`CABundle` does not contain a valid base64-encoded PEM bundle.Verify and re-encode the PEM bundle.

An array becomes unavailable after enabling verificationPortworx cannot validate the management certificate.Review the certificate errors, correct the certificate or CA configuration, and verify connectivity again.

To isolate certificate problems, repeat the `openssl` validation described in Check the array certificates from an affected Portworx node.

## Disable SSL certificate verification​

If you need to temporarily disable certificate verification:

-
Set `VerifySSL` to `false` in `pure.json` as described in Step 3: Update the stored configuration.

-
Update `pure.json` in your configured secret provider.

-
Allow Portworx to reload the updated configuration.

important

When SSL certificate verification is disabled, management traffic remains encrypted with HTTPS, but Portworx does not verify the identity of the management endpoint. Disable certificate verification only temporarily while resolving certificate issues.

In this topic:
