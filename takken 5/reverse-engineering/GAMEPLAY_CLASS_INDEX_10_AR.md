# نتائج التحليل — المرحلة 10: فهرس أولي لأصناف المشهد والعالم

تاريخ الفحص: 2026-10-21. المصدر المباشر: artifact من GitHub Actions run [39658646561](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39658646561)، artifact ID `12371909877`. فُكّ الأرشيف محليًا وجرى البحث داخل `output/dump.cs` (19,237,153 بايت) بدل الاعتماد على ملخصات سابقة فقط.

## 1. تأكيد مصدر البيانات

- التفريغ يحتوي 62,358 تعليق RVA.
- الملف يتضمن أصناف اللعبة ضمن `Assembly-CSharp.dll`، بالإضافة إلى أصناف Unity و.NET؛ لذلك يجب عدم خلط الأصناف المتشابهة بالاسم من المكتبات المختلفة.
- عناوين RVA التالية تخص النسخة التي أنتجت هذا التفريغ فقط، ولا يُفترض ثباتها في إصدارات أخرى.

## 2. أصناف اللعبة المحددة

### `Scene_Match_Setup` — TypeDefIndex 103

أساليب بأسماء مقروءة وعناوين موثقة في `dump.cs`:

| RVA | الأسلوب والتوقيع |
|---|---|
| `0x1840E14` | `BrowseCast(ABPHCKOPPOI)` |
| `0x1841268` | `ClosestToX(float)` |
| `0x18409F4` | `ClosestToClick(float, float)` |
| `0x1841368` | `AlreadyTaken(int)` |
| `0x1841154` | `Playable(int)` |
| `0x183F140` | `AddRandom()` |
| `0x18405DC` | `RemoveCast(int)` |
| `0x183EDDC` | `DescribeLayout(int)` |
| `0x183EE5C` | `Booked(int)` |

الاستنتاج المسموح: هذه الأساليب تخص اختيار المشاركين وإدارة قائمة المشاركين/وصف تخطيط المباراة. لا تكشف هذه التواقيع وحدها منطق القتال أثناء المباراة.

### `World` — TypeDefIndex 43

حقول ثابتة موثقة تشمل:

- المكان وحدود العالم: `location`, `oldLocation`, `ground`, `ceiling`, `farNorth`, `farSouth`, `farEast`, `farWest`.
- حدود الكاميرا: `camNorth`, `camSouth`, `camEast`, `camWest`.
- البيئة: `gWater`, `gRain`, `gSnow`, `weather`, `waterLevel`, `floodLevel`, `waterColour`.
- عناصر المشهد: `gBasket`, `basketNet`, `gVehicle`.

من أمثلة أساليب الصنف ذات RVA: `0x15F337C`, `0x15F34D0`, `0x15F37D4`, `0x16015A8`, `0x1602258`. الأسماء مموهة، لذا لم أسمِّ وظيفة تنفيذية لأي منها اعتمادًا على التوقيع وحده.

### `Character` — TypeDefIndex 116

تأكيد إضافي لوجود بيانات الحالة والحركة: `health`, `spirit`, `injury`, `dead`, `absent`, `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `stance`, `location`, `x/y/z`, `platform`, `seat`, `anim`, `angle`. مصفوفات الحركات مخزنة كـ `int[]`; هذا لا يفسر وحده معنى كل معرّف حركة.

### `SaveData` — TypeDefIndex 192

الحقول تؤكد حفظ بيانات الشخصيات والمسيرة ونتائج المباريات، إضافة إلى إعدادات الحلبة مثل `match`, `matchSize`, `arenaVenue`, `arenaCage`, `ringSize`, `ringShape`, `ringRopes`, `ringCanvas`, `ringApron`, `ringPosts`, `ringPads`, `ringMat`.

## 3. ما الخطوة التحليلية التالية؟

الأولوية الآن ربط سلاسل التشخيص من `stringliteral.json` بدوال فعلية، مثل `Ground grapple with anim=`, `Triggering tope at distance=`, `falling over ropes with anim=`, و`Closest pin side = `. عناوين هذه السلاسل ليست عناوين دوال؛ يجب فحص `script.json` أو تعليمات ARM64 حول مراجع السلاسل لتحديد الدالة المالكة، ثم توثيق اسم الصنف وRVA والتوقيع بدليل مباشر.

لم أستنتج أسماء بشرية للدوال المموهة ولم أعتبر وجود حقل أو نص دليلًا كافيًا على خوارزمية حركة بعينها.
