# خريطة ترابط الأنظمة — المرحلة 02

## الهدف

هذه المرحلة تحول خريطة اللعبة العامة إلى شبكة علاقات بين الأنظمة، حتى نعرف ماذا يجب أن نفهم أولًا وماذا يعتمد على ماذا.

> لا تعني الأسهم أن التنفيذ الداخلي مطابق حرفيًا؛ هي علاقات تحليلية مبنية على الأدلة المتوفرة حاليًا.

## 1. الرسم الرئيسي

```text
                    ┌────────────────────┐
                    │  GAME / MATCH      │
                    │    STATE           │
                    └─────────┬──────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     PLAYER INPUT           AI               MATCH RULES
          │                   │                   │
          └──────────┬────────┴──────────┬────────┘
                     ▼                   │
                CHARACTER               │
                     │                   │
       ┌─────────────┼─────────────┐     │
       ▼             ▼             ▼     │
  LOCOMOTION     COMBAT       TARGETING  │
       │             │             │     │
       │       ┌─────┼─────┐       │     │
       │       ▼     ▼     ▼       │     │
       │    ATTACK GRAPPLE GROUND  │     │
       │       │     │      │      │     │
       └───────┴─────┴──────┴──────┘     │
                     │                   │
                     ▼                   │
              ANIMATION / PHYSICS        │
                     │                   │
                     ▼                   │
              COMBAT RESOLUTION ◄────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       HEALTH      STAMINA    POSITION
          │          │          │
          └──────────┼──────────┘
                     ▼
               REACTION STATE
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       STUN/DOWN   GROUND     RECOVERY
                     │
                     ▼
                 MATCH STATE
```

## 2. الأولويات حسب الاعتماد

### المستوى A — النواة

1. Match/Game State
2. Character State
3. Input abstraction
4. Target/opponent relationship

بدون هذه الطبقة لا يمكن تفسير بقية الأنظمة.

### المستوى B — الحركة والقتال

5. Locomotion
6. Attack selection/execution
7. Grapple
8. Ground
9. Hit/reaction

### المستوى C — الحلبة والكاميرا

10. Ring geometry
11. Ropes/corners/boundaries
12. Camera/target framing

### المستوى D — العرض

13. Animation
14. Audio/events
15. HUD/touch UI

### المستوى E — الأنظمة العليا

16. Match rules
17. Results
18. Progression/save
19. Menus/setup

---

## 3. Character Dependency Graph

```text
Character
 │
 ├── Stats
 │    ├── Health
 │    ├── Stamina
 │    ├── Strength
 │    ├── Agility
 │    └── Skill
 │
 ├── State
 │    ├── Ground/OffGround
 │    ├── Target
 │    ├── Attack
 │    ├── Grapple
 │    └── Recovery
 │
 ├── Animation
 │    ├── anim
 │    ├── animTim
 │    └── charAnim
 │
 └── Moves
      ├── moveAttack
      ├── moveFront
      ├── moveBack
      ├── moveGround
      └── moveCrush
```

الأسماء أعلاه ظهرت في metadata التي تم تحليلها؛ أما العلاقة الدقيقة بينها فتحتاج مطابقة method/field definitions.

## 4. Ring Dependency Graph

```text
Ring Preset
    │
    ├── Shape / Size
    ├── Ground / Middle / Top
    ├── Canvas / Apron
    ├── Posts / Pads
    └── Ropes
           │
           ├── Rope position
           ├── Rope animator
           └── Rope transition
                    │
                    ▼
              Fighter position
                    │
              ┌─────┴─────┐
              ▼           ▼
        Inside ring    Outside ring
```

هذه نقطة مهمة جدًا: يجب ألا نفترض أن collision الحلبة جسم واحد قبل فحص التنفيذ.

## 5. Combat Dependency Graph

```text
Input / AI
   │
   ▼
Move intent
   │
   ▼
Attack viability
   │
   ├── distance
   ├── angle difference
   ├── victim angle
   ├── target
   └── current state
   │
   ▼
Move execution
   │
   ├── animation
   ├── force
   ├── travel
   └── impact
   │
   ▼
Victim reaction
   │
   ├── health
   ├── stamina
   ├── stun
   ├── ground
   └── recovery
```

