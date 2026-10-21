# نتائج الهندسة العكسية الفعلية — المرحلة 01

> **المصدر:** `Wrestling Empire 1.8.0` — الحزمة التي رفعها المستخدم للتحليل.
>
> **الهدف:** فهم البنية والسلوك والأنظمة لبناء لعبة أصلية مشابهة لاحقًا، وليس نسخ كود أو أصول اللعبة.

## 1. ما تم تحليله فعليًا

تم فتح ملف XAPK وفحص محتوياته محليًا. البنية الفعلية هي:

- `com.MDickie.WrestlingEmpire.apk` — APK الأساسي، حوالي 114 MB.
- `UnityDataAssetPack.apk` — AssetPack، حوالي 229 MB.
- `config.arm64_v8a.apk` — مكتبات ARM64، حوالي 26 MB.
- `global-metadata.dat` — حوالي 7.43 MB.
- `libil2cpp.so` — حوالي 55.0 MB.
- `datapack.unity3d` — حوالي 163.9 MB.

### ثقة النتيجة
**CONFIRMED** — هذه النتائج مبنية على الملفات الفعلية، وليست تخمينًا.

---

## 2. المحرك والبنية التنفيذية

من الـ manifests وملفات Unity:

- Unity: `6000.3.25f1`
- IL2CPP مستخدم في البناء.
- وجود `global-metadata.dat`.
- وجود `libil2cpp.so` و`libunity.so` ضمن split الخاص بـ ARM64.
- metadata version الظاهر في رأس `global-metadata.dat`: **39**.
- التطبيق ARM64 فقط ضمن split الذي تم فحصه.
- `minSdkVersion = 32`
- `targetSdkVersion = 36`
- `versionName = 1.8.0`
- `versionCode = 87`

هذا يعني أن منطق اللعبة الرئيسي ليس Assembly-CSharp.dll عاديًا يمكن قراءته مباشرة من APK؛ تم تحويله إلى IL2CPP، بينما تبقى metadata وبيانات Unity مفيدة جدًا لفهم البنية.

---

## 3. تقسيم البيانات مهم جدًا

الـ AssetPack يحتوي على حزم منفصلة واضحة:

1. `costumes`
2. `sprites`
3. `music`
4. `sound`
5. `world`

وكل واحدة لها Unity AssetBundle manifest مستقل.

### لماذا هذا مهم للعبة التي سنبنيها؟

هذا يدل على فصل المحتوى عن التطبيق التنفيذي، ويمكن الاستفادة من نفس الفكرة في لعبتنا الأصلية:

```text
Core Runtime
 ├─ Characters / Gameplay
 ├─ Match Logic
 ├─ AI
 └─ Input

Content Bundles
 ├─ Characters / Costumes
 ├─ UI / Sprites
 ├─ Music
 ├─ SFX
 └─ Arena / World
```

هذا ليس نسخًا للبنية الداخلية حرفيًا؛ هو استنتاج معماري مدعوم بتقسيم الملفات الموجود فعلًا.

**Confidence: CONFIRMED بالنسبة لتقسيم الملفات، INFERRED بالنسبة للتصميم المعماري المقترح.**

---

## 4. حجم وأنواع أصول الـ AssetBundles

### Costumes
تم العثور على **876** مسار Asset فعلي داخل manifest الخاص بالملابس/الشخصيات:

- 488 PNG
- 300 JPG
- 88 mesh

وتوجد فئات واضحة مثل:

- Bodies
- Bodies/Patterns
- Legs
- Legs/Patterns
- Legs/Footwear
- Arms/Accessories
- Faces
- Faces/Female
- Faces/Beards
- Faces/Masks
- Faces/Expressions
- Hair
- Models/Hair
- Models/Heads
- Scars

### الاستنتاج
الشخصية ليست مجرد Mesh واحد ثابت. يوجد نظام تركيب/تخصيص يعتمد على أجزاء ومواد/Textures متعددة.

**Confidence: CONFIRMED.**

---

## 5. الـ World / الحلبة

ملف `world.manifest` يحتوي على **107** Asset paths.

من الأسماء المؤكدة:

- `World/Rings/...`
- `World/Ropes/...`
- `World/Belts/...`
- `World/Crowds/...`
- `World/Screens/...`

