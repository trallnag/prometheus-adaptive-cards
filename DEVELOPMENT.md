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

What is not mentioned in [CONFIGURATION.md](./CONFIGURATION.md) is that PromAC
also checks `prometheus_adaptive_cards/config` for a config file. This location
can be used for "default" development settings. Simply uncomment 

### How to add config knob?

1. Add the config knob to an appropriate location in [CONFIGURATION.md](./CONFIGURATION.md).
2. Update the Pydantic models accordingly.
3. If possible, add `env_var` and `cli_arg` flags. Go to this [chapter](#how-to-add-env_var-and-cli_arg-support-for-knob).
4. Consider adding tests.

### How to change a config knob?

1. Update schema documentation in [CONFIGURATION.md](./CONFIGURATION.md).
2. Update Pydantic models accordingly.
3. Update tests.
4. Follow ["How to add config knob?"](#how-to-add-config-knob).

### How to add `env_var` and `cli_arg` support for knob?

1. Follow ["How to add config knob?"](#how-to-add-config-knob).
2. Make sure the flags `env_var` and `cli_arg` are set in the config schema
    documentation [here](./CONFIGURATION.md).
3. If the type of the knob is not `str`, add a cast to `_cast_vars`. This
    will cast to the correct type if the knob exists. If this cast fails an
    exception will be thrown. If the type is string, skip this step. Important:
    Only basic casting, no validation! Stuff like "must be URL" is done at
    the central validation step with Pydantic.
