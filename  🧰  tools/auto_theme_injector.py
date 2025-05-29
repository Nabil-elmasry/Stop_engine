# tools/auto_theme_injector.py

import os

TEMPLATE_IMPORT = (
    "import streamlit as st\n"
    "from modules.theme_loader import apply_custom_theme\n\n"
    "apply_custom_theme()\n"
)

PAGES_FOLDER = "Pages"

# مر على جميع ملفات الصفحات
for filename in os.listdir(PAGES_FOLDER):
    if filename.endswith(".py"):
        path = os.path.join(PAGES_FOLDER, filename)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # لو التنسيق مضاف مسبقًا، تجاهل
        if "apply_custom_theme()" in content:
            continue

        # لو مش مضاف، أضف التنسيق أعلى الملف
        with open(path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE_IMPORT + "\n" + content)

print("✅ تم حقن التنسيق في جميع الصفحات بنجاح.")