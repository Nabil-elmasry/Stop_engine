import os

TEMPLATE_IMPORT = "import streamlit as st\nfrom modules.theme_loader import apply_custom_theme\n\napply_custom_theme()\n"
PAGES_FOLDER = "Pages"

if os.path.exists(PAGES_FOLDER):
    for filename in os.listdir(PAGES_FOLDER):
        if filename.endswith(".py"):
            path = os.path.join(PAGES_FOLDER, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "apply_custom_theme()" in content:
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(TEMPLATE_IMPORT + "\n" + content)
    print("✅ تم حقن التنسيق في جميع الصفحات بنجاح.")
else:
    print(f"❌ مجلد الصفحات '{PAGES_FOLDER}' غير موجود. تأكد من وجوده داخل مجلد المشروع.")