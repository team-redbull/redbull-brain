# Lsctl command reference

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/lsctl/lsctl-reference (Portworx Enterprise 3.6)

Lsctl command reference | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

## lsctl​

The license server command line interface

```

lsctl [global options] command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl login`Log into the License Server, preserve configuration

`lsctl info`License server information

`lsctl client`Manage clients

`lsctl license`Manage/Load License server's licenses

`lsctl users`Manage users

`lsctl ha`License server High Availability setup

`lsctl help`, `h`Shows a list of commands or help for one command

#### Options​

OptionDescription

`--help`, `-h`show help

`--version`, `-v`print the version

## lsctl info​

License server information

```

lsctl info command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl info health`Display Health info

`lsctl info hostids`Display License server's hostIDs

`lsctl info endpoint`Display License server's endpoint

`lsctl info version`Display versions

#### Options​

OptionDescription

`--help`, `-h`show help

## lsctl client​

Manage attached Portworx clients

```

lsctl client command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl client ls`Display clients details

`lsctl client usage`Display clients checked-out features

#### Options​

OptionDescription

`--help`, `-h`show help

## lsctl login​

Log in to the license server

```

lsctl login [OPTIONS] <endpoint> [<instance>]

```

#### Options​

OptionDescription

`-u` value, `--username` valueSpecify username

`-p` value, `--password` valueSpecify password

`--allow-unknown-root-ca`Allow the license server to import an unknown SSL Root certificate authority

## lsctl license​

Manage and load license server's licenses

```

lsctl license command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl license ls`Display available license features details

`lsctl license activate`Activate licensing codes for license server

`lsctl license add`Adds a binary license file to license server

#### Options​

OptionDescription

`--help`, `-h`show help

## lsctl users​

Manage users

```

lsctl users command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl users ls`Lists users

`lsctl users create`Create new user

`lsctl users setrole`Set existing user's roles

`lsctl users passwd`Change existing user's password

`lsctl users delete`, `lsctl users rm`Delete user by ID

#### Options​

OptionDescription

`--help`, `-h`show help

## lsctl ha​

License server High Availability setup

```

lsctl ha command [command options] [arguments...]

```

#### Commands​

CommandDescription

`lsctl ha info`Display instance High Availability details

`lsctl ha conf`Configure License servers HA pair

#### Options​

OptionDescription

`--help`, `-h`show help

In this topic:
