# فحص مكتبة libil2cpp.so من artifact — المرحلة 07

## ما فُحص فعليًا

تم تنزيل artifact قديم من تشغيل GitHub Actions رقم `39655996545`، واسمه `wrestling-empire-il2cpp-dump`. رغم أن تشغيله فشل قبل تشغيل Il2CppDumper، يحتوي الـartifact على ملف `libil2cpp.so` كاملًا، لذلك أمكن فحص ترويسة ELF مباشرة.

- حجم الملف: `55,048,248` بايت.
- النوع: ELF 64-bit، little-endian، shared object.
- المعمارية: AArch64 / ARM64.
- بيئة البناء الظاهرة في الترويسة: Android API 25، NDK r27c.
- ELF Build ID: `d32d84554cf9e27ee55d1933a9d5702066310c74`.
- SHA-256: `08a31a15e7b64f7edac5e2d1998ea23d662fe413ab20e563d4182791003606ab`.

## حدود النتيجة

هذا يثبت نوع ومعمارية المكتبة التي احتفظ بها ذلك التشغيل، لكنه **لا يثبت وحده** أنها من نفس APK/الإصدار الدقيق الذي أُخذ منه `takken 5/global-metadata.dat`. يجب التحقق من تطابق الإصدار وABI قبل تفسير عناوين native أو اعتماد dump.

بحث ASCII مباشر في المكتبة لم يكشف أسماء اللعب المحددة مثل `moveAttack` أو `ringShape`؛ وهذا متوقع في مكتبة stripped، ولا يعني أن هذه الأنظمة غير موجودة. الخطوة التالية هي تشغيل محلل IL2CPP يدعم metadata v39 على المكتبة والـmetadata المطابقتين، ثم فحص `dump.cs` و`script.json` وملفات التسجيل الناتجة.

## سجل التشغيل

- تشغيل GitHub Actions الذي يحتوي artifact: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39655996545
- artifact الأصلي: `wrestling-empire-il2cpp-dump` (قد تنتهي صلاحيته حسب سياسة الاحتفاظ).
- سير العمل الحالي: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/workflows/dump-il2cpp.yml

هذه ملاحظات فحص ساكن موثقة؛ لم يتم الادعاء باستخراج الدوال بعد.
