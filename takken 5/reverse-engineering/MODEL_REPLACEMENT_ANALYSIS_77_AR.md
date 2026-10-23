# تحليل استبدال موديلات الشخصيات — المرحلة 77

التاريخ: 2026-10-23
المشروع: Wrestling Empire Android 1.8.0 فقط؛ لا علاقة له بمشروع X-Men.

## 1. تصحيح/تثبيت نقطة مهمة من المراحل السابقة
بعد مراجعة التفكيك المباشر مع تقارير المراحل 62 و63 و68، فإن الدالة الأهم لمسار تركيب الموديل هي:
`PKIOJFKPIBI.MHEFCABLLCN` عند RVA `0x14AC0F0`.

المسار التنفيذي المثبت داخلها يتضمن:
`Costume.shape[]` عند `[this + 0x328]` ثم قراءة `shape` من `[Costume + 0x48]` → تحويل الرقم إلى نص → `String.Concat` → `Resources.Load`، ثم في فروع الإعداد توجد `Instantiate` و`GetComponent` ونداءات `SkinnedMeshRenderer.set_sharedMesh`.

في التفكيك الموثق ظهرت نداءات setter عند:
- `0x14AEA28` → `UnityEngine.SkinnedMeshRenderer.set_sharedMesh` (`0x2DEAF04`).
- `0x14AEB00` → `UnityEngine.SkinnedMeshRenderer.set_sharedMesh`.
- `0x14AEBBC` → `UnityEngine.SkinnedMeshRenderer.set_sharedMesh`.

هذا يعني أن البحث لا يحتاج العودة إلى `Character.IKKBADFHKAL` للعثور على نقطة تعيين الـMesh؛ تلك الدالة تربط Character بالـCostume، بينما `MHEFCABLLCN` هي نقطة تركيب Mesh الأقوى.

## 2. الطرف الآخر من السلسلة أصبح مؤكدًا
تحليل `UnityDataAssetPack.apk` في المرحلة 68 أثبت وجود ملف `assets/costumes` الحقيقي، ووجود:
- 878 كائن/مسار Asset في manifest.
- 88 كائن `Mesh` فعليًا في SerializedFile.
- 15 Head Mesh.
- 34 Hair Mesh.
- 39 Mesh لأجزاء الجسم/الأطراف/الملابس.

والأهم أن مطابقة اسم `m_Name` مع الـmanifest نجحت بنسبة **88/88** بدون اسم مفقود أو مكرر. أمثلة:
- `Head_Jaw` → `Assets/Bundles/Costumes/Models/Heads/Head_Jaw.mesh`
- `Head_Thug` → `Assets/Bundles/Costumes/Models/Heads/Head_Thug.mesh`
- `H_Part2Part` → `Assets/Bundles/Costumes/Models/Hair/H_Part2Part.mesh`
- `R_Hand` → `Assets/Bundles/Costumes/Models/R_Hand.mesh`
- `Body` → `Assets/Bundles/Costumes/Models/Body.mesh`

إذن لم نعد أمام أسماء افتراضية؛ لدينا 88 Mesh objects حقيقية مرتبطة بمساراتها داخل AssetBundle.

## 3. ما أصبح مثبتًا كسلسلة واحدة
السلسلة الحالية هي:

`Character`
→ `Costume[]`
→ `Costume.shape[]`
→ `MHEFCABLLCN`
→ `String.Concat`
→ `Resources.Load`
→ `Object.Instantiate/GetComponent`
→ `SkinnedMeshRenderer.set_sharedMesh`
→ أحد Mesh objects الموجودة فعليًا في `assets/costumes`.

الجزء الأخير مدعوم بجرد AssetBundle الفعلي، وليس باستنتاج من أسماء الدوال.

## 4. العائق الوحيد قبل تحديد Mesh لكل قيمة shape
ما زال يلزم إثبات التحويل:

`shape[i] = N` → `Assets/Bundles/Costumes/Models/.../<Mesh>.mesh`

لا يجوز افتراض أن الرقم يساوي ترتيب الـmanifest أو ترتيب كائنات Mesh.

أفضل نقطة متابعة الآن هي تتبع سجلات ARM64 قبل كل `set_sharedMesh`، خصوصًا قيمة المرجع الموجودة في `x0`/`x1` في كل نداء، ثم تتبع المصدر الذي أعادته `Resources.Load` ونتيجة `GetComponent<SkinnedMeshRenderer>`.

بالتوازي يجب مطابقة النصوص الثابتة الموجودة في `script.json/stringliteral.json` مع الفروع المحددة، لأن وجود `Costumes/Models/Heads` و`Costumes/Models/Hair` في البرنامج وحده لا يكفي لإسنادها إلى فرع معين.

## 5. ما لم يتم بعد
- لم يتم إثبات mapping رقمي كامل لـ`shape[]` → Mesh.
- لم يتم استخراج Mesh إلى OBJ/FBX أو صيغة تحريرية.
- لم يتم استبدال Mesh داخل AssetBundle.
- لم يتم بناء APK معدل أو اختباره.

## 6. الخلاصة
نقطة التقدم الحقيقية الآن ليست مجرد معرفة أن اللعبة تستخدم Mesh؛ بل أصبح لدينا طرفا السلسلة:
1. **مصدر الاختيار:** `Costume.shape[]` داخل IL2CPP.
2. **نقطة التركيب:** `SkinnedMeshRenderer.set_sharedMesh` داخل `MHEFCABLLCN`.
3. **الأصول المستهدفة:** 88 Mesh حقيقية داخل `assets/costumes` مع مسارات معروفة.

لذلك فإن الخطوة التالية محددة جدًا: استخراج جدول `shape → resource path → Mesh object`، وبعدها يمكن الانتقال إلى استخراج/استبدال جزء واحد بأقل مخاطرة.
