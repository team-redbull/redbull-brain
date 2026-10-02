# Volume access using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/volume-access (Portworx Enterprise 3.6)

Volume access using pxctl | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## Overview​

This document outlines how to manage your volume access rules. Portworx allows you to change access permissions per volume. There are two ways to provide access, one is by adding a group and the other is by adding a specific user as a collaborator. When adding a collaborator, you must use the unique id of the user. Please consult with your admin on how to obtain the unique id of the user.

## Access types​

When adding a group or collaborator, an access type must also be given, which can be either Read, Write, or Admin:

- Read access type allows access to the volume without modifying it. With a Read access type, one can clone or inspect the volume.

- Write access type allows modification of the volume and its metadata. For example, the user can mount, unmount, and restore the volume from a snapshot in addition to all Read access.

- Admin access type allows full access to the volume, like deleting the volume in addition to all Write access.

## Setting access types​

To set access types, add one of the following suffixes to the group or collaborator separated by a colon ':'

- r - For Read access type

- w - For Write access type

- a - For Admin access type

## Volume access commands​

The `pxctl` command-line utility supports the following commands for updating volume access permissions.

#### Add volume access for a single group or collaborator​

```

pxctl volume access add <volume> --collaborator user1:a

```

#### Remove volume access from a group or collaborator​

```

pxctl volume access remove <volume> --collaborator user1

```

#### Mark a volume as public​

```

pxctl volume access add <volume> --public r

```

#### Show volume access​

```

pxctl volume access show <volume>

```

#### Update full volume access spec​

```

pxctl volume access update <volume> --groups group1:r,group2:w --collaborators user1:a

```

#### Updating volume ownership​

```

pxctl volume access update <volume> --owner <username>

```

note

The volume owner can only be a single username. In addition, volume ownership updates can only be performed by administrators.

In this topic:
