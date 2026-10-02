# Authorization using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/authorization (Portworx Enterprise 3.6)

Authorization using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Overview​

This page outlines how to interact with an authorization-enabled Portworx cluster. The main way to do it is by using the `pxctl context` command. Also, you can integrate with a generated token through `pxctl` command-line tool. Use your own JWT compliant application to generate security token. For more details, refer to the Generate tokens page.

## Contexts​

Portworx stores the following locally to your home directory, allowing you to switch between configurations with a few commands:

- contexts

- associated clusters

- privileges

- tokens

note

Since Portworx stores the context locally on each node, you must create your context on the node you're working on.

Run the `opt/pwx/bin/pxctl context` command with the `--help` flag to list the available subcommands and flags.

### Create a context​

You can create a new context by running the `pxctl context create` command and passing it the following arguments:

- the name of the context

- `--token` with the token Portworx must use for this context

- `--endpoint` with the endpoint for this context

Here's an example of how you can create a new context:

```

pxctl context create <context> --token <token> --endpoint <endpoint>

```

### Delete a context​

To delete a context, run the `pxctl context delete` command with the name of the context as in the following example:

```

pxctl context delete <context>

```

### List your contexts​

Portworx stores your contexts in the `~/.pxctl/contextconfig` directory. Use the `pxctl context list` command to view them:

```

pxctl context list

```

```

contextconfig:

  current: user

  configurations:

  - context: user

    token: XXXX

    identity:

      subject: user@example.com/username

      name: Example User

      email: user@example.com

    endpoint: http://localhost:9001

```

### Select the current context​

Once you've created your contexts, use the `pxctl context` command to switch between them. Under the hood, Portworx reads your current context and then uses the associated token for all commands.

note

Alternatively, you can use the global `--context` flag to run a single command with a given context.

Use the following command to set the current context:

```

pxctl context set <context>

```

Unset the current context with:

```

pxctl context unset

```

## How to debug token issues​

This section explains how to debug common token issues.

### Permission denied issues​

Problem symptom: You see an unexpected `Permission denied` or other auth-related error.

Find the root cause: Take a look into your token permissions. Decode and verify your token with a JWT token decoding tool such as jwt.io

note

The jwt.io debugger does client-side validation and debugging. It does not store your token anywhere.

### Protocol error​

Problem symptom: you see an error message similar to `rpc error: code = Internal desc = stream terminated by RST_STREAM with error code: PROTOCOL_ERROR`.

Find the root cause: Make sure your token doesn't contain a newline character. The `gRPC/http2` protocol doesn't allow newline characters. that your token does not accidentally contain a newline character. This is due to gRPC/http2 not allowing newline characters.

## Related topics​

- For information about enabling and managing Portworx authorization through Kubernetes, refer to the Authorization page.

In this topic:
