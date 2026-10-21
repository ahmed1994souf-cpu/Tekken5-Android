# كتالوج Classes / Methods — المرحلة 01

> الغرض: تنظيم الرموز التي ظهرت في تحليل metadata وربطها بأنظمة اللعبة. هذا ليس استخراجًا للكود الأصلي.

## 1. Character / Fighter

| الرمز | النوع التحليلي | النظام | الثقة |
|---|---|---|---|
| `Character` | Class/Type indicator | الشخصية | CONFIRMED |
| `Characters` | Collection/manager indicator | قائمة الشخصيات | CONFIRMED |
| `wrestler` | field/reference indicator | المقاتل | CONFIRMED |
| `opponent` | field/reference indicator | الخصم | CONFIRMED |
| `health` | field/state indicator | الصحة | CONFIRMED |
| `Stamina` | field/state indicator | التحمل | CONFIRMED |
| `Strength` | stat indicator | القوة | CONFIRMED |
| `Agility` | stat indicator | الرشاقة | CONFIRMED |
| `Skill` | stat indicator | المهارة | CONFIRMED |
| `Popularity` | stat indicator | التقدم/الشخصية | CONFIRMED |
| `FightStyle` | style indicator | أسلوب القتال | CONFIRMED |

## 2. Match

| الرمز | المعنى المحتمل | الثقة |
|---|---|---|
| `gMatch` | مرجع/حالة المباراة العامة | CONFIRMED symbol, semantics INFERRED |
| `match` | حالة/مرجع مباراة | CONFIRMED |
| `matches` | مجموعة مباريات | CONFIRMED |
| `matchSize` | حجم/عدد المشاركين أو تكوين المباراة | CONFIRMED symbol, semantics UNKNOWN |
| `bookingOpponent` | خصم مرتبط بالحجز/المباراة | CONFIRMED symbol, semantics INFERRED |
| `optReferees` | خيارات الحكام | CONFIRMED |
| `Scene_Match_Setup` | مشهد إعداد المباراة | CONFIRMED |

## 3. Combat

| الرمز | النظام | ما نستطيع قوله الآن |
|---|---|---|
| `moveAttack` | هجمات | توجد فئة/مرجع مرتبط بحركات الهجوم |
| `moveFront` | حركة أمامية | مرتبط بحركة/اتجاه |
| `moveBack` | حركة خلفية | مرتبط بحركة/اتجاه |
| `moveGround` | Ground moves | توجد فئة/مرجع لحركات أرضية |
| `moveCrush` | Crush/impact move | توجد فئة/مرجع للحركات المصنفة Crush |
| `attackViable` | قرار صلاحية الهجوم | مؤشر قوي على فحص صلاحية الهجوم |
| `grapple` | مصارعة/إمساك | وجود مفهوم grapple مؤكد |
| `broke grapple` | كسر الإمساك | النص يؤكد وجود حالة/تعليمات مرتبطة بكسر grapple |
| `gPinPoint` | نقطة/حالة pin | وجود مفهوم pin مؤكد |
| `pin` / `pinned` | Pin | وجود حالات مرتبطة بالتثبيت |

### نموذج الانتقال الذي سنختبره

```text
Neutral
  -> attack viability check
  -> attack / grapple
  -> impact or transition
  -> damage / stun / ground
  -> recovery
```

لا نعتبر أزمنة أو شروط الانتقال الدقيقة معروفة بعد.

## 4. Ring / Ropes

| الرمز | النظام |
|---|---|
| `ringPreset` | إعداد الحلبة |
| `ringShape` | شكل الحلبة |
| `ringGround` | أرضية الحلبة |
| `ringMiddle` | مستوى/جزء متوسط من الحلبة |
| `ringTop` | جزء علوي |
| `ringAnimator` | مؤشر Animator للحلبة |
| `ringAnim` | مؤشر animation للحلبة |
| `ringRopes` | نظام الحبال |
| `gRope` | مرجع/حالة rope |
| `ropeAnimator` | Animator للحبال |
| `ropeAnim` | animation للحبال |
| `ropeTransition` | انتقال مرتبط بالحبال |
| `ringPosts` | أعمدة الحلبة |
| `ringPads` | وسادات/أجزاء الأعمدة |
| `ringMat` | مادة الحلبة |
| `ringApron` | apron |
| `ringCanvas` | canvas/logo/جزء بصري |

