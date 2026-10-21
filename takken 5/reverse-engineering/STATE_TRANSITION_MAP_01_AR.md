# خريطة حالات وانتقالات القتال — الجولة 01

## الهدف
تحويل الأدلة الموجودة في `global-metadata.dat` إلى نموذج حالات قابل للاختبار. هذه ليست إعادة بناء للكود الأصلي؛ هي مواصفة سلوكية مستقلة.

## مستوى الدليل
- **CONFIRMED**: الاسم/النص موجود فعليًا في metadata.
- **STRONG INFERENCE**: عدة مؤشرات متوافقة تشير إلى نفس النظام.
- **UNKNOWN**: لا يمكن تحديد الشرط أو التوقيت من strings وحدها.

## 1. دورة المقاتل الأساسية

```text
                 ┌──────────┐
                 │  NEUTRAL │
                 └────┬─────┘
                      │ input / AI
          ┌───────────┼────────────┐
          ▼           ▼            ▼
       MOVE        ATTACK       GRAPPLE
          │           │            │
          │      ┌────┴────┐   ┌───┴────┐
          │      ▼         ▼   ▼        ▼
          │    HIT       MISS HOLD    FAIL
          │      │         │    │        │
          └──────┼─────────┼────┴────────┘
                 ▼
          REACTION / DAMAGE
                 │
        ┌────────┴────────┐
        ▼                 ▼
     STUN/HURT          GROUND
        │                 │
        └────────┬────────┘
                 ▼
             RECOVERY
                 │
                 ▼
              NEUTRAL
```

وجود `moveAttack`, `moveGround`, `moveCrush`, `attackViable`, `grapple`, `gPinPoint`, `health`, `Stamina`, `force`, `gravity`, `OffGround` يدعم هذا التقسيم، لكن أسماء الحالات الدقيقة غير مثبتة بعد.

## 2. Attack pipeline

```text
Intent
  ↓
Target / distance / angle checks
  ↓
attackViable
  ↓
moveAttack
  ↓
Animation / timing
  ↓
Impact check
  ├─ miss → recovery
  └─ hit  → force/damage/reaction
                    ↓
                 ground?
                 /     \
               yes      no
                ↓        ↓
          ground state  neutral/stun
```

### المؤكد
- `attackViable` موجود كرمز.
- `moveAttack` موجود.
- `distance`, `angleDifference`, `victimAngle` موجودة كأسماء بيانات/معاملات.
- توجد إشارات إلى `force` و`gravity` و`travel`.

### غير المؤكد
- معادلة الضرر.
- حدود المسافة الدقيقة.
- هل hit detection يعتمد بالكامل على animation events أو collision أو الاثنين.
- قيم startup/active/recovery.

## 3. Grapple pipeline

```text
NEUTRAL
   ↓
position / distance / angle
   ↓
GRAPPLE ATTEMPT
   ├── fail → recovery / neutral
   └── success
          ↓
       HOLD / GRAPPLE
          ├── break → neutral/recovery
          └── continue
                ↓
          move / throw / ground
                ↓
            victim reaction
```

`grapple`, `broke grapple`، وعبارات متعلقة بالحفاظ على السيطرة/تنفيذ الحركة تظهر ضمن metadata. هذا يدعم وجود مسار grapple مستقل، لكن تفاصيل الميكانيكية تحتاج اختبارًا ديناميكيًا.

## 4. Ground / airborne model

وجود `ground`, `OffGround`, `gravity`, `force`, `travel`، إضافة إلى أسماء حركات مثل `Falling DDT` و`Falling Neckbreaker` يشير إلى أن حالة المقاتل لا تقتصر على standing.

```text
STANDING
   │
   ├─ jump/fall ─────► AIRBORNE
   │                     │
   │                     ▼
   │                 LAND / IMPACT
   │                     │
   └───────────────► GROUND
                         │
                    recovery
                         │
                     STANDING
```

## 5. Rope / ring transition

