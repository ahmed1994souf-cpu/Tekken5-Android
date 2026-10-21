# خريطة IL2CPP والرموز المرتبطة باللعبة — 01

هذه المرحلة تربط الأدلة المستخرجة من `global-metadata.dat` بأنظمة اللعبة. لا تعتبر أسماء الـstrings وحدها إثباتًا لتنفيذ دالة معينة.

## 1. معلومات مؤكدة

- اللعبة: Wrestling Empire 1.8.0
- Package: `com.MDickie.WrestlingEmpire`
- Unity: `6000.3.25f1`
- Backend: IL2CPP
- `global-metadata.dat`: 7,429,976 bytes
- Metadata version: `39`
- `libil2cpp.so`: 55,048,248 bytes

## 2. أهم مجموعات الرموز

### Character / Fighter

رموز وحقول مرتبطة بالشخصية ظهرت في metadata:

- `Character`
- `Characters`
- `wrestler`
- `opponent`
- `charAnim`
- `anim`
- `animTim`
- `health`
- `Stamina`
- `Strength`
- `Agility`
- `Skill`
- `Popularity`
- `FightStyle`

**الاستنتاج:** الشخصية ليست مجرد Mesh؛ هناك طبقة بيانات/حالة تجمع الهوية والإحصائيات والأنيميشن والحالة القتالية.

الثقة: CONFIRMED لوجود الرموز، INFERRED للعلاقة المعمارية.

### Combat

رموز مهمة:

- `moveAttack`
- `moveFront`
- `moveBack`
- `moveGround`
- `moveCrush`
- `attackViable`
- `gPinPoint`
- `grapple`
- `block`
- `force`
- `gravity`
- `travel`
- `victimAngle`
- `angleDifference`
- `distance`
- `target`

**الاستنتاج:** يوجد على الأقل مفهوم مستقل لاختيار/صلاحية الحركة (`attackViable`) مع بيانات للحركة وموقع الهدف والاتجاه والمسافة.

الثقة: عالية بالنسبة لوجود المفاهيم، غير كافية لإثبات المعادلات.

### Ground / Knockdown

رموز:

- `ground`
- `OffGround`
- `moveGround`
- `Ground Moves`
- `Ground grapple with anim=`
- `falling over ropes with anim=`

هذا يدعم وجود فصل بين الحالة الواقفة والتفاعل الأرضي، لكن الانتقالات الدقيقة تحتاج اختبارًا ديناميكيًا.

### Grapple / Pin

رموز:

- `grapple`
- `broke grapple`
- `gPinPoint`
- `Pin`
- `pinned`
- `pin me`
- `your opponent`
- `maintain your grip`
- `try to hold moves`

**نموذج التحليل:**

```text
Target
  ↓
Grapple viability
  ↓
Grapple / hold
  ├─ break
  └─ move / throw
        ↓
     ground/reaction
        ↓
      pin check
```

لا نثبت أن هذا هو الـstate machine الداخلي؛ هو النموذج الأقرب الذي سنختبره.

### Ring / Ropes

رموز:

- `ringPreset`
- `ringShape`
- `ringSize`
- `ringGround`
- `ringMiddle`
- `ringTop`
- `ringCanvas`
- `ringApron`
- `ringPosts`
- `ringPads`
- `ringMat`
- `ringRopes`
- `ringAnimator`
- `ringAnim`
- `ringAnimTim`
- `ringFrame`
- `ringTransition`
- `gRope`
- `ropeX`
- `ropeY`
- `ropeZ`
- `ropeA`
- `ropeTexture`
- `ropeAnimator`
- `ropeAnim`
- `ropeAnimTim`
- `ropeFrame`
- `ropeTransition`

**الاستنتاج القوي:** الحلبة والحبال ممثلة كأنظمة متعددة المكونات، وليست مجرد Plane واحد.

### Match

رموز:

- `gMatch`
- `match`
- `matches`
- `matchSize`
- `Scene_Match_Setup`
- `optReferees`
- `winner`
- `pinned`

هذا يعطي نقطة دخول واضحة للتحليل القادم: Match Setup → Match Runtime → Result.

### Camera

رموز:

- `AdjustCamera`
- `eventCamera`
- `CameraPos`
- `Pinch`

يوجد دليل على طبقة كاميرا منفصلة وعلى دعم تفاعل لمس/تكبير، لكن من غير الصحيح استنتاج خوارزمية التتبع الدقيقة من هذه الأسماء فقط.

### Mobile Controls / UI

الأصول المؤكدة في AssetPack:

- `Controls/Virtual Buttons.prefab`
- `Controls/Controller_Overlay12.png`
- `Controls/Controller_Icon*.png`
- `Controls/Guide*.prefab`
- `Controls/Player_Meter_Right.prefab`
- `Labels/Label_Control.png`
- `Labels/Label_Pin*.png`
- `Labels/Label_Count*.png`
- `Labels/Label_Adrenaline.png`

هذا يثبت وجود طبقة تحكم/واجهة مخصصة للموبايل.

## 3. خريطة الترابط الحالية

```text
                     MATCH
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Character      Ring          Camera
          │            │            │
    ┌─────┼─────┐      │      target / position
    ▼     ▼     ▼      ▼            │
  Stats  Anim  State  Ropes         │
    │     │     │      │            │
    └─────┴─────┼──────┴────────────┘
                ▼
             COMBAT
                │
       ┌────────┼────────┐
       ▼        ▼        ▼
    Attack    Grapple   Ground
       │        │        │
       └────────┼────────┘
                ▼
          Hit / Reaction
                │
        ┌───────┴───────┐
        ▼               ▼
     Stamina/        Knockdown
      Health             │
        │                ▼
        └────────────► Recovery
                         │
                         ▼
                    Pin / Result
```

## 4. أهم الفجوات الحالية

لا تزال هذه الأمور UNKNOWN أو INFERRED:

1. الصيغة الدقيقة للـdamage.
2. علاقة Strength/Skill/Agility بالـdamage أو accuracy.
3. مدة startup/active/recovery لكل move.
4. شروط نجاح grapple.
5. خوارزمية اختيار الحركة في AI.
6. طريقة تحديد hitbox/hurtbox.
7. كيفية انتقال animation إلى reaction.
8. قواعد pin الدقيقة.
9. خوارزمية الكاميرا.
10. العلاقة الدقيقة بين native methods والرموز الموجودة في metadata.

## 5. المرحلة التالية

الخطوة القادمة ستكون إنشاء **IL2CPP Method/Type Extraction Report** أكثر تحفظًا: نحدد مناطق metadata التي يمكن تفسيرها بثقة، ثم نحاول ربطها بالـnative binary بدون نسخ أو نشر كود اللعبة الأصلي.

الهدف النهائي ليس الحصول على source code للعبة، بل مواصفات مستقلة كافية لبناء لعبة أصلية مشابهة في الأنظمة والسلوك.