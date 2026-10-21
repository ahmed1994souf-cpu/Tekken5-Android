# مواصفة أنظمة اللعب المستقلة — Wrestling Empire 1.8.0 (المرحلة 05)

## الغرض
تحويل القرائن الموجودة في تقارير metadata وملفات manifests إلى تصميم قابل للتنفيذ والاختبار في مشروع Godot مستقل. هذه المواصفة لا تدعي إعادة بناء الكود الأصلي حرفيًا.

## درجات الثقة
- **مؤكد (رمزي/ملفي):** الاسم أو الأصل ظهر في البيانات التي سبق توثيق فحصها.
- **استنتاج تصميمي:** نموذج جديد معقول يفسر القرائن، لكنه ليس إثباتًا لتنفيذ اللعبة الأصلي.
- **غير محسوم:** يتطلب تحليل دوال IL2CPP أو اختبارًا أثناء تشغيل اللعبة.

## 1. مكونات الشخصية المقترحة
القرائن الرمزية الموثقة تشمل health, Stamina, Strength, Agility, Skill, Popularity, FightStyle, charAnim, moveAttack, moveFront, moveBack, moveGround, moveCrush, attackViable, target, ground, وOffGround.

نموذج التنفيذ المستقل:
- **Stats:** health, stamina, strength, agility, skill.
- **Locomotion:** idle, walk, run, turn, airborne, falling, grounded.
- **Combat:** neutral, windup, attack, block, grapple, stunned, downed, recovery.
- **Targeting:** target الحالي، المسافة، فرق الاتجاه، صلاحية الحركة.
- **Match role:** wrestler, opponent, referee.
- **Customization:** fight style ومظهر قابل للتركيب.

وجود هذه الأسماء مؤكد في القرائن السابقة؛ تقسيمها إلى هذه المكونات هو اقتراح تصميمي.

## 2. حالات المباراة المقترحة
```text
PRE_MATCH
  -> ACTIVE
ACTIVE
  -> GRAPPLE
  -> PIN_ATTEMPT
  -> SUBMISSION_ATTEMPT
  -> OUTSIDE_RING
  -> KNOCKDOWN
  -> FINISH
PIN_ATTEMPT
  -> ACTIVE        (kick-out / interruption)
  -> FINISH        (pin succeeds)
GRAPPLE
  -> ACTIVE        (escape / release / move resolves)
  -> KNOCKDOWN
OUTSIDE_RING
  -> ACTIVE        (return to ring)
  -> FINISH        (count-out, only if match rules enable it)
```

هذا مخطط اختبار للعبة جديدة، وليس خريطة انتقالات مؤكدة للعبة الأصلية. شروط الفوز الدقيقة وعدّ الحكم يجب أن تبقى قابلة للضبط حسب نوع المباراة.

## 3. الحلبة والحدود
القرائن تشمل ringShape, ringSize, ringGround, ringMiddle, ringTop, ringRopes, ropeAnimator, ropeTransition، إضافة إلى نصوص inside the ring, outside the ring, وfalling over ropes.

للتنفيذ المستقل، افصل الحلبة إلى:
1. سطح اللعب الرئيسي مع collision.
2. أربعة جوانب/حواف.
3. حبال مستقلة ذات تصادم مرن أو انتقالات حركة.
4. منطقة خارج الحلبة.
5. نظام قواعد يقرر إن كان الخروج يؤثر في العد أو نتيجة المباراة.

لا تفترض أن أسماء ringTop أو ringMiddle تعني تلقائيًا طوابق تصادم؛ تحقق منها لاحقًا إن توفرت دوال metadata.

## 4. AI قابل للاختبار
قرائن مثل opponent, target, distance, angleDifference, وattackViable تدعم اختبار نموذج AI قائم على المسافة والاتجاه، لكنها لا تثبت خوارزمية اللعبة الأصلية.

الحالات المقترحة:
- APPROACH: الاقتراب عندما يكون الهدف بعيدًا.
- ORIENT: الدوران نحو الهدف.
- EVALUATE: فحص المسافة والاتجاه والتحمل وحالة الهدف.
- ATTACK: تنفيذ حركة صالحة.
- DEFEND: حجب أو تفادي هجوم متوقع.
- RECOVER: التعافي بعد السقوط أو الحركة.
- RING_RETURN: الرجوع إلى الحلبة إن كانت قواعد المباراة تتطلب ذلك.

كل انتقال يجب أن يسجل سببًا في debug log؛ هذا يساعد على اكتشاف سلوك الدوران المستمر أو الهجمات المتكررة.

## 5. إدارة الحركات
القرائن تشمل moveAttack, moveGround, moveCrush, attackViable ونصوص تعليمية عن BUTTON وDIRECTION وGRAPPLE. كما وثق التقرير السابق أسماء حركات مثل Suplex وFigure 4 Leglock.

في المشروع المستقل، اجعل كل حركة بيانات منفصلة تحتوي على:
- معرف الحركة واسمها.
- الفئة: strike / grapple / aerial / ground / submission.
- شروط البدء (مسافة، اتجاه، حالة الخصم).
- استهلاك stamina.
- مدة التحضير والتنفيذ والتعافي.
- نافذة التصادم والضرر/التأثير.
- إمكانية الإلغاء أو الإفلات.
- حركة/أنيميشن بديلة عند غياب أصل مناسب.

لا يمكن استنتاج أرقام الضرر أو توقيتات الأنيميشن من أسماء النصوص وحدها.

## 6. الخطوة الفنية التالية
1. تشغيل workflow على takken 5/global-metadata.dat والتحقق من بصمة SHA-256، magic، version word، وحجم الملف.
2. تنزيل artifact الناتج ومراجعة قائمة السلاسل المطابقة.
3. تحديد مكان libil2cpp.so الحقيقي ضمن split config.arm64_v8a.apk؛ تقرير inventory الحالي يصفه داخل الحزمة لكنه لا يثبت وجود ملف المكتبة الثنائية منفردًا في جذر المستودع.
4. استخدام محلل متوافق مع metadata v39 وملف المكتبة المطابق.
5. لا تنشر عناوين native أو أسماء دوال كحقائق إلا بعد أن يثبتها ناتج parser قابل لإعادة الإنتاج.

## ملاحظة عن الأصول
هذه المواصفة تصف سلوكًا وبنية عامة فقط. عند تنفيذ مشروع Godot، استخدم نماذج ورسومًا وأصواتًا أصلية أو مرخصة، ولا تضمّن ملفات اللعبة الأصلية أو كودها المفكك في المشروع.
