# المرحلة 46 — فحص Artifact التفريغ ومؤشرات تصنيف أصول الشخصيات

التاريخ: 2026-10-23  
النطاق: Wrestling Empire Android 1.8.0 فقط  
المصدر المباشر: Artifact GitHub Actions باسم `wrestling-empire-il2cpp-dump`، المعرّف `12374366190`، الناتج من التشغيل `39660693165`.

## 1. فحص محتويات Artifact فعليًا

تم تنزيل ملف ZIP وفحص قائمة الملفات داخله. يتضمن:
- `output/dump.cs` — تعريفات الأصناف والحقول والتواقيع (حوالي 19.2 MB).
- `output/il2cpp.h` — تعريفات IL2CPP (حوالي 51.2 MB).
- `output/script.json` — بيانات التفريغ (حوالي 54.5 MB).
- `output/stringliteral.json` — جدول النصوص الثابتة (حوالي 1.8 MB).
- `dumper.log` وملخص التفريغ.

**حد مهم:** لا يحتوي هذا الـ Artifact على `libil2cpp.so` ولا `UnityDataAssetPack.apk` ولا `datapack.unity3d` ولا `resources.resource`. لذلك لا يمكن استخدامه وحده لتفكيك تعليمات ARM64 أو استخراج Mesh.

## 2. تحقق مباشر من تعريفات الشخصية

من `output/dump.cs`:
- `Costume` هو `TypeDefIndex 53`، ويحوي `texture[]`, `r[]`, `g[]`, `b[]`, `flesh[]`, `shape[]`.
- `PKIOJFKPIBI` هو `TypeDefIndex 12`، ويربط `Costume` عند `0x328` بمصفوفة `GameObject[]` عند `0x330`، و`GameObject` عند `0x340`، و`SkinnedMeshRenderer` عند `0x350`، ومراجع `Material` ومصفوفاتها عند `0x360`, `0x378`, `0x388`, `0x390`, `0x3C0`.
- `Character` هو `TypeDefIndex 116`، ويحوي `Costume[] costume` عند `0x70` و`costumeChange` عند `0x80`.

هذه تعريفات بيانات موثقة من التفريغ؛ لا تكشف وحدها تنفيذ تركيب المجسم.

## 3. مؤشر جديد من جدول النصوص الثابتة

وجدت في `output/stringliteral.json` نصوص تصنيف حرفية تتضمن:
- `Costumes/Models`
- `Costumes/Models/Heads`
- `Costumes/Models/Hair`
- `Costumes/Bodies`
- `Costumes/Faces`
- `Costumes/Faces/Beards`
- `Costumes/Faces/Expressions`
- `Costumes/Faces/Masks`
- `Costumes/Arms`, `Costumes/Hands`, `Costumes/Legs`, `Costumes/Necks`, `Costumes/Scars`

هذا مؤشر مفيد إلى تقسيم تصنيفات الأزياء/النماذج في منطق اللعبة أو واجهتها. **ليس دليلًا كافيًا على أن هذه مسارات ملفات فعلية داخل AssetPack**، ولا يحدد أسماء ملفات Mesh. يلزم ربط النصوص بعناوين القراءة/الاستخدام في تعليمات ARM64 ثم فحص الأصول الفعلية.

## 4. الخطوة الفنية التالية

1. توفير `UnityDataAssetPack.apk` أو استخراج `datapack.unity3d` و`resources.resource` ومحتويات `assets/costumes` من نسخة اللعبة نفسها.
2. الحصول على `libil2cpp.so` المطابق للإصدار 1.8.0 وإعادة تفكيك الدوال المرشحة؛ Artifact التفريغ الحالي لا يتضمن المكتبة.
3. تتبع الدوال `Costume.PFCOCIOEFBN`, `MFBNABEJFIE`, `CHCBMJCHBOF`, `JBECIKIBKIP`, `ECNCADEADNG` وصولًا إلى أي استدعاءات أو كتابات تخص `SkinnedMeshRenderer.sharedMesh` أو إنشاء/تفعيل أجزاء `GameObject`.
4. إعداد فهرس أصول حقيقي يضم اسم الأصل ونوعه وحجمه ومعرّفه، ثم مطابقة الأجزاء مع بيانات Costume فقط عند وجود دليل.
5. لا تُجرى أي كتابة داخل APK الأصلي؛ أي تجربة مستقبلية تكون على نسخة اختبار مستقلة.

## الحالة بعد المرحلة 46

- [x] تنزيل Artifact التفريغ وفحص قائمة محتوياته.
- [x] إعادة التحقق من تعريفات Costume/Character/كائن العرض من `dump.cs`.
- [x] استخراج تصنيفات Models/Heads/Hair وغيرها من جدول النصوص.
- [ ] لا تزال ملفات أصول Mesh الأصلية غير متاحة داخل Artifact.
- [ ] لم يتم إثبات الدالة التي تبدل Mesh.
- [ ] لم يتم استخراج أو استبدال أي موديل.
- [ ] لم يتم إنشاء APK معدل أو اختباره.

الخلاصة: هذه المرحلة أضافت مؤشرًا جديدًا لتصنيفات نماذج/أزياء الشخصية، وحددت بدقة ما ينقص Artifact الحالي. عنق الزجاجة لا يزال الوصول إلى AssetPack والمكتبة الأصلية المطابقة، وليس مجرد وجود تعريفات Costume.
