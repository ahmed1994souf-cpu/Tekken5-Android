# Takken 5 — Reverse Engineering / Reimplementation Lab

هذا المجلد مخصص لتحليل بنية لعبة Wrestling Empire 1.8.0 المرفوعة من المستخدم، ثم إعادة بناء الأنظمة المطلوبة بشكل مستقل داخل مشروعنا. لا يتم وضع ملفات اللعبة الأصلية أو كودها المفكك أو خاماتها المحمية داخل المستودع.

## المصدر الذي تم تحليله
- الحزمة: `Wrestling Empire 1.8.0`
- Package: `com.MDickie.WrestlingEmpire`
- XAPK يحتوي على 3 APKs: base + UnityDataAssetPack + arm64-v8a
- Unity: `6000.3.25f1`
- Target SDK: 36
- Min SDK: 32
- المعمارية: ARM64

## بنية الحزمة المكتشفة

```text
Wrestling Empire XAPK
├── com.MDickie.WrestlingEmpire.apk
├── UnityDataAssetPack.apk
│   ├── assets/bin/Data/datapack.unity3d
│   ├── assets/bin/Data/resources.resource
│   ├── assets/costumes
│   ├── assets/music
│   ├── assets/sound
│   ├── assets/sprites
│   └── assets/world
└── config.arm64_v8a.apk
    ├── lib/arm64-v8a/libil2cpp.so
    └── lib/arm64-v8a/libunity.so
```

## هدفنا
إعادة بناء **الأنظمة** وليس نسخ ملفات اللعبة: شخصية، حركة، كاميرا، قتال، مسك/رمي، AI، حلبة، مباريات، واجهة الهاتف، وحفظ الحالة. يمكن استخدام التحليل لفهم السلوك والاعتماديات، ثم كتابة تنفيذ جديد خاص بنا.

## المرحلة الحالية
1. تحليل الحزمة وتحديد Unity/IL2CPP/AssetPack.
2. استخراج خريطة الأنظمة والبيانات اللازمة لإعادة التنفيذ.
3. تحويل النتائج إلى مواصفات Godot مستقلة.
4. بناء Prototype صغير قابل للتشغيل على Android.
5. إضافة الأنظمة بالتدريج مع اختبارات للهاتف.

## ملاحظة قانونية/تقنية
لن ننسخ أو نوزع كودًا مفككًا، مفاتيح توقيع، أو خامات أصلية محمية. أي شخصيات/خامات/أصوات في مشروعنا يجب أن تكون أصلية أو مرخصة.
