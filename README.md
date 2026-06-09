# `action-setup-build-env`

> Sets up source and build directories for the Phlex build environment.

## Usage

```yaml
- uses: Framework-R-D/action-setup-build-env@v1  # pin to commit SHA in production
  with:
    input-name: value
```

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `source-path` | Path where source code is checked out | false | `phlex-src` |
| `build-path` | Path for build directory | false | `phlex-build` |

## Outputs

| Name | Description |
|------|-------------|
| `source-dir` | Absolute path to source directory |
| `build-dir` | Absolute path to build directory |

## License

[Apache 2.0](LICENSE)
