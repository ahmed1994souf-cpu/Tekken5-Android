# متابعة تدقيق مسار الموديل — 2026-10-23

## فحص مباشر لملف dump.cs

تم فحص الملف `output/dump.cs` الموجود داخل Artifact `wrestling-empire-il2cpp-dump.zip`، وليس الاعتماد على مقتطفات تقارير سابقة فقط.

### نتائج مؤكدة

- `Costume` هو `TypeDefIndex 53`، وحقوله المعلنة تشمل `id`, `charID`, `limb`, `texture[]`, `r[]`, `g[]`, `b[]`, `flesh[]`, و`shape[]`.
- `Character` هو `TypeDefIndex 116`، ويحمل `Costume[] costume` عند الإزاحة `0x70`، و`costumeChange` عند `0x80`.
- `PKIOJFKPIBI` هو `TypeDefIndex 12`، ويحمل `Character LECDFJKPAPB` عند `0x20`، و`Animator MPIHDGHEAEM` عند `0x168`، و`GameObject MOMHHCLCACH` عند `0x108`.
- الدوال المهمة المعلنة في `Costume` تشمل:
  - `PFCOCIOEFBN` عند RVA `0x1663F6C`
  - `MFBNABEJFIE` عند RVA `0x1665040`
  - `CHCBMJCHBOF` عند RVA `0x166529C`
  - `JBECIKIBKIP` عند RVA `0x16662E0`
  - `BJALLCKDACJ` عند RVA `0x1666F90`
  - `ECNCADEADNG` عند RVA `0x16673A4`

## ما كشفته ملفات التفكيك الحالية

الـ Artifact يحتوي ملفات تفكيك لبعض دوال `Character`، مثل `MEKEMKCMCNN`, `DOBMPDMNJBK`, و`CKHMPNPJAJE`، لكنه لا يتضمن تفكيكًا مباشرًا للدوال الست المذكورة من `Costume`. لذلك لا نستطيع أن نستنتج من هذه الملفات وحدها أن دالة بعينها تغيّر `sharedMesh` أو تستبدل مجسم الشخصية.

## استنتاج عملي

المسار الأكثر دقة هو:
1. الحصول على `UnityDataAssetPack.apk` أو استخراج `datapack.unity3d` و`resources.resource` ومجلد `costumes`.
2. إعادة تشغيل التفكيك على عناوين الدوال الست أعلاه من ملف `libil2cpp.so` المطابق لنفس إصدار اللعبة.
3. تتبع مراجع `GameObject` و`Animator` والحقول ذات الصلة حتى نحدد نقطة تركيب الجسم/الزي.
4. تجربة تغيير قابلة للتراجع على شخصية واحدة فقط بعد تحديد ملف المجسم الصحيح.

**حدود النتيجة:** لم يتم استخراج مجسم مصارع بعد، ولم يتم استبدال موديل داخل اللعبة. ما تم تأكيده هنا هو بنية البيانات وعناوين الدوال المرشحة، مع تحديد فجوة التفكيك والأصول اللازمة.
