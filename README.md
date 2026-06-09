# `action-setup-build-env`

> Sets up source and build directories for the Phlex build environment.

## Usage

```yaml
- uses: Framework-R-D/action-setup-build-env@780fd75b00a291df6a42d9d2337651330ebdb907 # v1
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
