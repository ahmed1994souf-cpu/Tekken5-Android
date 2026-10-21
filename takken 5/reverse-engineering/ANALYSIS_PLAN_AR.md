# خطة الهندسة العكسية — مرحلة الفهم فقط

> الهدف في هذه المرحلة هو فهم اللعبة المرجعية بأكبر قدر ممكن من الدقة قبل بناء لعبة مشابهة. لا يتم تحويل الأنظمة إلى Godot الآن.

## A. خريطة المنتج كاملة

سنفصل اللعبة إلى طبقات ونوثق لكل طبقة:

1. **Boot / Runtime**
   - تسلسل الإقلاع
   - المشاهد
   - إدارة الذاكرة
   - تحميل البيانات
   - الانتقالات

2. **Characters**
   - بنية الشخصية
   - حالات الوقوف والمشي والجري والقفز والسقوط
   - حالات الضرر والـ knockdown
   - stamina/health
   - الإحصائيات والخصائص
   - العلاقات بين الشخصية والملابس/المعدات

3. **Animation**
   - قائمة الحالات
   - الانتقالات
   - blending
   - root motion أو الحركة البرمجية
   - ربط animation events بالـ hit/grapple/impact

4. **Combat / Wrestling**
   - attack startup/active/recovery
   - hitboxes/hurtboxes
   - grapple initiation
   - grapple states
   - throws/takedowns
   - ground states
   - stun/knockdown/recovery
   - damage calculation
   - stamina interaction
   - chain/sequence rules

5. **AI**
   - perception
   - target selection
   - المسافة المفضلة
   - attack choice
   - grapple choice
   - retreat/recovery
   - reaction to damage
   - ring awareness
   - objective selection

6. **Match / Rules**
   - أنواع المباريات
   - شروط الفوز
   - شروط الخسارة
   - العدادات
   - pin/submission أو الأنظمة المقابلة
   - referee/state transitions
   - بداية ونهاية المباراة

7. **Arena / World**
   - ring geometry
   - ropes/corners/objects
   - collision layers
   - خارج الحلبة
   - تفاعل الشخصيات مع البيئة

8. **Camera**
   - follow
   - combat framing
   - target selection
   - distance/height
   - transitions أثناء الحركات

9. **UI / Menus**
   - main menu
   - character selection
   - match selection
   - HUD
   - pause
   - result flow
   - save/load

10. **Progression / Data**
    - roster
    - stats
    - unlocks
    - currency/resources
    - career/progression
    - save schema

11. **Audio / Feedback**
    - attack sounds
    - impacts
    - crowd/environment
    - music states
    - UI feedback
    - vibration/haptics إن وجدت

12. **Mobile Layer**
    - touch controls
    - virtual joystick
    - gesture priority
    - orientation
    - performance profile
    - resolution/scaling

## B. ماذا سنستخرج من التحليل

لكل نظام سنسجل:

- **Observed behavior:** ما يحدث فعلياً.
- **State:** الحالات الممكنة.
- **Inputs:** ما الذي يسبب الانتقال.
- **Outputs:** ما الذي يتغير.
- **Timing:** المدد والفواصل عندما يمكن قياسها.
- **Dependencies:** الأنظمة التي يعتمد عليها.
- **Confidence:** مؤكد / مرجح / يحتاج اختبار.

## C. التحليل الساكن Static Analysis

بعد توفير XAPK/APK الأصلي للتحليل، سنفحص دون تعديل الملف الأصلي:

- AndroidManifest وpackage metadata.
- split APK structure.
- Unity version.
- IL2CPP/native library presence.
- AssetPack structure.
- resources وStreamingAssets وdata files.
- أسماء الملفات والـ metadata القابلة للقراءة.
- managed/native symbol information إن كانت متاحة قانونياً وتقنياً.
- references بين الأنظمة عندما يمكن استنتاجها.

لا نضع binary الأصلي أو dumps محمية داخل GitHub.

## D. التحليل الديناميكي Dynamic Analysis

إذا كانت لدينا نسخة قابلة للتشغيل، سنوثق السلوك من خلال سيناريوهات اختبار منظمة:

### Movement Matrix
- idle → walk
- walk → run
- run → stop
- turn
- jump/fall
- collision

### Combat Matrix
- neutral → attack
- attack → hit
- attack → miss
- hit → stun
- stun → recovery
- neutral → grapple
- grapple → throw
- throw → ground/recovery

### AI Matrix
- far
- approach
- attack range
- player attacks
- AI damaged
- player down
- AI down
- multiple targets

### Match Matrix
- match start
- normal combat
- advantage/disadvantage
- win condition
- loss condition
- reset

## E. لا ننتقل للبناء قبل اكتمال هذه الخريطة

الهدف النهائي لهذه المرحلة هو إنتاج **Game Design Reverse Map** مستقل يشرح كيف تعمل اللعبة من الداخل على مستوى السلوك والأنظمة، وليس نسخ كودها أو أصولها.

عند اكتمال الخريطة سنستخدمها كمرجع لتصميم لعبة جديدة أصلية بنفس العمق، مع شخصيات وأصول وقواعد وهوية خاصة بنا.
