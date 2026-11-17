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

## Path contract

Python 3.12 or newer is required. Source/build inputs must be nonempty workspace-relative paths without traversal, control characters, or existing symlink escapes, and the directories must not overlap. Both are validated before build-directory creation or output publication. The existing default paths and absolute-path output names are preserved. This action sets up directories only; it does not authorize target source execution or make build scripts and compiler configuration trusted.

## License

[Apache 2.0](LICENSE)
