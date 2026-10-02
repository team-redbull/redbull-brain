# storkctl global flags

Source: https://docs.portworx.com/portworx-enterprise/reference/cli/storkctl-reference/global-flags (Portworx Enterprise latest)

storkctl global flags | Portworx Enterprise Documentation

Global flags in `storkctl` provide configurable options that apply to all commands. These flags allow users to customize logging, output format, Kubernetes API request limits, and more.

For example, you can:

- Control logging behavior using `--logtostderr`, `--log_dir`, and `--v`.

- Specify the Kubernetes context with `--kubeconfig` and `--context`.

- Set API request limits using `--qps` and `--burst`.

- Define the CLI output format with `--output`.

The following table lists all available global flags, including their input types, descriptions, and default values.

FlagInput typeDescriptionDefaultRequired

`--alsologtostderr``bool`log to standard error as well as files`false`Optional

`--burst``int`restrict number of k8s API requests from stork`2000`Optional

`--context``string`name of the kubeconfig context to use-Optional

`--kubeconfig``string`path to the kubeconfig file to use for CLI requests-Optional

`--log_backtrace_at``string`when logging hits line file:N, emit a stack trace-Optional

`--log_dir``string`If non-empty, write log files in this directory-Optional

`--log_link``string`If non-empty, add symbolic links in this directory to the log files-Optional

`--logbuflevel``int`Buffer log messages logged at this level or lower (-1 means don't buffer; 0 means buffer INFO only; ...). Has limited applicability on non-prod platforms.`0`Optional

`--logtostderr``bool`log to standard error instead of files`false`Optional

`--namespace`, `-n``string`If present, the namespace scope for this CLI request`default`Optional

`--output`, `-o``string`output format. One of: table|json|yaml`table`Optional

`--qps``int`restrict number of k8s API requests from stork`1000`Optional

`--stderrthreshold``int`logs at or above this threshold go to stderr`2`Optional

`--v`, `-v``int`log level for V logs`0`Optional

`--vmodule``stringToString`comma-separated list of pattern=N settings for file-filtered logging-Optional

`--watch`, `-w``bool`watch stork resources`false`Optional
