from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence


PLANS = {
    "discover": [
        "Run tools/discover_devices.ps1",
        "Confirm the MaixCAM USB network adapter and IP with the user",
        "Read hostname, OS, storage, memory, temperature, camera nodes and Maix runtime over SSH",
    ],
    "deploy": [
        "Compute local application/config/model hashes",
        "Upload to a versioned staging directory with SCP",
        "Verify remote hashes before switching the active version",
    ],
    "start": ["Start the confirmed application service", "Read status.json and process state"],
    "stop": ["Request application stop", "Verify UART result publication becomes invalid"],
    "capture": ["Download raw.jpg, overlay.jpg and status.json atomically"],
    "logs": ["Read bounded recent logs without blocking the device runtime"],
    "set-config": ["Validate config locally", "Upload pending config", "Wait for apply ACK"],
    "download-failures": ["List failure samples", "Download new files", "Verify hashes and update index"],
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="V0 MaixCAM operation planner; it does not execute remote actions"
    )
    parser.add_argument("action", choices=sorted(PLANS))
    parser.add_argument("--host", help="Confirmed device hostname or IP")
    parser.add_argument("--local", type=Path, help="Local app/config/model path")
    parser.add_argument("--remote", help="Confirmed remote destination")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    record = {
        "status": "deferred",
        "execution": False,
        "action": args.action,
        "host": args.host,
        "local": None if args.local is None else str(args.local),
        "remote": args.remote,
        "steps": PLANS[args.action],
        "reason": "V0 does not execute SSH/SCP until the device and runtime are discovered",
    }
    print(json.dumps(record, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
