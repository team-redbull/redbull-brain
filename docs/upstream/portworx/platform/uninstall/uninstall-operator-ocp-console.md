# Uninstall Portworx Operator using the OpenShift console

Source: https://docs.portworx.com/portworx-enterprise/platform/uninstall/uninstall-operator-ocp-console (Portworx Enterprise 3.6)

Uninstall Portworx Operator using the OpenShift console | Portworx Enterprise Documentation

Skip to main content

Version: 3.7

-
Log in to the OpenShift console.

-
Select the Operators dropdown -> Installed Operators.

info

You can see all the installed Portworx Operator instances. If there are many Portworx Operator instances, you can use the Search box above to filter the required Portworx Operator instance.

-
From the Project dropdown, select a namespace or project that is pointing to the namespace where the Portworx Operator is installed.

-
In the Portworx Operator instance you want to uninstall, select the vertical ellipsis button. Then, from the options, select Uninstall Operator:

-
In the Uninstall Operator? window that appears, select Uninstall:

The Portworx Operator instance is uninstalled.

note

The cluster resources, if any, you configured will still be running. You should remove these resources manually.
