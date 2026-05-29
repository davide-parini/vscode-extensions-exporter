# VS Code Extensions Exporter

A Python script that exports a list of all locally installed VS Code extensions as tab-separated values.

## Output columns

| Column | Description |
|---|---|
| **Name** | Human-readable display name (e.g. `Python`) |
| **Identifier** | Unique marketplace ID in `publisher.name` format (e.g. `ms-python.python`) |
| **Version** | Currently installed version |
| **Last Updated** | When VS Code last installed or updated the extension |
| **Publisher** | Human-readable publisher name (e.g. `Microsoft`) |

## Data sources

- `~/.vscode/extensions/extensions.json` — primary source for identifier, version, timestamp, and publisher name
- `~/.vscode/extensions/<extension-folder>/package.json` — looked up per extension for the `displayName` field

The **Last Updated** timestamp is read from VS Code's own `installedTimestamp` metadata, which is recorded at install/update time and is more reliable than folder modification times.

## Usage

```bash
python export-extensions.py
```

Pipe to a file:

```bash
python export-extensions.py > extensions.tsv
```

Copy directly to clipboard (macOS):

```bash
python export-extensions.py | pbcopy
```

The output is tab-separated and pastes cleanly into Excel or Numbers.

> **Note:** Do not copy output by selecting text in the terminal — terminals visually expand tab characters into spaces, so what you copy will be space-separated instead of tab-separated. Always use `| pbcopy` or redirect to a file to preserve real tab characters.

## Requirements

- Python 3.6+
- VS Code installed with at least one extension (requires `~/.vscode/extensions/extensions.json` to exist)
