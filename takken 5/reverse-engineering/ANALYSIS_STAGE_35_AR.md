# ANALYSIS STAGE 35 — Character field access + native combat candidates

## الهدف

تحديث التحليل بعد تشغيل فحص ARM64 مباشر على `libil2cpp.so` مع `script.json` المستخرج من Wrestling Empire 1.8.0.

## تشغيل الفحص

- Workflow: `Scan Character Combat Fields`
- Run: `39844534828`
- النتيجة: `success`
- Artifact: `character-field-access-report`
- Binary: `55,048,248` bytes
- ScriptMethod records: `122,991`
- Direct field-offset matches: `56,202`

> الفحص الأولي واسع ويحتوي false positives لأن الإزاحات مثل `0xA0` موجودة أيضاً في أصناف أخرى. لذلك لا تُعتبر المطابقة وحدها وصولاً إلى Character.

## اكتشاف مهم: NFAFFEAGBAL.PKDBEDDFGPL

- RVA: `0x161A780`
- signature من dump.cs: `public static void PKDBEDDFGPL()`
- هذه الدالة كبيرة جداً وتغطي تقريباً حتى `0x16210F4`، وتحتوي على وصولات مباشرة إلى كائنات Character/بيانات مرتبطة بها.

أدلة native مؤكدة داخل الدالة:

### 1. وصول إلى Character ثم كتابة health

عند `0x161B4F4`:

```text
ldr x23, [x22, #0x20]
```

والـ `0x20` في `PKIOJFKPIBI` هو حقل من النوع `Character`.

ثم عند `0x161B564`:

```text
ldr s0, [x22, #0xB4]
str s0, [x23, #0xA0]
```

وبما أن `Character.health` هو `0xA0`، فهذا يثبت أن الدالة تكتب قيمة float إلى health لكائن Character تم الوصول إليه عبر حقل Character.

### 2. قراءة health لنفس Character

عند `0x161B594`:

```text
ldr s1, [x23, #0xA0]
```

ثم تستخدم القيمة في عملية حسابية:

```text
fdiv s0, s0, s10
fadd s0, s1, s0
```

لكن هذه العملية تكتب لاحقاً إلى كائن آخر عند `0x20`، لذلك لا يجوز وصفها بأنها damage formula حتى الآن.

### 3. وصولات متعددة إلى injury

داخل نفس الدالة توجد وصولات كثيرة إلى `Character.injury` (`0xA8`) و`injuryTime` (`0xAC`) مع شروط مرتبطة بالحالة.

عند `0x161ED78` توجد كتابة مباشرة إلى `0xA8`:

```text
ldr d0, [sp, #0x8]
str d0, [x23, #0xA8]
```

ثم توجد قراءات لاحقة لـ `injury` وحالات شرطية مرتبطة بها.

## اكتشاف مهم ثانٍ: Character.LICMFPCGJNN

- RVA: `0x188D674`
- signature:
  `public void LICMFPCGJNN(int FIMNNBLCOBH, float NFNOAMPPKNO = 1)`

الدالة تكتب مباشرة:

```text
str w20, [x19, #0xA8]   // injury
```

ثم تحسب وتكتب `injuryTime` عند `0xAC`.

كما تعدّل عناصر مرتبطة بحالة الشخصية عبر عمليات `fsub/fmul/fadd` على بيانات الحركة/الحالة.

**التصنيف:** CONFIRMED injury-state application/update function.

**غير مثبت:** أنها دالة damage النهائية نفسها؛ لا توجد فيها كتابة مباشرة إلى `health`.

## Character.AJAFNCJDPCD

- RVA: `0x188D9DC`
- signature:
  `public void AJAFNCJDPCD(int NEENFJAOBNB, int KAGGHGPPANP = 0, int ACNJCGOLCIC = 0)`

توجد في بدايتها كتابة:

```text
str w8, [x19, #0xA0]
str xzr, [x19, #0xA8]
str wzr, [x19, #0xB0]
```

أي health/injury/dead، لكنها جزء من تهيئة/إعادة ضبط حالة Character وليست دليلاً على damage.

## Character.BFDFOCBGFBP

- RVA: `0x187D218`
- signature:
  `public void BFDFOCBGFBP()`

تقرأ بيانات من كائن آخر ثم تنسخها إلى Character، بما فيها:

- `dead` -> `0xB0`
- `health` -> `0xA0`
- `injury` -> `0xA8`
- `injuryTime` -> `0xAC`

هذا يثبت مسار نسخ حالة Character، وليس damage formula.

## النتيجة الحالية

لدينا الآن أول دليل native قوي يربط مساراً واحداً فعلياً بين:

`PKIOJFKPIBI.Character field -> Character.health/injury`

وأصبح `NFAFFEAGBAL.PKDBEDDFGPL` أعلى أولوية لفحص combat resolution.

لكن **لم نثبت بعد معادلة الضرر النهائية** مثل:

`health = health - damage`

ولم نثبت بعد أي دالة هي التي تحسب `damage` من `force/strength/move/attacker`.

## الخطوة التالية

المرحلة التالية يجب أن تتعقب داخل `PKDBEDDFGPL` مصادر القيمة التي تصل إلى:

- `Character.health (0xA0)`
- `Character.injury (0xA8)`
- `Character.injuryTime (0xAC)`
- `Character.dead (0xB0)`

ثم نربطها بالـ `force`, `moveAttack`, `attackViable`, `attacker/target` وعمليات الاستدعاء القريبة، بدلاً من الاعتماد على أسماء strings فقط.
