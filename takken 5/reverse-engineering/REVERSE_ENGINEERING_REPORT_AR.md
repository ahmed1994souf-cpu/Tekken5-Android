# تقرير التحليل الأولي — Wrestling Empire 1.8.0

## 1. نتائج مؤكدة من XAPK

| العنصر | النتيجة |
|---|---|
| Package | `com.MDickie.WrestlingEmpire` |
| Version | `1.8.0` / code 87 |
| Engine | Unity 6000.3.25f1 |
| Scripting backend | IL2CPP (وجود `libil2cpp.so`) |
| CPU | ARM64 (`arm64-v8a`) |
| minSdk | 32 |
| targetSdk | 36 |
| البيانات | Unity AssetPack منفصل |

## 2. الطبقات المعمارية التي سنعيد بناءها

### Runtime
- Game loop / state machine
- Match state
- Character state machine
- Physics and collision
- Animation state machine
- Camera controller
- Input abstraction

### Combat
- Light/heavy attacks
- Grapple / grab
- Throws and takedowns
- Hit detection
- Damage/stamina/recovery
- Knockdown / recovery
- Blocking/defense
- Finisher/special action layer

### AI
- Perception
- Target selection
- Distance management
- Attack selection
- Grapple decision
- Recovery
- Ring awareness
- Match objective

### Match
- Ring bounds
- Referee/match rules layer
- Win/loss state
- Round/match transitions
- Respawn/reset
- Result screen

### Mobile
- Virtual joystick
- Context-sensitive action buttons
- Camera drag
- Touch priority/gesture arbitration
- Low-end Android performance profile

## 3. ما الذي لا ينبغي نسخه

لا ننسخ `libil2cpp.so`، ملفات Unity الأصلية، الشخصيات، الأصوات، النصوص، أو AssetBundles إلى مشروعنا. بدل ذلك، نستخدم النتائج لتحديد **السلوك والواجهات والبيانات** ثم نكتب تنفيذ Godot مستقل.

## 4. خريطة إعادة التنفيذ المقترحة

```text
Takken5Game
├── Core
│   ├── GameState
│   ├── MatchState
│   └── SaveSystem
├── Character
│   ├── CharacterController
│   ├── CharacterStateMachine
│   ├── HitboxSystem
│   └── AnimationDriver
├── Combat
│   ├── AttackDefinition
│   ├── GrappleSystem
│   ├── ThrowSystem
│   ├── DamageSystem
│   └── RecoverySystem
├── AI
│   ├── Perception
│   ├── DecisionBrain
│   └── CombatPlanner
├── Camera
│   ├── FollowCamera
│   └── CombatCamera
├── Mobile
│   ├── VirtualJoystick
│   ├── ActionButtons
│   └── TouchRouter
└── Match
    ├── Ring
    ├── Rules
    └── ResultFlow
```

## 5. ترتيب التنفيذ

1. حركة شخصية + كاميرا + joystick.
2. خصم واحد يتتبع اللاعب.
3. ضربات مع hitbox/hurtbox.
4. grapple + throw.
5. AI يختار بين الحركة/الهجوم/المسك/التراجع.
6. حلبة ومحددات ring bounds.
7. match state + الفوز والخسارة.
8. تحسين animation blending.
9. تحسين الأداء للهاتف.
10. توسيع roster والمباريات.

## 6. معيار النجاح

لا نعتبر المرحلة ناجحة لمجرد فتح التطبيق. يجب أن يستطيع المستخدم على الهاتف:

- تحريك اللاعب بالـ joystick.
- تدوير الكاميرا بالسحب.
- الاقتراب من الخصم.
- تنفيذ أكثر من حركة قتالية متتابعة.
- جعل الخصم يقرر ويتصرف بدل تنفيذ حركة واحدة ثابتة.
- إنهاء المباراة وإعادة ضبطها بدون إعادة تشغيل التطبيق.
