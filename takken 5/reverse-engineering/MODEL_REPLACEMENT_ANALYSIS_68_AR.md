# تحليل استبدال موديلات الشخصيات — المرحلة 68
التاريخ: 2026-10-23
النطاق: Wrestling Empire Android 1.8.0 فقط؛ لا يشمل مشروع X-Men.

## 1. الأصل الذي تم تحليله فعليًا
تمت قراءة الملف المرفوع `UnityDataAssetPack.apk` مباشرة، وليس الاعتماد على `asset_inventory.json` فقط.

- الحجم: 229,311,842 بايت.
- SHA-256: `7e07e31220b55f8d7660532c12a54b30fd29b0b8f172f4e1609b8f2403220155`
- يحتوي على 20 إدخالًا، ومن أهمها:
  - `assets/costumes`
  - `assets/costumes.manifest`
  - `assets/bin/Data/datapack.unity3d`
  - `assets/bin/Data/resources.resource`
  - حزم music/sound/sprites/world.

هذا يحل العائق الذي كان موثقًا في المرحلة 67: حزمة الأصول الفعلية أصبحت متاحة للتحليل المباشر.

## 2. فحص `assets/costumes.manifest`
ملف `assets/costumes.manifest` يضم 878 مسار Asset.

المسار المؤكد للموديلات هو:
`Assets/Bundles/Costumes/Models/...`

تم العثور على **88 ملف Mesh فعليًا** داخل قائمة الأصول، موزعة إلى:
- 15 Head Mesh.
- 34 Hair Mesh.
- 39 Mesh أخرى لأجزاء الجسم/الملابس والأطراف.

### Heads — 15
- Head_Chubby.mesh
- Head_Fat.mesh
- Head_Female.mesh
- Head_Gaunt.mesh
- Head_Giant.mesh
- Head_Hairy.mesh
- Head_Jaw.mesh
- Head_Narrow.mesh
- Head_Normal.mesh
- Head_Nose.mesh
- Head_Sarge.mesh
- Head_Slim.mesh
- Head_Squashed.mesh
- Head_Thug.mesh
- Head_Wide.mesh

### Hair — 34
- H_Anime01.mesh
- H_Bald2Balding.mesh
- H_Bun.mesh
- H_Curly2Afro.mesh
- H_Dreadlocks.mesh
- H_Fringe2Mop.mesh
- H_Full2Jungle.mesh
- H_Half2Half.mesh
- H_HighPony.mesh
- H_HighTop.mesh
- H_Long.mesh
- H_LongCombo.mesh
- H_LowPony.mesh
- H_Mohawk.mesh
- H_Oaf2Mao.mesh
- H_Part2Part.mesh
- H_Pigtails.mesh
- H_Pony_Classic.mesh
- H_Quiff.mesh
- H_Raised2Indent.mesh
- H_Recede2Growth.mesh
- H_Rows2Long.mesh
- H_Shaggy.mesh
- H_Shaggy_Fringe.mesh
- H_Shaggy_Fringe_X.mesh
- H_Short2Messy.mesh
- H_Side2Side.mesh
- H_Slick2Wide.mesh
- H_Spikey2Spikes.mesh
- H_Thick2Thick.mesh
- H_Thin2Bell.mesh
- H_Tupe.mesh
- H_Wedge2Guile.mesh
- H_Wolf2Heihachi.mesh

### Body/limb Mesh — 39
Body.mesh, Body_Bag.mesh, Breasts.mesh, Breasts_Baggy.mesh, Hips.mesh, Hips_Female.mesh,
L_Arm.mesh, L_ArmBag.mesh, L_Bicep.mesh, L_Foot.mesh, L_Glove.mesh, L_Hand.mesh,
L_Heel.mesh, L_Leg.mesh, L_LegBag.mesh, L_Leg_Baggy.mesh, L_Leg_Untucked.mesh,
L_Short.mesh, L_Skirt.mesh, L_Thigh.mesh, L_Thigh_Baggy.mesh, L_Toes.mesh, Neck.mesh,
R_Arm.mesh, R_ArmBag.mesh, R_Bicep.mesh, R_Foot.mesh, R_Glove.mesh, R_Hand.mesh,
R_Heel.mesh, R_Leg.mesh, R_LegBag.mesh, R_Leg_Baggy.mesh, R_Leg_Untucked.mesh,
R_Short.mesh, R_Skirt.mesh, R_Thigh.mesh, R_Thigh_Baggy.mesh, R_Toes.mesh.

## 3. تحليل UnityFS لـ `assets/costumes`
تم فك بنية UnityFS بنجاح بدل الاكتفاء بقراءة الـmanifest.

