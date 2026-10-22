# ANALYSIS STAGE 40 — روابط الاستدعاء لمرشحي الإصابة

التاريخ: 2026-10-22
النطاق: Wrestling Empire Android 1.8.0 فقط.

## نتيجة التتبع الساكن للاستدعاءات
تم استخدام disassembly من ملف `libil2cpp.so` الناتج عن artifact الناجح، مع جدول `ScriptMethod` من `script.json` لنسبة مواقع الاستدعاء إلى أقرب بداية طريقة معروفة.

### `Character$$LICMFPCGJNN(int, float)` — RVA `0x188D674`
تم العثور على استدعاءات مباشرة (`BL`) من هذه المواقع:
- `0x161F088` و`0x161F0B8` داخل نطاق `NFAFFEAGBAL$$PKDBEDDFGPL` (أقرب طريقة في جدول metadata عند `0x161A780`).
- `0x16A7944`, `0x16A7B48`, `0x16A7DF0` داخل نطاق `OHAIEDEDEPK$$MEMMHOMHLPH` (أقرب بداية طريقة عند `0x16A5358`).

هذه علاقة استدعاء مؤكدة في التعليمات، لكن دلالة أسماء المستدعين مشفّرة، ولا تكفي وحدها لتسميتهم مسارات ضرب أو Damage.

### `Character$$IPIFDEPOJGB(int, float)` — RVA `0x1888C94`
استدعاءات مباشرة مرصودة عند:
- `0x149FF30` ضمن `PKIOJFKPIBI$$MBOHBEAOEIJ`
- `0x14C4A74` ضمن `PKIOJFKPIBI$$IHMCDCGIOAE`
- `0x14C6F8C` ضمن `PKIOJFKPIBI$$PMCNGAKLJCA`
- `0x14CFF74` و`0x14D0138` ضمن `PKIOJFKPIBI$$CFFJHPLAPBK`
- `0x14F51FC` و`0x14F6994` ضمن `PKIOJFKPIBI$$LMAMMGEDLAC`
- `0x1511F74` ضمن `PKIOJFKPIBI$$OKJELDOEOBB`
- `0x15DCD00` ضمن `EFCOCKFHAHA$$DENMJHMDIJE`
- `0x16821C4` ضمن `Scene_Editor$$Update`

الاستدعاء من `Scene_Editor$$Update` يذكّرنا أن هذه الطريقة قد تُستخدم في سياقات أكثر من قتال اللعبة، لذلك لا يمكن استنتاج «الضرر» من الكتابة إلى الصحة وحدها.

## مستوى الثقة
- **CONFIRMED:** مواقع BL المذكورة تتجه إلى عناوين الطريقتين المحددتين في binary.
- **CONFIRMED:** `LICMFPCGJNN` تكتب إلى حقلي `injury` و`injuryTime` في جسمها.
- **INFERRED:** `IPIFDEPOJGB` طريقة عامة لتحديث قيم حالة الشخصية/الصحة، ويمكن أن تُستدعى في أكثر من سياق.
- **UNKNOWN:** أي مستدعٍ من القائمة مسؤول عن الضربة التي أدت إلى الإصابة، وما إذا كان استدعاء `LICMFPCGJNN` يسبق/يتبع احتساب الضرر أو يخص تغييرًا إداريًا/تحريريًا.

## الخطوة التالية
فحص كتل التعليمات حول الاستدعاءات داخل `NFAFFEAGBAL`, `OHAIEDEDEPK`, و`EFCOCKFHAHA` لتحديد القيم التي تُمرر في سجلات ARM64 إلى الوسيطين integer/float، مع ربطها بسياق اللعبة قبل إسناد دلالة قتالية.
