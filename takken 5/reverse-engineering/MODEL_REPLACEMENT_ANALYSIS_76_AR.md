# المرحلة 76 — تحليل مباشر لـ libil2cpp.so وتحديد مسار shape/texture

التاريخ: 2026-10-23
النطاق: Wrestling Empire Android 1.8.0 فقط.

## 1. مصدر ثنائي أقوى

تم استرجاع Artifact أحدث من GitHub Actions:
- Workflow: `39755570787`
- Artifact: `wrestling-empire-il2cpp-dump`
- Artifact ID: `12415643344`
- الحجم: `28,794,529` بايت
- SHA-256 المسجل لدى GitHub: `7b4edbfa84b4a3c6ae9fd5a0a4a77d1edd846166cf90eb3484c0cd5fa5d391a6`
- يحتوي فعليًا على `libil2cpp.so` بحجم يقارب 53 MB، بالإضافة إلى `dump.cs` و`script.json` وملفات native-disassembly.

تم فك المكتبة وإعادة تفكيك التعليمات مباشرة بواسطة `llvm-objdump`، وليس الاعتماد على التقرير النصي فقط.

## 2. تحليل Character.IKKBADFHKAL

الدالة:
`Character.IKKBADFHKAL(Costume)` — RVA `0x1887EC4`.

حدها الصحيح ينتهي قبل الدالة التالية عند `0x18882BC`.

من جسم ARM64:

- `x0` هو `Character`.
- `x1` هو `Costume` الممرر.
- عند `Character + 0x70` يتم الوصول إلى مصفوفة `Costume[]`.
- الدالة تكرر عناصر هذه المصفوفة وتتعامل مع بيانات الزي.
- في مسار واضح عند `0x1888170` تستدعي `Costume.BJALLCKDACJ` عند `0x1666F90`.

الأهم: هذا الجسم لا يستدعي مباشرةً `SkinnedMeshRenderer.set_sharedMesh` أو `MeshFilter.set_sharedMesh` في الجزء الذي فُحص.

## 3. تحليل Costume.BJALLCKDACJ

الدالة:
`Costume.BJALLCKDACJ(Costume, int)` — RVA `0x1666F90`.

الفحص المباشر يبين أنها تتعامل مع بيانات `Costume` وتستدعي:
`Costume.JGEEDIAOKBM` — RVA `0x1665AF4`.

وتظهر عمليات واضحة على حقول `Costume` نفسها، بما فيها تحديث `limb`/الفهارس أثناء مسار النسخ/المقارنة.

لا يظهر في هذا النطاق استدعاء مباشر إلى `SkinnedMeshRenderer.set_sharedMesh`.

## 4. نتيجة مهمة جدًا من PKIOJFKPIBI

التعريف الفعلي لـ `PKIOJFKPIBI` يحتوي على:

- `GameObject MOMHHCLCACH` عند `0x108`
- `Animator MPIHDGHEAEM` عند `0x168`
- `Costume JKPCKFFIKPJ` عند `0x328`
- `GameObject[] ELAGIOKEBEG` عند `0x330`
- `SkinnedMeshRenderer MLHKNLAKIGM` عند `0x350`
- `Material PKMCFNFFGMN` عند `0x360`
- `Material NCDMIAHNNFA` عند `0x378`
- `Material[] HBEONABGCCL` عند `0x388`
- `Material[] GPKNBNJEJJA` عند `0x390`
- `Material[] COBOBGNNEHE` عند `0x3C0`

وهذا يقوي المسار السابق بشكل كبير: كائن `PKIOJFKPIBI` ليس مجرد حامل بيانات؛ لديه مراجع صريحة لمكونات العرض الرسومية للشخصية، بما فيها `SkinnedMeshRenderer` ومواد متعددة.

## 5. فحص استدعاءات Mesh المباشرة

في `script.json` تم تأكيد وجود واجهات Unity التالية:

