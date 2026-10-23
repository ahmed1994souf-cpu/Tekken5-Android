# المرحلة 42 — استعادة سياق التحليل وتحديد فجوة أصول الشخصيات

التاريخ: 2026-10-23  
النطاق: Wrestling Empire Android 1.8.0 فقط.  
المستودع: `ahmed1994souf-cpu/Tekken5-Android`

## ما تم فحصه مباشرة في GitHub

تم فحص شجرة المستودع على الفرع `main`، وسجل آخر commits، وقراءة الملفات التالية مباشرة:
- `takken 5/reverse-engineering/COSTUME_TRACE_CHECKPOINT_41_AR.md`
- `takken 5/reverse-engineering/AVAILABLE_FILES_AUDIT_39_AR.md`
- `takken 5/reverse-engineering/MODEL_ASSET_PIPELINE_AUDIT_38_AR.md`
- `takken 5/reverse-engineering/MODEL_REPLACEMENT_ANALYSIS_37_AR.md`
- `takken 5/reverse-engineering/asset_inventory.json`
- `.github/workflows/dump-il2cpp.yml`

أحدث commit عند بدء هذه المرحلة هو `6839f8d1926ffcd8575121e94b610799c8608abe`، برسالة `Add direct dump.cs verification for character and costume fields`. آخر تشغيل ظاهر في سجل Actions كان ناجحًا، لكن ذلك تشغيل workflow لبناء APK وليس دليلًا على استخراج موديل أو نجاح استبداله.

## الحقائق المؤكدة من التقارير السابقة

1. `Costume` هو `TypeDefIndex 53` وحقوله المعلنة تتضمن `id`, `charID`, `limb`, `texture[]`, `r[]`, `g[]`, `b[]`, `flesh[]`, `shape[]`.
2. `Character` هو `TypeDefIndex 116`؛ حقل `costume` عند `0x70` و`costumeChange` عند `0x80`.
3. الكائن `PKIOJFKPIBI` (TypeDefIndex 12) يربط بيانات `Character` و`Costume` بمراجع `GameObject` و`SkinnedMeshRenderer` ومواد Unity. هذا يجعل الكائن هدفًا قويًا لتتبّع العرض، لكنه لا يثبت وحده أي دالة أو حقل يبدّل المجسم.
4. دوال Costume المرشحة من dump.cs هي `PFCOCIOEFBN` عند RVA `0x1663F6C`، و`MFBNABEJFIE` عند `0x1665040`، و`CHCBMJCHBOF` عند `0x166529C`، و`JBECIKIBKIP` عند `0x16662E0`، و`ECNCADEADNG` عند `0x16673A4`. لم تُوثق أجسام هذه الدوال في التقارير المتاحة.
5. جرد الأصول يصف XAPK بثلاثة أجزاء: APK الأساسي، و`UnityDataAssetPack.apk`، و`config.arm64_v8a.apk`. المسارات المتوقعة لحزمة الأصول تشمل `assets/bin/Data/datapack.unity3d`, و`assets/bin/Data/resources.resource`, و`assets/costumes`.
6. تقرير تدقيق الملفات المتاحة يقول إن `assets.zip` الموجود في مكتبة المحادثة لا يحتوي هذه العناصر المطلوبة؛ لذا لا يمكن اعتباره حزمة الأصول الكاملة. لم يتم في هذه المرحلة تنزيل محتويات المكتبة أو استخراج Mesh.

## الخطوة التالية — مرتبة حسب القيمة

### أ. استعادة Artifact التفريغ
افحص قائمة artifacts الخاصة بتشغيل workflow `Dump Wrestling Empire IL2CPP`، ثم نزّل artifact الذي يحتوي `dump.cs`, `script.json`, وملفات disassembly. لا يُعاد تشغيل تنزيل TransferNow إلا إذا كان artifact غير متاح أو غير مكتمل.

### ب. فحص أجسام دوال Costume
باستخدام ملف `libil2cpp.so` المطابق لنفس إصدار اللعبة، استخرج تعليمات ARM64 حول عناوين RVA المذكورة، وتحقق من تحويل RVA إلى VA وفق معلومات ELF قبل التفكيك. ابحث عن وصول إلى حقول `0x328`, `0x330`, `0x340`, `0x350` ومراجع المواد، وعن استدعاءات Unity المتعلقة بـ `SkinnedMeshRenderer` أو `GameObject`. لا تنسب وظيفة لأي دالة من اسمها وحده.

### ج. استعادة حزمة الأصول الصحيحة
الحصول على `UnityDataAssetPack.apk` من XAPK الأصلي هو عنق الزجاجة الحالي. بعد توفره، افحص قائمة ZIP وأحجام الملفات وتواقيعها أولًا؛ ثم افهرس أنواع Unity assets وأسماء الأصول. لا تُعد تسمية `assets.zip` أو metadata منفردة بديلًا عن AssetPack.

### د. معيار إثبات نجاح تغيير الشخصية
لا تُعلن نتيجة «تم استخراج الموديل» حتى يوجد ملف Mesh قابل للفحص. ولا تُعلن «تم الاستبدال» حتى يتم تعديل نسخة اختبار مستقلة، ثم التحقق من الظهور والخامات والهيكل والأنيميشن، مع إبقاء النسخة الأصلية دون تغيير.

## حالة المرحلة

- [x] العثور على التقارير الصحيحة في المستودع من خلال شجرة GitHub.
- [x] استعادة آخر نقطة موثقة وقراءة الجرد وسير العمل.
- [x] توثيق أن بناء APK الناجح لا يثبت نجاح تعديل موديل.
- [ ] الحصول على Artifact التفريغ وفحص تعليمات دوال Costume.
- [ ] الحصول على AssetPack الأصلي وفهرسة أصول الشخصيات.
- [ ] استخراج Mesh وتحديد مسار تحميله.
- [ ] اختبار استبدال واحد قابل للتراجع.

**الخلاصة:** لا حاجة لإعادة إرسال التقارير. البيانات البرمجية تحدد نقطة الربط المحتملة، لكن التقدم الحاسم التالي يتطلب إما Artifact التفريغ لتأكيد سلوك الدوال، أو AssetPack لاكتشاف ملفات الموديلات. حتى ذلك الحين يبقى استخراج واستبدال الموديل غير منجزين.