كما توجد عناصر واضحة مثل:

- `mat01.jpg`, `mat02.jpg`
- `post01.jpg`
- `rope01.jpg`, `rope04.jpg`, `rope05.jpg`, `rope09.jpg`
- `turnbuckle_black.jpg`
- canvas logos
- apron logos
- crowd textures
- belt textures

### استنتاج معماري مهم
الحلبة قابلة للتغيير بصريًا من خلال مواد/Textures متعددة، بدل اعتبارها صورة واحدة أو مشهدًا ثابتًا فقط.

**Confidence: CONFIRMED للأصول، INFERRED لقابلية إعادة استخدام النظام.**

---

## 6. نظام الصوت يعطي أدلة مباشرة على حالات اللعب

` sound.manifest` يحتوي على **262** Asset paths، منها **260 WAV**.

الفئات التي ظهرت مباشرة في أسماء الأصول تشمل:

- `Crowd`
- `Pyro`
- `Movement`
- `Weapons`
- `Impacts`
- `Instruments`
- `Referee`
- `Pain`
- `Menus`
- `World`

ومن الأسماء المؤكدة:

- `Referee/Pin01.WAV`
- `Referee/Count04.WAV`
- `Referee/Count10.WAV`
- `Impacts/Fall02.wav`
- `Impacts/Thud01.wav`
- `Movement/Ropes01.wav`
- `Movement/Swing*.wav`
- `Crowd/Chant_Count*.wav`
- `Crowd/Chant_Wrestle.wav`
- `Menus/Browse.wav`
- `Menus/Cash.wav`

### استنتاج
الصوت مرتبط بحالات/أحداث gameplay، وليس مجرد موسيقى خلفية. وجود مجموعة منفصلة للـ Referee وPin وCount وFall وRopes يعطي أساسًا قويًا لافتراض وجود event-driven feedback في المباراة.

**Confidence: CONFIRMED للأصول، INFERRED لطريقة الربط البرمجية.**

---

## 7. واجهة وتحكم الهاتف

في `sprites.manifest` توجد أصول واضحة للتحكم والـ HUD، منها:

- `Controls/Virtual Buttons.prefab`
- `Controls/Controller_Overlay12.png`
- `Controls/Controller_Icon*.png`
- `Controls/Guide*.prefab`
- `Controls/Player_Meter_Right.prefab`
- `Labels/Label_Control.png`
- `Labels/Label_Pin*.png`
- `Labels/Label_Count*.png`
- `Labels/Label_Adrenaline.png`
- `Labels/Label_Out_*.png`

### الاستنتاج
هناك طبقة Mobile Input/UI مخصصة، وليست مجرد أزرار Android خارجية.

كما يظهر في metadata نص مرتبط بـ `Pinch` و`For best results, please help the game identify any connected controllers`، ما يؤكد وجود تعامل مع touch/controller input على مستوى اللعبة.

**Confidence: CONFIRMED.**

---

## 8. مؤشرات مباشرة من metadata على أنظمة اللعبة

تحليل `global-metadata.dat` أعطى أسماء حقول/رموز وسلاسل نصية مرتبطة باللعبة، ومنها بشكل واضح:

- `Character`
- `Characters`
- `wrestler`
- `opponent`
- `match`
- `matches`
- `matchSize`
- `bookingOpponent`
- `optReferees`
- `Scene_Match_Setup`
- `AdjustCamera`
- `health`
- `Stamina`
- `Strength`
- `Agility`
- `Skill`
- `Popularity`
- `FightStyle`
- `anim`
- `animTim`
- `charAnim`
- `moveAttack`
- `moveFront`
- `moveBack`
- `moveGround`
- `moveCrush`
- `attackViable`
- `gPinPoint`
- `gMatch`
- `ringPreset`
- `ringShape`
- `ringCanvas`
- `ringApron`
- `ringPosts`
- `ringPads`
- `ringMat`
- `ringGround`
- `ringMiddle`
- `ringTop`
- `ringAnimator`
- `ringAnim`
- `ringRopes`
- `gRope`
- `ropeAnimator`
- `ropeAnim`
- `ropeTransition`
- `ground`
- `OffGround`
- `distance`
- `angleDifference`
- `victimAngle`
- `gravity`
- `force`
- `target`
- `travel`
- `control`

