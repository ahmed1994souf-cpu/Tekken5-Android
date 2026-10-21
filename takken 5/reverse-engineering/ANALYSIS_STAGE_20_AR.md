# المرحلة 20 — مطابقة script.json مع عناوين Character وScene_Game

التاريخ: 2026-10-21  
المصدر: `output/script.json` و`output/dump.cs` من artifact `12374366190` الذي نُزّل وفُحص مباشرة.

## نتيجة المطابقة

تم تحليل JSON محليًا. يحتوي `script.json` على 122,991 سجلًا في `ScriptMethod`. قيمة `Address` في JSON تطابق القيمة العددية لعناوين RVA الظاهرة في `dump.cs` للدوال المستهدفة في هذه النسخة. مثال: `0x187B054` يساوي `25669716` عشريًا.

| اسم الدالة | RVA في dump.cs | Address في script.json | التحقق |
|---|---:|---:|---|
| Character.MEKEMKCMCNN | 0x187B054 | 25669716 | متطابق |
| Character.DOBMPDMNJBK | 0x187B41C | 25670684 | متطابق |
| Character.CKHMPNPJAJE | 0x187C0F4 | 25673972 | متطابق |
| Character.EPNEPBPKCBH | 0x187D5F4 | 25679348 | متطابق |
| Character.NEGGBOHACLG | 0x187DD58 | 25681240 | متطابق |
| Scene_Game.Update | 0x159C578 | 22660472 | متطابق |
| Scene_Game.Start | 0x159D7F4 | 22665204 | متطابق |

## توقيعات ABI في script.json

- `Character$$MEKEMKCMCNN`: `void Character__MEKEMKCMCNN(Character_o* __this, Character_o* JLFCEOAPPNP, const MethodInfo* method)` — `viii`
- `Character$$CKHMPNPJAJE`: `void Character__CKHMPNPJAJE(Character_o* __this, Character_o* JLFCEOAPPNP, int32_t LFGIHJGLIGK, const MethodInfo* method)` — `viiii`
- `Scene_Game$$Update`: `void Scene_Game__Update(Scene_Game_o* __this, const MethodInfo* method)` — `vii`

هذه المطابقة تقلل خطر تتبع RVA خاطئ وتوفر أسماء رموز native يمكن البحث عنها عند تفكيك المكتبة. لكنها لا تكشف جسم الدالة أو معناها الوظيفي بمفردها.

## حدود الاستنتاج

**مؤكد:** أسماء الرموز وتواقيعها وعناوينها موجودة في `script.json`، وأرقام الدوال الخمس في Character وعناوين Scene_Game المذكورة تطابق عناوين dump.cs.

**غير مثبت:** ما إذا كانت أي من الدوال الخمس تنفذ مسكًا أو ضربة أو دفاعًا أو اختيار حركة AI. يلزم تفكيك تعليمات AArch64 وتتبع المراجع والقراءات/الكتابات.
