# Wrestling Empire IL2CPP — المرحلة 17: خريطة حالة العالم والحلبة والحفظ

## دليل مباشر من dump.cs
فُحصت تعريفات `World` و`Progress` و`SaveData` داخل artifact الذي أنتجته عملية Il2CppDumper. النتائج التالية هي أسماء حقول كما تظهر في التفريغ؛ ليست استنتاجات من تخمين أسماء الدوال.

## 1) الصنف `World`: البيئة والحلبة
يحتوي `World` على مجموعات حقول واضحة:
- حدود المكان والكاميرا: `ground`, `ceiling`, `farNorth/farSouth/farEast/farWest`, `camNorth/camSouth/camEast/camWest`.
- الطقس والماء: `weather`, `gRain`, `gSnow`, `gWater`, `waterLevel`, `floodLevel`, `floodTarget`.
- إضاءة/ضباب الساحة: `lightSetting`, `lightColour`, `lightPosition`, `lightAngle`, `fog`.
- الحلبة: `gArena`, `arenaShape`, `arenaBarriers`, `ringPreset`, `ringShape`, `ringSize`, `ringGround`, `ringMiddle`, `ringTop`.
- مكونات الحلبة: `gRing`, `gCanvas`, `gApron`, `gPosts`, `gSupports`, `gPads`, `gMat`.
- الحبال والزوايا: `ringRopes`, `no_ropes`, `gRope[]`, `ropeX/Y/Z/A[]`, `cornerX/Z/A[]`.
- القفص: `arenaCage`, `gCage[]`, `cageX/Y/Z[]`, `cageTop`.

**استنتاج محدود:** بنية البيانات تتضمن صراحةً إعدادات ومكونات الحلبة والحبال والقفص والبيئة. لا يثبت ذلك بعد طريقة التصادم أو شروط الخروج من الحلبة.

## 2) الصنف `Progress`: تقدم اللعب ونتائج المباريات
الحقول تشمل `progress`, `fed`, `rivalFed`, الوقت والتاريخ، `mission` وحقول الهدف/المهلة، `bank`, `matches[]`, `wins[]`, `titles[,] `, `trophies[,] `, `show[]`, `opponent[]`, `match[]`, `matchSize[]`, `result[]`, `attendance[]`, `rating[]`, `profit[]`، وإعدادات الساحة والحلبة مثل `arenaCage`, `ringSize`, `ringShape`, `ringRopes`.

هذا يدعم أن اللعبة تفصل بين بيانات المصارع وبين تقدم المسيرة/نتائج العروض، لكن معنى كل رقم داخل المصفوفات يحتاج تتبع مواضع القراءة والكتابة.

## 3) الصنف `SaveData`: ما يُخزَّن
توجد حقول `savedChars` و`backupChars` و`savedFeds` و`backupFeds`، إضافة إلى تقدم اللعب والمال ونتائج المباريات وإعدادات الحلبة والكاميرا والتحكم. تظهر أيضًا إعدادات مثل `optMeters`, `optGore`, `optReferees`, `optManagers`, `camType`, `camZoom`, `camHeight`, `buttonScale`, `buttonAlpha`.

هذا وصف لبنية نموذج الحفظ فقط؛ لا يعني أن تعديل ملف الحفظ مباشرة آمن أو متوافق مع إصدار اللعبة.

## كيف يساعد هذا في خريطة اللعبة
يمكن تنظيم التحقيق إلى ثلاث طبقات:
1. **تعريف المصارع** — `Character`: صحة/روح/إصابات/حركات/إحداثيات.
2. **حالة البيئة** — `World`: الأرض والحلبة والحبال والقفص والكاميرا والطقس.
3. **تقدم المسيرة والحفظ** — `Progress` و`SaveData`: المباريات والنتائج والإعدادات.

## الخطوة التالية المطلوبة للحصول على منطق التنفيذ
يلزم ربط هذه الحقول بدوالها الفعلية عبر تعليمات `libil2cpp.so` ومراجع القراءة/الكتابة (XREFs). ملف `dump.cs` يثبت وجود الحقول وتواقيع الدوال، لكنه لا يكشف جسم الدوال الأصلية. لذلك لا أضع حتى الآن ادعاءً عن معادلة الضرر أو الذكاء الاصطناعي أو منطق تثبيت الخصم.
