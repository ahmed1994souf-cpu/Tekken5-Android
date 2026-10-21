# خريطة اللعبة — Wrestling Empire 1.8.0

> هذه خريطة تحليلية لإعادة فهم الأنظمة والسلوك، وليست نسخة من كود أو أصول اللعبة الأصلية.

## 1. الخريطة العليا

```text
BOOT
 │
 ├─ Unity Runtime / IL2CPP
 │   ├─ Data loading
 │   ├─ AssetPack loading
 │   └─ Audio / Resources / World
 │
 ▼
MAIN MENU
 │
 ├─ Roster / Character setup
 ├─ Match setup
 ├─ Career / Progression
 └─ Options / Save
 │
 ▼
MATCH INITIALIZATION
 │
 ├─ Arena / Ring
 ├─ Fighters
 ├─ Rules
 ├─ Camera
 ├─ HUD
 └─ AI
 │
 ▼
MATCH LOOP
 │
 ├─ Input
 │   ├─ Touch / virtual controls
 │   └─ Context actions
 │
 ├─ Player Controller
 │   ├─ Locomotion
 │   ├─ Targeting
 │   ├─ Attack
 │   ├─ Grapple
 │   ├─ Ground interaction
 │   └─ Recovery
 │
 ├─ Opponent AI
 │   ├─ Perception
 │   ├─ Target selection
 │   ├─ Approach / positioning
 │   ├─ Attack decision
 │   ├─ Grapple decision
 │   └─ Recovery / reaction
 │
 ├─ Combat Resolution
 │   ├─ Hit detection
 │   ├─ Damage
 │   ├─ Stamina / state changes
 │   ├─ Knockdown
 │   ├─ Grapple / throw
 │   └─ Pin / match objective
 │
 ├─ Animation
 ├─ Camera
 ├─ Audio / effects
 └─ HUD
 │
 ▼
MATCH END
 │
 ├─ Winner / loser state
 ├─ Results
 ├─ Progression update
 └─ Return / next match
```

## 2. Fighter state machine

```text
                     ┌──────────────┐
                     │    IDLE      │
                     └──────┬───────┘
                            │ input / AI
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           MOVE          ATTACK        GRAPPLE
              │             │             │
              ▼             ▼             ▼
           TURNING       HIT/MISS      HOLD/THROW
              │             │             │
              └──────┬──────┴──────┬──────┘
                     ▼             ▼
                  DAMAGE        GROUND
                     │             │
                     ▼             ▼
                  STUN/DOWN ──► RECOVERY
                     │
                     └────────► IDLE/MOVE
```

### States يجب اختبارها ديناميكيًا

| النظام | الحالات المحتملة | درجة الثقة |
|---|---|---|
| Locomotion | idle, walk/run, turn, jump/fall | عالية جزئيًا |
| Combat | neutral, attack, hit, miss, recovery | عالية كتصنيف، التفاصيل غير مكتملة |
| Grapple | approach, hold, transition, throw | مؤكد كوجود مفهوم grapple، التفاصيل تحتاج اختبار |
| Ground | down, ground interaction, recovery | مؤشرات قوية |
| Match | intro, active, advantage, end/result | مؤشرات قوية |
| AI | observe, approach, attack, recover | استنتاج معماري يحتاج اختبار |

## 3. خريطة القتال

```text
PLAYER/AI INTENT
      │
      ▼
Target acquisition
      │
      ▼
Distance / position check
      │
 ┌────┴───────────┐
 │                │
 ▼                ▼
Attack          Grapple
 │                │
 ▼                ▼
Hit test       Grapple test
 │                │
 ├─ miss          ├─ fail
 │                 │
 ▼                 ▼
Impact          Hold/transition
 │                 │
 ▼                 ▼
Damage          Throw / takedown
 │                 │
 └───────┬─────────┘
         ▼
Reaction / stun / ground
         │
         ▼
Recovery
```

### ما نريد استخراجه لاحقًا

- مدة startup لكل حركة.
- نافذة active/hit.
- recovery.
- شروط نجاح grapple.
- كيفية اختيار حركة ground.
- علاقات damage وstamina.
- شروط knockdown وrecovery.
- هل الحركة تعتمد على animation event أم منطق collision منفصل.

## 4. خريطة AI

