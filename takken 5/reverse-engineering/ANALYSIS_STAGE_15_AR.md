# المرحلة 15 — مراجعة تشغيل التفريغ وتحديد مرشحي حلقة المباراة

تاريخ: 2026-10-21
المصدر: تشغيل GitHub Actions رقم 39660693165 وartifact رقم 12374366190، مع فحص مباشر لمحتويات ZIP.

## 1. تصحيح مهم لسجل المرحلة السابقة

كان التقرير السابق يقول إن رابط TransferNow أعاد HTML ولم تُقرأ المكتبة. فحص خطوات التشغيل الفعلية يثبت أن خطوة `Download libil2cpp.so` انتهت بحالة `success`، ثم نجحت خطوات `Run Il2CppDumper` و`Verify generated dump and summarize` ورفع الـartifact. لذلك لا يصح اعتبار تنزيل المكتبة فاشلًا في ذلك التشغيل. ما لا نملكه في artifact الحالي هو نسخة `libil2cpp.so` نفسها؛ الـZIP المرفوع يحتوي ملفات التفريغ وDummyDll والسجل، وليس المكتبة الثنائية.

## 2. فحص artifact الحالي

تم تنزيل وفحص ZIP مباشرة. الملفات الرئيسية:
- `output/dump.cs`: 19,237,153 بايت.
- `output/script.json`: 54,460,738 بايت.
- `output/stringliteral.json`: 1,867,749 بايت.
- `output/DummyDll/Assembly-CSharp.dll`: 517,632 بايت.
- `dumper.log`: موجود ضمن الأرشيف.

يحوي `script.json`:
- 122,991 سجلًا في `ScriptMethod`.
- 22,779 سجلًا في `ScriptString`.
- 9,035 سجلًا في `ScriptMetadata`.
- 14,993 سجلًا في `ScriptMetadataMethod`.
- 137,565 قيمة في `Addresses`.

وجود التفريغ لا يعني أن أجسام الدوال قد استعيدت؛ معظم دوال اللعبة المموهة في `dump.cs` تظهر كتواقيع فقط.

## 3. مرشح واضح لدورة تحديث المشهد

سجلات `ScriptMethod` تؤكد هذه الدوال في `Scene_Game`:
- `0x159C418` — `Scene_Game$$LateUpdate`
- `0x159C578` — `Scene_Game$$Update`
- `0x159D7F4` — `Scene_Game$$Start`
- `0x159C4F8` — `Scene_Game$$LEKCNDONCKO` (تعيد IEnumerator)

هذا يثبت مشاركة الصنف في دورة تحديث Unity، لكنه لا يثبت أن `Update` هو وحده الذي ينفذ AI أو الضربات. يجب تتبع الاستدعاءات في المكتبة الأصلية قبل نسبة سلوك بعينه إليه.

## 4. دوال Character التي تستحق التتبع

من `dump.cs` و`script.json`، هذه أمثلة مؤكدة على تواقيع تستقبل شخصية أخرى:
- `0x187B054` — `Character$$MEKEMKCMCNN(Character)`
- `0x187C0F4` — `Character$$CKHMPNPJAJE(Character, int)`
- `0x187D5F4` — `Character$$EPNEPBPKCBH(Character, int)`
- `0x187DD58` — `Character$$NEGGBOHACLG(Character, int)`

التوقيع يثبت تمرير مرجع إلى شخصية أخرى فقط. لا نسمّي هذه الدوال هجومًا أو ضررًا أو إمساكًا قبل فحص تعليمات التنفيذ والمستدعين.

## 5. نصوص قتال تؤكد مسارات ينبغي ربطها بالكود

وجدت في `ScriptString` النصوص التالية:
- `after ImpactChecks broke grapple`
- `attackViable=`
- `Closest pin side = `
- `Ground grapple with anim=`
- `Triggering flying attacks with viable=`
- `Triggering tope at distance=`
- `Evading crush with anim=`

هذه أدلة مباشرة على وجود رسائل/مصطلحات لهذه المسارات، لكنها ليست عناوين دوال. يلزم استخدام المكتبة المطابقة لتحديد مواضع الإشارة لهذه السلاسل وربطها بالدوال.

## 6. الخطوة التقنية التالية

1. عدم إعادة تشغيل التفريغ دون داعٍ؛ تشغيل 39660693165 نجح بالفعل.
2. تعديل سير العمل مستقبلًا بحيث ينفّذ فحص ELF وBuild ID ومعمارية المكتبة ثم يفكك الدوال المرشحة داخل runner، ويرفع تقريرًا نصيًا محدودًا فقط، لا المكتبة التجارية نفسها.
3. ربط مواضع النصوص ذات الصلة بالدوال المالكة، ثم توثيق اسم الصنف وRVA والتوقيع ومستوى الثقة.
4. إبقاء الضرر وقرار AI وشروط الفوز في حالة UNKNOWN إلى أن يظهر دليل من التعليمات أو اختبار قابل للتكرار.

## مستوى الثقة

- CONFIRMED: نجاح خطوة تنزيل المكتبة في التشغيل 39660693165؛ وجود ملفات التفريغ وأعداد السجلات أعلاه؛ أسماء الدوال والتواقيع المذكورة.
- INFERRED: `Scene_Game.Update/LateUpdate` نقطة مناسبة لبدء تتبع دورة المشهد.
- UNKNOWN: الوظائف الفعلية للدوال المموهة، معادلة الضرر، قرار AI، شروط pin/submission.
