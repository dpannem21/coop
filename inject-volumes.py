#!/usr/bin/env python3
import os
import sys
import yaml

USAGE = "Usage: python3 inject-volumes.py <compose-file> --inject|--eject"
if len(sys.argv) != 3:
    print(USAGE)
    sys.exit(1)

COMPOSE_FILE = sys.argv[1]
ACTION = sys.argv[2].lower()
VOLUMES_FILE = "custom-volumes.txt"


def load_custom_volumes():
    if not os.path.exists(VOLUMES_FILE):
        return []
    with open(VOLUMES_FILE) as f:
        lines = [l.strip() for l in f.readlines()]
        return [l for l in lines if l and not l.startswith("#")]


def make_mapping(vol_path):
    vol_path = os.path.expanduser(vol_path)
    # if user provided host:container mapping, leave as-is
    if ":" in vol_path:
        return vol_path
    base = os.path.basename(vol_path.rstrip("/"))
    container = os.path.join("/root", base or "root")
    return f"{vol_path}:{container}"


def read_compose(path):
    with open(path) as f:
        return yaml.safe_load(f)


def write_compose(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def is_claude_mount(mapping):
    # keep mappings that reference the CLAUDE variable or the .claude path
    s = mapping or ""
    return ("${CLAUDE}" in s) or ("$CLAUDE" in s) or (".claude" in s.lower())


def do_inject(compose):
    svc = compose.get("services", {}).get("coop")
    if not svc:
        print("No coop service found in compose file.")
        sys.exit(1)

    existing = svc.setdefault("volumes", [])
    custom = load_custom_volumes()
    if not custom:
        print("No custom volumes to inject.")
        return compose

    desired = [make_mapping(v) for v in custom]

    # ensure any existing claude mounts are preserved in desired
    for v in existing:
        if is_claude_mount(v) and v not in desired:
            desired.append(v)

    added = []
    for v in desired:
        if v not in existing:
            existing.append(v)
            added.append(v)

    for v in added:
        print(f"✓ Injected volume: {v}")

    return compose


def do_eject(compose):
    svc = compose.get("services", {}).get("coop")
    if not svc:
        print("No coop service found in compose file.")
        sys.exit(1)

    existing = svc.get("volumes", [])
    if not existing:
        print("No volumes present; nothing to eject.")
        return compose

    kept = [v for v in existing if is_claude_mount(v)]
    removed = [v for v in existing if v not in kept]

    for v in removed:
        print(f"✗ Removed volume: {v}")

    svc["volumes"] = kept
    return compose


def main():
    compose = read_compose(COMPOSE_FILE)

    if ACTION == "--inject":
        compose = do_inject(compose)
        write_compose(COMPOSE_FILE, compose)
    elif ACTION == "--eject":
        compose = do_eject(compose)
        write_compose(COMPOSE_FILE, compose)
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()