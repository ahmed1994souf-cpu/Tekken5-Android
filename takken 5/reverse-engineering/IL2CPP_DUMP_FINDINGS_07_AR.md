# نتائج التفريغ الفعلي — المرحلة 07

## حالة التفريغ
تم تنزيل artifact من تشغيل GitHub Actions رقم 39658284561 وفحصه محليًا. على الرغم من أن خطوة `Run Il2CppDumper` انتهت برمز خطأ بعد ظهور `Done!`، فإن ملفات التفريغ موجودة بالفعل داخل الأرشيف. سبب الخروج النهائي الظاهر في السجل هو محاولة استدعاء `Console.ReadKey` داخل runner لا يملك إدخال console تفاعليًا.

المصدر:
https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39658284561

## الملفات المستخرجة التي تم التحقق منها
- `output/dump.cs` — 19,237,153 بايت.
- `output/il2cpp.h` — 53,625,271 بايت.
- `output/script.json` — 54,460,738 بايت.
- `output/stringliteral.json` — 1,867,749 بايت.
- مجلد `output/DummyDll/` يحتوي تعريفات DLL وهمية، بما فيها `Assembly-CSharp.dll` بحجم 517,632 بايت.

هذه ملفات تفريغ مولدة من الأداة، وليست مشروع C# الأصلي. كثير من أسماء الدوال داخل اللعبة مبهمة/مموهة.

## نتائج ملموسة من dump.cs

### 1. صنف Character
- `TypeDefIndex: 116`
- حقول هوية/خصائص: `id`, `player`, `name`, `role`, `team`, `height`, `bodyMass`, `muscleMass`, `armMass`, `legMass`.
- الحالة: `health`, `spirit`, `injury`, `injuryTime`, `dead`, `absent`.
- الحركات: `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `taunt`.
- الحركة والموقع: `stance`, `location`, `x`, `y`, `z`, `platform`, `seat`, `anim`, `angle`.
- حقول التحركات هي مصفوفات أرقام `int[]`؛ هذا يثبت وجود مراجع/معرّفات حركات في نموذج البيانات، لكنه لا يكشف وحده أسماء كل حركة أو شروطها.

### 2. صنف SaveData
- `TypeDefIndex: 192`
- يتضمن `savedChars`, `savedFeds`, `backupChars`, `backupFeds`.
- تقدم/مسيرة: `wrestler`, `booker`, `progress`, `date`, `year`, `years`, `mission`, `bookingMission`.
- إحصاءات: `matches`, `wins`, `titles`, `trophies`, `bestRating`, `bank`.
- تكوين المباراة والحلبة: `match`, `matchSize`, `arenaVenue`, `arenaCage`, `ringSize`, `ringShape`, `ringRopes`, `ringCanvas`, `ringApron`, `ringPosts`, `ringPads`, `ringMat`.
- إعدادات مرتبطة باللعب: `optReferees`, `optManagers`, `optAnnouncers`, `optIntruders`, `optMeters`, `optGore`, `camType`, `camZoom`, `camHeight`.

### 3. صنفا World وProgress
يحتوي `World` و`Progress` على حقول ثابتة مرتبطة بموقع اللاعب والتقدم ومواصفات الساحة. كما تظهر حقول `ringShape`, `ringRopes`, `matchSize`, و`arenaCage` في سياق حفظ الإعدادات.

### 4. عناوين RVA
يحتوي `Character` على أساليب ذات عناوين RVA مثل `0x187979C`, `0x1879910`, `0x1879C14` وغيرها، لكن أسماء الأساليب مبهمة مثل `LKHMEONAGGF` و`MACHEOKJFAD`. هذه عناوين RVA مولدة من تفريغ هذه المكتبة؛ لا يجوز تعيين وظيفة بشرية محددة لها قبل تحليل IL/التعليمات أو تتبع الاستدعاءات.

## إصلاح سير العمل
تم تحديث `.github/workflows/dump-il2cpp.yml` في commit `44db68845009722a84cabdebe9b8d01c8b6174c8`:
- يسجل سجل تشغيل الأداة بدل اعتبار رمز خروجها وحده حاسمًا.
- يعتبر التفريغ صالحًا إذا كانت `dump.cs`, `script.json`, و`il2cpp.h` موجودة وغير فارغة.
- يولّد `dump_summary.json` مع أحجام وبصمات SHA-256 وعدد تعليقات RVA.
- لم يعد يضمّن `libil2cpp.so` في artifact؛ يرفع نتائج التحليل فقط.
- هذه التعديلات ستُختبر في التشغيل التالي؛ لا تدّعي هذه الوثيقة أن التشغيل المعدل نجح بعد.

## الخطوة التالية
1. تشغيل workflow المعدل والتحقق من artifact المنقح.
2. تحليل تعريفات الأصناف حول `Character` و`SaveData` و`World` و`Progress` واستخراج قوائم الحقول/الأساليب آليًا.
3. استخدام `script.json` وخرائط التسجيل لربط الأساليب المبهمة بعناوين native حيث تتوفر الأدلة.
4. لا نسمّي دالة «تنفيذ رمية» أو «تثبيت» حتى يظهر دليل مباشر من أسماء/تعليمات/استدعاءات؛ الحقول وحدها لا تثبت التنفيذ.
