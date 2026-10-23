# تحليل استبدال موديلات الشخصيات — المرحلة 73

## الهدف
متابعة إثبات العلاقة بين `Costume.shape[]` وMesh assets الفعلية داخل `assets/costumes` في Wrestling Empire Android 1.8.0، مع التركيز على `shape[3] -> Head Mesh`.

## نتيجة جديدة مهمة: تم فك ضغط Block Info بنجاح
الملف الفعلي الذي تم تحليله:
- `UnityDataAssetPack.apk`
- `assets/costumes`
- الحجم: `24,980,257` بايت

Header الخاص بـ UnityFS يؤكد:
- UnityFS version: 8
- Unity revision: `6000.3.25f1`
- archive size: `24,980,257`
- compressed block-info size: `88`
- uncompressed block-info size: `153`
- flags: `0x243`
- بسبب محاذاة UnityFS الحديثة، يبدأ Block Info المضغوط عند offset `64`.

تم فك Block Info باستخدام **LZ4 raw block** مع `uncompressed_size=153` بنجاح. هذا يصحح المحاولة السابقة التي استخدمت slice/offset غير صحيح.

### Block Info المفكوك
البداية:
- 16-byte hash = أصفار في هذا الملف.
- block count = `1`.
- بيانات البلوك التالية هي:
  - `0x051A61B4` = `85,615,028`
  - `0x017D2A81` = `24,980,097`
  - flags = `0x0041`

ملاحظة مهمة: ترتيب/دلالة حجمي block ما زال يحتاج تثبيتاً من Unity 6 parser، لأن القيمة الأولى أكبر من حجم bundle بينما الثانية تساوي تقريباً كامل مساحة البيانات المتبقية. المؤشر العملي القوي هو أن block data يبدأ عند offset `152`، وأن طوله المتوافق مع bundle هو `24,980,097` بايت. لذلك لا نعتمد بعد على تسمية الحقلين compressed/uncompressed بشكل نهائي.

## Data block
- يبدأ عند offset `152`.
- طول البيانات المتاح المتوافق مع قيمة الحجم الثانية: `24,980,097` بايت.
- بداية البيانات:
  `00 00 00 00 00 00 00 00 5D 00 00 08 00 00 00 6C 01 23 FB...`

محاولات فك هذه الطبقة باستخدام Python LZMA/LZ4 المباشر لم تعطِ SerializedFile صالحاً بعد. لذلك **لم يتم الادعاء بأننا استخرجنا الـMesh نفسه**.

## ما أصبح مثبتاً
1. `assets/costumes` ليس مجرد manifest؛ هو UnityFS AssetBundle حقيقي.
2. يوجد Block Info مضغوط يمكن فكّه فعلياً.
3. يوجد block واحد يغطي تقريباً كامل bundle.
4. `assets/costumes` يحتوي SerializedFile سابقاً تم تحديده:
   - object count = `877`
   - `788 Texture2D`
   - `88 Mesh`
   - `1 AssetBundle`
5. أسماء الـ88 Mesh تتطابق مع مسارات Mesh في manifest، ومنها 15 Head Mesh.
6. `Costume.shape[]` جزء من البيانات serialized الفعلية في `datapack.unity3d`.
7. `shape[3]` يستخدم القيم `0..14` فقط، وعددها يساوي عدد Head Meshes وهو 15.

## Head Meshes
الأسماء المؤكدة من manifest:
- Head_Giant
- Head_Fat
- Head_Female
- Head_Squashed
- Head_Gaunt
- Head_Wide
- Head_Narrow
- Head_Chubby
- Head_Slim
- Head_Sarge
- Head_Hairy
- Head_Nose
- Head_Thug
- Head_Jaw
- Head_Normal

**لا تزال مطابقة ID الرقمي 0..14 مع هذه الأسماء غير مثبتة.** ترتيب manifest وحده ليس دليلاً كافياً.

## الخطوة التالية
1. بناء parser أدق لـ Unity 6 AssetBundle block data، وتحديد معنى flags `0x41` وترتيب أحجام block.
2. الوصول إلى SerializedFile `CAB-4804a9fe55f251a9b5aff63c07138759` داخل bundle.
3. استخراج Object IDs الخاصة بالـ88 Mesh.
4. مقارنة Object IDs/containers مع بيانات `shape[3]` في `datapack.unity3d`.
5. إثبات mapping `shape[3] -> Head Mesh` بدليل مرجعي مباشر.
6. بعد تثبيت الرأس، تكرار نفس المنهج لباقي `shape[]` (Hair/Body/Arms/Legs وغيرها).

## الحالة الحالية
- Character/Costume data map: ~90%
- `shape[]` serialized proof: ~95%
- فهم UnityFS header + block-info: ~90%
- الوصول إلى Mesh object mapping: ~50%
- `shape[3] -> Head ID`: ~80% كفرضية، وليس إثباتاً نهائياً
- `Head ID -> Mesh name`: ~40%
- بقية shape indices: ~30%
- استخراج/استبدال موديل فعلي: 0% حتى الآن

**لا يوجد تعديل على APK أو موديلات اللعبة في هذه المرحلة؛ التركيز ما زال على استخراج خريطة صحيحة قبل الاستبدال.**