وجود هذه الرموز يؤكد أن الحلبة ممثلة بأجزاء متعددة، لكن تفاصيل الـcomponent hierarchy تحتاج تحليلًا إضافيًا.

## 5. Movement / Physics

| الرمز | النظام | الثقة |
|---|---|---|
| `distance` | المسافة بين كيانات/أهداف | CONFIRMED |
| `angleDifference` | فرق الزاوية | CONFIRMED |
| `victimAngle` | زاوية الضحية/المتلقي | CONFIRMED |
| `gravity` | الجاذبية | CONFIRMED |
| `force` | قوة/دفع | CONFIRMED |
| `travel` | انتقال/حركة | CONFIRMED |
| `ground` | حالة/سطح الأرض | CONFIRMED |
| `OffGround` | حالة خارج الأرض | CONFIRMED |

## 6. Targeting / AI

| الرمز | الاستخدام التحليلي |
|---|---|
| `target` | الهدف الحالي أو المرجع المستهدف |
| `opponent` | الخصم |
| `attackViable` | هل الهجوم صالح في الحالة الحالية |
| `distance` | شرط المسافة |
| `angleDifference` | شرط الاتجاه |
| `victimAngle` | محاذاة الضحية |

### فرضية AI قابلة للاختبار

```text
Acquire target
  ↓
Check distance + angle
  ↓
Check target state
  ↓
Check attack/grapple viability
  ↓
Choose action
  ↓
Observe result
  ↓
Reposition / repeat
```

هذه **فرضية سلوكية** وليست ادعاءً بأن AI الداخلي مكتوب بهذه الخطوات حرفيًا.

## 7. Camera

`AdjustCamera` هو أقوى مؤشر وصلنا إليه حاليًا على وجود منطق مخصص لضبط الكاميرا.

ما نحتاج إثباته:
- target camera أم midpoint.
- distance/height limits.
- transition أثناء grapple/ground/pin.
- التعامل مع خروج المقاتل من الحلبة.

## 8. Input / Mobile

الأصول التي تم توثيقها سابقًا تشمل:

- `Controls/Virtual Buttons.prefab`
- `Controls/Controller_Overlay12.png`
- `Controls/Controller_Icon*.png`
- `Controls/Guide*.prefab`
- `Player_Meter_Right.prefab`

وهذا يسمح بتثبيت وجود طبقة Mobile UI/Input، لكن mapping كل زر إلى method معين لم يثبت بعد.

## 9. Event-oriented systems

الأسماء الصوتية والـHUD تعطي أحداثًا مرشحة:

```text
Attack/Impact
   ├─ SFX
   ├─ animation reaction
   ├─ health/stamina update
   └─ camera/UI feedback

Pin
   ├─ referee voice
   ├─ count
   ├─ HUD label
   └─ match state

Fall/Rope
   ├─ impact/rope SFX
   ├─ movement state
   └─ possible boundary transition
```

طريقة الربط البرمجية نفسها UNKNOWN حتى يتم تحليل method bodies أو dynamic traces.

## 10. الأولويات التالية

1. استخراج **TypeDefinition/MethodDefinition** المرتبطة بـ `Character`, `gMatch`, `AdjustCamera`.
2. معرفة signatures والـfield types بدل الاعتماد على أسماء النصوص فقط.
3. ربط method إلى native address عند توفر بيانات IL2CPP المناسبة.
4. بناء State Transition Catalog.
5. بناء Combat Timing Catalog.
6. بناء AI Decision Catalog.
7. فصل كل نتيجة إلى CONFIRMED / INFERRED / UNKNOWN.

## قاعدة قانونية/تقنية

لن نخزن أو ننشر كودًا مفكوكًا من اللعبة أو أصولها المحمية. الكتالوج هنا يصف البنية والسلوك والأسماء الوظيفية اللازمة لفهم الأنظمة ثم تنفيذ لعبة أصلية مستقلة.