# Generate tokens

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/generate-token (Portworx Enterprise 3.6)

Generate tokens | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

With Portworx, you can use the `pxctl` command-line tool to generate a token. Run the `pxctl auth token generate` command with the `--help` flag to list the available subcommands and flags.

The `pxctl` command-line tool allows you to generate the tokens in the following ways:

- ECDSA

- RSA

- shared secret

For example, to generate a token with a shared secret, specify these flags:

- `--auth-config` with the path to the file providing account information

- `--shared-secret` with a string representing your shared secret.

- `--issuer` with the name of the issuer.

- `--output` with the name of the file

As an example, the following example generates a token:

```

echo "name: Example User

email: user@example.com

sub: user@example.com/username

roles: [\"system.user\"]

groups: [\"*\"]" > authconfig.yaml

pxctl auth token generate --auth-config=authconfig.yaml --issuer my_issuer \

    --shared-secret my_shared_secret \

    --output self-signed-token.txt

```

```

Token written to output file: self-signed-token.txt

```

Use the `cat` command to view the content of the `self-signed-token.txt` file:

```

cat self-signed-token.txt

```
