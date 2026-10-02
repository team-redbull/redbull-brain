# Portworx SDK

Source: https://docs.portworx.com/portworx-enterprise/reference/developer-sdk (Portworx Enterprise latest)

Portworx SDK | Portworx Enterprise Documentation

Portworx storage systems use the open source OpenStorage SDK for its API.

### API Reference​

Access the API documentation at OpenStorage API Reference.

#### Versions​

You may need to determine the OpenStorage SDK version running on your Portworx storage system. To accomplish this, execute the following command on one of your Portworx nodes:

```

curl http://localhost:9021/v1/identities/version

```

```

{"sdk_version":{"minor":101,"patch":34,"version":"0.101.34"}...

```

You can then check the Changelog to determine what has been added.

### OpenStorage SDK Ports on Portworx systems​

When you connect your OpenStorage SDK client to Portworx you can use either the default gRPC port 9020 or the default REST Gateway port of 9021. If the port range has been configured to another location during installation, you will find the OpenStorage SDK ports by grepping for SDK in the Portworx container logs.

In this topic:
