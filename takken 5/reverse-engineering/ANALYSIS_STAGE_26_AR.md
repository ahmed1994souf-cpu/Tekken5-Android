# المرحلة 26 — تحقق مستقل من تشغيل التفريغ وربط مؤشرات القتال

التاريخ: 2026-10-21  
النطاق: Wrestling Empire 1.8.0 فقط؛ لا علاقة لهذا التقرير بمشروع X-Man.

## 1. التحقق من تشغيل GitHub Actions

تم التحقق من التشغيل الأحدث:
- [تشغيل Dump Wrestling Empire IL2CPP رقم 16](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39677914247)
- [تفاصيل المهمة وسجل الخطوات](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39677914247/job/119492500528)
- الحالة: `completed / success`
- تم بنجاح تنزيل `libil2cpp.so`، العثور على metadata، بناء Il2CppDumper، إنتاج التفريغ، تفكيك المرشحين ARM64، والتحقق من النتائج ورفع artifact.
- artifact: `wrestling-empire-il2cpp-dump`، حجمه 12,728,332 بايت، وSHA-256: `40cf653e6e665b73eeefb2386fa71bcf27760856390003203019cff665cb149d`.

الملفات الرئيسية داخل artifact: `output/dump.cs` و`output/script.json` و`output/stringliteral.json` وملفات `native-disassembly/*.txt`. يؤكد ملخص البناء أن `dump.cs` يحتوي 62,358 طريقة لها RVA.

## 2. خريطة البيانات المرتبطة بالقتال

من `Character // TypeDefIndex: 116`:
- `health` عند الإزاحة `0xA0`
- `injury` عند `0xA8` و`injuryTime` عند `0xAC`
- `dead` عند `0xB0`
- قوائم الحركات `moveFront/moveBack/moveGround/moveAttack/moveCrush` عند `0xF0/0xF8/0x100/0x108/0x110`
- الإحداثيات `x/y/z` عند `0x130/0x134/0x138` و`anim` عند `0x144`.

هذه الحقول تحدد نقاطاً قابلة للتتبع في الدوال، لكنها لا تكشف بمفردها صيغة الضرر أو قرار اختيار الحركة.

## 3. أدلة النصوص التي تشير إلى مسارات قتال

توجد في `stringliteral.json` الرسائل التالية:
- `Selecting attack for v=`
- `Disallowing attack at impactY=`
- `Ground grapple with anim=`
- `after ImpactChecks broke grapple`
- `Straying too far from ground grapple targets!`
- `Injured by attacker=`
- `Triggering flying attacks with viable=`

التفسير الآمن: النصوص توحي بمسارات مستقلة لاختيار الهجوم، وفحص الاصطدام، والمسكات الأرضية، والإصابة. لم نثبت بعد عناوين XREF لهذه النصوص؛ لذلك لا يصح نسبها إلى RVA محدد أو إعلان اكتشاف دالة الضرر النهائية.

## 4. مراجعة المرشحين السابقين

الدالتان `Character.CKHMPNPJAJE` عند `0x187C0F4` و`Character.EPNEPBPKCBH` عند `0x187D5F4` تظهران عمليات نسخ بيانات ومصفوفات؛ لا يوجد دليل كافٍ لتسميتهما منفذتي هجوم. كما أن `Scene_Game.Update` عند `0x159C578` لا يثبت وحده وجود منطق AI أو ضرر.

## 5. الخطوة التالية الدقيقة

يلزم الحصول على الملف التنفيذي `libil2cpp.so` في بيئة التحليل مع `stringliteral.json`، ثم:
1. تحديد مواضع عناوين/مراجع النصوص في الملف التنفيذي.
2. استخراج الدوال التي تشير إلى رسائل اختيار الهجوم والإصابة والمسكات.
3. فحص تلك الدوال بحثاً عن القراءة والكتابة إلى حقول `Character.health` و`injury` و`anim`.
4. تتبع `Segment.result` و`Segment.winner` بصورة منفصلة لإثبات شروط الفوز/التثبيت.
5. تدوين النتائج مع مستوى ثقة، وعدم تخمين أسماء الدوال المشفرة.

## حدود هذه المرحلة

نجاح التفريغ مؤكد، لكن الملف التنفيذي الأصلي `libil2cpp.so` ليس ضمن محتويات artifact الذي فحصته؛ لذا لم تُثبت XREFs ولا دالة الضرر أو التثبيت النهائية. هذا تحليل ساكن، وليس تشغيلًا للعبة.
