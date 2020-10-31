# Configuration <!-- omit in toc --> 

To configure PromAC, you can choose from the three approaches configuration
file, environment variables and arguments passed to the executable and / or
interpreter. The configuration file must be used if you want to use something
else than the already included generic route. Both env vars and args only
support a subset of all available knobs you can set.

## Table of Content <!-- omit in toc --> 

- [Configuration via YAML](#configuration-via-yaml)
  - [General fields and structure](#general-fields-and-structure)
  - [Type: `<route>`](#type-route)
  - [Type: `<remove>`](#type-remove)
  - [Type: `<add>`](#type-add)
  - [Type: `<override>`](#type-override)
  - [Type: `<name_value>`](#type-name_value)
- [Configuration via Env Vars](#configuration-via-env-vars)
- [Configuration via CLI Args](#configuration-via-cli-args)

## Configuration via YAML

The main way to configure PromAC is YAML. And it is required for custom routes.
By default, PromAC will look for `/etc/promac/promac.yml`. You can override the
config location with the environment variable `CONFIG_FILE` or CLI argument
`--config_file`. PromAC also checks for `*.local.*` files. If found, the local
config will be merged into the main config. Illegal settings will abort the
program instead of falling back to the defaults. Following rules are defined for
the following documentation schema.

* `<<foo, bar>>` marks a set of values to choose from.
* `<boolean>`, `<string>` and so on mark primitive and complex types.
* `...` means as many as you want or none at all. Basically a collection.
* `env_var` means that you can set this via the environment. Inherited.
* `cli_arg` means that you can set this as a CLI argument. Inherited.
* `[]` brackets mean that the field is optional (with a default). If all leaves
    leaves are optional the branch is optional as well.
* `{}` brackets contain info.

The schema is split into multiple sections, but they all go into the same file.

### General fields and structure

```txt
logging: { env_var | cli_arg }
  [ level: { <<DEBUG, INFO, WARNING, ERROR, CRITICAL>> | default = INFO } ]
  [ format: { <<structured, unstructured>> | default = structured } ]
  structured:
    # By default a custom serializer is used that emits a simpler structured
    # log than Loguru itself by default.
    [ custom_serializer: { <boolean> | default = true } ]
  unstructured:
    # Passed on 1:1 to Loguru as the log format. Check Loguru docs.
    [ fmt: { <string> | default = '<green>{time:HH:mm:ss}</green> <level>{level}</level> <cyan>{function}</cyan> {message} <dim>{extra}</dim>' } ]
    [ colorize: { <boolean> | default = true } ]

server:
  [ host: <string> | default = '127.0.0.1' ]
  [ port: <int> | default = 8000 ]
  # Passed on to Uvicorn. Notice that this does not lead to Uvicorn redirecting
  # the requests by removing the root_path. This has to be done by a proxy
  # of your choice.
  [ root_path: <string> | default = '' ]

routing:
  [ filter: <filter> ]
  [ add: <add> ]
  [ override: <override> ]
  routes:
    [ - <route> ]
```

### Type: `<route>`

### Type: `<remove>`

### Type: `<add>`

### Type: `<override>`

### Type: `<name_value>`

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