هذه الأسماء لا تكشف الكود الأصلي وحدها، لكنها دليل قوي على وجود طبقات منفصلة للمباراة، الشخصية، الحركة، الهجوم، الحلبة، الحبال، الكاميرا، والصحة/الإحصائيات.

**Confidence: CONFIRMED لوجود هذه الرموز/السلاسل؛ UNKNOWN بالنسبة إلى التنفيذ الداخلي الدقيق.**

---

## 9. ما يمكن استنتاجه عن نظام الشخصية

لدينا أدلة على أن الشخصية لها على الأقل:

- Health
- Stamina
- Strength
- Agility
- Skill
- Popularity
- FightStyle
- animation state/timing
- attack/movement/ground move categories
- opponent/target relations

وهذا يختلف عن نموذج شخصية بسيط من نوع `position + attack`.

### النموذج الذي سنختبره لاحقًا

```text
Character
 ├─ Physical Stats
 │   ├─ Health
 │   ├─ Stamina
 │   ├─ Strength
 │   └─ Agility
 │
 ├─ Skill / Style
 ├─ Animation State
 ├─ Combat State
 ├─ Target / Opponent
 ├─ Ground / OffGround State
 └─ Equipment / Costume
```

هذا النموذج **تحليل معماري مقترح**، وليس ادعاءً بأن أسماء هذه المكونات كُتبت بهذا الشكل داخل اللعبة.

---

## 10. أدلة على نظام المصارعة/القتال

الـ metadata يحتوي على إشارات مباشرة إلى:

- `grapple`
- `broke grapple`
- `moveAttack`
- `moveGround`
- `moveCrush`
- `gPinPoint`
- `Pin`
- `pinned`
- `pin me`
- `your opponent`
- `execute a move`
- `added momentum`
- `score bonus damage`
- `Health Meter`
- `Stamina`
- `block`
- `cover up and block`
- `falling over ropes`
- `cut by rope`
- `inside the ring`
- `outside the ring`

### استنتاج قوي
نظام القتال ليس مجرد ضربات متتابعة؛ توجد حالات خاصة بالمصارعة مثل grapple/pin/ground/rope/ring-boundary، بالإضافة إلى صحة وتحمل.

**Confidence: CONFIRMED بالنسبة إلى وجود المؤشرات النصية؛ تفاصيل transition/logic ما زالت تحتاج dynamic analysis.**

---

## 11. أدلة على نظام الحلبة والحركة حولها

وجدنا متغيرات وأسماء واضحة مثل:

- `ringShape`
- `ringSize`
- `ringGround`
- `ringMiddle`
- `ringTop`
- `ringRopes`
- `ropeX/Y/Z/A`
- `ropeAnimator`
- `ropeTransition`
- `falling over ropes`
- `inside the ring`
- `outside the ring`

هذا يسمح لنا بوضع فرضية اختبارية بأن الحلبة ليست مجرد collision box واحد، بل لها مستويات/مكونات متعددة: أرضية، وسط/علوي، حبال، أطراف، وربما انتقالات عند عبور الحبال.

**Confidence: CONFIRMED للأسماء، INFERRED للنموذج الهندسي.**

---

## 12. الكاميرا

ظهر `AdjustCamera` بالإضافة إلى عدد كبير من مؤشرات camera position و`eventCamera` و`CameraPos` في البيانات.

هذا يدعم وجود نظام كاميرا gameplay منفصل عن مجرد Camera follow ثابت.

### ما لم نثبته بعد
لم نحدد بعد:

- هل الكاميرا lock-on دائمًا؟
- كيف تختار target؟
- ما هي معادلة المسافة/الارتفاع؟
- كيف تتصرف عند أكثر من خصم؟
- هل توجد حالات كاميرا خاصة للـ pin/grapple/finish؟

هذه ستكون ضمن الاختبارات الديناميكية.

---

## 13. الـ AI — ما الذي نعرفه الآن؟

لا أريد أن أخلط أسماء metadata مع كود AI مؤكد.