وجود `distance`, `angleDifference`, `victimAngle`, `attackViable`, `force`, و`travel` في metadata يجعل هذا مسارًا بحثيًا ذا أولوية عالية، لكنه لا يثبت الصيغة الرياضية التي تستخدمها اللعبة.

## 6. AI Dependency Graph

```text
AI
 │
 ├── Target
 │
 ├── Distance
 │
 ├── Opponent state
 │
 ├── Attack viability
 │
 ├── Match objective
 │
 └── Recovery
       │
       ▼
    Decision
       │
       ├── Move
       ├── Attack
       ├── Grapple
       ├── Ground action
       └── Reposition
```

حتى الآن لا نضع أسماء classes محددة في هذه الطبقة بدون دليل من metadata/method mapping.

## 7. Camera Dependency Graph

```text
Player ─────┐
            ├── target selection ──► AdjustCamera
Opponent ───┘
                       │
                       ├── distance
                       ├── angle
                       └── framing
```

`AdjustCamera` ظهر في metadata، لذلك ستكون هذه إحدى نقاط البحث في method dump.

## 8. Audio Event Graph

```text
Gameplay event
 │
 ├── Attack/Impact ──► Impact sound
 ├── Fall ───────────► Fall sound
 ├── Rope contact ───► Rope sound
 ├── Pin ─────────────► Referee/Count
 ├── Crowd event ────► Crowd sound
 └── Menu event ─────► UI sound
```

الأصول الصوتية نفسها تؤكد وجود مجموعات لهذه الأحداث، لكن ربطها بالـmethods يحتاج المرحلة التالية.

## 9. Mobile Input Graph

```text
Touch
 │
 ▼
Virtual Buttons / Controller Overlay
 │
 ▼
Input state
 │
 ├── movement
 ├── attack
 ├── grapple/context
 └── menu
 │
 ▼
Character / Match controller
```

## 10. أهم نقاط البحث القادمة

### P0 — أعلى أولوية
- `Character`
- `Characters`
- `gMatch`
- `gPinPoint`
- `attackViable`
- `moveAttack`
- `moveGround`
- `moveCrush`
- `grapple`
- `AdjustCamera`

### P1
- `health`
- `Stamina`
- `Strength`
- `Agility`
- `Skill`
- `distance`
- `angleDifference`
- `victimAngle`
- `force`
- `travel`
- `target`

### P2
- ring/rope animator and transition methods
- HUD and controller methods
- audio event routing
- menu/setup and progression

## 11. أسئلة يجب أن نجيب عنها

1. هل `attackViable` مجرد Boolean أم نتيجة حساب عدة شروط؟
2. هل `moveAttack` يشير إلى current move أم جدول moves؟
3. كيف ترتبط `anim`, `animTim`, و`charAnim`؟
4. هل `gPinPoint` كائن/نقطة فعلية أم مرجع gameplay؟
5. هل `gMatch` هو singleton/global reference؟
6. أين يتم حساب الضرر؟
7. أين يتم تعديل stamina؟
8. أين يتم إنشاء/إنهاء grapple؟
9. ما الذي يقرر انتقال fighter إلى ground؟
10. كيف تتعامل اللعبة مع rope transitions؟
11. هل AI يستدعي نفس move system الخاص باللاعب؟
12. هل camera تعتمد على player فقط أم player+opponent؟

## 12. معيار الإثبات

كل اكتشاف جديد سيحصل على واحدة من:

- **CONFIRMED** — ظهر مباشرة في البيانات/السلوك.
- **STRONG INFERENCE** — عدة أدلة مستقلة تدعمه.
- **INFERRED** — تفسير معماري محتمل.
- **UNKNOWN** — لا توجد أدلة كافية.

لن نحول UNKNOWN إلى حقيقة لمجرد أن التصميم يبدو منطقيًا.

## 13. النتيجة الحالية

الخريطة الآن لم تعد مجرد قائمة أنظمة. أصبحت لدينا شبكة dependency تحدد أين نبحث أولًا، وما الذي يعتمد على ماذا.

الخطوة التالية الصحيحة هي بناء **Method/Class Catalog** من metadata وربط الأسماء السابقة بالـtypes والـmethods والحقول، ثم استخدام هذا الكتالوج لتحديث الخريطة إلى مستوى أدق.