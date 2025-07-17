import os

TEMPLATE_IMPORT = "import streamlit as st\nfrom modules.theme_loader import apply_custom_theme\n\napply_custom_theme()\n"
PAGES_FOLDER = "pages"

def inject_theme_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if any("apply_custom_theme()" in line for line in lines):
        return  # تم الحقن بالفعل

    # تحديد أين تنتهي التعليقات في بداية الملف
    insert_index = 0
    for line in lines:
        if line.strip().startswith("#") or line.strip() == "":
            insert_index += 1
        else:
            break

    new_lines = lines[:insert_index] + [TEMPLATE_IMPORT + "\n"] + lines[insert_index:]

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if os.path.exists(PAGES_FOLDER):
    for filename in os.listdir(PAGES_FOLDER):
        if filename.endswith(".py"):
            path = os.path.join(PAGES_FOLDER, filename)
            inject_theme_code(path)
    print("✅ تم حقن التنسيق في جميع الصفحات بعد التعليقات بنجاح.")
else:
    print(f"❌ مجلد الصفحات '{PAGES_FOLDER}' غير موجود. تأكد من وجوده داخل مجلد المشروع.")