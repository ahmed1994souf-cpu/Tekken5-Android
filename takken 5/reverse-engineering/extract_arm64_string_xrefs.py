#!/usr/bin/env python3
"""Experimental ARM64 string-reference scanner with VA/RVA diagnostics for Wrestling Empire IL2CPP."""
import json, re, sys
from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
from capstone.arm64 import ARM64_OP_REG, ARM64_OP_IMM

binary = Path(sys.argv[1] if len(sys.argv) > 1 else "libil2cpp.so")
strings_json = Path(sys.argv[2] if len(sys.argv) > 2 else "output/stringliteral.json")
script_json = Path(sys.argv[3] if len(sys.argv) > 3 else "output/script.json")
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
rx=re.compile(r"attack|grapple|impact|injur|pinfall|pinning|submission|winner|damage|ground|throw|stun|knock|referee|victory|wrestl|finisher|ring ropes|ring the bell|fall only|counter attack|blocking|block an attack|move by holding", re.I)
# Exclude common runtime/library diagnostics that match generic combat words accidentally.
noise=re.compile(r"^count$|count must be positive and count must refer to a location|offset and length were out of bounds for the array|^count cannot be|^count must be|^argument count must|^bounds count cannot|^cachecount:|^command count\s*:|^array or count|^collection.*count|^index.*count|^dataset\.|^datatable\.|^a task.s exception|^an exception was thrown|^exception has been thrown|^end of stream encountered|^additional text encountered after finished reading json|^buffer too small|^invalid string length|^adding the specified count to the semaphore", re.I)
for item in data:
    value=item.get("value", "")
    addr=number(item.get("address"))
    if addr is not None and isinstance(value,str) and rx.search(value):
        targets.setdefault(addr,[]).append(value.replace("\n"," ").replace("\r"," ")[:180])

methods=[]
if script_json.exists():
    # script.json contains resolved method names and addresses, including generic
    # instantiations that are not represented by ordinary RVA comments in dump.cs.
    try:
        script_data=json.loads(script_json.read_text(errors="ignore"))
        for method in script_data.get("ScriptMethod", []):
            addr=number(method.get("Address"))
            name=method.get("Name")
            if addr is not None and isinstance(name,str) and name:
                methods.append((addr,name))
    except (ValueError, TypeError, AttributeError) as exc:
        print(f"Could not parse ScriptMethod entries: {exc}")
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
adr_hits=[]
segment_report=[]
with binary.open("rb") as f:
    elf=ELFFile(f)
    if elf.header["e_machine"] != "EM_AARCH64":
        out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text("XREF scan skipped: ELF is not AArch64.\n")
        sys.exit(0)
    for seg in elf.iter_segments():
        if seg["p_type"] != "PT_LOAD":
            continue
        base=int(seg["p_vaddr"])
        executable=bool(int(seg["p_flags"]) & 1)
        segment_report.append((base, base + int(seg["p_memsz"]), int(seg["p_offset"]), int(seg["p_filesz"]), executable))
        # String targets normally live in non-executable PT_LOAD segments too.
        # Record every load segment for VA diagnostics, but disassemble code only.
        if not executable:
            continue
        blob=seg.data()
        # Stream disassembly instead of retaining millions of instructions in RAM.
        pending={}
        for ins in md.disasm(blob,base):
            pending={reg:item for reg,item in pending.items() if item[2] >= ins.address}
            ops=ins.operands
            if ins.mnemonic == "adr" and len(ops)>=2 and ops[0].type==ARM64_OP_REG and ops[1].type==ARM64_OP_IMM:
                dest=int(ops[1].imm)
                if dest in targets:
                    adr_hits.append((dest, ins.address, method_at(ins.address), "; ".join(targets[dest])))
            if ins.mnemonic == "adrp" and len(ops)>=2 and ops[0].type==ARM64_OP_REG and ops[1].type==ARM64_OP_IMM:
                pending[ops[0].reg]=(int(ops[1].imm),ins.address,ins.address+16)
                continue
            if ins.mnemonic not in ("add","sub") or len(ops)<3:
                continue
            if ops[0].type!=ARM64_OP_REG or ops[1].type!=ARM64_OP_REG or ops[2].type!=ARM64_OP_IMM:
                continue
            reg=ops[1].reg
            if reg not in pending:
                continue
            page,adrpva,_=pending[reg]
            dest=page + (int(ops[2].imm) if ins.mnemonic=="add" else -int(ops[2].imm))
            if dest in targets:
                hits.append((dest,ins.address,adrpva,method_at(adrpva),"; ".join(targets[dest])))
            pending.pop(reg,None)

out.parent.mkdir(parents=True,exist_ok=True)
lines=[
"Experimental ARM64 string-reference scan",
f"Binary: {binary} ({binary.stat().st_size} bytes)",
f"Combat-like string addresses checked (filtered): {len(targets)}",
f"Resolved method addresses from script.json: {len(methods)}",
f"ADRP+ADD/SUB candidate references: {len(hits)}",
f"ADR direct candidate references: {len(adr_hits)}",
f"String target address range: {hex(min(targets)) if targets else 'none'} .. {hex(max(targets)) if targets else 'none'}",
f"String targets falling inside any PT_LOAD virtual range: {sum(1 for a in targets if any(lo <= a < hi for lo,hi,off,fs,ex in segment_report))}",
"All PT_LOAD ranges (VA start..end | file offset | file size | executable):",
*[f"0x{lo:x}..0x{hi:x} | off=0x{off:x} | filesz=0x{fs:x} | exec={ex}" for lo,hi,off,fs,ex in segment_report],
"Important: candidates require manual verification; nearest RVA method labels may be approximate.",
"ADR direct references: string address | instruction VA | nearest method label | string",
*[f"0x{addr:x} | 0x{va:x} | {method} | {val}" for addr,va,method,val in sorted(adr_hits,key=lambda x:x[1])],
"ADRP+ADD/SUB references: string address | ADRP VA | ADD/SUB VA | nearest method label | string"
]
for addr,addva,adrpva,method,val in sorted(hits,key=lambda x:x[1]):
    lines.append(f"0x{addr:x} | 0x{adrpva:x} | 0x{addva:x} | {method} | {val}")
if not hits and not adr_hits:
    lines.append("No exact ADR or ADRP+ADD/SUB references matched. Use the segment and target-range diagnostics above to check VA/RVA/file-offset normalization before interpreting this as evidence about usage.")
out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines[:12]))
