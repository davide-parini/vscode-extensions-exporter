import json
from datetime import datetime
from pathlib import Path

# VS Code records all extension metadata here (milliseconds since epoch for timestamps)
ext_dir = Path.home() / '.vscode' / 'extensions'
extensions_json = ext_dir / 'extensions.json'

headers = ["Name", "Identifier", "Version", "Last Updated", "Publisher"]
print("\t".join(headers))

with open(extensions_json, 'r', encoding='utf-8') as f:
    entries = json.load(f)

for entry in sorted(entries, key=lambda e: e.get("identifier", {}).get("id", "")):
    identifier = entry.get("identifier", {}).get("id", "")
    version = entry.get("version", "")
    metadata = entry.get("metadata", {})
    ts_ms = metadata.get("installedTimestamp")
    publisher = metadata.get("publisherDisplayName", "")

    # Skip entries without a valid identifier or recorded timestamp
    if not identifier or not ts_ms:
        continue

    # Look up the human-readable display name from package.json via relativeLocation
    display_name = identifier.split(".", 1)[1] if "." in identifier else identifier
    relative_location = entry.get("relativeLocation", "")
    if relative_location:
        folder = ext_dir / relative_location
        pkg_json = folder / 'package.json'
        try:
            with open(pkg_json, 'r', encoding='utf-8') as f:
                display_name = json.load(f).get("displayName", display_name)
            # Resolve NLS placeholder, e.g. "%displayName%" or "%ext.displayName%"
            if isinstance(display_name, str) and display_name.startswith('%') and display_name.endswith('%'):
                key = display_name[1:-1]
                nls_json = folder / 'package.nls.json'
                with open(nls_json, 'r', encoding='utf-8') as f:
                    display_name = json.load(f).get(key, display_name)
        except Exception:
            pass

    last_updated = datetime.fromtimestamp(ts_ms / 1000).strftime('%-m/%-d/%Y')

    print("\t".join([display_name, identifier, version, last_updated, publisher]))