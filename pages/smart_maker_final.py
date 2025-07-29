import pandas as pd
import pickle
import difflib

# تحميل بيانات التدريب لاستخراج الوحدات الأصلية
with open('modules/trained_model.pkl', 'rb') as f:
    trained_model = pickle.load(f)

# نفترض أن التدريب تم على DataFrame يحتوي على أعمدة حساسات بصيغة: Sensor Name | Value | Unit
trained_df = trained_model['sensor_data']
reference_units = dict(zip(trained_df['Sensor Name'], trained_df['Unit']))

# تحميل الملف الجديد المراد تحويله
uploaded_file = 'path/to/your_uploaded_file.csv'
df = pd.read_csv(uploaded_file)

# التأكد من وجود الأعمدة المطلوبة
required_cols = ['Sensor Name', 'Value']
if not all(col in df.columns for col in required_cols):
    raise ValueError("الملف يجب أن يحتوي على أعمدة 'Sensor Name' و 'Value' على الأقل.")

# إذا لم يوجد عمود وحدة القياس، نضيفه مؤقتًا بقيم فاضية
if 'Unit' not in df.columns:
    df['Unit'] = ""

# استكمال الوحدة القياسية من بيانات التدريب
def get_unit(sensor_name):
    # نحاول نطابق الاسم مع أقرب اسم من بيانات التدريب
    match = difflib.get_close_matches(sensor_name, reference_units.keys(), n=1, cutoff=0.8)
    if match:
        return reference_units[match[0]]
    return ""

# تعيين الوحدة لكل حساس إن لم تكن موجودة
df['Unit'] = df.apply(
    lambda row: row['Unit'] if pd.notnull(row['Unit']) and row['Unit'] != "" else get_unit(row['Sensor Name']),
    axis=1
)

# حفظ الملف بعد التنسيق
output_path = 'standardized_sensor_file.csv'
df.to_csv(output_path, index=False)

print(f"✅ تم تحويل الملف وحفظه في: {output_path}")