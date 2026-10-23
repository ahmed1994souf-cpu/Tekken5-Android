# التحليل 69 — ربط Character → Costume → shape من البيانات الفعلية

التاريخ: 2026-10-23
المشروع: Wrestling Empire Android 1.8.0 فقط.

## 1. ما تم فحصه فعليًا
تم تحليل الملف المرفوع `UnityDataAssetPack.apk` مباشرة، وليس الاعتماد على الجرد السابق فقط.

داخل `assets/bin/Data/datapack.unity3d`:
- UnityFS format 8.
- Unity `6000.3.25f1`.
- تم فك فهرس UnityFS الداخلي بنجاح.
- الحزمة تحتوي 67 ملفًا/مدخلًا مفهرسًا، ومن بينها `resources.assets`.
- `resources.assets` حجمها الداخلي 58,605,568 بايت.
- SerializedFile version 22، little-endian، وMetadata Size = 238,400، وData Offset = 238,448.
- `resources.assets` تحتوي 9,861 كائنًا.

## 2. اكتشاف مهم: DefaultData
داخل `resources.assets` يوجد TextAsset باسم `DefaultData`.
- حجم الكائن: 1,317,112 بايت.
- الحمولة الفعلية: 1,317,091 بايت.
- بداية الحمولة تطابق تنسيق .NET BinaryFormatter/NRBF (وجود SerializedStreamHeader وAssembly-CSharp metadata).
- هذا الملف ليس مجرد نصوص؛ يحتوي تعريفات الأصناف والبيانات الفعلية للشخصيات والأزياء.

## 3. تعريف Character داخل DefaultData
تم العثور على تعريف BinaryFormatter للصنف `Character`.
- عدد الحقول: 69.
- الحقل `name` في الموضع 2.
- الحقل `costume` في الموضع 21.
- نوع `costume`: `Costume[]`.

تم تتبع 349 كائن Character فعليًا في البيانات، وليس مجرد وجود اسم Character في جدول النصوص.

أمثلة مؤكدة:
- Wuri Cusson
- Ronan Raw
- John Crockett
- Machine Miuri
- Nirvana
- Lucy Lakes
- Scott Land
- Ralph Zipper
- Redneck Rosteen
- Thunder Tiger

## 4. تعريف Costume داخل DefaultData
تم العثور على تعريف `Costume` مباشرة داخل نفس تدفق BinaryFormatter.
الحقول التي ظهرت في التعريف:
- `id`
- `charID`
- `limb`
- `texture`
- `r`
- `g`
- `b`
- `flesh`
- `shape`

تم تتبع 1,049 كائن Costume فعليًا.

هذا يتوافق مع تحليل IL2CPP السابق الذي أثبت أن `Costume.shape[]` موجود عند +0x48 في كائن Costume.

## 5. أهم نتيجة جديدة: استخراج shape[] فعليًا
لم نعد في مرحلة القول إن `shape[]` موجود فقط. تم الآن استخراج القيم الفعلية من بيانات اللعبة.

مثال أول Costume:
- `id = 2`
- `charID = 0`
- `limb = 16`
- `shape[]` يحتوي 40 عنصرًا.
- بداية المصفوفة: `[0, 4, 1, 3, 100, 0, 0, 0, ...]`

مثال آخر:
- Character: `Wuri Cusson`
- لديه 3 أزياء مرتبطة به.
- أزياءه تستخدم قيم shape مختلفة، مثل slot 1 = 4 أو 1، وslot 2 = 0 أو 1، وslot 3 = 4 أو 1.

Character آخر:
- `Ronan Raw`
- لديه 3 أزياء.
- slot 3 من shape يصل إلى 13.

## 6. نتيجة قوية جدًا حول slot الخاص بالرأس
عند تحليل 1,049 Costume:
- `shape[3]` استخدم قيمًا غير صفرية من 1 إلى 14، إضافة إلى 0.
- أي أن مجموعة القيم الفعلية في هذا الموضع هي بالضبط 15 قيمة: `0..14`.

وفي `assets/costumes.manifest` يوجد بالضبط 15 Mesh للرؤوس:
- Head_Giant
- Head_Fat
- Head_Female
- Head_Squashed
- Head_Gaunt
- Head_Wide
- Head_Narrow
- Head_Chubby
- Head_Slim
- Head_Sarge
- Head_Hairy
- Head_Nose
- Head_Thug
- Head_Jaw
- Head_Normal

