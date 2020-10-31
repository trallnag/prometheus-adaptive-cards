# Development

## Configuration

For configuration of PromAC from the enduser's perspective please refer to
[CONFIGURATION.md](./CONFIGURATION.md). Looking at the architecture of PromAC,
the setup of the configuration is done in several steps that can be summarized
as follows:

1. Parse and merge YAML configuration files into settings box.
2. Read subset of configs from env vars and merge them into settings box. Before
    merging non-string types are cast to target types.
3. Read subset of configs from args and merge them into settings box.
4. Hand over settings box to Pydantic for validation and creating settings.

### How to add config knob?

### How to add `env_var` support for knob?

1. Follow ["How to add config knob?"](#how-to-add-config-knob).
2. Make sure the flag `env_var` is set in the config schema documentation [here](./CONFIGURATION.md).
3. If the type of the knob is not `str`, add a cast to `_cast_env_vars`. This
    will cast to the correct type if the knob exists in the environment
    variables. If this cast fails an exception will be thrown. If the type is
    string, skip this step. Important: Only basic casting, no validation! Stuff
    like "must be URL" is done at the central validation step with Pydantic.