- UnityFS format: 8.
- Unity version: `6000.3.25f1`.
- Block-info compression: LZ4.
- بيانات المحتوى: كتلة LZMA واحدة.
- بعد فك الضغط تم الحصول على SerializedFile باسم:
  `CAB-4804a9fe55f251a9b5aff63c07138759`
  مع ملف موارد خارجي `.resS`.

SerializedFile:
- Format version: 22.
- File size: 2,461,364 بايت.
- Metadata size: 34,593 بايت.
- Data offset: 34,656.
- Endianness: Little Endian.
- Object count: 877.
- Type counts: 788 Texture2D + 88 Mesh + 1 AssetBundle.

هذه النتيجة مهمة جدًا لأنها تثبت أن الـ88 Mesh التي ظهرت في الـmanifest ليست مجرد أسماء نظرية؛ يوجد **88 كائن Mesh فعلي** داخل SerializedFile نفسه.

## 4. مطابقة Mesh ↔ Asset path
تم استخراج اسم `m_Name` من بداية بيانات كل كائن Mesh ومقارنته بقائمة `Models` في الـmanifest.

النتيجة: **88/88 مطابقة ناجحة، 0 مفقود، 0 اسم مكرر.**

أمثلة مؤكدة:
- `H_Part2Part` → `Assets/Bundles/Costumes/Models/Hair/H_Part2Part.mesh`
- `R_Hand` → `Assets/Bundles/Costumes/Models/R_Hand.mesh`
- `Head_Jaw` → `Assets/Bundles/Costumes/Models/Heads/Head_Jaw.mesh`
- `Head_Thug` → `Assets/Bundles/Costumes/Models/Heads/Head_Thug.mesh`
- `Body` → `Assets/Bundles/Costumes/Models/Body.mesh`

وبالتالي أصبح لدينا الآن فهرس حقيقي لأجزاء جسم الشخصية، وليس مجرد تخمين من أسماء `Resources.Load`.

## 5. الربط مع IL2CPP السابق
النتيجة الجديدة تقوي سلسلة الدليل السابقة:

`Character`
→ `Costume[]`
→ `Costume.shape[]`
→ منطق `PKIOJFKPIBI.MHEFCABLLCN` عند RVA `0x14AC0F0`
→ String construction
→ `Resources.Load`
→ `Object.Instantiate`
→ `GameObject/GetComponent`
→ `SkinnedMeshRenderer.set_sharedMesh`

والآن يوجد طرف حقيقي للسلسلة:
`Resources/Costumes` assets → 88 Mesh objects فعلية بأسماء ومسارات معروفة.

## 6. ما لم يُثبت بعد
ما زال هناك رابط واحد رئيسي يجب إثباته قبل أي استبدال:

**قيمة `Costume.shape[]` الرقمية ↔ أي واحد من الـ88 Mesh.**

لا يجوز افتراض أن `shape[0]` = أول Mesh في الـmanifest أو أن الرقم يساوي ترتيب الكائنات. ترتيب AssetBundle ليس دليلًا على ذلك.

الخطوة التالية الدقيقة هي فحص:
1. طريقة تكوين اسم المورد في `MHEFCABLLCN` على مستوى ARM64.
2. أي جدول/قائمة تربط `shape` بالأسماء.
3. كائن `AssetBundle` والـcontainer لتأكيد path → object ID.
4. أي Costume/Character بيانات داخل `datapack.unity3d` يمكن أن تكشف القيم الرقمية المرتبطة بالموديلات.

## 7. حالة الاستبدال
- اكتشاف حزمة الأصول الفعلية: **100%**.
- فهرسة Mesh الأصلية: **100%**.
- مطابقة Mesh object مع path: **100%**.
- ربط `shape[]` الرقمي مع Mesh محدد: **لم يُثبت بعد**.
- استخراج Mesh إلى صيغة خارجية قابلة للتحرير: **لم يُنفذ بعد**.
- استبدال Mesh داخل نسخة منفصلة: **0%**.
- اختبار APK معدل داخل اللعبة: **0%**.

لم يتم تعديل APK الأصلي أو الكتابة فوق أي أصل. التحليل الحالي قراءة فقط.

## 8. تحديث التقدم
هذه المرحلة ترفع أهم جزء من مسار استبدال موديلات الشخصيات من حالة "الأصول غير متاحة" إلى حالة "الأصول مفكوكة ومفهرسة ومرتبطة بكائنات Mesh فعلية".

العائق الحالي لم يعد الحصول على `UnityDataAssetPack.apk`؛ العائق الحالي هو إثبات mapping الخاص بـ`shape[]` ثم الانتقال إلى استخراج/استبدال آمن على نسخة منفصلة.
