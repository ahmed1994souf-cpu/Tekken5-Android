# تحليل استبدال موديلات Wrestling Empire — المرحلة 50

التاريخ: 2026-10-23

## نتيجة فحص ScriptMethod
تم تحليل `output/script.json` داخل الأثر `wrestling-empire-il2cpp-dump`، والبحث عن دوال `Costume` و`Character` التي تستقبل كائن `Costume` أو إعدادات `PKIOJFKPIBI`.

### مرشحات جديدة
- `Character__IKKBADFHKAL` — RVA `0x1887EC4`; التوقيع: `void(Character_o*, Costume_o*, MethodInfo*)`. مرشح لفحص مسار تمرير الزي إلى الشخصية.
- `Character__BFDFOCBGFBP` — RVA `0x187D218`; التوقيع: `void(Character_o*, PKIOJFKPIBI_o*, MethodInfo*)`. مرشح لمسار إعدادات الشخصية/الزي.
- `Costume__BJALLCKDACJ` — RVA `0x1666F90`; يقبل `Costume_o*` آخر وعددًا صحيحًا.
- `Costume__NLDODOJBPHP` — RVA `0x1668E28`; يقبل `Costume_o*` آخر ويعيد `float`.
- `Costume__EGHLMOHFHOL` — RVA `0x16695EC`; يقبل `Costume_o*` آخر ويعيد `int32`.
- `Costume__JENEJOJNOOP` — RVA `0x1667FF8`; دالة من دون معاملات إضافية.
- `Costume__AJAFNCJDPCD` — RVA `0x1668160`; تقبل عددين صحيحين.

## تغييرات المستودع
تم تحديث `.github/workflows/dump-il2cpp.yml` لتوسيع التفكيك ARM64 ليشمل المرشحات السبعة أعلاه. التغيير في commit:
`8b92b4f660210ed8ce3d40a5aec326438e4b242a`

الرابط: https://github.com/ahmed1994souf-cpu/Tekken5-Android/blob/main/.github/workflows/dump-il2cpp.yml

التعديل يدفع GitHub Actions إلى تشغيل workflow بسبب مراقبة مسار الملف. لم أتحقق بعد من نجاح التشغيل الجديد أو تنزيل أثره، لذلك لا أعتبر نتائج التفكيك الإضافية متاحة بعد.

## مستوى الثقة والقيود
- وجود دوال تستقبل `Costume` مثبت من التواقيع المستخرجة.
- ارتباط `JGEEDIAOKBM` بالحقل `shape[]` وارتباط `ACIGFMENHIE` بالحقل `r[]` مدعوم بقراءة تعليمات ARM64 السابقة.
- لم يُحدّد بعد بشكل قاطع موضع إنشاء `Mesh` أو `SkinnedMeshRenderer` أو تعيين العظام.
- لا يوجد حتى الآن موديل مستخرج أو موديل بديل مركب، ولا APK معدل.
- ملف التفريغ يحمل تحذيرًا بأن metadata قد تكون محمية؛ لذلك يلزم التحقق من النتائج باستخدام التفكيك الأصلي.

## الخطوة التالية
بعد انتهاء الـ workflow، افحص تفكيك `Character_IKKBADFHKAL` و`Character_BFDFOCBGFBP` وقارن الاستدعاءات والمراجع بالمرشحات في `Costume`. بعد ذلك ابحث عن مسار تحميل الأصول أو ربط المجسم والمواد قبل تصميم آلية استبدال محافظة على الهيكل والتحريك.
