# modules/logger.py

import logging
import os
from logging.handlers import RotatingFileHandler

# إنشاء مجلد log/ إذا لم يكن موجودًا
log_dir = "log"
os.makedirs(log_dir, exist_ok=True)

# إعداد مسار ملف اللوج
LOG_FILE = os.path.join(log_dir, "app_log.txt")

# التحقق من وجود معالج مسبقاً (لتجنب التكرار إذا تم الاستيراد أكثر من مرة)
logger = logging.getLogger("StopEngineLogger")
if not logger.handlers:
    # إنشاء معالج تدوير الملفات
    log_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding='utf-8'
    )
    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    log_handler.setFormatter(log_format)

    # تهيئة اللوجر العام للمشروع
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    logger.propagate = False

# ✅ استخدام جاهز: import logger ثم logger.logger.info(...)