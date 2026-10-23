# المرحلة 44 — جسم Character.IKKBADFHKAL وتحليل مصفوفات الزي

## مصدر التحليل
استُخدم artifact `wrestling-empire-il2cpp-dump` من Workflow ناجح، مع `dump.cs` و`script.json` و`libil2cpp.so`. عنوان الدالة الذي طابقه `script.json` هو:
- `Character.IKKBADFHKAL(Costume)` — RVA `0x1887EC4`.

## ما يظهر في ARM64
الدالة تستقبل كائن `Character` في `x0` ومرجع `Costume` في `x1`. تفحص مصفوفة عند `Character + 0x70` وتكرّر عناصرها. عند كل عنصر تقرأ مصفوفات من كائن الزي عند الإزاحات:
- `+0x20` = `texture[]`
- `+0x40` = `flesh[]`
- `+0x48` = `shape[]`

وتنسخ قيماً من هذه المصفوفات إلى مصفوفات/كائنات مرتبطة بعناصر الشخصية، مع فحوص حدود null وطول المصفوفة. كما تستدعي `Costume.BJALLCKDACJ` عند `0x1666F90` ضمن مسار التكرار.

## الاستنتاج الدقيق
1. أصبح لدينا دليل تنفيذي على أن `Character.IKKBADFHKAL` يمر على بيانات الزي ويكتب قيم `texture/flesh/shape` إلى بنى أخرى مرتبطة بالشخصية.
2. هذا يثبت مسار تطبيق بيانات الزي وتوزيعها على عناصر الشخصية، لكنه **لا يثبت حتى الآن** أن الدالة تبدّل `SkinnedMeshRenderer.sharedMesh` أو تنشئ Mesh جديداً؛ لم يظهر في الجزء المفكك الذي فُحص إسناد مباشر واضح إلى `sharedMesh`.
3. ربط الحقول في `PKIOJFKPIBI` يظل مهماً: `+0x328` مرجع Costume، `+0x330` مصفوفة GameObjects، `+0x350` مرجع SkinnedMeshRenderer، و`+0x360/+0x378` ومصفوفات المواد مراجع عرض إضافية. نحتاج تتبع الكتابات لهذه الحقول أو الدوال التي تعمل على renderer لمعرفة تبديل المجسم الفعلي.

## المسار التالي
- تحليل `Costume.BJALLCKDACJ` عند `0x1666F90` بحدود الدالة كاملة؛ هي تتلقى `Costume` آخر، وتُستدعى من مسار تطبيق الزي.
- فحص استدعاءات `Character.IKKBADFHKAL` الأخرى وتتبّع دوال `Renderer/SkinnedMeshRenderer/Mesh/Material` في `script.json` وARM64.
- لا تزال ملفات الأصول الأصلية `datapack.unity3d`, `resources.resource`, و`assets/costumes` مطلوبة لتحديد واستخراج ملفات الموديلات الفعلية. لا يوجد بعد تعديل موديل أو APK معدل.

## حالة التقدم
- artifact الأصلي وفكّه وفحصه: مكتمل.
- تحديد سلوك `PFCOCIOEFBN` على Transform: مكتمل.
- تحديد أن `IKKBADFHKAL` ينسخ بيانات الزي إلى بنى الشخصية: مكتمل.
- إثبات تبديل Mesh فعلي: غير مكتمل.
- استخراج ملفات موديلات اللعبة: غير مكتمل.
