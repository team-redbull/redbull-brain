# RBAC role management using pxctl

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/role (Portworx Enterprise latest)

RBAC role management using pxctl | Portworx Enterprise Documentation

## Overview​

Starting with version 2.1, Portworx introduced support for RBAC. This document outlines how to manage your own custom roles for fine-grained access control within your Portworx clusters.

## Default Roles​

Portworx comes with a few standard roles that you can use when issuing tokens to users:

- system.admin: can run any command

- system.view: can only run read-only commands

- system.user: can only access volume lifecycle commands

- system.guest: similar to system.user, but for public volumes only.

All of these roles are immutable, except for system.guest. Admins may update the system.guest role to change how Portworx RBAC handles unauthenticated users.

## Custom Roles​

`pxctl role` gives you more fine-grained control over what users can do within your clusters. Run the `pxctl role` command with the `--help` flag to list the available subcommands and flags.

### Creating a custom role from a JSON file​

To define a custom role, you should first create a `JSON` file that describes that role. Say you've created a file named `role.json`. Then, to create the custom role, you will have to run this command:

```

pxctl role create --role-config role.json

```

Run the `pxctl role create` command with the `--help` flag to list the available subcommands and flags.

#### Role configuration​

A role configuration is comprised of a name and a list of rules. Each rule has the following:

- Services: Which services you want to provide access to.

- APIs: Which APIs you want to provide access to. You can use a simple regular expression to represent multiple APIs. i.e. to allow all enumerate APIs, add an entry `*enumerate*` to your `"apis"` array (see below).

Example configuration (role.json):

The following example configuration only allows access to volume enumerate commands and all inspect APIs for every service.

```

{

 	"name": "test.view",

 	"rules": [{

 			"services": [

 				"volumes"

 			],

 			"apis": [

 				"*enumerate*"

 			]

 		},

 		{

 			"services": [

 				"*"

 			],

 			"apis": [

 				"inspect*"

 			]

 		}

 	]

}

```

### Services and APIs​

To see all services and APIs you can use within your custom roles, see our API documentation.

### Other role commands​

- To delete a role, you can use `pxctl role delete <name>`

- To list all roles, you can use `pxctl role list`

- To update a role, you can use `pxctl role update --role-config <path to JSON config>`. This `JSON` config file is similar to the one used for `pxctl role create`.

## Using your custom roles​

Once you've created your custom roles, you can simply add the role names during token generation/user management.

Add the custom role in your auth-config during token creation:

```

name: User Name

email: user@example.com

sub: user@example.com/user

roles: ["test.view"]

groups: ["*"]

```

This token will now allow access to whichever services and APIs were defined in the custom role `test.view`.

## Updating the System Guest role​

Updating the `system.guest` role will change how Portworx authorization handles users that do not pass a token to any Portworx operation or SDK call. For more information, see the guest role overview.

### Disabling the System Guest role​

To disable the system.guest role, perform the following steps:

-
On one of your Portworx nodes, create the following `role.json` file:

```

{

  "name": "system.guest",

  "rules": [{

    "services": [

      "!*"

    ],

    "apis": [

      "!*"

    ]

  }]

}

```

-
Run the following `pxctl role update` command, specifying your `role.json` config:

```

pxctl role update --role-config role.json

```

### Re-enabling the system.guest role​

To re-enable the `system.guest` role to its default behavior, perform the following steps:

-
Create the following `role.json` file:

```

{

  "name": "system.guest",

  "rules": [{

      "services": [

        "mountattach",

        "volume",

        "cloudbackup",

        "migrate"

      ],

      "apis": [

        "*"

      ]

    },

    {

      "services": [

        "identity"

      ],

      "apis": [

        "version"

      ]

    },

    {

      "services": [

        "cluster",

        "node"

      ],

      "apis": [

        "inspect*",

        "enumerate*"

      ]

    }

  ]

}

```

-
Run the following `pxctl role update` command, specifying your `role.json` config:

```

pxctl role update --role-config role.json

```

In this topic:
