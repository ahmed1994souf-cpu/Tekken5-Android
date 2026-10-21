# Wrestling Empire 1.8.0 — Verified IL2CPP dump index

Date: 2026-10-21  
Repository: https://github.com/ahmed1994souf-cpu/Tekken5-Android  
Source artifact: GitHub Actions run 10, artifact `wrestling-empire-il2cpp-dump`  
Run: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39660693165

## Extraction result

The workflow completed successfully and produced these files:

| File | Size (bytes) | SHA-256 |
|---|---:|---|
| `dump.cs` | 19,237,153 | `bb488eec7a0298b72065663c1e6d1db1501f80b0e391be0d3fa3a811143f3d2d` |
| `script.json` | 54,460,738 | `0f1cc6c4b032734fd8413dd6d00a578d80d2a7828ab0ff6daaf29ba70b53d7c5` |
| `il2cpp.h` | 53,625,271 | `5790a262501f372e36098282387b71a8a944ab407c487a119e1adf7cd6b16503` |
| `stringliteral.json` | 1,867,749 | `1f9f6c2fbea7c63b99f22ef15c45c3d50c6571948c1803e09ba5580ffe132978` |

The generated dump contains 62,358 RVA-annotated methods. The dumper log and summary JSON are included in the artifact. This confirms a structural IL2CPP dump was generated; it does not recover original source code or deobfuscate method names.

## Verified type index

### `Character` — TypeDefIndex 116

Relevant serialized/gameplay data fields:
- Identity and role: `id`, `player`, `name`, `role`, `team`, `gender`
- Body and attributes: `height`, `age`, `bodyMass`, `muscleMass`, `armMass`, `legMass`, `stat`, `oldStat`, `newStat`
- Condition: `health`, `spirit`, `injury`, `injuryTime`, `dead`, `absent`
- Move loadouts: `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `taunt`
- Location/animation/promo state: `location`, `x`, `y`, `z`, `platform`, `seat`, `anim`, `promo`, `promoVariable`

Example confirmed method RVAs from `dump.cs`:
- `Character.LKHMEONAGGF()` — `0x187979C`
- `Character.MACHEOKJFAD(int)` — `0x1879910`
- `Character.BLDPMKCCEHH()` — `0x187A0F8`
- `Character.MEKEMKCMCNN(Character)` — `0x187B054`
- `Character.CKHMPNPJAJE(Character, int)` — `0x187C0F4`
- `Character.GMJJAPDJNKC(int, float, float, float)` — `0x187E27C`

These method names are obfuscated and their purpose must not be guessed from names alone.

### `SaveData` — TypeDefIndex 192

Confirmed fields include `ringShape` at offset `0x134` and `ringRopes` at offset `0x138`. The type has seven RVA-annotated methods in this dump, including constructor RVA `0x18C7720`.

### `Roster` — TypeDefIndex 196

Roster type exists in the dump and has 16 RVA-annotated methods. Example RVAs: `DCLLJJDMDFG` at `0x18CFBBC`, `EBKEFNJPEHA` at `0x18CFC58`, constructor at `0x18D08C0`. Method meanings are not yet established.

### Scene/control classes

- `Scene_Game` — TypeDefIndex 17: `LateUpdate` RVA `0x159C418`, coroutine `LEKCNDONCKO` RVA `0x159C4F8`, `Update` RVA `0x159C578`, `Start` RVA `0x159D7F4`. Its visible fields are diagnostic UI references and a timer, so do not assume this is the combat controller.
- `Scene_Match_Setup` — TypeDefIndex 103: `Start` RVA `0x182EB34`, `Update` RVA `0x182FEC4`, `AdjustCamera` RVA `0x182FA40`, `BrowseCast` RVA `0x1840E14`, `AddRandom` RVA `0x183F140`, `RemoveCast` RVA `0x18405DC`, `Booked` RVA `0x183EE5C`.
- `Scene_Controllers` — TypeDefIndex 117: `Start` RVA `0x1898A40`, `Update` RVA `0x1898BB8`.
- `Scene_Titles` — TypeDefIndex 158: `Start` RVA `0x189D394`, `Update` RVA `0x189D698`.
- `Scene_Database` — TypeDefIndex 14: `Start` RVA `0x1591870`, `Update` RVA `0x1593BB4`, `UpdateRankings` RVA `0x1591F1C`.

## What this proves — and what it does not

- **Confirmed:** metadata plus a library accepted by the workflow produced a large IL2CPP structural dump and generated DummyDll assemblies.
- **Confirmed:** the dump includes Character move-loadout arrays, character condition/position fields, ring settings, roster data, and scene setup methods.
- **Not confirmed yet:** exact attack/grapple state machine, AI decision logic, pinfall/elimination winner logic, or mapping string-literal addresses to the owning methods.
- **Important:** the native library's exact package/ABI pairing with the user-provided Wrestling Empire 1.8.0 XAPK still needs independent verification before relying on RVAs for runtime instrumentation or binary patching.

## Next analysis steps

1. Search `dump.cs` and `script.json` for classes containing combat/runtime references and ring interactions, then collect their fields and RVA method lists.
2. Cross-reference the gameplay strings from `stringliteral.json` with `script.json` metadata and native references where the dump format exposes them.
3. Build an evidence-labelled index for grapple, ground moves, rope climbing, ring generation, and match result flow. Keep hypotheses separate from confirmed links.
4. Preserve the original APK/library and do not patch or redistribute game binaries as part of this documentation pass.
