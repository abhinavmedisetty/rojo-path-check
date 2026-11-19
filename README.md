# Rojo Path Check

A small, dependency-free Python 3 tool that catches missing files and folders
in a Rojo project's JSON configuration before you sync to Roblox Studio.

Run this from the folder containing your `default.project.json`:

```sh
python /path/to/rojo_check.py
```

Or supply the project file explicitly:

```sh
python rojo_check.py ../my-project/default.project.json
```

On Windows, use `py` if `python` is unavailable. Relative Rojo mappings are
resolved from the project file's folder. Missing optional mappings are allowed.
The checker reads one standard JSON file and checks its immediate configuration
tree. It does not parse JSONC, load other project files, or validate Roblox
properties. It never modifies your files.

Exit codes are 0 for success, 1 for mapping or instance errors, and 2 if the
project cannot be read or lacks a valid root tree.

For the mapping format, see the [Rojo project docs](https://rojo.space/docs/v7/project-format/).

## License

MIT.
