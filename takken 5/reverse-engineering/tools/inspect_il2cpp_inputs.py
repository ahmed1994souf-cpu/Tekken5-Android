#!/usr/bin/env python3
"""Inspect IL2CPP input files without modifying them or claiming method addresses.

Usage:
  python inspect_il2cpp_inputs.py /path/to/global-metadata.dat /path/to/libil2cpp.so --out ./il2cpp-report

This standard-library helper reports basic file/ELF facts and candidate strings only.
It does NOT parse MethodDefinition tables or resolve native method pointers.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import struct
from pathlib import Path

INTEREST = re.compile(
    r"character|wrestl|opponent|attack|grapple|ground|pin|stamina|strength|"
    r"agility|skill|target|distance|angle|health|match|ring|rope|camera|"
    r"dialogue|promo|scene_map|ai",
    re.IGNORECASE,
)

def elf_summary(path: Path) -> dict:
    with path.open("rb") as f:
        head = f.read(64)
        if len(head) < 16 or head[:4] != b"\x7fELF":
            return {"is_elf": False, "note": "Not an ELF file or truncated header"}
        elf_class = head[4]
        endian_tag = head[5]
        if elf_class not in (1, 2) or endian_tag not in (1, 2):
            return {"is_elf": True, "note": "Unsupported ELF class/endianness"}
        endian = "<" if endian_tag == 1 else ">"
        if elf_class == 2 and len(head) >= 64:
            e_type, e_machine = struct.unpack_from(endian + "HH", head, 16)
            e_entry = struct.unpack_from(endian + "Q", head, 24)[0]
            e_phoff = struct.unpack_from(endian + "Q", head, 32)[0]
            e_phentsize, e_phnum = struct.unpack_from(endian + "HH", head, 54)
        elif elf_class == 1 and len(head) >= 52:
            e_type, e_machine = struct.unpack_from(endian + "HH", head, 16)
            e_entry = struct.unpack_from(endian + "I", head, 24)[0]
            e_phoff = struct.unpack_from(endian + "I", head, 28)[0]
            e_phentsize, e_phnum = struct.unpack_from(endian + "HH", head, 42)
        else:
            return {"is_elf": True, "note": "Truncated ELF header"}
        return {
            "is_elf": True,
            "class_bits": 64 if elf_class == 2 else 32,
            "endianness": "little" if endian_tag == 1 else "big",
            "elf_type": e_type,
            "machine_id": e_machine,
            "entry_virtual_address": hex(e_entry),
            "program_header_offset": e_phoff,
            "program_header_entry_size": e_phentsize,
            "program_header_count": e_phnum,
        }

def extract_ascii_strings(path: Path, min_len: int = 4):
    data = path.read_bytes()
    pattern = re.compile(rb"[\x20-\x7e]{" + str(min_len).encode() + rb",}")
    for match in pattern.finditer(data):
        try:
            value = match.group().decode("ascii")
        except UnicodeDecodeError:
            continue
        if INTEREST.search(value):
            yield {"file_offset": hex(match.start()), "value": value}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("metadata", type=Path, help="global-metadata.dat")
    ap.add_argument("library", type=Path, help="libil2cpp.so")
    ap.add_argument("--out", type=Path, default=Path("il2cpp-report"))
    args = ap.parse_args()

    for p in (args.metadata, args.library):
        if not p.is_file():
            raise SystemExit(f"Input file not found: {p}")

    args.out.mkdir(parents=True, exist_ok=True)
    summary = {
        "metadata": {"name": args.metadata.name, "size_bytes": args.metadata.stat().st_size},
        "native_library": {
            "name": args.library.name,
            "size_bytes": args.library.stat().st_size,
            "elf": elf_summary(args.library),
        },
        "limitations": [
            "ASCII string offsets are file offsets, not method addresses.",
            "This helper does not decode IL2CPP metadata tables.",
            "No original game code is copied into the report.",
        ],
    }
    (args.out / "input_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    rows = list(extract_ascii_strings(args.metadata))
    with (args.out / "metadata_string_candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_offset", "value"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Report written to: {args.out.resolve()}")
    print(f"Candidate metadata strings: {len(rows)}")
    print("Reminder: string offsets do not identify native methods.")

if __name__ == "__main__":
    main()
