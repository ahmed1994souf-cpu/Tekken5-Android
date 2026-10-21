# المرحلة 14 — ربط توقيعات Character بعناوين ScriptMethod

تاريخ: 2026-10-21  
المصدر: artifact `wrestling-empire-il2cpp-dump` من تشغيل Actions رقم `39660693165`. جرى فتح ZIP وتحليل `output/dump.cs` و`output/script.json` مباشرة.

## 1. تحقق من سلامة المخرجات وحدودها

يحتوي `script.json` على 122,991 سجلًا ضمن `ScriptMethod`، إضافة إلى `ScriptString` و`ScriptMetadata` و`ScriptMetadataMethod` و`Addresses`. ويذكر `dumper.log`:
- `Metadata Version: 39`
- `Il2Cpp Version: 39`
- `Dumping... Done!`
- تحذير `This file may be protected.`
- أخطاء متعددة في `restoring attributeIndex`.

لذلك نستخدم التواقيع والعناوين كفهرس للمتابعة، مع التنبيه إلى أن استعادة السمات (attributes) لم تكن كاملة. وجود سجل في ScriptMethod لا يعني أن الجسم المفكك للدالة معروف.

## 2. أمثلة قابلة للتحقق من الربط

| الصنف | الدالة المموهة | العنوان في ScriptMethod (عشري) | التوقيع المستخرج |
|---|---|---:|---|
| Character | `MEKEMKCMCNN` | 25669716 | `void(Character*, Character*, MethodInfo*)` |
| Character | `CKHMPNPJAJE` | 25673972 | `void(Character*, Character*, int32, MethodInfo*)` |
| PKIOJFKPIBI | `ILJPMBNOPLI` | 21644604 | `int32(PKIOJFKPIBI*, int32, MethodInfo*)` |
| PKIOJFKPIBI | `APFMNHHHGPB` | 21656684 | `float(PKIOJFKPIBI*, float, float, MethodInfo*)` |
| PKIOJFKPIBI | `HDEBMMPCIEI` | 21656716 | `int32(PKIOJFKPIBI*, float, float, int32, int32, MethodInfo*)` |
| PKIOJFKPIBI | `DBCNOGEDFKD` | 21660892 | `int32(PKIOJFKPIBI*, Vector3, MethodInfo*)` |
| PKIOJFKPIBI | `GDPFFMOCKIF` | يُستخرج من سجل ScriptMethod عند الحاجة | `void(PKIOJFKPIBI*, PKIOJFKPIBI*, int32, float, MethodInfo*)` |

**تنبيه العناوين:** الأرقام أعلاه هي القيم الموجودة في حقل `Address` في `script.json` كما هي؛ لم تُحوّل هنا إلى RVA أو file offset ولم يُثبت بعد أنها إزاحة مباشرة قابلة للاستخدام في أي أداة تفكيك. يلزم فهم طريقة تمثيل العنوان ومطابقة المكتبة الثنائية قبل الاعتماد عليها.

## 3. ما الذي تعنيه هذه البيانات؟

- دالتا `Character` المذكورتان تقبلان مرجعًا إلى `Character` أخرى؛ هذا يثبت تفاعلًا بين كائنين على مستوى التوقيع فقط، ولا يثبت أن إحداهما هجوم أو ضرر.
- `PKIOJFKPIBI` لديه عدد كبير من الدوال ذات معاملات عددية، ودوال تستقبل `Vector3` ومراجع إلى مثيلات من الصنف نفسه. هذه قرائن لاختيار الصنف للمرحلة التالية، وليست تعريفًا نهائيًا لدوره.
- لا يمكن تسمية دالة بأنها AI أو hitbox أو pin من توقيعها وحده.

## 4. الخطة التقنية التالية

1. تحديد مصدر المكتبة `libil2cpp.so` المطابق لنفس APK/الإصدار وABI الخاصين بهذا التفريغ.
2. فحص ترويسة ELF والـBuild ID، وتوثيق طريقة تحويل `Address` إلى موضع في الملف أو RVA.
3. استخدام disassembler يدعم ARM64 لقراءة الدوال المرشحة.
4. توثيق تعليمات القراءة/الكتابة والاستدعاءات قبل وضع أي تفسير سلوكي.
5. مقارنة الدليل الناتج مع حقول `Character` مثل `health`, `injury`, `stance`, `anim`, `moveAttack`.

## 5. الحالة

- [x] تم فحص ZIP الفعلي.
- [x] تم استخراج عدد سجلات ScriptMethod والتوقيعات/العناوين المذكورة.
- [x] تم توثيق تحذيرات dumper التي تحد من اليقين.
- [ ] لم يتم فك تعليمات ARM64 لهذه الدوال في هذه المرحلة.
- [ ] لا يوجد استنتاج مؤكد بعد عن معادلة الضرر أو AI أو شروط الفوز.

تشغيل التفريغ: https://github.com/ahmed1994souf-cpu/Tekken5-Android/actions/runs/39660693165