الـmetadata يحتوي على `ringAnimator`, `ringAnim`, `ringAnimTim`, `ringFrame`, `ringTransition`, `ropeAnimator`, `ropeAnim`, `ropeAnimTim`, `ropeFrame`, `ropeTransition`, و`ringShape`, `ringSize`, `ringGround`, `ringMiddle`, `ringTop`.

النموذج السلوكي المقترح:

```text
INSIDE RING
    │
    ├─ contact rope → ROPE INTERACTION
    │                    │
    │                    └─ transition/reaction
    │
    └─ cross boundary → OUTSIDE / FALL / RESET
```

لا نثبت هنا شروط الخروج أو الضرر من الحبال قبل الاختبار.

## 6. Pin / match objective

وجود `gPinPoint` و`Pin`, `pinned`, `match`, و`gMatch` يدل على ارتباط حالة pin بحالة المباراة.

```text
OPPONENT DOWN
      ↓
PIN ATTEMPT
      ↓
PIN STATE
  ┌───┴────┐
  ▼        ▼
BREAK    SUCCESS
  │        │
  ▼        ▼
CONTINUE  MATCH RESULT
```

`gPinPoint` قد يمثل نقطة/مرجعًا مرتبطًا بالـpin، لكن معناه الدقيق غير مثبت.

## 7. AI decision loop

```text
OBSERVE
  ↓
target / distance / angle / state
  ↓
DECIDE
  ├─ approach
  ├─ attack
  ├─ grapple
  ├─ ground action
  ├─ reposition
  └─ recover
  ↓
ACT
  ↓
RESULT
  ├─ success → continue
  ├─ miss → recovery
  ├─ damage → reaction
  └─ target down → ground/pin/objective
```

`target`, `distance`, `attackViable`, `opponent` و`match` تعطي أساسًا قويًا لهذا النموذج، لكن خوارزمية الاختيار نفسها UNKNOWN.

## 8. Camera state

`AdjustCamera` موجود صراحةً، كما توجد مؤشرات `eventCamera` و`CameraPos` و`Pinch`.

```text
MATCH CAMERA
   │
   ├─ default follow
   ├─ adjusted camera
   ├─ event camera
   └─ pinch/zoom input
```

لا نثبت حاليًا أن الكاميرا تستخدم midpoint بين المقاتلين؛ هذا اختبار لاحق.

## 9. Match state machine

```text
SETUP
  ↓
INTRO / INITIALIZATION
  ↓
ACTIVE MATCH
  │
  ├─ combat loop
  ├─ pin / elimination / objective
  ├─ ring interactions
  └─ interruptions/events
  ↓
END CONDITION
  ↓
RESULT
  ↓
POST-MATCH / NEXT STATE
```

وجود `Scene_Match_Setup`, `gMatch`, `match`, `matches`, `matchSize`, `optReferees` يدعم وجود طبقة match مستقلة.

## 10. أولويات الاختبار الديناميكي

| الأولوية | الاختبار | المطلوب إثباته |
|---|---|---|
| P0 | ضربة عادية | startup → impact → reaction |
| P0 | grapple | شروط النجاح والفشل |
| P0 | إسقاط | انتقال standing → ground |
| P0 | pin | شروط البداية والكسر والنجاح |
| P1 | stamina | هل تغير اختيار/قوة الهجوم |
| P1 | ring ropes | التصادم والانتقال |
| P1 | AI | distance → decision → action |
| P1 | camera | target/position/zoom |
| P2 | special moves | اختلافها عن attack العادي |
| P2 | multi-opponent | target selection |

## النتيجة الحالية
الخريطة لم تعد مجرد قائمة أنظمة؛ أصبحت **نموذج انتقالات** يمكن استخدامه في الاختبارات. المرحلة التالية هي ربط كل انتقال ببيانات IL2CPP/metadata ثم، حيث أمكن، native code دون نسخ أو توزيع كود اللعبة الأصلي.