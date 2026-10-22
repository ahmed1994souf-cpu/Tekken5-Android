# ANALYSIS STAGE 36 — تدقيق تقرير الوصول إلى حقول Character

التاريخ: 2026-10-22  
النطاق: Wrestling Empire Android 1.8.0 فقط.

## مصدر الفحص

راجعت ملف artifact الفعلي `character-field-access-report.zip`، وليس ملخص المرحلة السابقة فقط.

- GitHub Actions run: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39844534828
- Artifact: `character-field-access-report`
- الملف داخل الأرشيف: `character-field-access.txt`
- الحجم المضغوط: 596,403 bytes؛ النص المستخرج: 8,860,533 bytes.
- الفحص يسجل 56,202 مطابقة مباشرة لإزاحات ذاكرة، مع تحذير صريح بأن المطابقة لا تثبت أن سجل الأساس يشير إلى كائن Character.

## تدقيق مهم: بعض نتائج الماسح إيجابيات كاذبة

في التقرير تظهر أمثلة مثل:

```text
0x161a7a0 | health | 0xa0 | WRITE candidate | stp x24, x23, [sp, #0xa0] | sp
0x161a7a4 | dead   | 0xb0 | WRITE candidate | stp x22, x21, [sp, #0xb0] | sp
```

هذه تعليمات حفظ سجلات على المكدس (`sp`)، وليست كتابة إلى `Character.health` أو `Character.dead`. السبب أن الماسح يطابق الإزاحة الرقمية وحدها حتى عندما يكون سجل الأساس هو مؤشر المكدس. لذلك لا يصح عدّ كل نتيجة تحمل تسمية حقل كدليل على لمس ذلك الحقل.

## نتائج أعلى قيمة بعد التصفية اليدوية

### 1. مرشح كتابة health داخل `NFAFFEAGBAL.PKDBEDDFGPL`

```text
0x161b564 | health | 0xa0 | WRITE candidate | str s0, [x23, #0xa0] | x23
0x161b594 | health | 0xa0 | READ candidate  | ldr s1, [x23, #0xa0] | x23
```

هاتان التعليمتان تستخدمان `x23` لا `sp`، لذا هما أقوى من مطابقة المكدس. وبحسب تفريغ البنية، الإزاحة `0xA0` تطابق `Character.health`. لكن إثبات نوع الكائن يتطلب تتبع مصدر `x23` على طول مسار التحكم؛ كما أن كتابة قيمة إلى health لا تثبت وحدها أنها عملية إنقاص الضرر.

### 2. مرشح كتابة injury

```text
0x161ed78 | injury | 0xa8 | WRITE candidate | str d0, [x23, #0xa8] | x23
```

الإزاحة `0xA8` تطابق `Character.injury` وفق `dump.cs`. هذه إشارة مهمة تستحق فحص سياق التعليمات السابقة واللاحقة، لكنها لا تكشف وحدها سبب الإصابة أو طريقة حسابها.

### 3. تحديث injury وinjuryTime في Character

```text
0x188d6bc | injury     | 0xa8 | WRITE candidate | str w20, [x19, #0xa8] | x19 | Character$$LICMFPCGJNN
0x188d6f4 | injuryTime | 0xac | WRITE candidate | str w8,  [x19, #0xac] | x19 | Character$$LICMFPCGJNN
0x188d8f8 | injuryTime | 0xac | WRITE candidate | str w0,  [x19, #0xac] | x19 | Character$$LICMFPCGJNN
```

تتوافق هذه النتائج مع تصنيف الدالة `Character.LICMFPCGJNN` كتحديث لحالة الإصابة. لا يوجد في هذه المطابقات وحدها دليل على أنها دالة حساب الضرر النهائية.

## استنتاج المرحلة

- **مؤكد من artifact:** تقرير الفحص يحتوي على تعليمات ARM64 المطابقة للإزاحات، ويمكن تحديد المرشحين ضمن النطاقات التنفيذية.
- **مؤكد من المقارنة البنيوية:** `Character.health` عند `0xA0`، و`injury` عند `0xA8`، و`injuryTime` عند `0xAC`، و`dead` عند `0xB0` بحسب فهرس التفريغ.
- **غير مثبت:** أن كل سجل أساس من نوع Character، أو أن كتابة health هي خصم ضرر، أو معادلة الضرر، أو علاقة هذه المواضع بقرار AI أو إنهاء المباراة.

## الخطوة التالية الصحيحة

1. تحسين الماسح لاستبعاد الإزاحات القائمة على `sp` و`fp` من تصنيف حقول Character.
2. استخراج سياق تعليمات ARM64 حول `0x161B564` و`0x161B594` و`0x161ED78`، وتتبع تعريفات السجلات قبل هذه التعليمات.
3. ربط المرشحين باستدعاءات الدوال والحقول ذات الصلة مثل `moveAttack` و`moveCrush` قبل تسمية أي مسار بأنه ضرر أو هجوم.
4. الاحتفاظ بالتصنيفات الثلاثة: مؤكد، مرشح، وغير معروف؛ وعدم استنتاج منطق اللعب من أسماء الدوال المشفرة وحدها.
