# فهرسة نصوص مسارات/تصنيفات الأزياء — المرحلة 53

التاريخ: 2026-10-23

المصدر: `output/stringliteral.json` داخل أثر التشغيل [39939889590](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39939889590)، بعد تنزيله وفحصه.

## سلاسل نصية مؤكدة

ظهرت السلاسل التالية في جدول النصوص:
- `Costumes/Models` — العنوان `0x3369298`
- `Costumes/Models/Hair` — `0x33692A0`
- `Costumes/Models/Heads` — `0x33692A8`
- `Costumes/Bodies` — `0x3369240`
- `Costumes/Arms` و`Costumes/Hands` و`Costumes/Legs`
- `Costumes/Faces` و`Costumes/Faces/Beards` و`Costumes/Faces/Masks`
- `Costumes/Legs/Footwear` و`Costumes/Bodies/Patterns`

## التفسير وحدود الدليل

- **CONFIRMED:** هذه النصوص موجودة في جدول السلاسل المستخرج من `libil2cpp.so`.
- **INFERRED:** تنظيم المحتوى يفصل تصنيفات النماذج والرؤوس والشعر وأجزاء الجسم والملابس؛ وهذا يتفق مع حقول الزي المجزأة التي ظهرت في `Costume`.
- **UNKNOWN:** لا تثبت السلاسل وحدها أن هذه المسارات هي مسارات ملفات فعلية داخل AssetBundle؛ قد تكون تسميات واجهة/تصنيفات أو مفاتيح بحث. يجب تتبع مواضع استخدامها أو فحص metadata لحزمة الأصول قبل التعامل معها كمسارات تحميل.

## الخطوة التالية

ابحث عن مراجع هذه السلاسل داخل الكود الأصلي المفكك، ثم اربطها بالدوال التي تستخدم `shape[]` أو `texture[]`. بالتوازي، افحص قائمة أصول Unity/AssetPack المتاحة للبحث عن أصول تخص `Costumes/Models/Heads` و`Costumes/Models/Hair` دون افتراض أن أسماء المجلدات تطابق أسماء الملفات.
