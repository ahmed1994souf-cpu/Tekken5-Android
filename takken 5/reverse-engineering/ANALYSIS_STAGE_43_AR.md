# المرحلة 43 — تحليل فعلي من ARM64 لدوال Costume

## ما تم إنجازه في هذه المرحلة
تم العثور على artifact ناجح من GitHub Actions الخاص بتفريغ IL2CPP، ثم تنزيله وفحصه محليًا بدل الاعتماد على أسماء الدوال في `dump.cs` وحدها.

- Workflow: [Dump Wrestling Empire IL2CPP](https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39755570787)
- Artifact: `wrestling-empire-il2cpp-dump`، ID `12415643344`، حجمه 28,794,529 بايت، صالح حتى 2026-11-05 بحسب بيانات GitHub.
- ملفات تحققنا من وجودها داخل الأرشيف: `output/dump.cs`, `output/script.json`, `output/il2cpp.h`, `libil2cpp.so`, وملفات `native-disassembly`.
- `dump_summary.json` يسجل 62,358 طريقة ذات RVA في dump.cs. هذه نتيجة تفريغ ناجح، وليست دليلًا على استخراج ملفات الموديلات نفسها.

## دليل مهم: ما الذي تفعله دوال Costume؟

### 1) `Costume.PFCOCIOEFBN` — RVA `0x1663F6C`
فككنا تعليمات ARM64 من المكتبة الأصلية عند RVA هذا. الدالة تقرأ مصفوفة `GameObject[]` من كائن الشخصية `PKIOJFKPIBI` عند الإزاحة `0x330`، وتكرر عمليات على عناصرها. جدول العناوين في `script.json` يطابق الاستدعاءات التالية بدقة:
- `0x2E0AB80` = `UnityEngine.GameObject.get_transform`
- `0x2E16BD8` = `UnityEngine.Transform.set_localScale`
- `0x2E16544` = `UnityEngine.Transform.set_localPosition`

**الاستنتاج المؤكد:** هذه الدالة تعدّل مقياس/موضع Transform لعناصر GameObject المرتبطة بالشخصية. وهذا دليل على مسار تغيير هيئة/أجزاء الشخصية، لكنه ليس وحده دليلًا على استبدال `Mesh` أو `SkinnedMeshRenderer.sharedMesh`.

### 2) `Costume.JBECIKIBKIP` — RVA `0x16662E0`
تفكيك ARM64 يظهر استدعاءً إلى `Costume.PFCOCIOEFBN` عند `0x1666938` و`0x1666948`. كما يظهر تمرير مرجع `Costume` المخزن في كائن الشخصية عند الإزاحة `0x328` إلى:
- `Character.IKKBADFHKAL(Costume)` — RVA `0x1887EC4`

**الاستنتاج المؤكد:** هذه الدالة تمرر الزي إلى مسار داخل `Character` وتستدعي كذلك منطق تعديل Transform؛ إذن لا يصح اختزال نظام الزي إلى ألوان فقط. ما زلنا بحاجة لفحص جسم `Character.IKKBADFHKAL` لمعرفة هل يغيّر المراجع الرسومية أو المواد أو المكونات.

### 3) بنية البيانات التي تؤيد المسار
من `dump.cs`:
- `Costume` (TypeDefIndex 53): `id`, `charID`, `limb`, `texture[]`, قنوات `r/g/b`, `flesh[]`, `shape[]`.
- `PKIOJFKPIBI`: `Character` عند `0x20`، ومصفوفة GameObjects عند `0x330`، ومرجع Costume عند `0x328`، و`SkinnedMeshRenderer` عند `0x350`، ومواد عند `0x360`, `0x378`, ومصفوفات مواد عند `0x388`, `0x390`, `0x3C0`.
- `Character.IKKBADFHKAL(Costume)` موجود في dump.cs وscript.json عند RVA `0x1887EC4`.

هذه الحقول تثبت أن كائن الشخصية يحتفظ بمراجع لمكونات عرض وموديل ومواد، لكنها لا تكشف بمفردها أي Mesh أو ملف أصل يخص كل شخصية.

## الخطوة التالية المحددة
1. فك تعليمات ARM64 لدالة `Character.IKKBADFHKAL` عند `0x1887EC4` وربط الإزاحات التي تقرأها/تكتبها بحقول `Character` و`PKIOJFKPIBI`.
2. تتبع استدعاءات تغيير `sharedMesh` أو `SkinnedMeshRenderer` أو `MeshFilter`، إن ظهرت، وعدم افتراضها قبل رؤيتها.
3. متابعة دوال `Costume.MFBNABEJFIE` و`CHCBMJCHBOF` و`ECNCADEADNG` لمعرفة الفروق بين إعداد الزي، أجزاء الجسم، والقياسات.
4. بالتوازي، لا تزال ملفات الأصول اللازمة لتحديد ملفات الموديلات الفعلية مفقودة من الأرشيف السابق: `datapack.unity3d` و`resources.resource` و`assets/costumes`. لذلك لا يمكن بعد تسمية ملف موديل بعينه أو تسليم موديل بديل صالح للعبة.

## الحالة
- تنزيل artifact وفتح `dump.cs` و`script.json` و`libil2cpp.so`: **تم**.
- إثبات أن دالة Costume تغيّر Transform لمجموعة GameObjects: **تم**.
- إثبات استدعاء مسار Character مع مرجع Costume من دالة أخرى: **تم**.
- تحديد دالة تعيّن Mesh بديلًا أو استخراج ملفات موديل أصلية: **لم يكتمل بعد**.
- تعديل أصول اللعبة أو بناء نسخة معدلة: **لم يحدث**.