```text
SENSE
 │
 ├─ player visible?
 ├─ distance
 ├─ relative position
 ├─ fighter state
 └─ match objective
 │
 ▼
DECIDE
 │
 ├─ approach
 ├─ reposition
 ├─ attack
 ├─ grapple
 ├─ ground action
 ├─ defend/recover
 └─ change target
 │
 ▼
ACT
 │
 ▼
OBSERVE RESULT
 │
 ├─ success → continue pressure
 ├─ miss → recovery/reposition
 ├─ damaged → reaction
 └─ target down → ground/pin/objective
```

**مهم:** هذا يصف نموذجًا تحليليًا. لا نعتبر كل فرع تنفيذًا داخليًا مؤكدًا حتى تثبته الملاحظة أو البيانات.

## 5. خريطة الحلبة

```text
                 OUTSIDE RING
       ┌──────────────────────────┐
       │        ropes / edge      │
       │   ┌──────────────────┐   │
       │   │                  │   │
       │   │      RING        │   │
       │   │                  │   │
       │   │  P        AI     │   │
       │   │                  │   │
       │   └──────────────────┘   │
       │      corners / ropes     │
       └──────────────────────────┘
```

ينبغي لاحقًا تحديد:
- أبعاد الحلبة.
- حدود الحركة.
- collision مع الحبال والزوايا.
- الخروج من الحلبة.
- التفاعل مع البيئة.
- هل الحلبة كيان واحد أم عدة colliders.

## 6. خريطة الكاميرا

```text
Player ─────┐
            ├─► Target / opponent selection
Opponent ───┘
                 │
                 ▼
          Camera positioning
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   distance    height    angle
       │         │         │
       └─────────┼─────────┘
                 ▼
          combat framing
```

سنختبر لاحقًا هل الكاميرا تستخدم target واحدًا أو midpoint بين المقاتلين، وكيف تتعامل مع المسافات والزوايا والحواجز.

## 7. خريطة البيانات والأصول

```text
AssetPack
 ├─ world
 │   └─ arena/world-related assets
 ├─ costumes
 │   └─ character customization assets
 ├─ sprites
 │   └─ UI / 2D assets
 ├─ sound
 │   └─ effects / impacts / UI
 ├─ music
 │   └─ music tracks
 └─ Unity Data
     ├─ datapack.unity3d
     └─ resources.resource
```

## 8. خريطة الشخصية

```text
Character
 ├─ identity / roster data
 ├─ visual body
 ├─ costume / equipment
 ├─ stats
 │   ├─ health-related
 │   ├─ stamina
 │   ├─ strength
 │   ├─ agility
 │   └─ skill
 ├─ locomotion
 ├─ combat state
 ├─ grapple state
 ├─ ground state
 └─ AI/controller relationship
```

## 9. خريطة الواجهة على الهاتف

```text
Touch
 │
 ├─ movement / virtual joystick
 ├─ attack
 ├─ grapple/context action
 ├─ target/context controls
 └─ menu/pause
       │
       ▼
Input abstraction
       │
       ▼
Player Controller / UI state
```

سنفصل في التحليل بين **زر الإدخال** وبين **القرار الفعلي الذي يحدث داخل اللعبة**؛ وهذا مهم جدًا عند بناء لعبتنا لاحقًا.

## 10. ما ينقص لإغلاق الخريطة

الأولوية التالية ليست بناء Godot، بل استخراج الأدلة التي تربط هذه الأنظمة ببعضها:

1. تحليل metadata الخاصة بـ IL2CPP.
2. حصر أسماء الـclasses والـmethods ذات العلاقة بالقتال والشخصيات والكاميرا وAI.
3. ربط الموارد بالأجزاء الوظيفية بدل الاكتفاء بأسماء الملفات.
4. إنشاء جدول كامل لحالات الشخصية.
5. إنشاء جدول transitions للقتال والمصارعة.
6. إنشاء جدول AI decision points.
7. اختبار match lifecycle من البداية إلى النتيجة.
8. توثيق ما هو **CONFIRMED / INFERRED / UNKNOWN**.

## قاعدة العمل

لن ننسخ كود اللعبة أو أصولها. الهدف هو الوصول إلى **مواصفات سلوكية ومعمارية** كافية لبناء لعبة أصلية مشابهة في الأنظمة والإحساس العام، مع أصول وكود مستقلين.