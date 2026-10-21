# نتائج التحليل — المرحلة 09: ربط بيانات الشخصية والمباريات

تاريخ التحليل: 2026-10-21. المصدر: artifact `wrestling-empire-il2cpp-dump.zip` الناتج من تشغيل GitHub Actions رقم 39658646561. تم فتح الأرشيف محليًا وفحص `dump.cs` و`stringliteral.json` مباشرة.

## 1. التحقق من بنية الأصناف (dump.cs)

### Character — TypeDefIndex 116
تم استخراج تعريف الصنف كاملًا تقريبًا (نحو 9.8 KB) وإحصاء 77 أسلوبًا يحمل RVA. حقول مؤكدة:
- هوية ومظهر: `id`, `name`, `role`, `team`, `height`, `bodyMass`, `muscleMass`, `costume`.
- حالة: `health`, `spirit`, `injury`, `injuryTime`, `dead`, `absent`.
- قوائم حركة: `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `taunt`، وكلها حقول مصفوفات `int[]`.
- مكان/وضع: `stance`, `location`, `x`, `y`, `z`, `platform`, `seat`, `anim`, `angle`.

أمثلة من الأساليب الموثقة كما ظهرت في التفريغ (الأسماء مبهمة ولا ننسب لها وظيفة بالتخمين):
- `0x187979C` — `LKHMEONAGGF()`
- `0x187B054` — `MEKEMKCMCNN(Character)`
- `0x187C0F4` — `CKHMPNPJAJE(Character, int = 1)`
- `0x187D8D4` — `ONPPCMFKAEL(int, int = 0)`

هذه العناوين تخص مكتبة اللعبة التي جرى تفريغها، ولا ينبغي افتراض أنها ثابتة بين إصدارات مختلفة.

### SaveData — TypeDefIndex 192
تم إحصاء 7 أساليب مع RVA. الحقول تؤكد أن الحفظ يحتوي:
- قوائم الشخصيات والاتحادات المحفوظة والاحتياطية.
- بيانات المسيرة والمهام والتاريخ والأموال والنتائج والإحصاءات.
- إعدادات المباراة والحلبة: `match`, `matchSize`, `arenaVenue`, `arenaCage`, `ringSize`, `ringShape`, `ringRopes`, `ringCanvas`, `ringApron`, `ringPosts`, `ringPads`, `ringMat`.
- إعدادات الكاميرا والتحكم والصوت والجودة.

### Scene_Match_Setup — TypeDefIndex 103
تم العثور على أساليب ذات أسماء مقروءة، وهو دليل أوضح على واجهة إعداد المباراة:
- `0x1840E14` — `BrowseCast(...)`
- `0x1841268` — `ClosestToX(float)`
- `0x18409F4` — `ClosestToClick(float, float)`
- `0x1841368` — `AlreadyTaken(int)`
- `0x1841154` — `Playable(int)`
- `0x183F140` — `AddRandom()`
- `0x18405DC` — `RemoveCast(int)`
- `0x183EDDC` — `DescribeLayout(int)`
- `0x183EE5C` — `Booked(int)`

هذه الأسماء تدعم وجود اختيار المشاركين، منع الاختيار المكرر، التحقق من قابلية اللعب، وإضافة/إزالة المشاركين. لكنها تخص إعداد المباراة، ولا تكشف وحدها منطق المصارعة داخل المباراة.

## 2. أدلة نصية إضافية من stringliteral.json

تم فحص ملف السلاسل المستخرج (22,779 مدخلًا). أمثلة ذات صلة مباشرة:
- `0x336CA10`: `Ground grapple with anim=`
- `0x3367B28`: `Cancelling tope because `
- `0x337AF88`: `Triggering tope at distance=`
- `0x335F950`: `falling over ropes with anim=`
- `0x335F718`: `cut by rope at `
- `0x3368A98`: `Closest pin side = `
- `0x3373F88`: `Opponents can be eliminated by pin or submission.`
- `0x3373F80`: `Opponents can be defeated by submission or stoppage.`
- `0x336C4F8`: `German Suplex`
- `0x336A6B0`: `Dragon Suplex`
- `0x336A370`: `Diving Grapple`

تنبيه: العناوين أعلاه هي عناوين السلاسل النصية داخل الملف وفق إخراج الأداة، وليست عناوين RVA للدوال.

## 3. ما الذي لا يزال مجهولًا؟
أسماء كثيرة في `Character` مموهة، و`dump.cs` لا يحتوي جسم كود C# الفعلي؛ بل تعريفات وتواقيع. السلاسل النصية تثبت وجود المصطلح أو رسالة التشخيص، لكنها لا تربط وحدها النص بدالة معينة. لا يمكن من هذا التفريغ وحده الجزم بتسلسل تنفيذ حركة معينة أو شروط نجاحها.

## 4. الخطوة التالية
- إجراء تحليل بنيوي لـ `script.json` وربط مؤشرات الأصناف والأساليب مع `dump.cs`، ثم إعداد فهرس قابل للبحث لأساليب `Character` و`Scene_Match_Setup` و`SaveData`.
- البحث عن أصناف اللعبة ذات أسماء مقروءة مرتبطة بالمباراة/القتال/العالم، وعدم الخلط بين أصناف اللعبة وأصناف .NET/Unity ذات الأسماء العامة.
- إذا بقيت أسماء الأساليب مموهة، فستتطلب معرفة السلوك بدقة تحليل التعليمات الأصلية في `libil2cpp.so` (disassembly) أو تتبع استدعاءات موثق؛ لا تكفي أسماء الحقول وحدها.