- `UnityEngine.SkinnedMeshRenderer.get_sharedMesh`
- `UnityEngine.SkinnedMeshRenderer.set_sharedMesh`
- `UnityEngine.MeshFilter.get_sharedMesh`
- `UnityEngine.MeshFilter.set_sharedMesh`
- `UnityEngine.MeshFilter.set_mesh`

ثم فُحصت أجسام الدوال التالية مباشرة في `libil2cpp.so`:

- `Costume.PFCOCIOEFBN` — `0x1663F6C`
- `Costume.MFBNABEJFIE` — `0x1665040`
- `Costume.CHCBMJCHBOF` — `0x166529C`
- `Costume.JBECIKIBKIP` — `0x16662E0`
- `Costume.ECNCADEADNG` — `0x16673A4`
- `Character.IKKBADFHKAL` — `0x1887EC4`

لم يظهر استدعاء مباشر إلى setters الخاصة بـ `sharedMesh` داخل هذه النطاقات.

كما لم يظهر في هذه النطاقات استدعاء مباشر واضح إلى `Material.set_color` أو `Material.set_shader`.

## 6. ماذا يعني هذا؟

هذا لا يعني أن اللعبة لا تغير Mesh.

بل يحدد أن عملية الربط قد تكون في طبقة أخرى، مثل:

1. دالة أخرى تُستدعى بعد تجهيز `Costume`.
2. دالة تعمل على `PKIOJFKPIBI.MLHKNLAKIGM` (`SkinnedMeshRenderer`).
3. دالة تبحث عن Mesh/Material من جدول أو AssetBundle ثم تمرره إلى renderer عبر مسار غير مباشر.
4. استخدام دوال wrapper/metadata أو استدعاء غير مباشر بدل BL مباشر إلى setter.

لذلك البحث التالي أصبح أكثر تحديدًا: **العثور على جميع المراجع إلى حقل `PKIOJFKPIBI + 0x350` ثم تتبع الدوال التي تستخدم الـSkinnedMeshRenderer.**

## 7. استنتاج جديد حول shape[]

لدينا الآن دليل تنفيذي متصل:

`Character +0x70 (Costume[])`
→ `Costume.texture[] / flesh[] / shape[]`
→ `Character.IKKBADFHKAL`
→ `Costume.BJALLCKDACJ`
→ بيانات Costume/عناصر الشخصية

لكن `shape[index]` لا يزال غير مربوط باسم Mesh فعلي مثل `Head_Normal` أو `Head_Fat`.

لا يجوز اعتبار ذلك مثبتًا قبل العثور على نقطة قراءة `shape[]` التي تؤدي إلى اختيار Mesh أو إلى جدول Mesh IDs.

## 8. الخطوة التالية

الأولوية الآن:

1. البحث في `libil2cpp.so` عن كل دالة تقرأ `PKIOJFKPIBI + 0x350`.
2. تتبع كل استدعاء مرتبط بـ `SkinnedMeshRenderer`.
3. البحث عن جداول Mesh/Material التي تستخدم قيم `shape[]` أو `texture[]`.
4. بعد تحديد مسار Mesh، الرجوع إلى `assets/costumes` لمحاولة ربط ID بملف Asset فعلي.

## الحالة

- IL2CPP dump: مثبت.
- `libil2cpp.so` مطابق للـartifact: متاح وفُحص مباشرة.
- Costume → Character: مثبت تنفيذيًا.
- Character → SkinnedMeshRenderer: مثبت بنيويًا عبر الحقل `+0x350`.
- `shape[]` → Mesh ID: غير مثبت بعد.
- Mesh ID → ملف Asset: غير مثبت بعد.
- استبدال Mesh فعلي داخل APK: لم يحدث بعد.

هذه المرحلة رفعت نقطة البحث من مستوى "Costume عام" إلى مستوى **SkinnedMeshRenderer الخاص بكائن الشخصية**.
