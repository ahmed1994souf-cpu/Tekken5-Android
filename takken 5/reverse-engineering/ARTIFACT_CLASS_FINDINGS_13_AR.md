# المرحلة 13 — فحص artifact ناجح واختيار طبقة المباراة

تاريخ الفحص: 2026-10-21  
المصدر الفعلي: artifact `wrestling-empire-il2cpp-dump` من تشغيل GitHub Actions رقم `39660693165`.

## 1. تأكيد أن التفريغ موجود فعلًا

تم تنزيل ZIP من artifact وفحص محتوياته مباشرة. الملفات ذات الصلة:
- `output/dump.cs` — 19,237,153 بايت.
- `output/script.json` — 54,460,738 بايت.
- `output/stringliteral.json` — 1,867,749 بايت.
- `output/DummyDll/Assembly-CSharp.dll` — 517,632 بايت.

تشغيل GitHub Actions: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39660693165  
صفحة workflow: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/workflows/dump-il2cpp.yml

وجود هذه الملفات في artifact مع حالة تشغيل `success` يؤكد أن عملية dump أخرجت بيانات قابلة للتحليل. لا يعني ذلك أن كل الأسماء المموهة فُك معناها أو أن سلوك اللعبة قد أُعيد بناؤه.

## 2. دليل مهم: توجد طبقة مركزية لإدارة الشخصيات

من `output/dump.cs`:

### Character — TypeDefIndex 116
حقول مؤكدة:
- `health`, `spirit`, `injury`, `injuryTime`, `dead`, `absent`.
- `moveFront`, `moveBack`, `moveGround`, `moveAttack`, `moveCrush`, `taunt` (كلها `int[]`).
- `stance`, `location`, `x`, `y`, `z`, `platform`, `seat`, `anim`, `angle`.
- `stat`, `oldStat`, `newStat` (كلها `float[]`).

### Characters — TypeDefIndex 24
يحتوي `public static Character[] c` و`no_chars` إلى جانب بيانات قائمة الشخصيات وواجهة ملفاتها. هذا دليل مباشر على وجود سجل مركزي للشخصيات، لكنه لا يثبت أنه الحلقة التي تدير قتال المباراة.

### PKIOJFKPIBI — TypeDefIndex 12
يحمل مرجعًا إلى `Character` في الحقل `LECDFJKPAPB`، وكذلك مراجع إلى مثيلات من نوعه `FNJCLDPBDNL` و`GNCOJJEDPGM` ومصفوفات `Vector3[]`. وجود هذه الحقول يجعله مرشحًا للتحقيق في كائن مرتبط بالشخصية أو الحركة، لكنه **ليس إثباتًا** على أنه مدير AI أو hitbox؛ يلزم تتبع استخدام الحقول في التعليمات.

### EHBPDHJCHFJ — TypeDefIndex 102
يحوي `static Character[] MBNHFOJBDAN` و`static PKIOJFKPIBI[] LDHNJMGPOCE` مع حقول ثابتة عديدة. قد يكون طبقة إدارة/واجهة مرتبطة بمجموعة شخصيات، لكن الاسم المموه لا يسمح بتسمية وظيفته نهائيًا.

## 3. خريطة الحلبة مؤكدة على مستوى البيانات

في `World` — TypeDefIndex 43 — توجد حقول واضحة:
- الحدود: `ground`, `ceiling`, `farNorth`, `farSouth`, `farEast`, `farWest`.
- الحلبة: `gRing`, `gApron`, `gPosts`, `gSupports`, `gPads`, `gMat`.
- الحبال: `gRope`, `ropeX`, `ropeY`, `ropeZ`, `ropeA`, `ringRopes`.
- الأبعاد/الإعدادات: `ringSize`, `ringGround`, `ringMiddle`, `ringTop`, `ringShape`.

هذه أسماء حقول مثبتة من dump، ويمكن اعتمادها عند رسم خريطة بيانات العالم. لا تثبت وحدها معادلات الحركة أو التصادم.

## 4. ما الذي لم يُحسم بعد؟

`dump.cs` يعرض أسماء الدوال والتواقيع وعناوين RVA، بينما أجسام الدوال تظهر كـ`{ }` في التفريغ. لذلك لم تُستخرج من هذا الفحص وحده:
- معادلة الضرر أو أثر الإحصاءات على الضربات.
- قرار AI وتوقيت اختيار الحركة.
- شروط نجاح التثبيت أو الإخضاع.
- تسلسل الانتقال من الإمساك إلى الطرح.

## 5. الخطوة التالية الدقيقة

1. فهرسة كل دوال `PKIOJFKPIBI` مع توقيعاتها وRVA بدل قراءة قائمة طويلة يدويًا.
2. استخراج عناوين الدوال التي تتعامل مع حقول `Character.health`, `anim`, `stance`, `moveAttack` من التفكيك الأصلي للمكتبة المطابقة.
3. تتبع مواضع قراءة/كتابة الحقول، ثم بناء جدول callers/callees موثق.
4. تسجيل أي معنى وظيفي كفرضية فقط حتى تؤكده تعليمات أو تجربة قابلة للتكرار.

## الحالة

- [x] تنزيل artifact ناجح وفحص محتوياته الفعلية.
- [x] تأكيد الحقول المركزية في `Character` و`Characters` و`World`.
- [x] تحديد `PKIOJFKPIBI` و`EHBPDHJCHFJ` كمرشحين للتحقيق دون اختلاق أسماء وظيفية.
- [ ] لم يتم حتى الآن تفكيك تعليمات ARM64 أو تأكيد AI/الضرر/شروط الفوز.
