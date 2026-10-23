# المرحلة 75 — اكتشاف نقطة ربط Costume مع كائن الشخصية runtime

التاريخ: 2026-10-23
النطاق: Wrestling Empire Android 1.8.0 فقط.

## النتيجة الجديدة

تم استرجاع Artifact حقيقي من GitHub Actions:
- Workflow run: `39660693165`
- Artifact: `wrestling-empire-il2cpp-dump`
- الحجم المضغوط: `12,711,896` بايت
- الـArtifact غير منتهي الصلاحية وقت الفحص.
- تم فحص `output/dump.cs` فعليًا، وحجمه `19,237,153` بايت داخل الـArtifact.

هذه المرة لا نعتمد على تقرير Markdown فقط؛ تم فتح التفريغ نفسه والبحث داخله.

## 1. تعريف Costume المؤكد

`Costume` هو `TypeDefIndex: 53`، وحقوله هي:

- `id` عند `0x10`
- `charID` عند `0x14`
- `limb` عند `0x18`
- `texture[]` عند `0x20`
- `r[]` عند `0x28`
- `g[]` عند `0x30`
- `b[]` عند `0x38`
- `flesh[]` عند `0x40`
- `shape[]` عند `0x48`

ومن الدوال المؤكدة في التفريغ:

- `PFCOCIOEFBN` — RVA `0x1663F6C`
- `MFBNABEJFIE` — RVA `0x1665040`
- `CHCBMJCHBOF` — RVA `0x166529C`
- `JGEEDIAOKBM` — RVA `0x1665AF4`
- `JBECIKIBKIP` — RVA `0x16662E0`
- `BJALLCKDACJ` — RVA `0x1666F90` ويستقبل `Costume` آخر
- `ECNCADEADNG` — RVA `0x16673A4`
- `JENEJOJNOOP` — RVA `0x1667FF8`
- `AJAFNCJDPCD` — RVA `0x1668160`

مهم: وجود `shape[]`, `texture[]`, `flesh[]` مثبت من التفريغ، لكن معنى كل عنصر من عناصر المصفوفات لم يُثبت بعد من الجسم الثنائي للدوال.

## 2. الاكتشاف الأهم: Costume لا يعمل منفردًا

دوال `Costume` لا تستقبل أرقامًا فقط؛ عدة دوال رئيسية تستقبل كائنًا من النوع:

`PKIOJFKPIBI`

ومن أمثلتها:

- `PFCOCIOEFBN(PKIOJFKPIBI, int)`
- `MFBNABEJFIE(PKIOJFKPIBI, int)`
- `CHCBMJCHBOF(PKIOJFKPIBI, int, int, int, int)`
- `JBECIKIBKIP(PKIOJFKPIBI, int, int, int, int)`
- `ECNCADEADNG(PKIOJFKPIBI, int, int, int, int)`

هذا يحدد لنا نقطة الربط التالية للتحليل: `Costume -> PKIOJFKPIBI`.

## 3. لماذا PKIOJFKPIBI مهم جدًا لاستبدال الموديل

`PKIOJFKPIBI` هو `TypeDefIndex: 12`، ويحتوي على مراجع Unity runtime مباشرة، منها:

- `GameObject MOMHHCLCACH` عند `0x108`
- `Outline3D OODJMCMJECA` عند `0x118`
- `Animator MPIHDGHEAEM` عند `0x168`
- كما يحتوي على `Character LECDFJKPAPB` عند `0x20`

ويحتوي أيضًا على بيانات/مصفوفات كثيرة مرتبطة بحالة الكائن والحركة.

هذه نقطة مهمة جدًا: لدينا الآن مسار بنيوي موثق:

`Character.costume[] (0x70)`
→ `Costume`
→ دوال Costume
→ `PKIOJFKPIBI`
→ `GameObject + Animator`

لذلك `PKIOJFKPIBI` هو المرشح الأقوى حاليًا ليكون كائن الشخصية الذي تُطبّق عليه بيانات الزي أثناء التشغيل.

## 4. ما الذي لم نثبته بعد

لا يزال هناك فرق مهم بين "نقطة ربط الموديل" وبين "Mesh محدد".

لم يثبت التفريغ وحده أن:

- `MOMHHCLCACH` هو جذر الموديل النهائي.
- أو أن Mesh معين يُحمل من `shape[]` مباشرة.
- أو أن رقمًا في `shape[]` يساوي Mesh ID محددًا مثل `Head_Normal` أو `Head_Fat`.
- أو أن `texture[]` يشير مباشرة إلى Texture2D محددة.

إثبات هذه النقاط يتطلب جسم دوال `Costume` من `libil2cpp.so` المطابق لنفس التفريغ، وليس `dump.cs` فقط.

## 5. مسار التحليل القادم

الأولوية أصبحت محددة وليست بحثًا عامًا:

1. تحليل جسم `Costume::PFCOCIOEFBN` عند RVA `0x1663F6C`.
2. تحليل `Costume::MFBNABEJFIE` عند `0x1665040`.
3. تحليل `Costume::CHCBMJCHBOF` عند `0x166529C`.
4. تحليل `Costume::JBECIKIBKIP` عند `0x16662E0`.
5. تحليل `Costume::ECNCADEADNG` عند `0x16673A4`.
6. مقارنة هذه الدوال مع `PKIOJFKPIBI::BFDFOCBGFBP` عند `0x187D218`.
7. تتبع أي وصول إلى حقول `shape/texture/flesh` ثم أي استدعاء Unity متعلق بـ `GameObject`, `Animator`, `Renderer`, `SkinnedMeshRenderer`, `Mesh` أو `Material`.

## الخلاصة

المرحلة 75 رفعت مستوى اليقين في مسار استبدال الشخصيات بشكل واضح:

- **Character → Costume** مثبت.
- **Costume → PKIOJFKPIBI** مثبت من تواقيع الدوال.
- **PKIOJFKPIBI → GameObject + Animator** مثبت من تعريف الصنف.
- **Costume → Mesh محدد** غير مثبت بعد.
- **shape[index] → اسم Mesh محدد** غير مثبت بعد.

إذن الهدف التالي ليس إعادة جرد الشخصيات؛ الهدف هو تحليل أجسام دوال Costume الخمس وربطها بكائن `PKIOJFKPIBI`.

لم يتم تعديل APK الأصلي أو استبدال أي Mesh فعلي في هذه المرحلة، ولم يتم خلط هذا المشروع مع مشروع X-Men.
