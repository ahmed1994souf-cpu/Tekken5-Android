#!/usr/bin/env python3
"""Read-only first-pass diagnostics for Unity IL2CPP global-metadata.dat.

This intentionally does not modify the input file or claim native method addresses.
It reports the magic/version/header words and printable string evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

MAGIC = 0xFAB11BAF
TERMS = (
    b"grapple", b"suplex", b"tope", b"flying", b"pin", b"referee",
    b"stamina", b"injury", b"career", b"roster", b"arena", b"ring",
    b"count-out", b"count out", b"finisher", b"submission", b"weapon",
)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("metadata", type=Path)
    ap.add_argument("--out", type=Path, default=Path("metadata-first-pass"))
    args = ap.parse_args()
    data = args.metadata.read_bytes()
    args.out.mkdir(parents=True, exist_ok=True)
    magic = struct.unpack_from("<I", data, 0)[0] if len(data) >= 4 else None
    version = struct.unpack_from("<I", data, 4)[0] if len(data) >= 8 else None
    words = [struct.unpack_from("<I", data, off)[0]
             for off in range(0, min(len(data), 256) - 3, 4)]
    strings = []
    for match in re.finditer(rb"[\x20-\x7e]{5,}", data):
        raw = match.group(0)
        low = raw.lower()
        if any(term in low for term in TERMS):
            strings.append({"offset_hex": hex(match.start()),
                            "text": raw[:240].decode("ascii", "replace")})
    summary = {
        "input": str(args.metadata),
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "magic_hex": hex(magic) if magic is not None else None,
        "magic_matches_il2cpp": magic == MAGIC,
        "metadata_version_word": version,
        "first_256_bytes_as_u32_le": [
            {"offset_hex": hex(i * 4), "value_hex": hex(v), "value": v}
            for i, v in enumerate(words)
        ],
        "matched_printable_strings_count": len(strings),
        "matched_printable_strings": strings[:500],
        "limitations": [
            "This is a diagnostic scan, not a complete v39 metadata parser.",
            "Offsets reported for printable strings are file offsets, not method addresses.",
            "Method/type extraction and native address mapping require a compatible parser and matching libil2cpp.so."
        ]
    }
    (args.out / "metadata_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.out / "metadata_strings.tsv").open("w", encoding="utf-8") as f:
        f.write("file_offset_hex\ttext\n")
        for item in strings:
            f.write(f'{item["offset_hex"]}\t{item["text"].replace(chr(9), " ")}\n')
    print(json.dumps({k: summary[k] for k in (
        "input", "size_bytes", "sha256", "magic_hex",
        "magic_matches_il2cpp", "metadata_version_word",
        "matched_printable_strings_count")}, ensure_ascii=False, indent=2))
    return 0 if magic == MAGIC else 2

if __name__ == "__main__":
    raise SystemExit(main())
