# المرحلة 36 — مسار موديلات الشخصيات واستبدالها (Wrestling Empire Android)

التاريخ: 2026-10-22  
المصدر: artifact الفعلي `wrestling-empire-il2cpp-dump` من تشغيل GitHub Actions رقم `39677914247`، بعد تنزيل ZIP وفحص `output/dump.cs` محليًا.

## الهدف

الأولوية هي استبدال الموديل ثلاثي الأبعاد للمصارع، لا الاكتفاء بتغيير الاسم أو الألوان أو الخامات. هذه المرحلة ترسم مسار التحقيق من كود IL2CPP إلى الأصول؛ ولا تدعي أن ملفات Mesh قد استُخرجت بعد.

## 1. أدلة مؤكدة من dump.cs

### `PKIOJFKPIBI` — TypeDefIndex 12

الحقول ذات الصلة:

| الحقل | النوع | الإزاحة |
|---|---|---:|
| `LECDFJKPAPB` | `Character` | `0x20` |
| `JKPCKFFIKPJ` | `Costume` | `0x328` |
| `JDCACLAIOKP` | `GameObject` | `0x340` |
| `MLHKNLAKIGM` | `SkinnedMeshRenderer` | `0x350` |

هذا يثبت أن كائنًا من هذا الصنف يحمل مرجع بيانات المصارع ومرجع الزي ومراجع مرتبطة بكائن Unity ومكوّن رسم هيكلي. لا يكفي وحده لإثبات أن هذا الصنف ينشئ الموديل أو أن `MLHKNLAKIGM` هو كل جسم المصارع؛ يجب تتبع عمليات الكتابة والاستدعاءات.

### `Costume` — TypeDefIndex 53

الحقول:

- `id`, `charID`, `limb`
- `texture[]`
- `r[]`, `g[]`, `b[]`
- `flesh[]`, `shape[]`

توجد دوال تستقبل `PKIOJFKPIBI`، ومنها:

- `PFCOCIOEFBN(PKIOJFKPIBI, int)` — RVA `0x1663F6C`
- `MFBNABEJFIE(PKIOJFKPIBI, int)` — RVA `0x1665040`
- `CHCBMJCHBOF(PKIOJFKPIBI, int, int, int, int)` — RVA `0x166529C`
- `JBECIKIBKIP(PKIOJFKPIBI, int, int, int, int)` — RVA `0x16662E0`
- `ECNCADEADNG(PKIOJFKPIBI, int, int, int, int)` — RVA `0x16673A4`

هذه أهداف مناسبة للتفكيك لأنها تربط بيانات الزي بكائن المصارع، لكن أسماءها المموهة وتواقيعها لا تكشف وحدها أيها يبدل أجزاء الجسم أو الخامات.

### أصناف أخرى تحمل SkinnedMeshRenderer

ظهر في التفريغ أيضًا:

- `BJPINJCPNOK` — TypeDefIndex 6، الحقل `KCGOOEDNDBC` عند `0xC0`.
- `FDBECCMMFDP` — TypeDefIndex 9، الحقل `KCGOOEDNDBC` عند `0x140`.
- `PKIOJFKPIBI` — TypeDefIndex 12، الحقل `MLHKNLAKIGM` عند `0x350`.

لذلك ينبغي مقارنة هذه الأصناف قبل الجزم بأن `PKIOJFKPIBI` هو نقطة تركيب الموديل الوحيدة.

## 2. ما لا يثبته التفريغ الحالي

- لا يحتوي هذا artifact على ملفات موديلات مصدّرة بصيغ مثل FBX أو OBJ.
- حقول `Costume.texture/shape/flesh` لا تثبت أن اللعبة تسمح باستبدال Mesh كامل من خلالها.
- `SkinnedMeshRenderer` يؤكد وجود مكوّن عرض شبكة مرتبطة بالعظام، لكنه لا يكشف اسم ملف المصدر ولا كيفية تحميله.
- عناوين RVA لا تستخدم لتعديل المكتبة مباشرة قبل مطابقة ABI والإصدار والتحقق من عنوان الدالة داخل ELF.

## 3. خطة التحقيق التالية

1. فحص ملفات حزمة Android الأصلية بحثًا عن ملفات Unity serialized assets وAssetBundles وملفات الموارد المرافقة `.resS` و`.resource`.
2. استخراج قائمة أسماء الأصول وأنواعها، ثم البحث عن `Mesh`, `SkinnedMeshRenderer`, `Avatar`, `AnimationClip`, ومواد/خامات الشخصيات.
3. تفكيك دوال `Costume` أعلاه ومقارنة استخدام الحقول `limb/shape/flesh/texture` مع الكتابة إلى `MLHKNLAKIGM` أو `sharedMesh` أو `sharedMaterials`.
4. تحديد مسار اختبار قابل للتراجع لمصارع واحد فقط، مع الاحتفاظ بنسخة أصلية من الأصول.
5. قبل الاستبدال الكامل، التحقق من توافق العظام (skeleton/bones)، الـbind poses، والخامات؛ وإلا قد يظهر النموذج مشوهًا أو بلا حركة.

## 4. مسار عملي مدعوم بمراجع

دليل MDickie الرسمي يميز بين Content Mods لتغيير الأصول وبين Code Mods لتغيير الكود، ويذكر WECCL كـcontent loader في بيئة المودات المدعومة. لكن هذا الدليل موجّه أساسًا إلى بيئة الكمبيوتر؛ لم يثبت حتى الآن أن WECCL أو طريقة تعديل ملفات الكمبيوتر تعمل على نسخة Android 1.8.0.

مراجع:
- دليل MDickie الرسمي: https://www.mdickie.com/guides/wempire_mods.pdf
- توثيق Unity عن فحص ملفات البناء: https://docs.unity.cn/6000.7/Documentation/Manual/assets-analyze-built-assets.html

## الحالة

- [x] تنزيل artifact وتحليل `dump.cs` فعليًا.
- [x] تحديد مراجع بيانات الشخصية والزي ومكوّن `SkinnedMeshRenderer`.
- [x] تحديد دوال `Costume` ذات الأولوية للتفكيك.
- [ ] استخراج موديلات الشخصيات من ملفات أصول Android.
- [ ] إثبات كيفية تحميل/تبديل Mesh.
- [ ] اختبار استبدال مصارع واحد مع حفظ النسخة الأصلية.

النتيجة: أصبح لدينا مسار محدد للتحقيق في موديل الشخصية، لكن استبدال الموديل لم يُنفّذ بعد.