هذا لا يكفي وحده لإثبات ترتيب `0..14 → أسماء الرؤوس`، لكنه دليل قوي جدًا أن `shape[3]` هو مرشح مباشر لفهرسة مجموعة الرؤوس، لأن عدد القيم وعدد Mesh الرؤوس متطابقان تمامًا.

**ما زال ترتيب الرقم → اسم الرأس غير مثبت 100%**؛ لا أعتبر قائمة manifest ترتيبًا دليلاً نهائيًا قبل مطابقتها مع الكود.

## 7. مؤشرات أخرى من shape[]
التوزيع حسب الموضع يوضح أن shape ليست قيمة واحدة عامة، بل مصفوفة slots:

- slot 0: لا توجد قيم غير صفرية في 1,049 Costume المفحوصة.
- slot 1: القيم غير الصفرية 1..4.
- slot 2: القيمة غير الصفرية الأساسية 1.
- slot 3: القيم 1..14 + 0، وهو أقوى مرشح للرأس.
- slot 4: القيم 70،72،75،80،84،85،90،100،110.
- توجد slots أخرى تستخدم 1 أو -1 أو 100 حسب الزي.

هذا يؤكد أن ربط `shape[i]` يحتاج معرفة معنى الـslot أولًا، ثم معرفة مجموعة الموارد الخاصة به؛ لا يجوز اعتبار كل الأرقام فهرسًا واحدًا عالميًا لكل Mesh.

## 8. ربط جديد مع مسار IL2CPP
النتيجة الجديدة تتصل مباشرة بما ثبت في المراحل السابقة:

`Character.costume`
→ كائن `Costume`
→ `Costume.shape[]`
→ `PKIOJFKPIBI.MHEFCABLLCN` عند RVA `0x14AC0F0`
→ قراءة عنصر shape مفهرس
→ `Int32.ToString`
→ `String.Concat`
→ `Resources.Load`
→ `Instantiate`
→ `SkinnedMeshRenderer.set_sharedMesh`

المراحل السابقة أثبتت مسار IL2CPP بالتفكيك؛ هذه المرحلة تضيف لأول مرة بيانات Character/Costume/shape الحقيقية من الحزمة نفسها.

## 9. ما تم حله الآن وما بقي
### تم حله بدرجة عالية
- الوصول إلى `datapack.unity3d` الحقيقي.
- فك UnityFS وفهرسة ملفاته الداخلية.
- الوصول إلى `resources.assets` الحقيقي.
- العثور على `DefaultData`.
- تفسير `DefaultData` كتدفق BinaryFormatter/NRBF.
- استخراج 349 Character.
- استخراج 1,049 Costume.
- استخراج shape[] الفعلية.
- إثبات أن Character يملك `Costume[]` داخل البيانات.
- إثبات أن shape slots تحمل مجموعات أرقام مختلفة، وليست ID عالميًا بسيطًا.

### لم يُحسم بعد
1. الرقم `shape[slot]` → اسم Mesh/Resource النهائي.
2. ترتيب `0..14` بالنسبة إلى أسماء الـ15 Head Mesh.
3. تحديد معنى كل slot من 40 slot بدقة.
4. تحديد النص الثابت الذي يسبق رقم shape في `String.Concat` داخل MHEFCABLLCN.
5. استخراج Mesh إلى صيغة قابلة للتحرير.
6. استبدال Mesh فعليًا داخل APK واختبار اللعبة.

## 10. الخطوة التالية الدقيقة
الخطوة التالية ليست تخمين أسماء الموديلات. سيتم بناء جدول:

`Character name → Costume id → shape slot → numeric value → Resource key → Mesh object`

والتركيز الأول سيكون `shape[3]` لأن لدينا الآن 15 قيمة مقابلة لـ15 Head Mesh، ثم نستخدم مسار IL2CPP/Resource string لإثبات ترتيب الأسماء.

بعد ذلك ننتقل إلى `shape[4]` وبقية slots.

## التقدم التقريبي بعد هذه المرحلة
- خريطة Character/Costume: **95%**.
- استخراج بيانات shape الحقيقية: **95%**.
- فهم دالة تركيب المجسم وتعيين sharedMesh: **75%**.
- ربط shape بالـResource key: **55%**.
- ربط الرقم بالـMesh المحدد: **45%** (تحسن بسبب تطابق 15/15 للرؤوس، لكنه ليس إثبات ترتيب).
- استخراج/استبدال موديل فعلي واختباره: **0%**.

هذه النسب تصف تقدم التحليل فقط؛ لم يتم تعديل APK الأصلي أو استبدال أي Mesh أو اختبار نسخة معدلة.