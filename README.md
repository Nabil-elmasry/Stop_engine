# 🚗 StopEngine with AI

نظام ذكي يعمل بتقنيات الذكاء الاصطناعي للتشخيص المبكر لانحراف قراءات حساسات السيارات قبل حدوث الأعطال الفعلية،  
ويقدم رؤية استباقية تساعد الفني أو المستخدم في اتخاذ قرار قبل ظهور كود العطل أو إضاءة لمبة 

Check Engine.

---

## ✨ مميزات المشروع:

- 📊 تحليل قراءات الحساسات ومقارنتها مع بيانات تدريب سليمة.
- 🔍 اكتشاف الانحراف في القيم قبل ظهور كود عطل.
- 🧠 استخدام نموذج ذكاء صناعي مدرب مسبقًا للتعرف على الحالات السليمة.
- 📈 رسم بياني يوضح درجة انحراف كل حساس.
- 📝 تقرير نهائي يشرح الحالة الفنية المتوقعة.
- 💾 حفظ الحالات واسترجاعها لاحقًا.
- 🖥️ واجهة تفاعلية مبنية باستخدام Streamlit.

---

## 🛠️ مكونات المشروع:

- `Pages/`: صفحات التطبيق مثل التدريب، التنبؤ، الهبوط...
- `data/`: ملفات البيانات الخاصة بالحساسات السليمة والمعطوبة.
- `assets/`: ملفات ثابتة مثل الشعار وملفات CSS.
- `tools/`: سكربتات مساعدة مثل أداة تطبيق التنسيق تلقائيًا.
- `modules/`: دوال وأكواد مساعدة للموديلات والمعالجة والتحليل.
- `model.pkl`: النموذج المدرب بعد التدريب.
- `app.py`: الصفحة الرئيسية (لو تم استخدامها).

---

## 📦 المتطلبات:

```bash
streamlit
scikit-learn
pandas
matplotlib
seaborn
pdfplumber
plotly
numpy
pymupdf
graphviz
....
💡 فكرة المشروع:

في أجهزة كشف الأعطال (مثل Launch أو OBD)، لا يظهر كود العطل إلا بعد أن تصل قراءة الحساس إلى حد غير مسموح به.
لكن هنا، يتم تدريب النموذج على قراءات سليمة، وعند رفع قراءات جديدة، يقارنها مباشرة بالقيم المرجعية
ويكشف الانحراف قبل أن يتحول إلى مشكلة فعلية.


---

🧠 من المطور:

تم تطوير المشروع بواسطة:

Eng. Nabil Elmasry
🔧 متخصص دعم فني وخبرة في قراءة وتحليل بيانات الحساسات
🎓 مدمج بين المعرفة التقنية والفنية والذكاء الاصطناعي