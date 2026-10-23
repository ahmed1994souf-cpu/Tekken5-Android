# تدقيق الملفات المتاحة — متابعة تتبع موديلات Wrestling Empire

التاريخ: 2026-10-23

## نتيجة فحص الملفات المحفوظة في المكتبة

تم العثور على ملف `assets.zip` محفوظ في مكتبة المحادثات (10,650,098 بايت)، وملف `global-metadata(2).dat` (4,572,724 بايت). تم فتح ZIP وفحص أسماء محتوياته فعليًا، وليس الاعتماد على اسمه فقط.

### ما يحتويه assets.zip

- عدد عناصر ZIP: 68.
- يحتوي على `assets/bin/Data/data.unity3d` بحجم 1,095,858 بايت، وترويسة الملف تشير إلى Unity `6000.3.25f1`.
- يحتوي على `assets/bin/Data/Managed/Metadata/global-metadata.dat` بحجم 7,429,976 بايت.
- لا يحتوي على `datapack.unity3d`.
- لا يحتوي على مسارات `assets/costumes` أو `resources.resource` المعروفة في جرد حزمة أصول اللعبة.

### بصمات SHA-256

- `assets.zip`: `2c44a9d3efd8a0b1f2f23367f49ceb6b3ea09a226a9cc29a0b3685536212ecc6`
- `global-metadata(2).dat`: `ead68deeaf6a7652243dd87a90d0d74d21b1e2e47566d2908917321b7518e6e5`
- `assets/bin/Data/Managed/Metadata/global-metadata.dat` داخل ZIP: `22ff7f1421a3128efeda7eeccbd985a92346dcd9b12e05bf29ef7e24221883e8`

## الاستنتاج المؤكد وحدوده

الملف `assets.zip` ليس حزمة أصول كاملة وفق المسارات المطلوبة لتتبع موديلات المصارعين؛ فملفات `datapack.unity3d` و`resources.resource` ومجلد `costumes` غير موجودة داخله. كما أن ملفي metadata يختلفان في الحجم والبصمة، لذلك لا يجوز اعتبارهما الملف نفسه أو دمج نتائجهما دون التحقق من مصدر كل واحد.

هذا الفحص لا يثبت أن `assets.zip` ليس من اللعبة؛ فهو يتضمن بيانات Unity متوافقة مع إصدار Unity المذكور في الجرد. لكنه يثبت أن الحزمة المتاحة وحدها لا تكفي لتحديد ملفات الموديلات الفعلية.

## الخطوة التالية

نحتاج إلى ملف `UnityDataAssetPack.apk` من XAPK الأصلي، أو على الأقل استخراج هذه العناصر منه:

1. `assets/bin/Data/datapack.unity3d`
2. `assets/bin/Data/resources.resource`
3. مجلد `assets/costumes` إن كان موجودًا داخل الحزمة.

بعد الحصول عليها، تُفهرس الملفات وتُفحص أنواع الأصول، ثم نربط الأصول بمراجع `SkinnedMeshRenderer` و`sharedMesh` و`sharedMaterials` التي حددها تحليل IL2CPP السابق. لم يتم استخراج نموذج مصارع أو استبداله بعد، ولن ندّعي ذلك قبل وجود دليل فعلي.
