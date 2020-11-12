# Configuration <!-- omit in toc --> 

To configure PromAC, you can choose from the three approaches configuration
file, environment variables and arguments passed to the executable and / or
interpreter. The configuration file must be used if you want to use something
else than the already included generic route. Both env vars and args only
support a subset of all available knobs you can set.

## Table of Content <!-- omit in toc --> 

- [Configuration via YAML](#configuration-via-yaml)
  - [Section: `logging`](#section-logging)
  - [Section: `server`](#section-server)
  - [Section: `routing`](#section-routing)
  - [Type: `<route>`](#type-route)
  - [Type: `<remove>`](#type-remove)
  - [Type: `<add>`](#type-add)
  - [Type: `<override>`](#type-override)
- [Configuration via Env Vars](#configuration-via-env-vars)
- [Configuration via CLI Args](#configuration-via-cli-args)

## Configuration via YAML

The main way to configure PromAC is YAML. And it is required for custom routes.
By default, PromAC will look for `/etc/promac/promac.yml`. You can override the
config location with the environment variable `CONFIG_FILE` or CLI argument
`--config_file`. PromAC also checks for `*.local.*` files. If found, the local
config will be merged into the main config. Illegal settings will abort the
program instead of falling back to the defaults. 

Generic placeholders are defined as follows:

* `=`: Assigned default. Field is optional. If all leaves of a branch are optional
    the branch is optional as well. This is recursive.
* `<<foo, bar>>`: Set of literals of the type `string` to choose from.
* `<boolean>`: Boolean that can take the values `true` or `false`.
* `<string>`: Regular string.





* `[]`: Field is optional and may come with a default. If all leaves leaves are
    optional the branch is optional as well.





* `{}`: 

* `<<foo, bar>>`: a set of literals to choose from.
* `<boolean>`: a boolean that can take the values `true` or `false`.
* `<filename>`: a valid path in the current working directory.
* `<int>`: an integer value.
* `<labelname>`: a string matching the regular expression `[a-zA-Z_][a-zA-Z0-9_]*`.
* `<labelvalue>`: a string of unicode characters.
* `<url>`: a valid URL path
* `<string>`: a regular string
* `<tmpl_string>`: a string which is template-expanded before usage

* `...` means as many as you want or none at all. Basically a collection.
* `env_var` means that you can set this via the environment. Inherited.
* `cli_arg` means that you can set this as a CLI argument. Inherited.



The schema is split into multiple sections, but they all go into the same file.
The codified version of the configuration schema can be found [here](./prometheus_adaptive_cards/config/settings.py).

### Section: `logging`

Settings related to logging. All fields have the `env_var` and `cli_arg` flag.

```yml
logging:
  level: <<DEBUG, INFO, WARNING, ERROR, CRITICAL>> = INFO
  format: <<structured, unstructured>> = structured
  structured:
    custom_serializer: <boolean> = true
    unstructured:
      fmt: <string> = check source
      colorize: <boolean> = true
```

### Section: `server`

Settings related PromAC's web server. All fields have the `env_var` and `cli_arg` flag.

```yml
server:
  host: <string> = '127.0.0.1'
  port: <int> = 8000
  root_path: <string> = ''
```

### Section: `routing`

Declarative description of PromAC's routing and behaviour.

```yml
routing:
  remove: <remove> = null
  add: <add> = null
  override: <override> = null
  routes:
    - <route> ...
```

### Type: `<route>`

An arbitrary number of routes can be added. Every route starts with an endpoint
in the PromAC API, goes through a number of transformation steps, get parsed
through a templating function and finally gets send out to a list of receivers.

A route with the name `generic` will always exist.

```txt
# The name under which the route should be available. Will be concatenated with
# the (optional) root path and "generic": `/${root_path}/route/${name}`. Unique.
name: <string>

# Should all subpaths be interpreted as webhook URLs? This means that in the
# following string `/${root_path}/route/${name}/${base64_encoded_webhook}` the
# path beyond `${name}/` will be extracted, decoded and injected into the list
# of webhooks for this route.
[ catch: <boolean> | default = true]

# Values of annotations where the name matches are added to webhooks.
extract_webhooks:
    [ - <string> | default = [] | ... ]
extract_webhooks_re:
    [ - <regex> | default = [] | ... ]

[ split_by: ]
    target: <<annotation, label>>
    value: <string>

# If set, the payload will be split and grouped according to the given label or
# annotation name. All following steps are done for every group individually.
# Only one of the following two fields may be not null.
[ split_by_annotation: <string> | default = ~ ]
[ split_by_label: <string> | default = ~ ]

remove: <remove> = null
add: <add> = null
override: <override> = null

webhooks:
  [ - <url> | defaults = [] | ... ]
```

Example(s):

```yml
name: super-critical
remove:
  re_labels:
    - (^__.*)
  re_annotations:
    - (^__.*)
webhooks:
  - https://webex.com/what/ever/1234
```

### Type: `<remove>`

Removes labels and annotations. You can choose between fixed strings and regex.
The regex patterns are always unanchored. So if you want to anchor them use `^$`.
Only regards the names, not values of labels and annotations.

```txt
annotations:
  [ - <string> | default = [] | ... ]
labels:
  [ - <string> | default = [] | ... ]
re_annotations:
  [ - <regex> | default = [] | ... ]
re_labels:
  [ - <regex> | default = [] | ... ]
```

Example(s):

```yml
annotations:
  - very_long_annotation
  - justANumber
labels:
  - password
re_annotations:
  - (^__.*)
```

### Type: `<add>`

Add additional labels and annotations. Existing fields are not overwritten.

```txt
annotations:
  [ - <namevalue> | defaults to empty list | ... ]
labels:
  [ - <namevalue> | defaults to empty list | ... ]
```

### Type: `<override>`

Add additional labels and annotations. Existing fields are overwritten.

```txt
annotations:
  [ - <namevalue> | defaults to empty list | ... ]
labels:
  [ - <namevalue> | defaults to empty list | ... ]
```

## Configuration via Env Vars

All variables are uppercase and must start with the prefix `PROMAC__`. Nested
fields are declared by using a double underscore as separator. Only config
knobs that have the `env_var` flag can be set via the environment. Casting is
done accordingly disregarding quoting and whatnot. Check out the 
[chapter "Configuration via YAML"](#configuration-via-yaml).

For example, the equivalent of the following

```yml
foo:
  bar:
    zoom: hallo welt
```

would be `PROMAC__FOO__BAR__ZOOM="hallo welt"`.

## Configuration via CLI Args

All arguments are lowercase. Nesting is declared by using a period. Only config
knobs that have the `cli_arg` flag can be set as a CLI argument. Casting is
done accordingly disregarding quoting and whatnot. Check out the 
[chapter "Configuration via YAML"](#configuration-via-yaml).

For example, the equivalent of the following

```yml
foo:
  bar:
    zoom: hallo welt
```

would be `--foo.bar.zoom "hallo welt"`.
