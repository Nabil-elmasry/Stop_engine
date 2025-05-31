# tools/data_cleanup_tool.py

import os
import shutil

def cleanup_data():
    folder = "data"
    if os.path.exists(folder):
        for file in os.listdir(folder):
            if file.endswith(".csv") or file.endswith(".txt"):
                os.remove(os.path.join(folder, file))
        print("✅ تم حذف جميع ملفات البيانات.")
    else:
        print("❌ مجلد البيانات غير موجود.")