# FlashArray and FlashBlade JSON file reference

Source: https://docs.portworx.com/portworx-enterprise/reference/pure-reference/pure-json-reference (Portworx Enterprise latest)

FlashArray and FlashBlade JSON file reference | Portworx Enterprise Documentation

Portworx uses a single secret for both FlashArray and FlashBlade configuration. If you are planning on using both together, specify all of your FlashBlade and FlashArray entries in a single JSON file.

note

You can provision Portworx Enterprise to automatically create and maintain the `pure.json` configuration file by enabling Portworx Fusion Controller in your Portworx cluster. After you enable Portworx Fusion Controller, you do not need to manually generate or manage individual FlashArray or FlashBlade tokens or update the configuration file when arrays are added or removed from the fleet. Portworx Fusion Controller handles discovery and token management through Fusion Coordinator, reducing operational overhead and simplifying integration with Portworx Enterprise.
For more information on how to enable Portworx Fusion Controller, see Enable Portworx Fusion Controller.

```

{

    "FlashArrays": [

        {

            "MgmtEndPoint": "<management-endpoint-of-first-fa>",

            "APIToken": "<first-fa-api-token>"

        },

        {

            "MgmtEndPoint": "<management-endpoint-of-second-fa>",

            "APIToken": "<second-fa-api-token>"

        }

    ],

    "FlashBlades": [

        {

            "MgmtEndPoint": "<management-endpoint-of-first-fb>",

            "APIToken": "<api-token-of-first-fb>",

            "NFSEndPoint": "<nfs-endpoints-of-first-fb>"

        },

        {

            "MgmtEndPoint": "<management-endpoint-of-second-fb>",

            "APIToken": "<api-token-of-second-fb>",

            "NFSEndPoint": "<nfs-endpoints-of-second-fb>"

        }

    ],

    "SSLOptions": {

        "VerifySSL": true,

        "CABundle": "<base64-encoded-ca-bundle>"

    }

}

```

### FlashArray object reference​

KeyValueRequired?

`MgmtEndPoint`Your FlashArray management endpoint.
Data type: string
Format: either an IP address or a fully qualified domain name (without a protocol).

Note: For IPv6 addresses, ensure that the IP address is enclosed in square brackets, for example: `"MgmtEndPoint": "[XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX]"`.
Yes

`APIToken`Your FlashArray API token.
Data type: string
Format: XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXYes

### FlashBlade object reference​

KeyValueRequired?

`MgmtEndPoint`Your FlashBlade management endpoint.
Data type: string
Format: either an IP address or a fully qualified domain name (without a protocol).

Note: For IPv6 addresses, ensure that the IP address is enclosed in square brackets, for example: `"MgmtEndPoint": "[XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX]"`.
Yes

`APIToken`Your FlashBlade API token.
Data type: string
Format: T-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXYes

`NFSEndPoint`Your FlashBlade NFS endpoint.
Data type: string
Format: either an IP address or a fully qualified domain name (without a protocol).

Note: For IPv6 addresses, ensure that the IP address is enclosed in square brackets, for example: `"MgmtEndPoint": "[XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX]"`.
Yes

### `SSLOptions` object reference​

The optional `SSLOptions` object controls SSL certificate verification for FlashArray and FlashBlade management endpoints. `SSLOptions` is a top-level object in `pure.json` and applies to all configured arrays. If you omit this object, Portworx Enterprise encrypts management traffic but does not verify certificates presented by the management endpoints.

note

`SSLOptions` requires Portworx Enterprise 3.7.0 or later. For configuration and troubleshooting information, see Enable SSL Certificate Verification for FlashArray and FlashBlade.

KeyValueRequired?

`VerifySSL`Specifies whether Portworx Enterprise verifies certificates presented by FlashArray and FlashBlade management endpoints.

Data type: Boolean
Default: `false`

When set to `true`, Portworx Enterprise validates each certificate against the node's system CA pool and any CA certificates provided in `CABundle`. The certificate for each management endpoint must contain a Subject Alternative Name (SAN) that matches its `MgmtEndPoint` value.No

`CABundle`Specifies the CA certificate or certificate chain used to verify certificates that are not trusted by the node's system CA pool.

Data type: String
Format: Base64-encoded PEM certificate or certificate chain, provided as a single-line string
Default: `""`

Specify this value for self-signed certificates or certificates signed by a private enterprise CA. You can omit it when the certificates are trusted by the node's system CA pool. Portworx Enterprise ignores this value when `VerifySSL` is `false`.No

## Related topics​

- Portworx with FlashArray

- Configure FlashBlade as a Direct Access filesystem

- Verify SSL Certificates for FlashArray and FlashBlade Connections

In this topic:
