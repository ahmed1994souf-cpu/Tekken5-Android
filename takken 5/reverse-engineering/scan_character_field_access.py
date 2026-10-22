#!/usr/bin/env python3
"""Scan ARM64 IL2CPP code for direct Character field accesses.

This is evidence collection only: a field access is not automatically a semantic
meaning. The report groups reads/writes of health/injury/dead and move lists and
labels the nearest ScriptMethod RVA when available.
"""
import json, sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from capstone.arm64 import ARM64_OP_MEM, ARM64_OP_REG

binary = Path(sys.argv[1] if len(sys.argv) > 1 else "libil2cpp.so")
script_json = Path(sys.argv[2] if len(sys.argv) > 2 else "output/script.json")
out = Path(sys.argv[3] if len(sys.argv) > 3 else "native-disassembly/character-field-access.txt")
fields = {
    0xA0: "health",
    0xA8: "injury",
    0xAC: "injuryTime",
    0xB0: "dead",
    0xF0: "moveFront",
    0xF8: "moveBack",
    0x100: "moveGround",
    0x108: "moveAttack",
    0x110: "moveCrush",
}

def number(v):
    if isinstance(v, int): return v
    if isinstance(v, str):
        try: return int(v.strip(), 0)
        except ValueError:
            try: return int(v.strip(), 16)
            except ValueError: return None
    return None

methods=[]
if script_json.exists():
    try:
        data=json.loads(script_json.read_text(errors="ignore"))
        for m in data.get("ScriptMethod", []):
            a=number(m.get("Address")); n=m.get("Name")
            if a is not None and isinstance(n,str): methods.append((a,n))
    except Exception as e:
        print("script.json parse warning:", e)
methods.sort()

def method_at(addr):
    lo,hi=0,len(methods)
    while lo<hi:
        mid=(lo+hi)//2
        if methods[mid][0] <= addr: lo=mid+1
        else: hi=mid
    return methods[lo-1][1] if lo else "unknown"

md=Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.detail=True
hits=[]
with binary.open("rb") as f:
    elf=ELFFile(f)
    for seg in elf.iter_segments():
        if seg["p_type"] != "PT_LOAD" or not (int(seg["p_flags"]) & 1):
            continue
        base=int(seg["p_vaddr"])
        for ins in md.disasm(seg.data(), base):
            for op in ins.operands:
                if op.type != ARM64_OP_MEM:
                    continue
                disp=int(op.mem.disp)
                if disp not in fields:
                    continue
                access="read/write candidate"
                mnem=ins.mnemonic.lower()
                if mnem.startswith("st") or mnem in {"stp","stnp","sturb","sturh","stur"}:
                    access="WRITE candidate"
                elif mnem.startswith("ld") or mnem in {"ldp","ldnp","ldurb","ldurh","ldur"}:
                    access="READ candidate"
                base_reg=ins.reg_name(op.mem.base) if op.mem.base else "none"
                # Stack/frame accesses with matching numeric offsets are common false positives.
                # Keep them visible for audit, but never elevate them to object-field candidates.
                base_kind = "STACK/FRAME (exclude from object candidates)" if base_reg in {"sp", "x29", "fp"} else "NON-STACK base (object identity still unproven)"
                hits.append((ins.address, fields[disp], disp, access, mnem, ins.op_str, base_reg, base_kind, method_at(ins.address)))

lines=[
"Character field-access scan (direct ARM64 memory operands)",
f"Binary: {binary} ({binary.stat().st_size} bytes)",
f"Methods indexed from script.json: {len(methods)}",
f"Total matching instructions: {len(hits)}",
"IMPORTANT: these are direct offset matches only; a match does not prove that the base register is a Character object.",
"",
"RVA | field | offset | access | instruction | base | base classification | nearest ScriptMethod",
]
for a,field,off,access,mnem,opstr,base,base_kind,method in hits:
    lines.append(f"0x{a:x} | {field} | 0x{off:x} | {access} | {mnem} {opstr} | {base} | {base_kind} | {method}")

lines += ["", "High-value NON-STACK WRITE candidates (health/injury/dead; object identity still unproven):"]
for row in hits:
    if row[1] in {"health","injury","dead"} and row[3].startswith("WRITE") and row[6] not in {"sp", "x29", "fp"}:
        lines.append(f"0x{row[0]:x} | {row[1]} | {row[3]} | {row[5]} | base={row[6]} | {row[8]}")

# Narrow follow-up: only instructions attributed to methods whose metadata name
# belongs to the game's Character class. This avoids treating unrelated Unity
# classes that happen to use the same numeric offsets as character logic.
lines += ["", "Character-method-only WRITE candidates (still static candidates, not semantic proof):"]
character_rows = [
    row for row in hits
    if row[8].startswith("Character$")
    and row[1] in {"health", "injury", "injuryTime", "dead", "moveFront", "moveBack", "moveGround", "moveAttack", "moveCrush"}
    and row[3] == "WRITE candidate"
    and row[6] not in {"sp", "x29", "fp"}
]
for row in character_rows:
    lines.append(f"0x{row[0]:x} | {row[1]} | {row[3]} | {row[5]} | base={row[6]} | method={row[8]}")
lines.append(f"Character-method-only non-stack writes: {len(character_rows)}")

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"Wrote {len(hits)} matching instructions to {out}")
