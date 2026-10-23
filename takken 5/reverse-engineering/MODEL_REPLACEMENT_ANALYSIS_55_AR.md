# تتبّع تركيب مجسم الشخصية — المرحلة 55

التاريخ: 2026-10-23
النطاق: Wrestling Empire Android 1.8.0 فقط.
المصدر: تم تنزيل وفحص Artifact GitHub Actions رقم 39939889590 باسم `wrestling-empire-il2cpp-dump` (Artifact ID 12495029758، SHA-256 المعلن من GitHub: `b7d8b9dd6b00097d6cd832b33d02ce58e100c955d5db80de86ce90075d5044b3`). فُحص `libil2cpp.so` و`output/script.json` مباشرة، ثم أُعيد تفكيك حدود الدوال باستخدام عناوين ScriptMethod.

## اكتشاف رئيسي جديد: نقطة تركيب المجسم

الدالة `PKIOJFKPIBI.MHEFCABLLCN` عند RVA `0x14AC0F0` هي أقوى نقطة وجدناها حتى الآن لمسار بناء مجسم الشخصية.

تطابق عنوانها وتوقيعها من `script.json`:
- `void PKIOJFKPIBI__MHEFCABLLCN(PKIOJFKPIBI_o* __this, const MethodInfo* method)`

عند تفكيك جسم الدالة كاملًا حتى بداية الدالة التالية، ظهرت الاستدعاءات التالية:
- `UnityEngine.SkinnedMeshRenderer.set_sharedMesh`: **24 استدعاءً مباشرًا**.
- `UnityEngine.GameObject.GetComponent<object>`: 72 استدعاءً.
- `UnityEngine.Transform.Find`: 14 استدعاءً.
- `UnityEngine.GameObject.get_transform`: 21 استدعاءً.
- `UnityEngine.Renderer.set_enabled`: 7 استدعاءات.
- `UnityEngine.MeshFilter.set_mesh`: استدعاءان.
- `UnityEngine.Resources.Load`: استدعاء واحد.
- `UnityEngine.Object.Instantiate<object>`: استدعاء واحد.
- `UnityEngine.Object.Destroy`: استدعاء واحد.
- استدعاءات أخرى لتسمية كائنات أو تسجيل رسائل.

**الاستنتاج المؤكد:** هذه الدالة لا تقتصر على نسخ بيانات الزي أو تعديل المقاييس؛ إنها تتعامل مباشرة مع مكونات الرسم الهيكلي وتعيّن لها Mesh، كما تبحث عن مكونات وكائنات فرعية وتحمّل/تنشئ موردًا. لذلك أصبحت نقطة البدء الأساسية لتتبع كيفية بناء جسم المصارع.

**ما لا نعرفه بعد:** لم نربط بعد كل استدعاء من استدعاءات `set_sharedMesh` بأصل بعينه، ولم نثبت أن أي Mesh يمكن استبداله خارجيًا دون قيود الهيكل والعظام.

## اكتشاف داعم: دوال Costume تعدّل هيئة الأجزاء

فُككت حدود الدوال اعتمادًا على ترتيب العناوين في `script.json`، بدل الاكتفاء بنوافذ قصيرة ثابتة:

### `Costume.PFCOCIOEFBN` — RVA `0x1663F6C`
وجدت استدعاءات متكررة إلى:
- `GameObject.get_transform`: 35
- `Transform.set_localScale`: 14
- `Transform.set_localPosition`: 11
- `Transform.set_localEulerAngles`: 1
- `Transform.get_localScale`: 5

هذا يثبت أن الدالة تضبط مقياس/موضع/دوران كائنات أجزاء الشخصية. لا يثبت هذا وحده أنها تحمل Mesh جديدًا.

### `Costume.MFBNABEJFIE` — RVA `0x1665040`
تظهر عمليات قراءة وتعديل `Transform.localScale`، ما يدعم أنها جزء من مسار ضبط هيئة/مقياس الأجزاء.

### `Costume.JBECIKIBKIP` — RVA `0x16662E0`
تستدعي `Character.IKKBADFHKAL` عند `0x1887EC4`، كما تستدعي `Costume.PFCOCIOEFBN` مرتين. هذا يربط مسار معالجة بيانات الزي بمسار تهيئة الشخصية، لكنه لا يكفي وحده لتحديد جميع الأدوار.

### `Costume.ECNCADEADNG` — RVA `0x16673A4`
تستدعي أيضًا `Character.IKKBADFHKAL` وطرقًا أخرى من `Costume`. يلزم تحديد سياقها الدقيق قبل وصفها بأنها نقطة الاستبدال.

## دليل إضافي من المراجع المباشرة

في `script.json` توجد واجهات Unity التالية:
- `UnityEngine.SkinnedMeshRenderer.set_sharedMesh` عند `0x2DEAF04`.
- `UnityEngine.MeshFilter.set_sharedMesh` عند `0x2DEAC3C`.
- `UnityEngine.AssetBundle.LoadAsset` عند `0x2DCF1EC` وواجهات ذات صلة.
- `UnityEngine.Resources.Load` عند `0x2E04A60`.

فحص تعليمات الاستدعاء داخل المكتبة وجد 24 استدعاءً مباشرًا لـ `SkinnedMeshRenderer.set_sharedMesh` من داخل `PKIOJFKPIBI.MHEFCABLLCN`. أما استدعاءات `MeshFilter.set_sharedMesh` التي ظهرت في هذا الفحص فكانت ضمن دوال TextMeshPro، ولا تُعد دليلًا على مجسم المصارع.

## أين نركز الآن؟

1. تحليل الفروع الـ24 داخل `MHEFCABLLCN` لمعرفة أي مكوّن/فهرس/قيمة `shape[]` يقود إلى كل تعيين Mesh.
2. فحص سلسلة `Resources.Load` و`Instantiate` داخل الدالة، وتحديد النص أو المفتاح الذي يصل إلى التحميل، دون افتراض اسم أصل غير مثبت.
3. تتبع من يستدعي `MHEFCABLLCN` وربطه بمسار اختيار المصارع أو تطبيق الزي.
4. متابعة فهرسة الأصول: تقرير تدقيق الملفات يثبت أن `assets.zip` المتاح لا يحتوي `datapack.unity3d` أو `resources.resource` أو مجلد `assets/costumes`؛ لذلك لا يمكن حتى الآن تسمية ملف Mesh أصلي محدد.
5. بعد تحديد أصل Mesh وآلية تحميله، إعداد تجربة مستقلة قابلة للتراجع لشخصية واحدة فقط.

## حالة التقدم التقريبية

- بنية بيانات Costume/Character: **80%**.
- فهم عمليات تهيئة أجزاء الزي: **65%**.
- تحديد دالة تركيب/تعيين Mesh: **70%** (تقدّم بحثي، بعد العثور على دالة تعيّن sharedMesh مباشرة).
- ربط Mesh محدد بـ shape/أصل فعلي: **25%**.
- استخراج نموذج بديل واختباره داخل اللعبة: **0%**.

هذه نسب تقديرية لمراحل البحث وليست ضمانًا للجاهزية. لم يتم تعديل اللعبة أو استخراج نموذج بديل أو بناء APK معدل في هذه المرحلة.
