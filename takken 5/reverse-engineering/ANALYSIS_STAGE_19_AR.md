# المرحلة 19 — فحص مباشر لأثر GitHub Actions وملف dump.cs

التاريخ: 2026-10-21  
المستودع: `ahmed1994souf-cpu/Tekken5-Android`  
أثر GitHub Actions المفحوص: `wrestling-empire-il2cpp-dump`  
Artifact ID: `12374366190` — Workflow run: `39660693165`

## 1. ما تم التحقق منه مباشرة

تم تنزيل ZIP الخاص بالأثر من GitHub Actions وفحص محتوياته محليًا. يحتوي الأثر على الأقل على:

- `output/dump.cs` — 19,237,153 بايت.
- `output/script.json` — 54,460,738 بايت.
- `output/stringliteral.json` — 1,867,749 بايت.
- `dumper.log` — سجل تشغيل Il2CppDumper.

سجل الأداة يذكر Metadata Version 39 وIl2Cpp Version 39، وينتهي برسالة `Done!` لتوليد dump وملفات Dummy DLL. كما تظهر تحذيرات مثل `This file may be protected` وأخطاء استعادة بعض السمات؛ لذلك النجاح هنا يعني أن المخرجات وُلّدت، لا أن كل البيانات استُعيدت بلا نقص.

## 2. تأكيد من dump.cs

عُثر على التعريفات التالية في الملف المستخرج:

- `Scene_Game` — TypeDefIndex 17، بداية التعريف قرب السطر 2388.
  - `LateUpdate()` RVA `0x159C418`
  - `Update()` RVA `0x159C578`
  - `Start()` RVA `0x159D7F4`
- `World` — TypeDefIndex 43، بداية التعريف قرب السطر 3780.
- `Scene_Match_Setup` — TypeDefIndex 103، بداية التعريف قرب السطر 7141.
- `Character` — TypeDefIndex 116، بداية التعريف قرب السطر 8102.
- `SaveData` — TypeDefIndex 192، بداية التعريف قرب السطر 10440.

### حقول Character المؤكدة من dump.cs

| الحقل | الإزاحة |
|---|---:|
| health | 0xA0 |
| spirit | 0xA4 |
| injury / injuryTime | 0xA8 / 0xAC |
| dead / absent | 0xB0 / 0xB4 |
| moveFront | 0xF0 |
| moveBack | 0xF8 |
| moveGround | 0x100 |
| moveAttack | 0x108 |
| moveCrush | 0x110 |
| taunt | 0x118 |
| stance / location | 0x128 / 0x12C |
| x / y / z | 0x130 / 0x134 / 0x138 |
| platform / seat / anim | 0x13C / 0x140 / 0x144 |
| angle | 0x154 |
| cuffed | 0x164 |

### توقيعات الدوال المؤكدة

- `Character.MEKEMKCMCNN(Character)` — RVA `0x187B054`
- `Character.DOBMPDMNJBK(Character)` — RVA `0x187B41C`
- `Character.CKHMPNPJAJE(Character, int)` — RVA `0x187C0F4`
- `Character.EPNEPBPKCBH(Character, int)` — RVA `0x187D5F4`
- `Character.NEGGBOHACLG(Character, int)` — RVA `0x187DD58`

هذه التواقيع والعناوين مؤكدة من dump.cs. لكن أسماء الدوال المموهة لا تكشف وحدها هل هي ضربة أو مسك أو دفاع أو قرار AI.

## 3. ماذا يثبت هذا الأثر، وماذا لا يثبت؟

**مؤكد:** نجح الـworkflow في إنتاج dump.cs وscript.json وstringliteral.json؛ ووجود أنواع اللعبة وحقول Character وتواقيع الدوال أعلاه تحقق منه بالفحص المباشر.

**غير مثبت بعد:** لا يحتوي dump.cs على أجسام C# الأصلية لهذه الدوال؛ يظهر فقط توقيع الدالة وRVA. لذلك لا يمكن استنتاج معادلة الضرر أو ترتيب حركات المصارعة أو شروط الفوز من هذه التواقيع وحدها.

**الخطوة التقنية التالية:** مطابقة عناوين RVA مع تعليمات AArch64 في `libil2cpp.so`، ثم تتبع الدوال التي تقرأ/تكتب حقول `health` و`anim` وحقول الحركة، واستخراج المراجع الواردة (XREFs) قبل إعطاء أي اسم وظيفي مستنتج. يجب التأكد من أن المكتبة التي ستُفكك هي نفسها ذات Build ID `d32d84554cf9e27ee55d1933a9d5702066310c74` المذكور في تقرير التحليل السابق؛ لا يكفي تطابق اسم الملف.

## 4. تنبيه حول الملف الأصلي

الأثر الذي فُحص هنا هو ZIP لنتائج التفريغ، وليس نسخة خام من `libil2cpp.so`. هذا يؤكد أن الـworkflow أنتج المخرجات، لكنه لا يعني أن الملف الخام رُفع إلى مستودع GitHub. لا أضع المكتبة الثنائية الخام في المستودع تلقائيًا؛ الخطوة الصحيحة هي حفظها كـartifact خاص/مؤقت أو تنزيلها إلى بيئة التحليل، مع التحقق من المصدر والـhash.

