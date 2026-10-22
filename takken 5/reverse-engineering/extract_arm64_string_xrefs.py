#!/usr/bin/env python3
"""Experimental ARM64 ADRP+ADD string-reference scanner for Wrestling Empire IL2CPP."""
import json, re, sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from capstone.arm64 import ARM64_OP_REG, ARM64_OP_IMM

binary = Path(sys.argv[1] if len(sys.argv) > 1 else "libil2cpp.so")
strings_json = Path(sys.argv[2] if len(sys.argv) > 2 else "output/stringliteral.json")
dump_cs = Path(sys.argv[3] if len(sys.argv) > 3 else "output/dump.cs")
out = Path(sys.argv[4] if len(sys.argv) > 4 else "native-disassembly/string-xrefs.txt")
if not binary.exists() or not strings_json.exists():
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("XREF scan skipped: binary or stringliteral.json missing.\n")
    sys.exit(0)

def number(v):
    if isinstance(v, int): return v
    if isinstance(v, str):
        s=v.strip()
        try: return int(s, 0)
        except ValueError:
            try: return int(s, 16)
            except ValueError: return None
    return None

data=json.loads(strings_json.read_text(errors="ignore"))
targets={}
rx=re.compile(r"attack|grapple|impact|injur|pinfall|pinning|submission|winner|damage|ground|throw|stun|knock|referee|count|match over|victory", re.I)
for item in data:
    value=item.get("value", "")
    addr=number(item.get("address"))
    if addr is not None and isinstance(value,str) and rx.search(value):
        targets.setdefault(addr,[]).append(value.replace("\n"," ").replace("\r"," ")[:180])

methods=[]
if dump_cs.exists():
    s=dump_cs.read_text(errors="ignore")
    for m in re.finditer(r"// RVA:\s*(0x[0-9a-fA-F]+).*?\n(?:.*\n){0,3}?\s*(?:public|private|protected|internal).*?\s([A-Za-z_][A-Za-z0-9_]*)\s*\(", s):
        try: methods.append((int(m.group(1),16),m.group(2)))
        except Exception: pass
methods.sort()
def method_at(addr):
    lo,hi=0,len(methods)
    while lo<hi:
        mid=(lo+hi)//2
        if methods[mid][0] <= addr: lo=mid+1
        else: hi=mid
    if lo: return methods[lo-1][1] + " (nearest preceding RVA)"
    return "unknown"

md=Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail=True
hits=[]
with binary.open("rb") as f:
    elf=ELFFile(f)
    if elf.header["e_machine"] != "EM_AARCH64":
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text("XREF scan skipped: ELF is not AArch64.\n")
        sys.exit(0)
    for seg in elf.iter_segments():
        if seg["p_type"] != "PT_LOAD" or not (int(seg["p_flags"]) & 1):
            continue
        base=int(seg["p_vaddr"]); blob=seg.data()
        ins=list(md.disasm(blob,base))
        for i,ad in enumerate(ins):
            if ad.mnemonic != "adrp" or len(ad.operands)<2 or ad.operands[1].type != ARM64_OP_IMM:
                continue
            reg=ad.operands[0].reg
            page=int(ad.operands[1].imm)
            # Search a few subsequent instructions for ADD immediate based on the ADRP destination.
            for nxt in ins[i+1:i+5]:
                ops=nxt.operands
                if nxt.mnemonic in ("add","sub") and len(ops)>=3 and ops[0].type==ARM64_OP_REG and ops[1].type==ARM64_OP_REG and ops[1].reg==reg and ops[2].type==ARM64_OP_IMM:
                    dest=page + (int(ops[2].imm) if nxt.mnemonic=="add" else -int(ops[2].imm))
                    if dest in targets:
                        hits.append((dest,nxt.address,ad.address,method_at(ad.address),"; ".join(targets[dest])))
                    # Do not keep searching through unrelated register transformations.
                    break

out.parent.mkdir(parents=True,exist_ok=True)
lines=[
"Experimental ARM64 string-reference scan",
f"Binary: {binary} ({binary.stat().st_size} bytes)",
f"Combat-like string addresses checked: {len(targets)}",
f"ADRP+ADD/SUB candidate references: {len(hits)}",
"Important: candidates require manual verification; nearest RVA method labels may be approximate.",
"String address | ADRP RVA/VA | ADD/SUB RVA/VA | nearest method label | string"
]
for addr,addva,adrpva,method,val in sorted(hits,key=lambda x:x[1]):
    lines.append(f"0x{addr:x} | 0x{adrpva:x} | 0x{addva:x} | {method} | {val}")
if not hits:
    lines.append("No exact ADRP+ADD/SUB references matched. This can mean string addresses use a different address basis or the compiler uses another addressing sequence; it does not prove the strings are unused.")
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines[:12]))
