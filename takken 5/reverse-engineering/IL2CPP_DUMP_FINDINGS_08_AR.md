# نتائج التحليل — المرحلة 08 (مؤكدة من artifact)

تاريخ الفحص: 2026-10-21.

## نتيجة التشغيل المعدل
- Workflow: [Dump Wrestling Empire IL2CPP](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39658646561)
- الحالة: **success**.
- Artifact: [wrestling-empire-il2cpp-dump.zip](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39658646561/artifacts/12371909877)
- حجم artifact: 12,711,905 بايت.
- التحقق في سجل التشغيل: `dump.cs` = 19,237,153 بايت؛ `script.json` = 54,460,738؛ `il2cpp.h` = 53,625,271؛ `stringliteral.json` = 1,867,749.
- فُحصت ترويسة/بصمات SHA-256 للملفات في التشغيل. عدد تعليقات RVA داخل `dump.cs`: 62,358.
- تظهر أخطاء `attributeIndex` في سجل الأداة، ثم `Done!`، ثم تعطل `Console.ReadKey` النهائي. خطوة التحقق من الملفات ورفعها نجحت؛ لذلك لا ينبغي الخلط بين تعطل مطالبة المفاتيح التفاعلية وبين فشل إنتاج التفريغ.

## حقول مثبتة من dump.cs
### Character (TypeDefIndex 116)
الحقول تشمل `health`, `spirit`, `injury`, `dead`, `absent`, `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `taunt`, `stance`, `location`, `x/y/z`, `platform`, `seat`, `anim`, و`angle`. مصفوفات الحركة مخزنة كـ `int[]`؛ لا يمكن من الحقول وحدها معرفة معنى كل رقم.

### SaveData (TypeDefIndex 192) وProgress (TypeDefIndex 101)
تتضمن حقول تقدم المسيرة والمباريات والنتائج والإحصاءات، مثل `wrestler`, `booker`, `progress`, `mission`, `matches`, `wins`, `titles`, `trophies`, `match`, `matchSize`, `arenaVenue`, `arenaCage`, `ringSize`, `ringShape`, `ringRopes`, `ringCanvas`, `ringApron`, `ringPosts`, `ringPads`, و`ringMat`.

### World (TypeDefIndex 43)
توجد حقول ثابتة مثل `location`, `ground`, `ceiling`, حدود العالم (`farNorth/farSouth/farEast/farWest`)، حدود الكاميرا، المطر/الثلج/الماء، `gMap`, و`gArena`. هذا يدعم وجود نظام عالمي/مكاني، لكنه لا يثبت وحده تفاصيل بنية كل خريطة أو ترتيب مشاهدها.

## دليل مستقل من stringliteral.json
تم فحص القيم النصية المستخرجة، وظهرت نصوص لعب واضحة:
- Grapple: `Diving Grapple`, `Grapple High`, `Grapple Low`, `Ground grapple with anim=`.
- تحكم: `ATTACK, RUN or PICK-UP with or without a direction.`
- هجمات جوية: `Tope Attack`, `Tope Crush`, `You can perform moves from the tope rope if you whip`.
- أسماء حركات: `Alabama Slam`, `Body Slam`, `Choke Slam`, `German Suplex`, `Dragon Suplex`, `Dropkick`, `Mounted Punches`.
- شروط الفوز: نصوص تشير صراحة إلى pin وsubmission، بما فيها `Opponents can be eliminated by pin or submission.`
- سلوك الحبال/الاصطدام: `falling over ropes with anim=`, `cut by rope at`, `Cancelling tope because`.

هذه النصوص أدلة على وجود مصطلحات/حالات في اللعبة، لكنها ليست وحدها إثباتًا لاسم الدالة التي تنفذ كل حركة أو لتسلسل شروطها. عناوين النصوص مثل `0x336...` هي عناوين literal في الملف كما أخرجتها الأداة، وليست RVA لدوال native.

## الخطوة التالية
1. استخراج مقاطع `dump.cs` الخاصة بالأصناف التي تشير إليها السلاسل (خصوصًا الأنظمة/الأصناف المرتبطة بـ grapple وtope وrope وpin/submission).
2. البحث عن الأساليب التي تشير إليها نصوص التشخيص مثل `Ground grapple with anim=` و`Triggering tope at distance=`، ثم توثيق اسم الصنف وRVA والتوقيع كما هو دون تخمين.
3. عند الحاجة، ربط الأساليب في `script.json` و`il2cpp.h`؛ لا يُنسب سلوك تنفيذي لدالة مبهمة قبل ظهور دليل مباشر.