لكن لدينا مؤشرات مثل:

- `opponent`
- `target`
- `attackViable`
- `distance`
- `angleDifference`
- `bookingOpponent`
- نصوص مرتبطة بالمنافس والخصم والحركة داخل/خارج الحلبة.

هذا يجعل وجود target selection/attack viability plausible جدًا، لكن **تفاصيل قرار AI لم تثبت بعد**.

المرحلة القادمة يجب أن تختبر عمليًا:

1. ماذا يفعل الخصم عند المسافة البعيدة؟
2. متى يقترب؟
3. متى يهاجم؟
4. هل يغير الهجوم حسب وضع اللاعب؟
5. كيف يتصرف عند سقوط اللاعب؟
6. كيف يتصرف قرب الحبال/خارج الحلبة؟
7. ماذا يحدث عند وجود أكثر من خصم؟

**Confidence: UNKNOWN/INFERRED حتى يتم dynamic analysis.**

---

## 14. أهم اكتشاف حتى الآن: اللعبة Data-Driven بدرجة كبيرة

لدينا ثلاث طبقات واضحة من البيانات:

```text
APK
 ├─ Runtime + native libraries
 ├─ global-metadata.dat
 └─ Unity core data

AssetPack
 ├─ costumes
 ├─ sprites
 ├─ music
 ├─ sound
 └─ world

Gameplay Metadata / Strings
 ├─ Character / wrestler
 ├─ Match
 ├─ moves
 ├─ health/stamina/stats
 ├─ ring/ropes
 ├─ camera
 └─ opponent/target
```

هذا مهم جدًا لنا: بدل محاولة تقليد اللعبة بصريًا فقط، سنفهم أولًا **نموذج البيانات والسلوك** ثم نصمم نظامًا أصليًا مرنًا.

---

## 15. ما لم نفعله بعد — ولا ندعي أننا فعلناه

لم نصل بعد إلى:

- استخراج جميع classes/methods بصورة موثوقة.
- إعادة بناء signatures للـ IL2CPP.
- تحديد كل state machine للحركة.
- استخراج معادلات damage/stamina.
- تحديد جميع move IDs وmove timings.
- تحديد خوارزمية AI.
- تحديد كل match rules.
- تحليل كل Scene/Prefab بالتفصيل.
- اختبار اللعبة runtime خطوة بخطوة.

وهذه بالضبط هي الخطوات التالية.

---

## 16. المرحلة التالية — التحليل الحقيقي الأعمق

### A — Metadata

سنستخرج من `global-metadata.dat` ما يمكن تحديده بشكل موثوق:

- type definitions
- method names
- field names
- enum-like structures
- string tables
- علاقات الأنواع حيث يمكن إثباتها

### B — Unity data

سنفحص:

- `data.unity3d`
- `datapack.unity3d`
- `resources.resource`
- manifests
- scene/asset references المتاحة

### C — Runtime/native

سنقارن metadata مع `libil2cpp.so` لاستخراج صورة أدق عن العلاقة بين الأنواع والـ native methods، دون نشر dump أو كود proprietary في GitHub.

### D — Dynamic behavior

بعد ذلك ننتقل إلى جدول:

```text
Neutral
 → Move
 → Attack startup
 → Hit/Miss
 → Impact
 → Stun/Reaction
 → Ground/Knockdown
 → Recovery
 → Grapple
 → Throw
 → Pin
 → Match result
```

وهذا سيكون أهم جزء قبل أن نبدأ لعبتنا الأصلية.

---

## الحالة الحالية

**STATIC ANALYSIS: IN PROGRESS — تقدم حقيقي تم على الملف الفعلي.**

أصبح لدينا الآن أدلة مباشرة على:

- Unity/IL2CPP
- تقسيم AssetBundles
- نظام تخصيص الشخصيات
- الحلبة والحبال
- الصوت المرتبط بالأحداث
- Mobile controls/HUD
- stats الشخصية
- combat/move/pin/grapple indicators
- camera indicators
- opponent/target indicators

**قرار المشروع:** لا نبدأ تحويلًا إلى Godot الآن. نستمر في reverse engineering حتى تصبح خريطة الأنظمة الأساسية واضحة بدرجة كافية.